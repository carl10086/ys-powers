#!/usr/bin/env python3
"""
ys-powers skills 本地安装脚本

功能：
1. 获取 ys-powers 项目的本地目录
2. 在当前工作目录创建 ./.claude/ 下的子目录
3. Skills: 文件夹级全量覆盖（同名文件夹整体替换）
4. Rules/Commands/Hooks/References: 文件级同名覆盖（同名文件替换，保留目标独有的文件/文件夹）
5. Agents: 文件夹级全量覆盖
6. Hooks: 复制后自动注册到 .claude/settings.local.json

使用方法：
    python install/local-install.py
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
    except (json.JSONDecodeError, IOError):
        return

    source_renames = renames.get(source_name, {})
    if not source_renames:
        return

    for old_name in source_renames:
        # 防止路径遍历：跳过包含路径分隔符或以 . 开头的名称
        if "/" in old_name or old_name.startswith("."):
            print(f"  跳过非法重命名键: {old_name}", file=sys.stderr)
            continue

        stale_file = target_dir / old_name
        if stale_file.exists():
            if stale_file.is_dir():
                shutil.rmtree(stale_file)
            else:
                stale_file.unlink()
            print(f"  清理 stale 文件: {old_name}")


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
        target_name: 目标子目录名（相对于 .claude/）
        strategy: 复制策略 ('folder' 或 'file')

    Returns:
        是否安装成功
    """
    project_root = get_project_root()
    source_dir = project_root / source_name
    target_dir = Path.cwd() / ".claude" / target_name

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


def install_hooks_settings() -> bool:
    """
    注册 hooks 到 settings.local.json

    读取 hooks/hooks.json（如果存在），转换路径后合并到 .claude/settings.local.json
    路径转换: ${CLAUDE_PLUGIN_ROOT} -> ${CLAUDE_PROJECT_DIR}/.claude
    """
    project_root = get_project_root()
    hooks_json_path = project_root / "hooks" / "hooks.json"

    if not hooks_json_path.exists():
        print("ℹ Hooks 配置未找到（hooks/hooks.json 不存在），跳过注册")
        return True

    try:
        # 读取 hooks.json
        with open(hooks_json_path, 'r', encoding='utf-8') as f:
            hooks_config = json.load(f)

        if "hooks" not in hooks_config:
            print("ℹ hooks.json 中没有 hooks 字段，跳过注册")
            return True

        # 转换路径：把 ${CLAUDE_PLUGIN_ROOT} 替换为 ${CLAUDE_PROJECT_DIR}/.claude
        hooks_str = json.dumps(hooks_config["hooks"])
        hooks_str = hooks_str.replace("${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_PROJECT_DIR}/.claude")
        converted_hooks = json.loads(hooks_str)

        # 读取现有的 settings.local.json
        settings_path = Path.cwd() / ".claude" / "settings.local.json"
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            settings = {}

        # 合并 hooks（如果已存在则追加，避免覆盖）
        if "hooks" not in settings:
            settings["hooks"] = {}

        for hook_type, hook_list in converted_hooks.items():
            if hook_type not in settings["hooks"]:
                settings["hooks"][hook_type] = hook_list
                print(f"  添加 hook: {hook_type}")
            else:
                # 用整个 hook dict 的 JSON 字符串（排序键）作为去重 key
                # 避免 matcher 为空字符串时误判为重复
                existing_hooks = {json.dumps(h, sort_keys=True) for h in settings["hooks"][hook_type]}
                for hook in hook_list:
                    hook_key = json.dumps(hook, sort_keys=True)
                    if hook_key not in existing_hooks:
                        settings["hooks"][hook_type].append(hook)
                        print(f"  追加 hook: {hook_type}")
                        existing_hooks.add(hook_key)
                    else:
                        print(f"  跳过已存在 hook: {hook_type}")

        # 写回 settings.local.json（先备份）
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        if settings_path.exists():
            backup_path = settings_path.with_suffix('.json.bak')
            shutil.copy2(settings_path, backup_path)
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

        print(f"✓ Hooks 注册成功")
        print(f"  配置文件: {settings_path}")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ hooks.json 解析失败: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Hooks 注册失败: {e}", file=sys.stderr)
        return False


def main():
    """主入口：批量处理所有目录"""
    project_root = get_project_root()
    print(f"项目根目录: {project_root}")
    print(f"目标根目录: {Path.cwd() / '.claude'}")
    print()

    results = []

    for source_name, (target_name, strategy) in DIRECTORIES.items():
        success = install_directory(source_name, target_name, strategy)
        results.append((source_name, success))
        if success:
            print()

    # 注册 hooks（如果 hooks 目录安装成功）
    hooks_success = any(name == "hooks" and success for name, success in results)
    if hooks_success:
        print("正在注册 hooks...")
        hook_register_success = install_hooks_settings()
        results.append(("hooks-registration", hook_register_success))
        if hook_register_success:
            print()

    # 统计结果
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    print(f"安装完成: {success_count}/{total_count} 成功")

    # 如果有失败，以非零状态码退出
    if success_count == 0 and total_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
