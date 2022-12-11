from pathlib import Path

from setuptools import Command
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

from setuptools import setup, find_packages

from gateway.version import __version__ as package_version

package_root = Path(__file__).parent
project_root = package_root.parent


class CustomBuildGRPC(Command):
    """Command to generate project *_pb2.py modules from proto files."""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Build gRPC modules."""
        from grpc_tools import protoc
        import shutil

        try:
            db_controller_proto_file = (
                project_root / "db_controller" / "proto" / "db_controller.proto"
            )
            output_path = package_root / "gateway" / "proto"
            temp_proto_dir = package_root / "gateway-api"

            Path.mkdir(temp_proto_dir)
            shutil.copy(db_controller_proto_file, temp_proto_dir)

            db_controller_proto_command = [
                "grpc_tools.protoc",
                f"--proto_path={output_path.relative_to(package_root)}={temp_proto_dir.name}",
                f"--python_out={package_root.relative_to(package_root)}",
                f"--grpc_python_out={package_root.relative_to(package_root)}",
            ] + [
                str(
                    temp_proto_dir.relative_to(package_root)
                    / db_controller_proto_file.name
                )
            ]

            if protoc.main(db_controller_proto_command) != 0:
                raise Exception("Problem with building db-controller gRPC modules")

        except Exception as e:
            print(e)
        finally:
            shutil.rmtree(temp_proto_dir, ignore_errors=True)


class CustomBuild(build_py):
    """Command for Python modules build."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = CustomBuildGRPC(dist)
        super().__init__(dist)

    def run(self):
        """Build Python and GRPC modules."""
        super().run()
        self.subcommand.run()


class CustomDevelop(develop):
    """Command for develop installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = CustomBuildGRPC(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


class CustomInstall(install):
    """Command for pip installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = CustomBuildGRPC(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


class CustomEggInfo(egg_info):
    """Command for pip installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = CustomBuildGRPC(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


setup(
    name="posts_analyser_gateway",
    version=package_version,
    description="Gateway service for posts analyser project",
    author="Maciek Stopa, Tomasz Kurkowski",
    url="https://github.com/cansubmarinesswim/posts-analyser",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "wheel",
        "grpcio>=1.48.0",
        "grpcio-status>=1.48.0",
        "protobuf>=4.21.0",
        "flask",
        "py-healthcheck",
        "requests",
    ],
    setup_requires=["wheel", "grpcio-tools>=1.48.0"],
    python_requires=">=3.8",
    cmdclass={
        "build_py": CustomBuild,
        "build_grpc": CustomBuildGRPC,
        "develop": CustomDevelop,
        "egg_info": CustomEggInfo,
        "install": CustomInstall,
    },
    long_description=(package_root / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
