# Spec: Unified Installer for ys-powers

## Objective

为 `ys-powers` 设计并实现一个**统一安装器**，替代现有的 `global-install.py` 与 `local-install.py` 两个分散脚本，解决代码重复、hooks 注入缺失、无更新/卸载能力等问题。

**用户故事：**
- 作为用户，我希望通过一个命令完成全局或本地安装，而不必记住多个脚本路径
- 作为用户，我希望安装后能自动注册 hooks，无需手动编辑 settings.json
- 作为用户，我希望在任意项目都能运行安装器，给指定项目安装 ys-powers 能力
- 作为用户，我希望能够安全地更新或卸载已安装的能力

**验收标准：**
1. 运行 `make global-install` 后，`~/.claude/` 下出现完整的 skills/rules/commands/agents/hooks/references，且 `~/.claude/settings.json` 已注册 hooks
2. 运行 `make local-install` 后，当前项目的 `./.claude/` 下出现相同结构，且 `./.claude/settings.local.json` 已注册 hooks
3. 运行 `make local-install project-dir=~/projects/foo` 后，指定目录的 `.claude/` 下出现安装内容
4. 运行 `make uninstall-global` 后，`~/.claude/` 下仅 ys-powers 管理的同名文件/目录被清理（如 `skills/using-agent-skills/` 被删，但用户自有的 `skills/find-docs/` 保留），且 `settings.json` 中的相关 hooks 被移除
5. 现有 `local-install.py` 行为保持不变（向后兼容），但文档标记为 deprecated

## Tech Stack

- Python 3.9+（复用现有脚本的标准库：`pathlib`、`shutil`、`json`、`argparse`）
- Makefile（封装常用命令，降低用户记忆负担）
- 零外部依赖

## Commands

### 统一安装器 CLI

```bash
# 安装
python install/install.py install global                           # 全局安装到 ~/.claude/
python install/install.py install local                            # 本地安装到 ./.claude/
python install/install.py install local --target ~/projects/foo    # 安装到指定目录

# 更新（增量同步 + hooks 去重 merge）
python install/install.py update global
python install/install.py update local
python install/install.py update local --target ~/projects/foo

# 卸载（清理文件 + 反注册 hooks）
python install/install.py uninstall global
python install/install.py uninstall local
python install/install.py uninstall local --target ~/projects/foo
```

### Makefile 封装

```bash
make global-install                           # → install global
make local-install                            # → install local
make local-install project-dir=~/projects/foo # → install local --target
make update-global                            # → update global
make update-local                             # → update local
make uninstall-global                         # → uninstall global
make uninstall-local                          # → uninstall local
```

### 向后兼容（deprecated）

```bash
python install/local-install.py   # 行为不变，打印 deprecation warning
python install/global-install.py  # 行为不变，打印 deprecation warning
```

## Project Structure

```
ys-powers/
├── install/
│   ├── install.py          # 统一安装器入口（新增）
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── config.py       # DIRECTORIES 配置、路径常量
│   │   ├── fs.py           # 文件系统操作（folder/file 策略、stale cleanup）
│   │   └── hooks.py        # hooks 注入/反注册逻辑
│   ├── local-install.py    # 现有，保留但标记 deprecated
│   ├── global-install.py   # 现有，保留但标记 deprecated
│   └── renames.json        # 现有，继续使用
├── Makefile                # 新增：封装常用命令
└── docs/ys-powers/specs/
    └── 2026-05-14-unified-installer-design.md  # 本 spec
```

## Code Style

复用现有脚本的编码风格，提取共享模块后保持一致。

**示例（install.py 入口）：**

