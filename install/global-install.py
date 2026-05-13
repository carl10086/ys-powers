#!/usr/bin/env python3
"""
ys-powers skills 全局安装脚本

功能：
1. 获取 ys-powers 项目的本地目录
2. 在用户主目录的 ~/.claude/ 下创建子目录
3. Skills: 文件夹级全量覆盖（同名文件夹整体替换）
4. Rules/Commands/Hooks/References: 文件级同名覆盖（同名文件替换，保留目标独有的文件/文件夹）
5. Agents: 文件夹级全量覆盖
6. 根据 install/renames.json 清理 stale 文件

使用方法：
    python install/global-install.py

注意：
- Hooks 全局自动注册暂未实现，安装完成后请根据提示手动配置 ~/.claude/settings.json
- 全局安装后，Claude Code 在所有项目都会加载 ~/.claude/ 下的能力
"""

import shutil
import sys
import json
from pathlib import Path


# 要安装的目录配置
# 格式: 源目录名 -> (目标子目录名, 策略)
# 策略: 'folder' = 文件夹级全量覆盖, 'file' = 文件级同名覆盖
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


def get_global_claude_dir() -> Path:
    """获取全局 Claude 配置目录 ~/.claude/"""
    return Path.home() / ".claude"


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


def install_folder_level(source_dir: Path, target_dir: Path) -> bool:
    """
    文件夹级全量覆盖策略

    对于源目录中的每个子项（文件/文件夹）：
    - 如果目标中存在同名项，删除它
    - 然后复制源项到目标

    保留目标目录中独有的、不在源目录中的项目
    """
    try:
        # 确保目标目录存在
        target_dir.mkdir(parents=True, exist_ok=True)

        # 遍历源目录中的所有项目
        for source_item in source_dir.iterdir():
            # 防止路径遍历：跳过包含路径分隔符或以 . 开头的名称
            if "/" in source_item.name or "\\" in source_item.name or source_item.name.startswith("."):
                print(f"  跳过非法名称: {source_item.name}", file=sys.stderr)
                continue
            target_item = target_dir / source_item.name

            # 如果目标中已存在同名项，删除它
            if target_item.exists():
                if target_item.is_dir():
                    shutil.rmtree(target_item)
                else:
                    target_item.unlink()

            # 复制源项到目标
            if source_item.is_dir():
                shutil.copytree(source_item, target_item)
            else:
                shutil.copy2(source_item, target_item)

        return True
    except PermissionError as e:
        print(f"    错误: 权限不足 - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"    错误: 复制过程中发生错误 - {e}", file=sys.stderr)
        return False


def install_file_level(source_dir: Path, target_dir: Path) -> bool:
    """
    文件级同名覆盖策略

    使用 shutil.copytree 的 dirs_exist_ok=True 参数：
    - 同名文件会被覆盖
    - 目标独有的文件/文件夹会被保留
    - 源目录中新增的文件会被复制
    """
    try:
        # dirs_exist_ok=True 实现文件级增量覆盖
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        return True
    except PermissionError as e:
        print(f"    错误: 权限不足 - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"    错误: 复制过程中发生错误 - {e}", file=sys.stderr)
        return False


def install_directory(source_name: str, target_name: str, strategy: str) -> bool:
    """
    安装单个目录

    Args:
        source_name: 源目录名（相对于项目根目录）
        target_name: 目标子目录名（相对于 ~/.claude/）
        strategy: 复制策略 ('folder' 或 'file')

    Returns:
        是否安装成功
    """
    project_root = get_project_root()
    source_dir = project_root / source_name
    target_dir = get_global_claude_dir() / target_name

    # 检查源目录是否存在
    if not source_dir.exists():
        print(f"⚠ {source_name.capitalize()} 目录不存在，跳过")
        print(f"  源路径: {source_dir}")
        return False

    if not source_dir.is_dir():
        print(f"⚠ {source_name.capitalize()} 路径不是目录，跳过", file=sys.stderr)
        print(f"  源路径: {source_dir}", file=sys.stderr)
        return False

    # file 策略下：先清理 stale 文件，再执行覆盖
    if strategy == "file":
        cleanup_stale_files(source_name, target_dir)

    # 根据策略执行复制
    if strategy == "folder":
        strategy_desc = "文件夹级全量覆盖"
        success = install_folder_level(source_dir, target_dir)
    elif strategy == "file":
        strategy_desc = "文件级同名覆盖"
        success = install_file_level(source_dir, target_dir)
    else:
        print(f"✗ {source_name.capitalize()} 未知策略: {strategy}", file=sys.stderr)
        return False

    # 输出结果
    if success:
        print(f"✓ {source_name.capitalize()} 安装成功（{strategy_desc}）")
        print(f"  源目录: {source_dir}")
        print(f"  目标目录: {target_dir}")
    else:
        print(f"✗ {source_name.capitalize()} 安装失败", file=sys.stderr)

    return success


def print_hooks_todo() -> None:
    """
    打印 hooks 全局注册的 TODO 提示。

    当前版本暂不自动注册 hooks 到 ~/.claude/settings.json，
    仅打印提示信息，由用户手动配置。
    """
    print()
    print("=" * 60)
    print("[TODO] Hooks 全局自动注册暂未实现")
    print("=" * 60)
    print()
    print("如需使用全局 hooks，请手动编辑 ~/.claude/settings.json：")
    print()
    print("1. 创建或编辑 ~/.claude/settings.json")
    print("2. 将 hooks/hooks.json 中的内容复制进去")
    print("3. 将路径中的 ${CLAUDE_PLUGIN_ROOT} 替换为 ~/.claude 的绝对路径")
    print("   例如: /Users/yourname/.claude")
    print()
    print("示例（将 ${CLAUDE_PLUGIN_ROOT} 替换为绝对路径）:")
    print('  "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"')
    print('  → "command": "bash /Users/yourname/.claude/hooks/session-start.sh"')
    print()
    print("注意: 全局 hooks 对所有项目生效。如需项目级覆盖，")
    print("      可在项目 ./.claude/settings.local.json 中定义同名 hook。")
    print("=" * 60)


def main():
    """主入口：批量处理所有目录"""
    project_root = get_project_root()
    global_dir = get_global_claude_dir()
    print(f"项目根目录: {project_root}")
    print(f"目标根目录: {global_dir}")
    print()

    results = []

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        success = install_directory(source_name, target_name, strategy)
        results.append((source_name, success))
        if success:
            print()

    # 打印 hooks TODO 提示
    print_hooks_todo()

    # 统计结果
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    print(f"安装完成: {success_count}/{total_count} 成功")

    # 如果有失败，以非零状态码退出
    if success_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
