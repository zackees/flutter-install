"""
Unit test file.
"""

import os
import unittest
from shutil import which
from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()
INSTALLED = paths.INSTALLED


class UseExePaths(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_java(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test java")
        # self.assertEqual(0, java.main(["-version"]))
        rtn = os.system("java -version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_adb(self) -> None:
        """Tests that we can bind to the adb executable."""
        print("Test adb")
        # self.assertEqual(0, adb.main(["version"]))
        rtn = os.system("adb version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_avdmanager(self) -> None:
        """Tests that we can bind to the avdmanager executable."""
        print("Test avdmanager")
        print(f"which avdmanager: {which('avdmanager')}")
        # self.assertEqual(0, avdmanager.main(["list"]))
        # rtn = avdmanager.main(["list"])
        # self.assertEqual(0, rtn)
        rtn = os.system("avdmanager list")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_gradle(self) -> None:
        """Tests that we can bind to the gradle executable."""
        print("Test gradle")
        # os.system("printenv")
        # self.assertEqual(0, gradle.main(["-version"]))
        # rtn = gradle.main(["-version"])
        # self.assertEqual(0, rtn)
        rtn = os.system("gradle -version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_sdkmanager(self) -> None:
        """Tests that we can bind to the sdkmanager executable."""
        print("Test sdkmanager")
        print(f"which sdkmanager: {which('sdkmanager')}")
        # rtn = sdkmanager.main(["--version"])
        # self.assertEqual(0, rtn)
        rtn = os.system("sdkmanager --version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_emulator(self) -> None:
        """Tests that we can bind to the emulator executable."""
        print("Test emulator")
        # self.assertEqual(0, emulator.main(["-help"]))
        # rtn = emulator.main(["-help"])
        # self.assertEqual(0, rtn)
        rtn = os.system("emulator -help")
        self.assertEqual(0, rtn)

    # @unittest.skipIf(not INSTALLED, "Not installed")
    @unittest.skip("Disabled for now")
    def test_aapt(self) -> None:
        """Tests that we can bind to the aapt executable."""
        print("Test aapt")
        # self.assertEqual(0, aapt.main(["v"]))
        # rtn = aapt.main(["v"])
        # self.assertEqual(0, rtn)
        rtn = os.system("aapt v")
        self.assertEqual(0, rtn)

    # @unittest.skipIf(not INSTALLED, "Not installed")
    @unittest.skip("Disabled for now")
    def test_aapt2(self) -> None:
        """Tests that we can bind to the aapt2 executable."""
        print("Test aapt2")
        # self.assertEqual(0, aapt2.main(["v"]))
        # rtn = aapt2.main(["version"])
        # self.assertEqual(0, rtn)
        rtn = os.system("aapt2 version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_flutter(self) -> None:
        """Tests that we can bind to the aapt2 executable."""
        print("Test flutter")
        # self.assertEqual(0, aapt2.main(["v"]))
        # rtn = flutter.main(["--version"])
        # self.assertEqual(0, rtn)
        rtn = os.system("flutter --version")
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
