from pathlib import Path

from setuptools import setup, find_packages

from gateway.version import __version__ as package_version

project_root = Path(__file__).parent

setup(
    name="posts_analyser_gateway",
    version=package_version,
    description="Gateway service for posts analyser project",
    author="Maciek Stopa, Tomasz Kurkowski",
    url="https://github.com/cansubmarinesswim/posts-analyser",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "py-healthcheck",
    ],
    long_description=(project_root / "README.md").read_text(),
    long_description_content_type="text/markdown",
)