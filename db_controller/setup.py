from pathlib import Path

from setuptools import Command
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

from db_controller.version import __version__ as package_version

package_root = Path(__file__).parent
project_root = package_root.parent


class BuildPackageProtos(Command):
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
            main_proto_file = package_root / "proto" / "db_controller.proto"

            output_path = package_root / "db_controller" / "proto"

            temp_proto_dir = package_root / "db-controller-api"
            Path.mkdir(temp_proto_dir)
            shutil.copy(main_proto_file, temp_proto_dir)

            main_proto_command = [
                "grpc_tools.protoc",
                f"--proto_path={output_path.relative_to(package_root)}={temp_proto_dir.name}",
                f"--python_out={package_root.relative_to(package_root)}",
                f"--grpc_python_out={package_root.relative_to(package_root)}",
            ] + [str(temp_proto_dir.relative_to(package_root) / main_proto_file.name)]

            if protoc.main(main_proto_command) != 0:
                raise Exception(
                    "Problem with building db-controller gRPC modules"
                )

        except Exception as e:
            print(e)
        finally:
            shutil.rmtree(temp_proto_dir, ignore_errors=True)


class BuildPyGRPC(build_py):
    """Command for Python modules build."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildPackageProtos(dist)
        super().__init__(dist)

    def run(self):
        """Build Python and GRPC modules."""
        super().run()
        self.subcommand.run()


class DevelopGRPC(develop):
    """Command for develop installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildPackageProtos(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


class CustomInstall(install):
    """Command for pip installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildPackageProtos(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


class CustomEggInfo(egg_info):
    """Command for pip installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildPackageProtos(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


setup(
    name="db_controller",
    version=package_version,
    description="posts analyser database controller component",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "wheel",
        "grpcio>=1.48.0",
        "grpcio-status>=1.48.0",
        "bcrypt>=4.0.0",
        "protobuf>=4.21.0",
        "psycopg2-binary>=2.9.3, <3.0",
        "sqlalchemy>=1.4, <2.0",
        "password-strength>=0.0.3",
    ],
    setup_requires=["wheel", "grpcio-tools>=1.48.0"],
    python_requires=">=3.8",
    cmdclass={
        "build_py": BuildPyGRPC,
        "build_grpc": BuildPackageProtos,
        "develop": DevelopGRPC,
        "egg_info": CustomEggInfo,
        "install": CustomInstall,
    },
    entry_points={
        "console_scripts": [
            "db-controller-service = db_controller.app:main",
        ]
    },
)
