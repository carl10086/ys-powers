#!/usr/bin/env python3
"""
opencli skills 本地安装脚本

Usage:
    python install/opencli-skills.py install [PROJECT_DIR]
    python install/opencli-skills.py uninstall [PROJECT_DIR]

将 external/opencli/skills/ 下的 skill 目录复制到目标项目的 .claude/skills/。
默认 PROJECT_DIR 为当前工作目录。
"""

import argparse
import sys
from pathlib import Path

from lib.fs import install_directory, uninstall_directory


def get_project_root() -> Path:
    """通过脚本位置自定位 ys-powers 源目录。"""
    return Path(__file__).resolve().parent.parent


def do_install(project_root: Path, target_project: Path) -> bool:
    """安装 opencli skills 到目标项目。"""
    source_dir = project_root / "external/opencli/skills"

    if not source_dir.exists():
        print(f"✗ opencli skills 源目录不存在: {source_dir}", file=sys.stderr)
        return False

    target_claude = target_project / ".claude"
    return install_directory(
        project_root,
        "external/opencli/skills",
        target_claude,
        "skills",
        "folder",
    )


def do_uninstall(project_root: Path, target_project: Path) -> bool:
    """从目标项目卸载 opencli skills。"""
    source_dir = project_root / "external/opencli/skills"

    if not source_dir.exists():
        print(f"✗ opencli skills 源目录不存在: {source_dir}", file=sys.stderr)
        return False

    target_claude = target_project / ".claude"
    return uninstall_directory(
        project_root,
        "external/opencli/skills",
        target_claude,
        "skills",
        "folder",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="opencli skills installer")
    parser.add_argument(
        "action",
        choices=["install", "uninstall"],
        help="install or uninstall opencli skills",
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="target project directory (default: current directory)",
    )
    args = parser.parse_args()

    project_root = get_project_root()
    target_project = args.project_dir.resolve()

    # 守卫：目标项目目录必须存在
    if not target_project.exists():
        print(f"✗ 目标项目目录不存在: {target_project}", file=sys.stderr)
        return 1

    if not target_project.is_dir():
        print(f"✗ 目标路径不是目录: {target_project}", file=sys.stderr)
        return 1

    print(f"项目根目录: {project_root}")
    print(f"目标项目: {target_project}")
    print()

    if args.action == "install":
        success = do_install(project_root, target_project)
    else:
        success = do_uninstall(project_root, target_project)

    print()
    if success:
        print(f"✓ 操作完成: {args.action}")
        return 0
    else:
        print(f"✗ 操作失败: {args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
