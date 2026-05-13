#!/usr/bin/env python3
"""
ys-powers 本地卸载脚本

功能：
1. 清理当前项目 ./.claude/ 下由 ys-powers 安装的文件和目录
2. 根据 install/renames.json 清理 stale（旧名）文件
3. 提示用户手动检查 ./.claude/settings.local.json 中的 hooks

清理范围：
- skills/、commands/、agents/、rules/、hooks/、references/
- renames.json 中记录的旧名文件（仅针对 file 策略目录）

保留内容：
- 用户自己的 settings.json、settings.local.json（仅提示检查 hooks）
- memory/、plugins/ 等非 ys-powers 目录
- 用户自定义文件

使用方法：
    python install/remove-local

注意：
- 本脚本只删除 ys-powers 安装的内容，不会删除整个 .claude/ 目录
- 运行前请确认当前目录是目标项目根目录
"""

import shutil
import sys
import json
from pathlib import Path


# 要清理的目录配置
# 格式: 源目录名 -> (目标子目录名, 策略)
# 策略: 'folder' = 文件夹级删除, 'file' = 文件级删除（需额外处理 renames）
DIRECTORIES = {
    "skills": ("skills", "folder"),
    "rules": ("rules", "file"),
    "commands": ("commands", "file"),
    "agents": ("agents", "folder"),
    "hooks": ("hooks", "file"),
    "references": ("references", "file")
}


def get_project_root() -> Path:
    """通过脚本位置确定项目根目录"""
    script_path = Path(__file__).resolve()
    # 脚本位于 install/ 目录下，项目根目录是上一级
    return script_path.parent.parent


def get_local_claude_dir() -> Path:
    """获取当前项目的 Claude 配置目录 ./.claude/"""
    return Path.cwd() / ".claude"


def cleanup_stale_files(source_name: str, target_dir: Path) -> None:
    """
    根据 renames.json 清理目标目录中的 stale 文件。

    读取 install/renames.json，根据当前 source_name 取对应映射，
    删除目标目录中仍存在的旧名文件。
    """
    project_root = get_project_root()
    renames_path = project_root / "install" / "renames.json"

    if not renames_path.exists():
        return

    try:
        with open(renames_path, 'r', encoding='utf-8') as f:
            renames = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  警告: 无法读取 renames.json: {e}", file=sys.stderr)
        return

    if not isinstance(renames, dict):
        print(f"  警告: renames.json 格式错误，应为对象", file=sys.stderr)
        return

    source_renames = renames.get(source_name, {})
    if not isinstance(source_renames, dict):
        print(f"  警告: renames.json 中 {source_name} 不是对象", file=sys.stderr)
        return

    if not source_renames:
        return

    for old_name in source_renames:
        # 防止路径遍历：跳过包含路径分隔符或以 . 开头的名称
        if "/" in old_name or "\\" in old_name or old_name.startswith("."):
            print(f"  跳过非法重命名键: {old_name}", file=sys.stderr)
            continue

        stale_file = target_dir / old_name
        try:
            # 先尝试 unlink（安全处理文件和 symlink 本身，不跟随 symlink）
            stale_file.unlink()
            print(f"  清理 stale 文件: {old_name}")
        except IsADirectoryError:
            # 是目录，递归删除
            try:
                shutil.rmtree(stale_file)
                print(f"  清理 stale 目录: {old_name}")
            except (PermissionError, OSError) as e:
                print(f"  错误: 无法删除 {old_name}: {e}", file=sys.stderr)
        except FileNotFoundError:
            pass
        except (PermissionError, OSError) as e:
            print(f"  错误: 无法删除 {old_name}: {e}", file=sys.stderr)


def remove_directory(source_name: str, target_name: str, strategy: str) -> bool:
    """
    删除单个目录

    Args:
        source_name: 源目录名（用于查找 renames.json 中的映射）
        target_name: 目标子目录名（相对于 ./.claude/）
        strategy: 删除策略 ('folder' 或 'file')

    Returns:
        是否删除成功（目录不存在也视为成功）
    """
    target_dir = get_local_claude_dir() / target_name

    # 如果目标目录不存在，跳过
    if not target_dir.exists():
        print(f"ℹ {source_name.capitalize()} 目录不存在，跳过")
        return True

    # file 策略下：先清理 stale 文件，再删除整个目录
    if strategy == "file":
        cleanup_stale_files(source_name, target_dir)

    # 删除整个目录
    try:
        if target_dir.is_dir():
            shutil.rmtree(target_dir)
        else:
            target_dir.unlink()
        print(f"✓ {source_name.capitalize()} 已删除")
        print(f"  路径: {target_dir}")
        return True
    except PermissionError as e:
        print(f"✗ {source_name.capitalize()} 删除失败: 权限不足 - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ {source_name.capitalize()} 删除失败: {e}", file=sys.stderr)
        return False


def print_hooks_reminder() -> None:
    """
    打印 hooks 清理提示。

    当前版本暂不自动修改 settings.local.json，
    仅打印提示信息，由用户手动检查并移除 ys-powers 注册的 hooks。
    """
    print()
    print("=" * 60)
    print("[提示] Hooks 反注册需手动完成")
    print("=" * 60)
    print()
    print("如需彻底清理 ys-powers 的 hooks，请手动检查并编辑：")
    print(f"  {get_local_claude_dir() / 'settings.local.json'}")
    print()
    print("需要检查并移除的 hooks 路径特征：")
    print("  - 包含 ${CLAUDE_PROJECT_DIR}/.claude/skills/ 的路径")
    print("  - 包含 ${CLAUDE_PROJECT_DIR}/.claude/commands/ 的路径")
    print("  - 包含 ${CLAUDE_PROJECT_DIR}/.claude/rules/ 的路径")
    print("  - 包含 ${CLAUDE_PROJECT_DIR}/.claude/hooks/ 的路径")
    print("  - 包含 ${CLAUDE_PROJECT_DIR}/.claude/references/ 的路径")
    print()
    print("注意: 如果你计划稍后重新安装 ys-powers（本地或全局），")
    print("      可以保留 hooks 配置，安装脚本会自动去重。")
    print("=" * 60)


def main():
    """主入口：批量清理所有目录"""
    local_dir = get_local_claude_dir()
    print(f"项目目录: {Path.cwd()}")
    print(f"目标根目录: {local_dir}")
    print()

    # 检查目标根目录是否存在
    if not local_dir.exists():
        print(f"⚠ {local_dir} 不存在，无需清理")
        return

    results = []

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        success = remove_directory(source_name, target_name, strategy)
        results.append((source_name, success))
        if success:
            print()

    # 打印 hooks 清理提示
    print_hooks_reminder()

    # 统计结果
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    print(f"清理完成: {success_count}/{total_count} 成功")

    # 检查 .claude/ 是否为空目录（只有空目录时提示）
    if local_dir.exists():
        try:
            remaining = list(local_dir.iterdir())
            if not remaining:
                print()
                print(f"ℹ {local_dir} 已为空目录，如需删除可手动执行：")
                print(f"    rmdir {local_dir}")
        except PermissionError:
            pass

    # 如果有失败，以非零状态码退出
    if success_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
