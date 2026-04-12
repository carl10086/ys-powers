#!/usr/bin/env python3
"""
ys-powers skills 本地安装脚本

功能：
1. 获取 ys-powers 项目的本地目录
2. 在当前工作目录创建 ./.claude/skills
3. 将项目中的 skills 目录全量覆盖到目标位置

使用方法：
    python install/local-install.py
"""

import shutil
import sys
from pathlib import Path


def get_project_root() -> Path:
    """通过脚本位置确定项目根目录"""
    script_path = Path(__file__).resolve()
    # 脚本位于 install/ 目录下，项目根目录是上一级
    return script_path.parent.parent


def install_skills():
    """执行 skills 安装"""
    # 1. 确定源目录
    project_root = get_project_root()
    source_dir = project_root / "skills"

    if not source_dir.exists():
        print(f"错误：源目录不存在 {source_dir}", file=sys.stderr)
        sys.exit(1)

    if not source_dir.is_dir():
        print(f"错误：源路径不是目录 {source_dir}", file=sys.stderr)
        sys.exit(1)

    # 2. 确定目标目录（当前工作目录）
    target_dir = Path.cwd() / ".claude" / "skills"

    # 3. 执行复制（全量覆盖）
    try:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        print(f"✓ Skills 安装成功（全量覆盖）")
        print(f"  源目录: {source_dir}")
        print(f"  目标目录: {target_dir}")
    except PermissionError as e:
        print(f"错误：权限不足，无法写入 {target_dir}", file=sys.stderr)
        print(f"详情: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误：复制过程中发生错误 - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    install_skills()
