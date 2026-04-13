#!/usr/bin/env python3
"""
ys-powers skills 本地安装脚本

功能：
1. 获取 ys-powers 项目的本地目录
2. 在当前工作目录创建 ./.claude/skills 和 ./.claude/rules
3. 将项目中的 skills 和 rules 目录全量覆盖到目标位置

使用方法：
    python install/local-install.py
"""

import shutil
import sys
from pathlib import Path


# 要安装的目录映射：源目录名 -> 目标子目录名
DIRECTORIES = {
    "skills": "skills",
    "rules": "rules"
}


def get_project_root() -> Path:
    """通过脚本位置确定项目根目录"""
    script_path = Path(__file__).resolve()
    # 脚本位于 install/ 目录下，项目根目录是上一级
    return script_path.parent.parent


def install_directory(source_name: str, target_name: str) -> bool:
    """
    安装单个目录

    Args:
        source_name: 源目录名（相对于项目根目录）
        target_name: 目标子目录名（相对于 .claude/）

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

    # 执行复制（全量覆盖）
    try:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        print(f"✓ {source_name.capitalize()} 安装成功（全量覆盖）")
        print(f"  源目录: {source_dir}")
        print(f"  目标目录: {target_dir}")
        return True
    except PermissionError as e:
        print(f"✗ {source_name.capitalize()} 安装失败", file=sys.stderr)
        print(f"  错误: 权限不足，无法写入 {target_dir}", file=sys.stderr)
        print(f"  详情: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ {source_name.capitalize()} 安装失败", file=sys.stderr)
        print(f"  错误: 复制过程中发生错误 - {e}", file=sys.stderr)
        return False


def main():
    """主入口：批量处理所有目录"""
    project_root = get_project_root()
    print(f"项目根目录: {project_root}")
    print(f"目标根目录: {Path.cwd() / '.claude'}")
    print()

    results = []

    for source_name, target_name in DIRECTORIES.items():
        success = install_directory(source_name, target_name)
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
