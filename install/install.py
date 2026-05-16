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


def _detect_local_target(project_root: Path, explicit_target: Path | None) -> Path | None:
    """
    local scope 且未显式指定 --target 时，尝试自动检测目标目录。

    如果当前目录不是 ys-powers 仓库本身，且存在 .claude/settings.local.json，
    则推断用户想对当前项目进行操作。

    Returns:
        检测到的目标目录（不含 .claude 后缀），或 None（未检测到）
    """
    if explicit_target is not None:
        return None  # 用户已显式指定，不自动检测

    cwd = Path.cwd()
    # 避免在 ys-powers 仓库本身操作时误检测
    if cwd.resolve() == project_root.resolve():
        return None

    settings_local = cwd / ".claude" / "settings.local.json"
    if settings_local.exists():
        return cwd

    return None


def _validate_uninstall(target_dir: Path, scope: str) -> bool:
    """
    卸载前校验：确认目标目录确实安装了 ys-powers。

    Returns:
        校验通过返回 True，否则返回 False
    """
    if not target_dir.exists():
        print(f"✗ 目标目录不存在: {target_dir}", file=sys.stderr)
        return False

    # 检查是否有 ys-powers 的痕迹（至少 skills 或 hooks 目录存在）
    indicators = ["skills", "hooks", "settings.local.json" if scope == "local" else "settings.json"]
    found_any = any((target_dir / name).exists() for name in indicators)

    if not found_any:
        print(f"⚠ 目标目录未检测到 ys-powers 安装痕迹: {target_dir}", file=sys.stderr)
        print(f"  预期存在以下至少一项: {', '.join(indicators)}", file=sys.stderr)
        return False

    return True


def do_install(project_root: Path, target_dir: Path, scope: str) -> bool:
    """执行安装或更新。"""
    all_ok = True

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        if not install_directory(project_root, source_name, target_dir, target_name, strategy):
            all_ok = False

    if not inject_hooks(project_root, target_dir, scope):
        all_ok = False

    return all_ok


def do_uninstall(project_root: Path, target_dir: Path, scope: str) -> bool:
    """执行卸载。"""
    all_ok = True

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        if not uninstall_directory(project_root, source_name, target_dir, target_name, strategy):
            all_ok = False

    if not remove_hooks(project_root, target_dir, scope):
        all_ok = False

    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description="ys-powers installer")
    parser.add_argument("action", choices=["install", "update", "uninstall"],
                        help="install, update, or uninstall")
    parser.add_argument("scope", choices=["global", "local"],
                        help="global (~/.claude/) or local (./.claude/)")
    parser.add_argument("-p", "--target", type=Path, default=None,
                        help="target project directory (local scope only)")
    args = parser.parse_args()

    project_root = get_project_root()

    # 守卫：确认自定位正确
    guard_file = project_root / "skills" / "using-agent-skills" / "SKILL.md"
    if not guard_file.exists():
        print(f"✗ 无法定位 ys-powers 源目录: {project_root}", file=sys.stderr)
        print("  请确保从 ys-powers 仓库内运行此脚本。", file=sys.stderr)
        return 1

    # local scope 自动检测：未指定 --target 且当前目录不是 ys-powers 本身时
    auto_detected = None
    if args.scope == "local" and args.target is None:
        auto_detected = _detect_local_target(project_root, args.target)
        if auto_detected:
            target_dir = auto_detected / ".claude"
            print(f"ℹ 自动检测到本地项目: {auto_detected}")
        else:
            target_dir = get_target_dir(args.scope, args.target)
    else:
        target_dir = get_target_dir(args.scope, args.target)

    print(f"项目根目录: {project_root}")
    print(f"目标根目录: {target_dir}")
    print()

    if args.action in ("install", "update"):
        success = do_install(project_root, target_dir, args.scope)
    elif args.action == "uninstall":
        if not _validate_uninstall(target_dir, args.scope):
            return 1
        success = do_uninstall(project_root, target_dir, args.scope)
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
