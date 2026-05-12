# Spec: Stale File Cleanup on Install

## Objective

解决 `local-install.py` 安装时因 commands/skills/hooks 目录文件重命名导致的 stale 文件残留问题。

## 背景

当前 `local-install.py` 对 commands/rules/hooks/references 目录使用「文件级同名覆盖」策略（file strategy）：
- 同名文件 → 覆盖
- 目标独有的文件 → 保留

**问题**：当源侧文件重命名（如 `review.md` → `ys-review.md`）时，源侧旧名被删除，但目标侧的旧名文件不会自动消失，导致新旧两个文件共存。

## Tech Stack

- Python 3.9+
- 标准库：`json`, `pathlib`, `shutil`
- 无新增第三方依赖

## Commands

```bash
# 本地安装
python install/local-install.py

# 验证安装后无 stale 文件
ls .claude/commands/ | sort
```

## Project Structure

```
install/
  local-install.py      # 修改：安装前读取 renames.json 并清理
  renames.json          # 新增：重命名映射文件
  __pycache__/

CLAUDE.md               # 修改：新增 STALE-FILE-CLEANUP 章节
```

## Code Style

- Python: 遵循项目现有风格（无 formatter 约束，保持与 `local-install.py` 当前风格一致）
- JSON: 2 空格缩进，UTF-8 编码
- Markdown: 中文为主，技术术语/文件路径/命令名保留英文

## Testing Strategy

- **手动验证**：运行 `local-install.py` 后，检查 `.claude/commands/` 目录，确认旧名文件已删除
- **回归测试**：确认正常安装流程不受影响（同名文件仍被覆盖，新增文件仍被复制）

## Boundaries

- **Always**: 每次 rename 操作后更新 `renames.json`；安装前总是读取 renames.json 并清理
- **Ask first**: 删除目标侧文件前是否需要确认（当前设计：直接删除，因为重命名是明确的意图）
- **Never**: 不处理 skills/agents 目录（folder 策略整体覆盖，不需要此机制）；不处理跨目录移动

## Success Criteria

- [ ] `install/renames.json` 存在且包含至少一条映射（review.md → ys-review.md）
- [ ] `local-install.py` 安装前读取 renames.json，删除目标侧旧名文件
- [ ] `CLAUDE.md` 包含 STALE-FILE-CLEANUP 章节，记录 rename 映射维护规则
- [ ] 运行 `local-install.py` 后，`.claude/commands/` 下不再同时存在 `review.md` 和 `ys-review.md`

## Open Questions

- [ ] renames.json 的 key 格式：用旧文件名（如 `review.md`）还是旧路径（如 `commands/review.md`）？
  - **决策**：旧文件名，因为按目录分组（顶层 key 是目录名）
- [ ] 是否需要在安装脚本输出中打印被清理的文件列表？
  - **决策**：是，便于排查
