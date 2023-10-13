"""
Unit test file.
"""

import os
import unittest

from pyflutterinstall.config import config_load

config = config_load()
# INSTALLED = config.get("INSTALL_DIR") is not None
INSTALLED = config.vars.get("INSTALL_DIR") is not None


class JavaTest(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_java(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test java")
        # self.assertEqual(0, java.main(["-version"]))
        rtn = os.system("java -version")
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
