"""
Resources for pyflutterinstall
"""

# pylint: disable=line-too-long,fixme

import os
import sys
from pathlib import Path
import platform

FLUTTER_GIT_DOWNLOAD = (
    "git clone --depth 1 https://github.com/flutter/flutter.git -b stable"
)
# Note that commit is 135454af32477f815a7525073027a3ff9eff1bfd
CMDLINE_TOOLS = [
    "sources;android-33",
    "system-images;android-30;default;x86_64",
    "system-images;android-27;google_apis_playstore;x86",
    "cmdline-tools;latest",
    "platform-tools",
    "build-tools;33.0.1",
    "platforms;android-33",
    "emulator",
    "tools",
]


def get_platform_java_sdk() -> str:
    """Gets the java platform specific url"""
    if sys.platform == "win32":
        return "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_windows-x64_bin.zip"
    if platform.machine() == "x86_64":
        arch = "x64"
    else:
        arch = "aarch64"
    if sys.platform == "darwin":
        #return f"https://download.oracle.com/java/17/archive/jdk-17.0.6_macos-{arch}_bin.tar.gz"
        return "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_osx-x64_bin.tar.gz"
    elif "linux" in sys.platform:
        # return f"https://download.oracle.com/java/17/archive/jdk-17.0.6_linux-{arch}_bin.tar.gz"
        return "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz"
    raise NotImplementedError(f"Unsupported platform: {sys.platform}")


def get_android_sdk_url() -> str:
    """Gets the android platform specific url"""
    version = "9123335"
    if sys.platform == "win32":
        os_name = "win"
    elif sys.platform == "darwin":
        os_name = "mac"
    else:
        os_name = "linux"
    return f"https://dl.google.com/android/repository/commandlinetools-{os_name}-{version}_latest.zip"


def get_chrome_url() -> str:
    """Gets the chrome platform specific url"""
    if sys.platform == "win32":
        return "https://dl.google.com/chrome/install/375.126/chrome_installer.exe"
    if sys.platform == "darwin":
        return "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg"
    return "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"


CHROME_URL = get_chrome_url()
ANDROID_SDK_URL = get_android_sdk_url()
JAVA_SDK_URL = get_platform_java_sdk()
GRADLE_URL = "https://services.gradle.org/distributions/gradle-7.2-bin.zip"
PROJECT_ROOT = Path(os.getcwd())
INSTALL_DIR = PROJECT_ROOT / "FlutterSDK"
ENV_FILE = PROJECT_ROOT / ".env"
DOWNLOAD_DIR = PROJECT_ROOT / ".downloads"
ANDROID_SDK = INSTALL_DIR / "Android" / "sdk"
FLUTTER_TARGET = INSTALL_DIR / "flutter"
JAVA_DIR = INSTALL_DIR / "java"
GRADLE_DIR = INSTALL_DIR / "gradle"
IS_GITHUB_RUNNER = os.getenv("GITHUB_ACTIONS", "false") == "true"
