# pyflutterinstall

[![Win_Tests](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win.yml)
[![Win_FullInstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_win_fullinstall.yml)
[![MacOS_Tests](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos.yml)
[![MacOS_Fullinstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos_fullinstall.yml)
[![Mac_arm_Fullinstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos_arm_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_macos_arm_fullinstall.yml)
[![Ubuntu_Tests](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu.yml)
[![Ubuntu_Fullinstall](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu_fullinstall.yml/badge.svg)](https://github.com/zackees/pyflutterinstall/actions/workflows/push_ubuntu_fullinstall.yml)

Installs all dependencies for pyflutter/AndroidSDK on Windows.

```bash
pip install pyflutterinstall
cd <DIRECTORY YOU WANT TO INSTALL>
pyflutterinstall
```
The SDK will be installed at `FlutterSDK`

Use this tool if you need to:
  * Install FlutterSDK
  * -or- Install the AndroidSDK
  
Your path will be updated with the dependencies so that you can execute `sdkmanager`, `adb`, `emulator` and the like.
  
# Why?

Installing the Android SDK toolchain is **hard**! This tool takes care of all of this for
Windows/Linux/MacOS and does it in a fully automated way. This is great for reproducabilty of tool chain install across your
team.


#### Versions

  * Android API: 33
  * Java: 20
  * Flutter: <TODO>

Usage
```bash
> pip install pyflutterinstall
> pyflutterinstall
```

# Releases
  * 1.4.1: Adds build tools to the path, enabling aapt and aapt2 and others.
  * 1.4.0: Remove the trampoline hack, now sets paths properly thanks to setenvironment 2.0
  * 1.2.7: Use a trampoline for apkanalyzer to fix missing class paths
  * 1.2.6: Java trampoline fixed for Mac OSX
  * 1.2.5: Java is now jdk v17 by default
  * 1.2.4: Java v11.0.2 -> v11.0.18 (fixes OkHttp3 bug)
  * 1.2.2: Fixes for sdkmanager.
  * 1.2.1: Fixes for avdmanager.
  * 1.2.0: Now uses shims for adb, avdmanager, emulator, gradle, java, sdkmanager
  * 1.1.3: Fix 1.1.2
  * 1.1.2: Adds --install-dir option to install to a specific directory.
  * 1.1.1: Expose the post_run testing function to test environments.
  * 1.1.0: Adds ant install.
  * 1.0.10: Emulator tools now installed on path.
  * 1.0.9: adb is now installed on the path.
  * 1.0.8: Gradle upgrade to 7.5, JDK is downgraded to 9.
  * 1.0.7: Windows now uses user environment variables to avoid elevated privileges.
  * 1.0.6: Fix macos install.
  * 1.0.5: Gradle is now installed as well.
  * 1.0.3: Uses pexpect to run commands.
  * 1.0.2: MacOS: now installs cocoapods dependency.
  * 1.0.1: Update setenvironment to 1.0.9 to get expanded paths.
  * 1.0.0: Windows, Mac and Linux now supported and all tests pass.
  * 0.0.2: Automated tests for windows.
  * 0.0.1: Initial release - windows supported.

# TODO
  * [ ] Integrate the Windows Universal bridge driver for devices:
    * https://adb.clockworkmod.com/
