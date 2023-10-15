"""
Trampoline command gracefully stubs out commands and delegates to the
actual commands if they exist.

The benefit of this is that by altering the path we can control how
commands are found.
"""

import os
import subprocess
import sys
from pathlib import Path
from pyflutterinstall.which_all import which_all

from pyflutterinstall.paths import Paths

Paths().apply_env()


def trampoline(
    command: str, args: list[str] | None = None, default_path: Path | str | None = None
) -> int:
    """Trampoline"""
    if args is None:
        args = sys.argv[1:]
    if isinstance(default_path, Path):
        default_path = str(default_path)
    # Not multithreaded safe.
    prev_path = os.environ.get("PATH", "")
    try:
        env = os.environ.copy()
        depth = int(env.get("RECURSIVE", "0"))
        if depth > 9:
            # If you get this error then the path correction isn't correct.
            print(f"Recursion limits while procesing {command} stub, aborting.")
            return 1
        env["RECURSIVE"] = str(depth + 1)
        if default_path is not None:
            new_path = os.pathsep.join([default_path, prev_path])
            os.environ["PATH"] = new_path
        if default_path is not None and os.path.isfile(default_path):
            paths = [default_path]
        else:
            paths = which_all(command, filter_package_exes=True)
        if paths:
            cmd_list = [paths[0]] + args
            if "--which" in sys.argv:
                print("Real tool is at:", paths[0])
                return 0
            rtn = subprocess.call(cmd_list, env=env)
            return rtn
        print(
            f"Trampoline {command} could not find the real {command} installed on the system paths."
        )
        return 1
    finally:
        if prev_path:
            os.environ["PATH"] = prev_path
