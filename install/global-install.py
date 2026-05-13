#!/usr/bin/env python3
"""
[DEPRECATED] ys-powers skills 全局安装脚本

请使用新的 Makefile 命令：
    make global-install

本脚本保留用于向后兼容，将在未来版本移除。
"""

import subprocess
import sys
from pathlib import Path


def main():
    print("⚠ DEPRECATED: Use \"make global-install\" instead. This script will be removed in a future version.")
    print()
    sys.stdout.flush()

    script_dir = Path(__file__).resolve().parent
    install_py = script_dir / "install.py"

    result = subprocess.run([sys.executable, str(install_py), "install", "global"])
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
