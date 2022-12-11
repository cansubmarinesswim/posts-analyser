from pathlib import Path

from setuptools import Command
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from setuptools import setup

from version import __version__ as package_version

project_root = Path(__file__).parent


class BuildWithModelComponents(Command):
    """Command to fetch model data in the building stage"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Fetch models data"""
        import requests
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        model_name = model_name = f"cardiffnlp/twitter-roberta-base-sentiment"
        labels_source = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/mapping.txt"
        
        model_dir = project_root / "model"

        tokenizer_file = model_dir / "tokenizer"
        model_file = model_dir /  "model"
        labels_file = model_dir / "labels.txt"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(tokenizer_file)

        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.save_pretrained(model_file)

        label_response = requests.get(labels_source)
        with open(labels_file, 'wb') as f:
            f.write(label_response.content)
        
        with open("src/model_dir.py", "w") as f:
            f.write(f'model_dir = "{model_dir}"\n')


class CustomBuild(build_py):
    """Command for Python modules build."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildWithModelComponents(dist)
        super().__init__(dist)

    def run(self):
        """Build Python and GRPC modules."""
        super().run()
        self.subcommand.run()


class CustomDevelop(develop):
    """Command for develop installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildWithModelComponents(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


class CustomEggInfo(egg_info):
    """Command for pip installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildWithModelComponents(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


class CustomInstall(install):
    """Command for pip installation."""

    def __init__(self, dist):
        """Create a sub-command to execute."""
        self.subcommand = BuildWithModelComponents(dist)
        super().__init__(dist)

    def run(self):
        """Build GRPC modules before the default installation."""
        self.subcommand.run()
        super().run()


setup(
    name="posts_sentiment_analyser",
    version=package_version,
    description="ML model server for sentiment analysis",
    author="Maciek Stopa",
    url="https://github.com/cansubmarinesswim/posts-analyser",
    packages=['posts_sentiment_analyser'],
    package_dir={'posts_sentiment_analyser':'src'},
    include_package_data=True,
    install_requires=[
        "flask",
        "py-healthcheck",
        "numpy",
        "scipy",
        "torch",
        "transformers",
        "waitress"
    ],
    setup_requires=[
        "requests",
        "transformers",
    ],
    long_description=(project_root / "README.md").read_text(),
    long_description_content_type="text/markdown",
    cmdclass={
        "build_py": CustomBuild,
        "develop": CustomDevelop,
        "egg_info": CustomEggInfo,
        "install": CustomInstall,
    }
)