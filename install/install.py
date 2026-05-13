#!/usr/bin/env python3
"""
ys-powers unified installer

Usage:
    python install/install.py install global
    python install/install.py install local [--target <path>]
    python install/install.py update global
    python install/install.py update local [--target <path>]
    python install/install.py uninstall global
    python install/install.py uninstall local [--target <path>]
"""

import argparse
import sys
from pathlib import Path

from lib.config import DIRECTORIES
from lib.fs import install_directory, uninstall_directory
from lib.hooks import inject_hooks, remove_hooks


def get_project_root() -> Path:
    """通过脚本位置自定位 ys-powers 源目录。"""
    return Path(__file__).resolve().parent.parent


def get_target_dir(scope: str, target: Path | None = None) -> Path:
    """获取目标安装目录。"""
    if scope == "global":
        return Path.home() / ".claude"
    if target:
        return target / ".claude"
    return Path.cwd() / ".claude"


def resolve_hooks_path_variable(scope: str, target_dir: Path) -> str:
    """解析 hooks 路径变量替换值。"""
    if scope == "global":
        return str(target_dir.resolve())
    return "${CLAUDE_PROJECT_DIR}/.claude"


def do_install(project_root: Path, target_dir: Path, path_var: str, merge: bool) -> bool:
    """执行安装或更新。"""
    all_ok = True

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        if not install_directory(project_root, source_name, target_dir, target_name, strategy):
            all_ok = False

    if not inject_hooks(project_root, target_dir, path_var, merge=merge):
        all_ok = False

    return all_ok


def do_uninstall(project_root: Path, target_dir: Path, path_var: str) -> bool:
    """执行卸载。"""
    all_ok = True

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        if not uninstall_directory(project_root, source_name, target_dir, target_name, strategy):
            all_ok = False

    if not remove_hooks(project_root, target_dir, path_var):
        all_ok = False

    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description="ys-powers installer")
    parser.add_argument("action", choices=["install", "update", "uninstall"],
                        help="install, update, or uninstall")
    parser.add_argument("scope", choices=["global", "local"],
                        help="global (~/.claude/) or local (./.claude/)")
    parser.add_argument("--target", type=Path, default=None,
                        help="target project directory (local scope only)")
    args = parser.parse_args()

    project_root = get_project_root()

    # 守卫：确认自定位正确
    guard_file = project_root / "skills" / "using-agent-skills" / "SKILL.md"
    if not guard_file.exists():
        print(f"✗ 无法定位 ys-powers 源目录: {project_root}", file=sys.stderr)
        print("  请确保从 ys-powers 仓库内运行此脚本。", file=sys.stderr)
        return 1

    target_dir = get_target_dir(args.scope, args.target)
    path_var = resolve_hooks_path_variable(args.scope, target_dir)

    print(f"项目根目录: {project_root}")
    print(f"目标根目录: {target_dir}")
    print()

    if args.action in ("install", "update"):
        success = do_install(project_root, target_dir, path_var, merge=(args.action == "update"))
    elif args.action == "uninstall":
        success = do_uninstall(project_root, target_dir, path_var)
    else:
        # argparse 已限制 choices，此处不会到达
        parser.print_help()
        return 1

    print()
    if success:
        print(f"✓ 操作完成: {args.action} {args.scope}")
        return 0
    else:
        print(f"✗ 操作失败: {args.action} {args.scope}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
