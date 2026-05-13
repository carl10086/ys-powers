"""文件系统操作：安装策略、stale cleanup、卸载"""

import json
import shutil
import sys
from pathlib import Path

def cleanup_stale_files(project_root: Path, source_name: str, target_dir: Path) -> None:
    """
    根据 renames.json 清理目标目录中的 stale 文件。

    读取 install/renames.json，根据当前 source_name 取对应映射，
    删除目标目录中仍存在的旧名文件。
    """
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
            except OSError as e:
                print(f"  错误: 无法删除 {old_name}: {e}", file=sys.stderr)
        except FileNotFoundError:
            pass
        except OSError as e:
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


def install_directory(
    project_root: Path,
    source_name: str,
    target_dir: Path,
    target_name: str,
    strategy: str
) -> bool:
    """
    安装单个目录

    Args:
        project_root: ys-powers 项目根目录
        source_name: 源目录名（相对于项目根目录）
        target_dir: 目标目录（如 ~/.claude/ 或 ./.claude/）
        target_name: 目标子目录名（如 skills, rules）
        strategy: 复制策略 ('folder' 或 'file')

    Returns:
        是否安装成功
    """
    source_dir = project_root / source_name
    target_subdir = target_dir / target_name

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
        cleanup_stale_files(project_root, source_name, target_subdir)

    # 根据策略执行复制
    if strategy == "folder":
        strategy_desc = "文件夹级全量覆盖"
        success = install_folder_level(source_dir, target_subdir)
    elif strategy == "file":
        strategy_desc = "文件级同名覆盖"
        success = install_file_level(source_dir, target_subdir)
    else:
        print(f"✗ {source_name.capitalize()} 未知策略: {strategy}", file=sys.stderr)
        return False

    # 输出结果
    if success:
        print(f"✓ {source_name.capitalize()} 安装成功（{strategy_desc}）")
        print(f"  源目录: {source_dir}")
        print(f"  目标目录: {target_subdir}")
    else:
        print(f"✗ {source_name.capitalize()} 安装失败", file=sys.stderr)

    return success


def uninstall_directory(
    project_root: Path,
    source_name: str,
    target_dir: Path,
    target_name: str,
    strategy: str,
) -> bool:
    """
    卸载单个目录

    遍历源目录中的每个项目，仅删除目标目录中与之同名的文件/目录。
    对于 file 策略，额外清理 renames.json 中记录的旧名。
    绝不删除整个目标目录，保留目标中不在源目录里的项目。

    Args:
        project_root: ys-powers 项目根目录
        source_name: 源目录名（相对于项目根目录）
        target_dir: 目标目录（如 ~/.claude/ 或 ./.claude/）
        target_name: 目标子目录名（如 skills, rules）
        strategy: 复制策略 ('folder' 或 'file')，用于决定是否清理 stale 文件

    Returns:
        是否卸载成功（目标不存在视为成功）
    """
    # strategy 当前未使用，保留参数以维持 API 一致性
    _ = strategy

    source_dir = project_root / source_name
    target_subdir = target_dir / target_name

    if not target_subdir.exists():
        print(f"ℹ {target_name.capitalize()} 未安装，跳过卸载")
        return True

    if not source_dir.exists():
        print(f"✗ {source_name.capitalize()} 源目录不存在，跳过卸载", file=sys.stderr)
        return False

    all_ok = True

    # 遍历源目录，删除目标中同名的项目
    for source_item in source_dir.iterdir():
        # 路径遍历防护
        if (
            "/" in source_item.name
            or "\\" in source_item.name
            or source_item.name.startswith(".")
        ):
            continue

        target_item = target_subdir / source_item.name
        if target_item.exists():
            try:
                if target_item.is_dir():
                    shutil.rmtree(target_item)
                else:
                    target_item.unlink()
                print(f"  删除: {target_name}/{source_item.name}")
            except PermissionError as e:
                print(
                    f"  错误: 无法删除 {target_name}/{source_item.name}: 权限不足 - {e}",
                    file=sys.stderr,
                )
                all_ok = False
            except Exception as e:
                print(
                    f"  错误: 无法删除 {target_name}/{source_item.name}: {e}",
                    file=sys.stderr,
                )
                all_ok = False

    # 清理 renames.json 中记录的旧名
    cleanup_stale_files(project_root, source_name, target_subdir)

    if all_ok:
        print(f"✓ {target_name.capitalize()} 卸载成功")
    else:
        print(f"✗ {target_name.capitalize()} 卸载失败", file=sys.stderr)

    return all_ok