```python
#!/usr/bin/env python3
"""ys-powers unified installer."""

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
    if scope == "global":
        return Path.home() / ".claude"
    if target:
        return target / ".claude"
    return Path.cwd() / ".claude"


def resolve_hooks_path_variable(scope: str, target_dir: Path) -> str:
    if scope == "global":
        return str(target_dir.resolve())
    return "${CLAUDE_PROJECT_DIR}/.claude"


def main() -> int:
    parser = argparse.ArgumentParser(description="ys-powers installer")
    parser.add_argument("action", choices=["install", "update", "uninstall"])
    parser.add_argument("scope", choices=["global", "local"])
    parser.add_argument("--target", type=Path, help="项目目录（仅 local 有效）")
    args = parser.parse_args()

    project_root = get_project_root()
    target_dir = get_target_dir(args.scope, args.target)
    path_var = resolve_hooks_path_variable(args.scope, target_dir)

    if args.action in ("install", "update"):
        for source_name, (target_name, strategy) in DIRECTORIES.items():
            install_directory(project_root, source_name, target_dir, target_name, strategy)
        inject_hooks(project_root, target_dir, path_var, args.action == "update")
    elif args.action == "uninstall":
        for source_name, (target_name, strategy) in DIRECTORIES.items():
            uninstall_directory(project_root, source_name, target_dir, target_name, strategy)
        remove_hooks(project_root, target_dir, path_var)

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**关键约定：**
- 使用 `pathlib.Path` 处理路径，不使用 `os.path`
- 函数返回 `bool` 或 `int`（exit code），错误打印到 `sys.stderr`
- 状态输出使用 `print(f"✓ {name} ...")` 风格
- 路径遍历防护：跳过包含 `/`、`\\` 或以 `.` 开头的名称
- 备份策略：修改 `settings.json` / `settings.local.json` 前先复制 `.bak`

## Testing Strategy

- **无自动化测试**：安装脚本属于运维工具，验证以手动执行 + 目录结构检查为主
- **验证清单：**
  1. 运行 `make global-install`，检查 `~/.claude/` 目录结构正确，hooks 已注入 `settings.json`
  2. 运行 `make local-install`，检查 `./.claude/` 目录结构正确，hooks 已注入 `settings.local.json`
  3. 运行 `make local-install project-dir=~/tmp/test-project`，检查指定目录安装正确
  4. 运行 `make update-global`，检查增量同步不破坏用户已有配置
  5. 运行 `make uninstall-global`，检查 `~/.claude/` 下 ys-powers 文件已清理，hooks 已反注册
  6. 验证 `local-install.py` 仍能正常运行（向后兼容）

## Boundaries

- **Always：**
  - `install` / `update` 操作前备份目标 settings 文件
  - `uninstall` 采用**精确匹配删除**：遍历源目录中的每个项目，仅删除目标目录中与之同名的文件/目录；对于 file 策略，额外清理 `renames.json` 中记录的旧名。绝不删除整个目标目录，绝不删除目标中不在源目录里的项目
  - 路径遍历防护：所有文件名/目录名校验必须跳过含路径分隔符或以 `.` 开头的名称
  - `update` 使用增量 merge（file 策略：dirs_exist_ok=True；folder 策略：同名替换，保留独有文件）
  - hooks 注入使用 JSON 序列化去重，避免重复注册
- **Ask first：**
  - 修改 `local-install.py` 或 `global-install.py` 的行为（当前方案是保留并标记 deprecated）
  - 在 `install/lib/` 之外新增共享模块
  - 添加外部依赖（如 `click`、`rich`）
  - 修改 DIRECTORIES 配置（增减安装目录）
- **Never：**
  - 删除整个 `~/.claude/` 或 `./.claude/` 目录
  - 在 uninstall 中删除用户的 `settings.json`、`memory/`、自定义 hooks 等
  - 引入 `--source` 参数（通过 `__file__` 自定位，保持简单）
  - 支持多 IDE/CLI（当前范围仅限 Claude Code）

## Success Criteria

1. `install/install.py` 实现 `install/update/uninstall` × `global/local` 全部 6 种组合
2. `--target` 参数支持给任意目录安装 local 能力
3. `make global-install` / `make local-install` / `make update-global` / `make uninstall-global` 等命令工作正常
4. 全局安装自动将 hooks 注入 `~/.claude/settings.json`，本地安装自动注入 `./.claude/settings.local.json`
5. `uninstall` 精确清理：遍历源目录，仅删除目标目录中同名的文件/目录；file 策略下额外清理 `renames.json` 中的旧名。不删除用户其他配置，不删除整个目标目录
6. 现有 `local-install.py` 行为不变，运行后打印 deprecation warning
7. `install/lib/` 中的共享模块被 global/local deprecated 脚本和新的 install.py 共用

## Open Questions

1. 现有 `global-install.py` 和 `local-install.py` 是直接删除还是保留并改写成调用 `install/install.py` 的薄包装？
   - **建议**：保留并改写成薄包装（向后兼容 + 打印 deprecation warning），减少用户迁移成本。
2. `update` 与 `install` 在 folder 策略下的差异是否需要显式区分？folder 策略本身就是"同名替换"，install 和 update 的行为天然一致。
   - **建议**：`update` 在 CLI 层面作为 `install` 的别名存在，仅在 hooks 处理上增加去重 merge（install 是追加，update 是去重追加）。
