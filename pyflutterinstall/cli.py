"""
Runs the installer

When this is done, the directory structure will look like this
sdk/Android:
    build-tools
    cmdline-tools
    emulator       # Generated by the Android SDK Manager
    flutter
    java
    licenses       # Generated by the Android SDK Manager
    patcher        # Generated by the Android SDK Manager
    platforms      # Generated by the Android SDK Manager
    platform-tools # Generated by the Android SDK Manager
    system-images  # Generated by the Android SDK Manager
    tools          # Generated by the Android SDK Manager
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check

import argparse
import os
import sys
from pathlib import Path
import shutil
import subprocess
from typing import Callable
from download import download  # type: ignore
from colorama import just_fix_windows_console  # type: ignore


from pyflutterinstall.resources import (
    JAVA_SDK_URL,
    FLUTTER_GIT_DOWNLOAD,
    ANDROID_SDK_URL,
    CHROME_URL,
    CMDLINE_TOOLS,
    INSTALL_DIR,
    DOWNLOAD_DIR,
    ANDROID_SDK,
    FLUTTER_TARGET,
    JAVA_DIR
)

from pyflutterinstall.util import (
    execute,
    make_title,
    make_dirs,
    set_global_skip_confirmation,
)

from pyflutterinstall.envset_win32 import add_system_path, set_env_var


assert (
    shutil.which("git") is not None
), "Git is not installed, please install, add it to the path then continue."


def install_java_sdk() -> None:
    make_title("Installing Java SDK")
    print(f"Install Java SDK from {JAVA_SDK_URL} to {INSTALL_DIR}")
    java_sdk_zip_file = Path(
        download(JAVA_SDK_URL, DOWNLOAD_DIR / os.path.basename(JAVA_SDK_URL))
    )
    print(f"Unpacking {java_sdk_zip_file} to {JAVA_DIR}")
    shutil.unpack_archive(java_sdk_zip_file, JAVA_DIR)
    base_java_dir = JAVA_DIR / os.listdir(JAVA_DIR)[0]
    print(base_java_dir)
    java_bin_dir = base_java_dir / "bin"
    print(java_bin_dir)
    add_system_path(java_bin_dir)
    set_env_var("JAVA_HOME", base_java_dir)
    print("Java SDK installed.\n")


def install_android_sdk() -> None:
    make_title("Installing Android SDK")
    print(
        f"Install Android commandline-tools SDK from {ANDROID_SDK_URL} to {INSTALL_DIR}"
    )
    # sdk\Android\tools\bin\sdkmanager.bat
    path = download(ANDROID_SDK_URL, DOWNLOAD_DIR / os.path.basename(ANDROID_SDK_URL))
    print(f"Unpacking {path} to {INSTALL_DIR}")
    shutil.unpack_archive(path, ANDROID_SDK / "cmdline-tools" / "tools")
    sdkmanager_path = (
        ANDROID_SDK
        / "cmdline-tools"
        / "tools"
        / "cmdline-tools"
        / "bin"
        / "sdkmanager.bat"
    )
    # add_system_path(sdkmanager_path.parent)
    if not os.path.exists(sdkmanager_path):
        raise FileNotFoundError(f"Could not find {sdkmanager_path}")
    print("About to install Android SDK tools")
    # install latest
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install "platform-tools"',
        send_confirmation="y\n",
        ignore_errors=True,
    )
    set_env_var("ANDROID_SDK_ROOT", ANDROID_SDK)
    set_env_var("ANDROID_HOME", ANDROID_SDK)
    # update tools
    print(f"Updating Android SDK with {sdkmanager_path}")
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --update',
        send_confirmation="y\n",
        ignore_errors=True,
    )
    tools_to_install = [f'"{tool}"' for tool in CMDLINE_TOOLS]
    for tool in tools_to_install:
        execute(
            f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install {tool}',
            send_confirmation="y\n",
            ignore_errors=True,
        )
    execute(
        f'{sdkmanager_path} --licenses --sdk_root="{ANDROID_SDK}"',
        send_confirmation="y\ny\ny\ny\ny\ny\ny\nn\n",
        ignore_errors=True,
    )


def install_flutter() -> None:
    make_title("Installing Flutter")
    print(f"Install Flutter from {FLUTTER_GIT_DOWNLOAD} to {FLUTTER_TARGET}")
    if not FLUTTER_TARGET.exists():
        execute(f'{FLUTTER_GIT_DOWNLOAD} "{FLUTTER_TARGET}"', ignore_errors=True)
    else:
        print(f"Flutter already installed at {FLUTTER_TARGET}")
    # Add flutter to path
    add_system_path(FLUTTER_TARGET / "bin")
    execute(
        f'flutter config --android-sdk "{ANDROID_SDK}" --no-analytics',
        send_confirmation="y\n",
        ignore_errors=True,
    )
    execute(
        "flutter doctor --android-licenses", send_confirmation="y\n", ignore_errors=True
    )
    print("Flutter installed.\n")


def install_chrome() -> None:
    print("\n################# Installing Chrome #################")
    # Install chrome for windows
    stdout = subprocess.check_output(
        "flutter doctor",
        shell=True,
        text=True,
        encoding="utf-8",
        universal_newlines=True,
    )
    if "Cannot find Chrome" in stdout:
        print("Chrome not found, installing")
        print(f"Install Chrome from {CHROME_URL} to {INSTALL_DIR}")
        path = download(CHROME_URL, DOWNLOAD_DIR / os.path.basename(CHROME_URL))
        print(f"Downloaded chrome at {path}")
        # install it
        os.system(f'"{path}"')


def ask_if_interactive(
    is_interactive: bool, callback_name: str, callback: Callable
) -> None:
    if is_interactive:
        if input(f"install {callback_name} (y/n)? ") == "y":
            callback()
    else:
        callback()


def postinstall_run_flutter_doctor() -> None:
    cmd = "flutter doctor -v"
    make_title(f"Executing '{cmd}'")
    if not shutil.which("flutter"):
        print("Flutter not found in path")
        return
    subprocess.call(cmd, shell=True, text=True, universal_newlines=True)


def main():
    just_fix_windows_console()  # Fixes color breakages
    parser = argparse.ArgumentParser(description="Installs Flutter Dependencies")
    parser.add_argument(
        "--skip-confirmation",
        action="store_true",
        help="Skip confirmation",
        default=False,
    )
    parser.add_argument("--skip-java", action="store_true", help="Skip Java SDK")
    parser.add_argument("--skip-android", action="store_true", help="Skip Android SDK")
    parser.add_argument("--skip-flutter", action="store_true", help="Skip Flutter SDK")
    parser.add_argument("--skip-chrome", action="store_true", help="Skip Chrome")
    args = parser.parse_args()
    any_skipped = any(
        [args.skip_java, args.skip_android, args.skip_flutter, args.skip_chrome]
    )
    # Check if windows comes after argparse to enable --help
    if sys.platform != "win32":
        print("This script is only for Windows")
        sys.exit(1)
    print(f"This will install Flutter and its dependencies into {os.path.basename(INSTALL_DIR)}")
    skip_confirmation = (
        args.skip_confirmation or input("auto-accept all? (y/n): ").lower() == "y"
    )
    interactive = not skip_confirmation
    set_global_skip_confirmation(skip_confirmation)
    print("\nInstalling Flutter SDK and dependencies\n")
    make_dirs()
    if not args.skip_java:
        ask_if_interactive(interactive, "java_sdk", install_java_sdk)
    if not args.skip_android:
        ask_if_interactive(interactive, "android_sdk", install_android_sdk)
    if not args.skip_flutter:
        ask_if_interactive(interactive, "flutter", install_flutter)
    if not args.skip_chrome:
        ask_if_interactive(interactive, "chrome", install_chrome)
    if not args.skip_flutter:
        postinstall_run_flutter_doctor()
    if not any_skipped:
        print("\nDone installing Flutter SDK and dependencies\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
