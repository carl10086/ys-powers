#!/usr/bin/env python3
"""
ys-powers skills 本地安装脚本

功能：
1. 获取 ys-powers 项目的本地目录
2. 在当前工作目录创建 ./.claude/skills 和 ./.claude/rules
3. Skills: 文件夹级全量覆盖（同名文件夹整体替换）
4. Rules: 文件级同名覆盖（同名文件替换，保留目标独有的文件/文件夹）

使用方法：
    python install/local-install.py
"""

import shutil
import sys
from pathlib import Path


# 要安装的目录配置
# 格式: 源目录名 -> (目标子目录名, 策略)
# 策略: 'folder' = 文件夹级全量覆盖, 'file' = 文件级同名覆盖
DIRECTORIES = {
    "skills": ("skills", "folder"),
    "rules": ("rules", "file"),
    "commands": ("commands", "file")
}


def get_project_root() -> Path:
    """通过脚本位置确定项目根目录"""
    script_path = Path(__file__).resolve()
    # 脚本位于 install/ 目录下，项目根目录是上一级
    return script_path.parent.parent


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

    # 统计结果
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    print(f"安装完成: {success_count}/{total_count} 成功")

    # 如果有失败，以非零状态码退出
    if success_count == 0 and total_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
