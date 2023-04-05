import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# The directory containing this file
HERE = os.path.dirname(__file__)

NAME = "pyflutterinstall"
DESCRIPTION = "Installs the flutter sdk and dependencies"
URL = "https://github.com/zackees/pyflutterinstall"
EMAIL = "dont@email.me"
AUTHOR = "Zach Vorhies"
REQUIRES_PYTHON = ">=3.9"
VERSION = "1.2.5"

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fd:
    LONG_DESCRIPTION = fd.read()

with open(os.path.join(HERE, "requirements.txt")) as fd:
    REQUIREMENTS = [line.strip() for line in fd.readlines() if line.strip()]


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system('"{0}" setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(VERSION))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    python_requires=REQUIRES_PYTHON,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    author="Zach Vorhies",
    author_email="dont@email.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Environment :: Console",
    ],
    install_requires=REQUIREMENTS,

    entry_points={
        "console_scripts": [
            "pyflutterinstall = pyflutterinstall.cli:main",
            "pyflutteractivate = pyflutterinstall.setenv:init_dotenv",
            "pyflutterprintconfig = pyflutterinstall.config:print_config",
            "sdkmanager = pyflutterinstall.cmds.sdkmanager:main",
            "avdmanager = pyflutterinstall.cmds.avdmanager:main",
            "adb = pyflutterinstall.cmds.adb:main",
            "gradle = pyflutterinstall.cmds.gradle:main",
            "emulator = pyflutterinstall.cmds.emulator:main",
            "java = pyflutterinstall.cmds.java:main"
        ],
    },
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_data={},
    include_package_data=True,
    extras_require={
        "test": ["pytest"],
    },
    cmdclass={
        "upload": UploadCommand,
    },
)
