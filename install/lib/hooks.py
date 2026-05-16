"""Hooks 注入与反注册"""

import json
import shutil
import sys
from pathlib import Path


def _load_hooks_config(project_root: Path, scope: str) -> dict | None:
    """
    读取 hooks/hooks.json，local install 时替换路径前缀。

    Returns:
        转换后的 hooks dict，或 None（文件不存在/解析失败）
    """
    hooks_json_path = project_root / "hooks" / "hooks.json"

    if not hooks_json_path.exists():
        print("ℹ Hooks 配置未找到（hooks/hooks.json 不存在），跳过")
        return None

    try:
        with open(hooks_json_path, 'r', encoding='utf-8') as f:
            hooks_config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"✗ hooks.json 解析失败: {e}", file=sys.stderr)
        return None

    if "hooks" not in hooks_config:
        print("ℹ hooks.json 中没有 hooks 字段，跳过")
        return None

    hooks_str = json.dumps(hooks_config["hooks"])
    if scope == "local":
        # 假设：hooks.json 中所有 "$HOME/.claude" 出现均为 hooks 路径前缀
        hooks_str = hooks_str.replace("$HOME/.claude", "${CLAUDE_PROJECT_DIR}/.claude")
    return json.loads(hooks_str)


def _backup_and_write_settings(settings_path: Path, settings: dict) -> bool:
    """备份并写回 settings 文件。"""
    try:
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        if settings_path.exists():
            backup_path = settings_path.with_suffix('.json.bak')
            shutil.copy2(settings_path, backup_path)
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"✗ 写回设置失败: {e}", file=sys.stderr)
        return False


def inject_hooks(
    project_root: Path,
    target_dir: Path,
    scope: str
) -> bool:
    """
    将 hooks 注入目标 settings 文件。

    Args:
        project_root: ys-powers 项目根目录
        target_dir: 目标目录（如 ~/.claude/ 或 ./.claude/）
        scope: 安装范围（"global" 或 "local"）

    Returns:
        是否注入成功
    """
    converted_hooks = _load_hooks_config(project_root, scope)
    if converted_hooks is None:
        return True

    # 确定目标 settings 文件
    if scope == "global":
        settings_path = target_dir / "settings.json"
    else:
        settings_path = target_dir / "settings.local.json"

    try:
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            settings = {}

        if "hooks" not in settings:
            settings["hooks"] = {}

        for hook_type, hook_list in converted_hooks.items():
            if hook_type not in settings["hooks"]:
                settings["hooks"][hook_type] = hook_list
                print(f"  添加 hook: {hook_type}")
            else:
                existing_hooks = {
                    json.dumps(h, sort_keys=True)
                    for h in settings["hooks"][hook_type]
                }
                for hook in hook_list:
                    hook_key = json.dumps(hook, sort_keys=True)
                    if hook_key not in existing_hooks:
                        settings["hooks"][hook_type].append(hook)
                        print(f"  追加 hook: {hook_type}")
                        existing_hooks.add(hook_key)
                    else:
                        print(f"  跳过已存在 hook: {hook_type}")

        if _backup_and_write_settings(settings_path, settings):
            print(f"✓ Hooks 注册成功")
            print(f"  配置文件: {settings_path}")
            return True
        return False

    except Exception as e:
        print(f"✗ Hooks 注册失败: {e}", file=sys.stderr)
        return False


def remove_hooks(
    project_root: Path,
    target_dir: Path,
    scope: str
) -> bool:
    """
    从目标 settings 文件中反注册 ys-powers 的 hooks。

    通过精确匹配 hook 的 JSON 序列化 key 来移除，不删除用户自定义 hooks。

    Args:
        project_root: ys-powers 项目根目录
        target_dir: 目标目录
        scope: 安装范围（"global" 或 "local"）

    Returns:
        是否反注册成功（目标不存在视为成功）
    """
    converted_hooks = _load_hooks_config(project_root, scope)
    if converted_hooks is None:
        return True

    # 确定目标 settings 文件
    if scope == "global":
        settings_path = target_dir / "settings.json"
    else:
        settings_path = target_dir / "settings.local.json"

    if not settings_path.exists():
        print("ℹ 设置文件不存在，跳过 hooks 反注册")
        return True

    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"✗ 读取设置失败: {e}", file=sys.stderr)
        return False

    if "hooks" not in settings or not settings["hooks"]:
        print("ℹ 设置文件中无 hooks，跳过反注册")
        return True

    removed_any = False

    for hook_type, hook_list in converted_hooks.items():
        if hook_type not in settings["hooks"]:
            continue

        # 构建要移除的 hook key 集合
        keys_to_remove = {json.dumps(h, sort_keys=True) for h in hook_list}

        original_len = len(settings["hooks"][hook_type])
        settings["hooks"][hook_type] = [
            h for h in settings["hooks"][hook_type]
            if json.dumps(h, sort_keys=True) not in keys_to_remove
        ]

        if len(settings["hooks"][hook_type]) < original_len:
            removed_any = True
            print(f"  移除 hook: {hook_type}")

        # 如果该类型下已空，删除该 key
        if not settings["hooks"][hook_type]:
            del settings["hooks"][hook_type]

    # 如果 hooks 整体已空，删除 hooks 字段
    if settings.get("hooks") == {}:
        del settings["hooks"]

    if removed_any:
        if _backup_and_write_settings(settings_path, settings):
            print(f"✓ Hooks 反注册成功")
            return True
        return False
    else:
        print("ℹ 未找到匹配的 hooks，无需反注册")
        return True
