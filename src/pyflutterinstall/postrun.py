"""
Pre run script
"""

# pylint: disable=R0801,invalid-name

import os
import sys
from shutil import which
import warnings

# coloram has an issue that just_fix_windows_console is broken
# so rename init to just_fix_windows_console
from colorama import init as just_fix_windows_console  # type: ignore
from pyflutterinstall.util import print_tree_dir
from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    just_fix_windows_console()  # Fixes color breakages
    android_home = os.environ.get("ANDROID_HOME")
    if android_home is None:
        warnings.warn("ANDROID_HOME not set")
        return 1
    print("ANDROID_HOME = " + android_home)
    print(f"dir $ANDROID_HOME = {os.listdir(android_home)}")
    print_tree_dir(android_home)
    print("Environment:")
    for key, value in os.environ.items():
        # skip path
        if key == "PATH":
            continue
        print(f"  {key} = {value}")
    print("PATH:")
    for path in os.environ["PATH"].split(os.pathsep):
        print(f"  {path}")

    if sys.platform != "win32":
        print("Printing ~/.bashrc file")
        bashrc = os.path.expanduser("~/.bashrc")
        assert os.path.exists(bashrc)
        with open(bashrc, encoding="utf-8", mode="r") as f:
            print(f.read())

    # needle = os.path.join("cmdline-tools", "latest", "bin")
    # found = False
    # for path in os.environ["PATH"].split(os.pathsep):
    #    if needle in path:
    #        found = True
    #        break
    # if not found:
    #    raise RuntimeError(f'Android tools "{needle} not found in PATH')

    print("Checking that adb is in the path")
    if not which("adb"):
        print("adb not found in path")
        return 1
    print("Checking if Flutter is in path")
    if not which("flutter"):
        print("Flutter not found in path")
        return 1
    rtn = os.system("java -version")
    if rtn != 0:
        print("Java not found in path")
        return 1
    os.system("flutter doctor -v")
    if which("sdkmanager") is None:
        print("sdkmanager not found in path")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
