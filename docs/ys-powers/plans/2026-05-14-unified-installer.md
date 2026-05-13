# Implementation Plan: Unified Installer

## Overview

基于 spec `docs/ys-powers/specs/2026-05-14-unified-installer-design.md`，将现有的 `global-install.py` 与 `local-install.py` 重构为一个统一安装器，提取共享模块，新增 update/uninstall 能力，并提供 Makefile 封装。

## Architecture Decisions

- **共享模块优先**：先提取 `install/lib/`，再构建 `install/install.py`，最后把 deprecated 脚本改写成薄包装
- **垂直切片**：每个任务完成一条完整的能力路径（如：fs 模块 → install global → verify），而非按层横向开发
- **Hooks 独立开发**：`lib/hooks.py` 与 `lib/fs.py` 无依赖关系，可并行实现
- **向后兼容最后做**：只有在新安装器验证通过后才改写 deprecated 脚本

## Dependency Graph

```
lib/config.py         lib/hooks.py
      ↑                      ↑
lib/fs.py ←────────────┬─────┘
      ↑                │
install/install.py ────┘
      ↑
Makefile
      ↑
local-install.py (deprecated wrapper)
global-install.py (deprecated wrapper)
```

## Task Breakdown

### Phase 1: 共享模块（基础设施）

---

**Task 1: 提取文件系统共享模块 `lib/config.py` + `lib/fs.py`**

- **Description:** 从 `local-install.py` 提取 DIRECTORIES 配置、folder/file 复制策略、stale cleanup 逻辑到共享模块，新增 uninstall_directory 能力。
- **Acceptance criteria:**
  - [ ] `install/lib/__init__.py` 存在且可导入
  - [ ] `install/lib/config.py` 导出 `DIRECTORIES` 字典（与现有配置一致）
  - [ ] `install/lib/fs.py` 导出 `install_directory()` 和 `uninstall_directory()`
  - [ ] `install_directory()` 支持 folder 策略（全量覆盖子项）和 file 策略（dirs_exist_ok=True）
  - [ ] `install_directory()` 在 file 策略下自动调用 `cleanup_stale_files()`
  - [ ] `cleanup_stale_files()` 读取 `install/renames.json` 并清理目标目录中的旧名文件/目录
  - [ ] `uninstall_directory()` 采用精确匹配删除：遍历源目录中的每个项目，仅删除目标目录中与之同名的文件/目录；绝不删除整个目标目录
  - [ ] `uninstall_directory()` 在 file 策略下，额外调用 `cleanup_stale_files()` 清理 `renames.json` 中记录的旧名
  - [ ] `uninstall_directory()` 保留目标目录中不在源目录里的项目（如用户自有的 `skills/find-docs/`）
  - [ ] 所有函数保持路径遍历防护（跳过含 `/`、`\\`、以 `.` 开头的名称）
  - [ ] 错误处理：权限错误打印到 stderr 并返回 False，不抛异常终止流程
- **Verify:**
  - [ ] `cd install && python -c "from lib.fs import install_directory, uninstall_directory; print('ok')"` 无报错
  - [ ] 运行临时测试脚本，验证 folder 策略能正确复制 `skills/` 到 `/tmp/test-claude/skills/`
  - [ ] 验证 file 策略能正确复制 `rules/` 到 `/tmp/test-claude/rules/`，并保留目标已有文件
  - [ ] 验证 uninstall_directory 只删除目标中与源同名的项目，保留目标中独有的项目（如在 `/tmp/test-claude/skills/` 下手动添加的 `user-skill/` 应保留）
  - [ ] 验证 file 策略下 uninstall_directory 同时清理 `renames.json` 中记录的旧名文件
- **Files likely touched:**
  - `install/lib/__init__.py`
  - `install/lib/config.py`
  - `install/lib/fs.py`
- **Estimated scope:** Medium

---

**Task 2: 提取 Hooks 共享模块 `lib/hooks.py`**

- **Description:** 从 `local-install.py` 提取 hooks 注入逻辑，新增全局 settings.json 支持、update 去重 merge、remove_hooks 反注册能力。
- **Acceptance criteria:**
  - [ ] `install/lib/hooks.py` 导出 `inject_hooks()` 和 `remove_hooks()`
  - [ ] `inject_hooks()` 读取 `hooks/hooks.json`，将 `${CLAUDE_PLUGIN_ROOT}` 替换为传入的 `path_var`
  - [ ] `inject_hooks()` 支持 `merge=True`（update 模式：去重追加）和 `merge=False`（install 模式：直接追加）
  - [ ] 去重逻辑：使用 `json.dumps(hook, sort_keys=True)` 作为 key，避免重复注册
  - [ ] 目标文件：global 模式写入 `~/.claude/settings.json`，local 模式写入 `{target}/.claude/settings.local.json`
  - [ ] 写回前自动备份原文件为 `.json.bak`
  - [ ] `remove_hooks()` 读取转换后的 hooks 清单，从目标 settings 文件中精确匹配并移除
  - [ ] `remove_hooks()` 如果目标 settings 文件不存在或 hooks 字段已空，优雅跳过
