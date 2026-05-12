# Plan: Stale File Cleanup on Install

## 依赖图

```
renames.json (任务1)
    ↓
local-install.py 修改 (任务2)
    ↓
CLAUDE.md 更新 (任务3)
    ↓
验证安装 (任务4)
```

## 任务清单

### 任务 1：创建 renames.json 并补录已有重命名

**目标**：创建重命名映射文件，包含已发生的 rename。

**改动**：
- 新建 `install/renames.json`

**验收标准**：
- [ ] 文件位于 `install/renames.json`
- [ ] 包含 `commands/review.md → ys-review.md` 的映射
- [ ] JSON 格式正确，2 空格缩进

**验证步骤**：
```bash
python -m json.tool install/renames.json > /dev/null && echo "JSON valid"
```

---

### 任务 2：修改 local-install.py，安装前清理 stale 文件

**目标**：安装 file 策略目录前，读取 renames.json 并删除目标侧的旧名文件。

**改动**：
- 在 `install/local-install.py` 中新增 `cleanup_stale_files()` 函数
- 在 `install_directory()` 中、执行复制**之前**调用清理函数（仅对 file 策略）

**关键逻辑**：
1. 读取 `install/renames.json`（如果存在）
2. 根据当前 source_name 取对应的重命名映射
3. 遍历映射：若 `target_dir / old_name` 存在，则删除并打印日志

**验收标准**：
- [ ] 新增函数 `cleanup_stale_files(source_name, target_dir)`
- [ ] 仅在 file 策略下触发清理
- [ ] 清理在复制之前执行
- [ ] 打印被删除的文件名（便于排查）
- [ ] renames.json 不存在时跳过清理（不报错）

**验证步骤**：
```bash
# 1. 语法检查
python -m py_compile install/local-install.py

# 2. 运行安装
python install/local-install.py
# 预期输出包含："清理 stale 文件: review.md"
```

---

### 任务 3：更新 CLAUDE.md，添加 STALE-FILE-CLEANUP 章节

**目标**：记录 renames.json 的维护规则，确保后续 rename 操作不会遗忘更新映射。

**改动**：
- 在 `CLAUDE.md` 末尾或合适位置新增 `## STALE-FILE-CLEANUP` 章节

**内容要点**：
- 说明 renames.json 的作用
- AI 维护规则：每次 rename 后必须更新
- 格式示例
- 人类 review 确认流程

**验收标准**：
- [ ] CLAUDE.md 包含 STALE-FILE-CLEANUP 章节
- [ ] 章节说明 renames.json 的位置和格式
- [ ] 明确 AI 在 rename 后的维护义务
- [ ] 包含 review.md → ys-review.md 的示例

**验证步骤**：
```bash
grep -A 20 "STALE-FILE-CLEANUP" CLAUDE.md
```

---

### 任务 4：端到端验证

**目标**：确认安装后不再同时存在新旧两个文件。

**验证步骤**：
1. 确保目标项目的 `.claude/commands/` 下同时有 `review.md` 和 `ys-review.md`（模拟 stale 状态）
2. 运行 `python install/local-install.py`
3. 检查 `.claude/commands/`：
   - [ ] `ys-review.md` 存在（新文件被复制）
   - [ ] `review.md` 不存在（旧文件被清理）

**回归测试**：
- [ ] 正常安装流程不受影响（同名文件仍被覆盖）
- [ ] folder 策略目录不受此逻辑影响（skills/agents 仍走全量覆盖）

---

## 检查点

- **检查点 1**（任务 1 完成后）：renames.json 格式正确，包含 review.md 映射
- **检查点 2**（任务 2 完成后）：local-install.py 能正确读取 renames.json 并打印清理日志
- **检查点 3**（任务 3 完成后）：CLAUDE.md 记录完整，人可读可理解
- **检查点 4**（任务 4 完成后）：端到端验证通过，无 stale 文件残留

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| renames.json 被误删或格式错误 | 清理逻辑在文件不存在时静默跳过，不阻塞安装 |
| 清理误删非 stale 文件 | 只删除 renames.json 中显式列出的旧名，不扫描 |
| 后续 rename 遗忘更新映射 | CLAUDE.md 明确记录 AI 维护义务 + 人 review 确认 |
