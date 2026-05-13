# Implementation Plan: 全局安装与本地卸载

## Overview

基于 spec `docs/ys-powers/specs/2026-05-13-global-install-design.md`，新增两个独立脚本：
- `install/global-install.py`：将 ys-powers 安装到 `~/.claude/`
- `install/remove-local`：清理当前项目 `./.claude/` 下的 ys-powers 文件

`local-install.py` 保持不变。

## Architecture Decisions

- **完全独立脚本（方案 A）**：`global-install.py` 和 `remove-local` 各自维护完整的逻辑，不提取共享模块。牺牲一点维护性，换取最简单的运行时依赖关系。
- **hooks 暂手动处理**：全局 `settings.json` 的 hooks merge 过于复杂，当前版本仅打印转换后的 JSON 片段供用户手动复制。
- **remove-local  hooks 降级为提示**：与 global-install 保持一致，仅打印待清理的 hooks 清单，不自动修改 `settings.local.json`。

## Task List

### Phase 1: global-install.py

- [ ] **Task 1: 创建 `install/global-install.py`**
  - **Description:** 复制 `local-install.py` 的核心逻辑，修改目标目录为 `~/.claude/`，实现目录安装 + stale 清理 + hooks 打印提示。
  - **Acceptance criteria:**
    - [ ] 脚本能正确识别项目根目录（通过脚本位置）
    - [ ] `skills/`、`agents/` 使用 folder 策略安装到 `~/.claude/`
    - [ ] `rules/`、`commands/`、`hooks/`、`references/` 使用 file 策略安装到 `~/.claude/`
    - [ ] file 策略目录执行 `cleanup_stale_files()`，根据 `renames.json` 清理旧名文件
    - [ ] 读取 `hooks/hooks.json`，将 `${CLAUDE_PLUGIN_ROOT}` 替换为 `~/.claude` 绝对路径，打印转换后的 JSON 片段
    - [ ] 脚本末尾打印 `[TODO] hooks 全局自动注册待实现`
  - **Verification:**
    - [ ] 运行 `python install/global-install.py`，观察输出无报错
    - [ ] 检查 `~/.claude/` 下存在 `skills/`、`commands/`、`agents/`、`rules/`、`hooks/`、`references/`
    - [ ] 检查 `~/.claude/skills/` 内容完整（与源目录一致）
  - **Dependencies:** None
  - **Files likely touched:**
    - `install/global-install.py`
  - **Estimated scope:** Medium

### Checkpoint: After Task 1
- [ ] `global-install.py` 运行成功，`~/.claude/` 目录结构正确
- [ ] hooks 提示内容可手动复制
- [ ] 无权限错误或其他异常

### Phase 2: remove-local

- [ ] **Task 2: 创建 `install/remove-local`**
  - **Description:** 实现本地卸载脚本，删除 `./.claude/` 下 ys-powers 安装的目录，清理 stale 文件，打印 hooks 清理提示。
  - **Acceptance criteria:**
    - [ ] 删除 `./.claude/` 下的 `skills/`、`commands/`、`agents/`、`rules/`、`hooks/`、`references/`
    - [ ] 对 file 策略目录，读取 `renames.json` 清理旧名文件
    - [ ] 读取 `hooks/hooks.json`，打印需要手动从 `settings.local.json` 中移除的 hooks 清单
    - [ ] 不删除 `./.claude/` 下用户自己的配置（如 `settings.json`、`memory/` 等）
    - [ ] 如果 `./.claude/` 不存在或部分目录不存在，优雅处理（打印提示，不报错）
  - **Verification:**
    - [ ] 先运行 `local-install.py`，确认 `./.claude/` 安装成功
    - [ ] 再运行 `remove-local`，确认上述目录已删除
    - [ ] 确认 `./.claude/` 中用户自定义文件（如手动创建的 `settings.json`）保留
  - **Dependencies:** None（可与 Task 1 并行，但建议顺序执行以便测试）
  - **Files likely touched:**
    - `install/remove-local`
  - **Estimated scope:** Medium

### Checkpoint: After Task 2
- [ ] `remove-local` 运行成功，本地 ys-powers 文件已清理
- [ ] 用户自定义配置未受影响
- [ ] stale 文件和 hooks 提示正确输出

### Phase 3: 兼容性验证

- [ ] **Task 3: 验证 `local-install.py` 行为不变**
  - **Description:** 确保现有本地安装脚本未受新文件影响，仍能正常工作。
  - **Acceptance criteria:**
    - [ ] `local-install.py` 安装到 `./.claude/` 成功
    - [ ] 安装策略（folder/file）与修改前一致
    - [ ] `renames.json` 的 stale 清理正常工作
    - [ ] hooks 注册到 `settings.local.json` 正常工作
  - **Verification:**
    - [ ] 运行 `local-install.py`，检查 `./.claude/` 目录结构
    - [ ] 检查 `./.claude/settings.local.json` 中 hooks 已注册
  - **Dependencies:** Task 1, Task 2（需要确认新脚本不影响旧脚本）
  - **Files likely touched:** None（只读验证）
  - **Estimated scope:** Small

### Checkpoint: Complete
- [ ] 三个脚本各自独立运行，无冲突
- [ ] 全局安装和本地安装可共存（Claude Code 优先级机制下本地覆盖全局）
- [ ] 准备提交

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `global-install.py` 误删 `~/.claude/` 中用户已有配置 | High | 严格复用 local-install 的 folder/file 策略，只覆盖同名项，保留独有文件 |
| `remove-local` 误删用户自定义文件 | High | 只遍历 DIRECTORIES 中定义的目录名，不扫描整个 `.claude/` |
| hooks 提示内容格式错误，用户无法直接复制 | Low | 使用 `json.dumps(..., indent=2)` 输出标准 JSON 格式 |
| `Path.home()` 在某些环境下返回错误值 | Low | 使用标准库 `pathlib.Path.home()`，覆盖主流平台 |

## Open Questions

- 无（spec 中的 open questions 已解决）