- **Verify:**
  - [ ] `cd install && python -c "from lib.hooks import inject_hooks, remove_hooks; print('ok')"` 无报错
  - [ ] 在 `/tmp/test-claude/` 下创建假的 `settings.json`，运行 `inject_hooks()`，验证 hooks 已追加且文件已备份
  - [ ] 再次运行 `inject_hooks(merge=True)`，验证 hooks 没有去重追加（同一 hook 只出现一次）
  - [ ] 运行 `remove_hooks()`，验证 settings.json 中 ys-powers 的 hooks 已移除，其他配置保留
- **Files likely touched:**
  - `install/lib/hooks.py`
- **Estimated scope:** Medium

---

### Checkpoint: After Phase 1

- [ ] `lib/fs.py` 和 `lib/hooks.py` 均可独立导入且功能完整
- [ ] uninstall_directory 不会误删用户配置（已在临时目录验证）
- [ ] remove_hooks 不会误删用户自定义 hooks（已在临时目录验证）

---

### Phase 2: 统一入口与 Makefile

---

**Task 3: 创建 `install/install.py` 统一安装器入口**

- **Description:** 使用 argparse 构建 CLI，编排 `lib.fs` 和 `lib.hooks` 完成 install/update/uninstall × global/local 全部 6 种组合。
- **Acceptance criteria:**
  - [ ] `python install/install.py install global` 将能力安装到 `~/.claude/`
  - [ ] `python install/install.py install local` 将能力安装到 `./.claude/`
  - [ ] `python install/install.py install local --target ~/projects/foo` 安装到指定目录
  - [ ] `python install/install.py update global` 增量同步 `~/.claude/`，hooks 去重 merge
  - [ ] `python install/install.py uninstall global` 清理 `~/.claude/` 下与 ys-powers 源目录同名的文件/目录，反注册 hooks，保留用户其他文件
  - [ ] `python install/install.py uninstall local` 清理 `./.claude/` 下与 ys-powers 源目录同名的文件/目录，反注册 hooks，保留用户其他文件
  - [ ] `--target` 仅在 `local` scope 下有效，global 时忽略或报错
  - [ ] `get_project_root()` 通过 `Path(__file__).resolve().parent.parent` 自定位源目录
  - [ ] 路径变量：`global` → `~/.claude` 绝对路径；`local` → `${CLAUDE_PROJECT_DIR}/.claude`
  - [ ] 退出码：0 = 全部成功；1 = 有失败（至少一个目录或 hooks 操作失败）
- **Verify:**
  - [ ] 运行 `python install/install.py install global`，检查 `~/.claude/` 下存在 skills/rules/commands/agents/hooks/references
  - [ ] 检查 `~/.claude/settings.json` 已注册 SessionStart hooks
  - [ ] 运行 `python install/install.py install local --target /tmp/test-project`，检查 `/tmp/test-project/.claude/` 结构正确
  - [ ] 运行 `python install/install.py uninstall global`，检查 `~/.claude/` 下与源目录同名的项目已删除，不在源目录中的用户文件保留，settings.json 中 hooks 已移除
- **Files likely touched:**
  - `install/install.py`
- **Estimated scope:** Medium
- **Dependencies:** Task 1, Task 2

---

**Task 4: 创建 `Makefile` 封装常用命令**

- **Description:** 提供 `make global-install`、`make local-install`、`make update-global`、`make uninstall-global` 等命令，支持 `project-dir` 参数。
- **Acceptance criteria:**
  - [ ] `Makefile` 位于项目根目录
  - [ ] `make global-install` → `python install/install.py install global`
  - [ ] `make local-install` → `python install/install.py install local`
  - [ ] `make local-install project-dir=~/foo` → `python install/install.py install local --target ~/foo`
  - [ ] `make update-global` / `make update-local` 正确映射
  - [ ] `make uninstall-global` / `make uninstall-local` 正确映射
  - [ ] `YS_POWERS_ROOT` 通过 `$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))` 自定位
  - [ ] 所有目标标记为 `.PHONY`
- **Verify:**
  - [ ] `make global-install` 成功执行且输出与直接运行 `install.py` 一致
  - [ ] `make local-install project-dir=/tmp/test-project` 成功安装到指定目录
  - [ ] `make uninstall-global` 成功清理全局安装
- **Files likely touched:**
  - `Makefile`
- **Estimated scope:** Small
- **Dependencies:** Task 3

---

### Checkpoint: After Phase 2

- [ ] `make global-install` 工作正常，`~/.claude/` 结构和 hooks 正确
- [ ] `make uninstall-global` 工作正常，清理彻底且不残留
- [ ] `--target` 参数支持跨项目安装

