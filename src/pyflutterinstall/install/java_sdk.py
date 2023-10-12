"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
import warnings
from typing import Optional

from download import download  # type: ignore

from pyflutterinstall.resources import (
    # DOWNLOAD_DIR,
    # INSTALL_DIR,
    # JAVA_DIR,
    get_platform_java_sdk,
    JAVA_SDK_VERSIONS,
    JAVA_VERSION,
)
from pyflutterinstall.setenv import add_env_path, set_env_var
from pyflutterinstall.util import make_title

from pyflutterinstall.paths import Paths


def install_java_sdk(version: Optional[int] = None) -> int:
    make_title("Installing Java SDK")
    paths = Paths()
    paths.apply_env()
    java_sdk_url = get_platform_java_sdk(version)
    local_file = paths.DOWNLOAD_DIR / os.path.basename(java_sdk_url)
    print(f"Install Java SDK from {java_sdk_url} to {local_file}")
    java_sdk_zip_file = Path(download(url=java_sdk_url, path=local_file, replace=False))
    # if os.path.exists(JAVA_DIR):
    #    print(f"Removing existing Java SDK at {JAVA_DIR}")
    #    shutil.rmtree(JAVA_DIR)
    print(f"Unpacking {java_sdk_zip_file} to {paths.JAVA_DIR}")
    shutil.unpack_archive(java_sdk_zip_file, paths.JAVA_DIR)
    base_java_dir = paths.JAVA_DIR / os.listdir(paths.JAVA_DIR)[0]
    print(base_java_dir)
    if sys.platform == "darwin":
        java_bin_dir = base_java_dir / "Contents" / "Home" / "bin"
    else:
        java_bin_dir = base_java_dir / "bin"
    # check that java is in the path
    print(java_bin_dir)
    java_exe = "java.exe" if os.name == "nt" else "java"
    assert java_exe in os.listdir(java_bin_dir), "java not found in java bin dir"
    add_env_path(java_bin_dir)
    if sys.platform == "darwin":
        set_env_var("JAVA_HOME", str(base_java_dir / "Contents" / "Home"))
    else:
        set_env_var("JAVA_HOME", str(base_java_dir))
    found_java_path = shutil.which("java")
    assert found_java_path is not None, "No java path found"
    if str(java_bin_dir) not in found_java_path:
        msg = f"java installed not in expected path ({str(java_bin_dir)}), instead it's {found_java_path}\n"
        msg += f"os environmental settings: {os.environ}"
        warnings.warn(msg)
        raise AssertionError(msg)
    assert (
        str(java_bin_dir) in found_java_path
    ), f"java installed not in expected path ({str(java_bin_dir)}), instead it's {found_java_path}"
    java_version = subprocess.check_output(
        "java -version", shell=True, universal_newlines=True, stderr=subprocess.STDOUT
    )
    print(f"Java SDK installed: {java_version}\n")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        type=int,
        default=JAVA_VERSION,
        help="The version of Java to install",
        choices=JAVA_SDK_VERSIONS.keys(),
    )
    args = parser.parse_args()
    install_java_sdk(args.version)


if __name__ == "__main__":
    main()