---

### Phase 3: 向后兼容

---

**Task 5: 改写 `local-install.py` 和 `global-install.py` 为 deprecated 薄包装**

- **Description:** 保留现有脚本文件，将其核心逻辑替换为调用 `lib/` 共享模块和 `install/install.py`，运行后打印 deprecation warning。
- **Acceptance criteria:**
  - [ ] `local-install.py` 行为与改写前完全一致（安装到 `./.claude/`、注册 `settings.local.json` hooks、清理 stale 文件）
  - [ ] `global-install.py` 行为与改写前完全一致（安装到 `~/.claude/`、打印 hooks TODO → 改为自动注入）
  - [ ] 两个脚本运行时首行打印 deprecation warning，提示用户使用新的 `make` 命令
  - [ ] deprecation warning 格式：`⚠ DEPRECATED: Use "make local-install" instead. This script will be removed in a future version.`
  - [ ] 两个脚本的退出码、错误输出、成功输出与改写前保持一致
- **Verify:**
  - [ ] 运行 `python install/local-install.py`，确认输出以 deprecation warning 开头，后续行为不变
  - [ ] 运行 `python install/global-install.py`，确认输出以 deprecation warning 开头，且 hooks 已自动注入（不再打印 TODO）
  - [ ] 对比改写前后的输出差异，确保除 deprecation warning 外无其他变化
- **Files likely touched:**
  - `install/local-install.py`
  - `install/global-install.py`
- **Estimated scope:** Small
- **Dependencies:** Task 1, Task 2, Task 3

---

### Checkpoint: After Phase 3

- [ ] 现有用户工作流不受影响（`local-install.py` 仍能正常运行）
- [ ] 用户能看到清晰的迁移提示（deprecation warning 指向 `make` 命令）

---

### Phase 4: 端到端验证

---

**Task 6: 端到端手动验证**

- **Description:** 执行完整的验证清单，覆盖 install/update/uninstall × global/local 全部场景。
- **Acceptance criteria:**
  - [ ] 验证 1：`make global-install` 后，`~/.claude/` 下存在全部 6 个目录，settings.json 已注册 hooks
  - [ ] 验证 2：`make local-install` 后，`./.claude/` 下存在全部 6 个目录，settings.local.json 已注册 hooks
  - [ ] 验证 3：`make local-install project-dir=/tmp/test-project` 后，指定目录安装正确
  - [ ] 验证 4：`make update-global` 后，增量同步不破坏用户已有配置（如在 `~/.claude/rules/` 下手动添加的文件保留）
  - [ ] 验证 5：`make uninstall-global` 后，`~/.claude/` 下仅与 ys-powers 源目录同名的项目被删除，用户自有项目（如 `skills/find-docs/`）保留，settings.json 中 hooks 已移除
  - [ ] 验证 6：`python install/local-install.py` 行为不变且打印 deprecation warning
  - [ ] 验证 7：`python install/global-install.py` 行为不变且打印 deprecation warning，hooks 自动注入
- **Verify:**
  - [ ] 逐项执行验证清单，全部通过
  - [ ] 检查 git diff，确认无意外修改（如不应修改 refer/、不应删除现有文档）
- **Files likely touched:** None（只读验证）
- **Estimated scope:** Small
- **Dependencies:** Task 3, Task 4, Task 5

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `uninstall_directory()` 误删用户自有文件 | Critical | 改为精确匹配删除：遍历源目录，仅删除目标中同名的项目；file 策略下额外清理 `renames.json` 旧名。绝不删除整个目标目录 |
| `lib/fs.py` 的路径遍历防护有漏洞 | High | 复用现有逻辑（已验证），增加临时目录单元测试 |
| `remove_hooks()` 误删用户自定义 hooks | High | 精确匹配 ys-powers 注入的 hooks（通过 JSON key 比较），不删除其他 hooks |
| `install.py` 的 `__file__` 自定位在某些运行方式下失效 | Medium | 增加守卫：`assert project_root / "skills" / "using-agent-skills" / "SKILL.md"` 存在 |
| Makefile 的 `YS_POWERS_ROOT` 在符号链接场景下解析错误 | Low | 使用 `realpath` 解析 Makefile 自身位置，而非依赖 `pwd` |
| 用户同时运行 global-install 和 local-install 导致 hooks 重复 | Low | inject_hooks 的去重逻辑同时适用于 global 和 local settings 文件 |

## Parallelization

可并行的任务：
- **Task 1（lib/fs.py）和 Task 2（lib/hooks.py）可并行开发**，两者无依赖关系
- Task 3 依赖 Task 1 + Task 2
- Task 4 依赖 Task 3
- Task 5 依赖 Task 1 + Task 2 + Task 3
- Task 6 依赖全部前置任务
