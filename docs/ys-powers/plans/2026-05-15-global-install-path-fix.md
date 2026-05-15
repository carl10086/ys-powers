# Plan: Global Install 路径兼容性修复

**基于 Spec**：`docs/ys-powers/specs/2026-05-15-global-install-path-fix-design.md`

---

## 依赖关系图

```
┌───────────────────────────────────────────────────────────┐
│  Task 1: Hooks 路径重构                           │
│  (基础设施——所有安装验证的基础)              │
└───────────────────────────────────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────────────────────────┐
│  Task 2: idea-refine 容器路径修复                │
│  Task 3: html-generator agent 解耦                │
│  (与 Task 1 无代码依赖，可并行)                │
└───────────────────────────────────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────────────────────────┐
│  Task 4: html-anything prompts 解析验证          │
│  (依赖 Task 3，需要 /html 命令可运行)            │
└───────────────────────────────────────────────────────────┘
```

**关键洞察**：Task 1 是基础设施，Task 2/3 是内容修复（互不依赖），Task 4 是验证任务（依赖 Task 3）。

---

## Checkpoint 1: Hooks 基础设施就绪

在 Task 1 完成后，确认安装系统可正确生成 settings.json。

---

## Task 1: Hooks 路径重构

**目标**：消除 `${CLAUDE_PLUGIN_ROOT}` 假插件变量，让 global install 后的 hooks 路径可移植。

**垂直切片**：`hooks.json` → `install/lib/hooks.py` → `~/.claude/settings.json`

### 1.1 重写 hooks/hooks.json

- 把 `${CLAUDE_PLUGIN_ROOT}` 改为区分场景的路径：
  - Global 场景：`bash $HOME/.claude/hooks/session-start.sh`
  - Local 场景：`bash ${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh`
- 问题：hooks.json 是单一文件，如何区分 global/local？
- 解决：保持两个独立配置文件（`hooks-global.json` 和 `hooks-local.json`），或在 `hooks.py` 中做简单字符串替换

**Acceptance**:
- `hooks.json` 中不再出现 `${CLAUDE_PLUGIN_ROOT}`
- 内容本身是“最终形态”，不依赖安装时替换

### 1.2 简化 install/lib/hooks.py

- 移除 `_load_hooks_config` 中的 `${CLAUDE_PLUGIN_ROOT}` → `path_var` 替换逻辑
- 改为：直接读取 `hooks.json`，不做任何内容替换
- 保留设置文件的合并/去重逻辑（这部分与路径无关）
- 删除 `resolve_hooks_path_variable` 函数或改为空实现（因为不再需要 path_var）

**Acceptance**:
- `hooks.py` 中不再有 `replace("${CLAUDE_PLUGIN_ROOT}", path_var)` 语句
- 安装脚本语法检查通过

### 1.3 更新 install.py 的调用点

- `do_install` 和 `do_uninstall` 不再需要 `path_var` 参数
- 或者保留空参数以维持接口兼容，但内部不使用

**Acceptance**:
- `install.py` 运行不报错

### 1.4 验证 Global Install 输出

```bash
cd ~/soft/projects/ys-powers
make global-install
cat ~/.claude/settings.json | grep "SessionStart" -A 5
```

**Verify**:
- 输出中含有 `bash $HOME/.claude/hooks/session-start.sh`
- 不含绝对用户名（如 `/Users/carlyu/...`）
- 不含 `${CLAUDE_PLUGIN_ROOT}`

### 1.5 验证 Local Install 输出

```bash
make local-install project-dir=/tmp/test-project
cat /tmp/test-project/.claude/settings.local.json | grep "SessionStart" -A 5
```

**Verify**:
- 输出中含有 `bash ${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh`
- 不含绝对路径

### 1.6 验证卸载/重装

```bash
make uninstall-global
make global-install
# 确认 settings.json 中没有重复 hooks
```

**Files touched**:
- `hooks/hooks.json`
- `install/lib/hooks.py`
- `install/install.py` (可能的调用点修改)

---

## Checkpoint 2: Skills 和 Agents 路径修复完成

在 Task 2 和 Task 3 完成后，确认所有 skill/agent 不再引用硬编码或错误的容器路径。

---

## Task 2: idea-refine 容器路径修复

**目标**：移除硬编码的容器路径 `/mnt/skills/user/...`。

**垂直切片**：`SKILL.md` → ideate 命令 → 脚本执行

### 2.1 修改 skills/idea-refine/SKILL.md

第 22 行：
```markdown
# 当前
bash /mnt/skills/user/idea-refine/scripts/idea-refine.sh

# 改为
bash ./scripts/idea-refine.sh
```

**理由**：与 html-anything 保持一致，信任 Claude Code 从 skill 目录解析相对路径。

**Acceptance**:
- `SKILL.md` 中不再出现 `/mnt/skills/user/`
- `./scripts/idea-refine.sh` 位于 skill 目录下的正确位置

### 2.2 验证

```bash
# 确认脚本存在
ls ~/.claude/skills/idea-refine/scripts/idea-refine.sh

# 在非 ys-powers 项目启动 Claude Code，运行 /ideate
```

**Verify**:
- 不报错 "file not found"
- 能正常触发 idea-refine skill

**Files touched**:
- `skills/idea-refine/SKILL.md`

---

## Task 3: html-generator agent 解耦

**目标**：让 agent 不直接引用 skill 文件路径，通过 `skill` 工具调用。

**垂直切片**：`html-generator.md` → skill 调用 → html-anything 工作流

### 3.1 修改 agents/html-generator.md

```markdown
# 当前 Workflow 第 1 步
1. **Read the skill guide.** Load `skills/html-anything/SKILL.md` and follow its Standard Workflow.
2. **Load style guidance.** Read `prompts/styles/_design.md`, `prompts/styles/catalog.json`, and the matching source/style prompts.

# 改为
1. **Load the skill.** Invoke `skill: html-anything` to load the full workflow guide and style system.
2. **Confirm style scope.** The skill will handle style guidance and prompt loading internally.
```

**说明**：`skill: html-anything` 加载后，skill 的 instructions 会指导 Claude Code 读取 `./prompts/...`，无需 agent 自己处理。

**Acceptance**:
- `html-generator.md` 中不再出现 `skills/html-anything/SKILL.md` 文件路径
- 使用 `skill: html-anything` 语法

### 3.2 验证

```bash
# 在非 ys-powers 项目运行 /html test
```

**Verify**:
- Agent 能正确触发 html-anything skill
- 不报错 "skills/html-anything/SKILL.md not found"

**Files touched**:
- `agents/html-generator.md`

---

## Checkpoint 3: Prompts 解析行为确认

在 Task 4 完成后，确认 Claude Code 能正确加载 skill 内部的 prompts。

---

## Task 4: html-anything prompts 解析验证

**目标**：验证 Claude Code 是否从 skill 文件所在目录解析 `./prompts/...` 相对路径。

**垂直切片**：`html-anything/SKILL.md` → `./prompts/...` → 页面生成

### 4.1 检查当前状态

当前 `skills/html-anything/SKILL.md` 已使用 `./prompts/...` 相对路径，与 html-anything 原项目一致。无需代码修改，只需验证。

### 4.2 验证步骤

```bash
# 1. 确认 prompts 目录已复制到 global install
ls ~/.claude/skills/html-anything/prompts/styles/_design.md

# 2. 在非 ys-powers 项目运行 /html test
# 3. 观察 Claude Code 是否能读取 _design.md 和 catalog.json
```

### 4.3 分支逻辑

**如果验证通过**（Claude Code 从 skill 目录解析）：
- 保持现状，无需修改
- 在 audit 文档中记录验证结果

**如果验证失败**（Claude Code 从 CWD 解析）：
- 执行后备方案：将关键 prompts 内容内联到 SKILL.md
- 或者在 skill 启动时先执行脚本确定 prompts 绝对路径（复杂度更高，不推荐）

**Acceptance**:
- `/html` 命令能正确读取 prompts 并生成符合风格的 HTML

**Files touched**:
- 可能无（如验证通过）
- 或 `skills/html-anything/SKILL.md`（如需内联 prompts）

---

## 风险与应对

| 风险 | 可能性 | 影响 | 应对策略 |
|------|--------|------|----------|
| Claude Code 不支持 `skill: html-anything` 语法 | 中 | 高 | 回退到 `Read ~/.claude/skills/html-anything/SKILL.md` 绝对路径 |
| 验证发现 prompts 路径解析失败 | 中 | 中 | 内聑 prompts 内容到 SKILL.md |
| 安装脚本合并逻辑回退（旧 hooks 未清除） | 低 | 中 | 手动检查 settings.json，确认无重复 |
| 用户 settings.json 已有自定义 SessionStart hooks | 低 | 低 | 合并逻辑应正确处理，不覆盖用户配置 |

---

## 总体时间估算

| Task | 预估时间 | 说明 |
|------|---------|------|
| Task 1: Hooks 路径重构 | 30 min | 涉及文件修改 + 多次验证安装/卸载 |
| Task 2: idea-refine 修复 | 10 min | 单行替换 |
| Task 3: html-generator 解耦 | 15 min | 文案调整 |
| Task 4: prompts 验证 | 20 min | 需要在 Claude Code 中测试 |
| 总计 | ~75 min | 含验证时间 |

---

## 执行顺序

```
┌───────────────────────────────────────┐
│  Task 1: Hooks 路径重构                           │
│  → 修改 hooks.json + hooks.py                      │
│  → 验证 global install / local install              │
├────────────────────────────────────────┤
│  Checkpoint 1: Hooks 基础设施就绪               │
└────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  Task 2: idea-refine 修复  (可与 Task 3 并行)    │
│  Task 3: html-generator 解耦 (可与 Task 2 并行)    │
├────────────────────────────────────────┤
│  Checkpoint 2: Skills/Agents 路径修复完成           │
└────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  Task 4: html-anything prompts 验证                 │
│  → 在 Claude Code 中测试 /html                   │
├────────────────────────────────────────┤
│  Checkpoint 3: 全部验证通过，任务完成              │
└────────────────────────────────────────┘
```

**Files touched summary**:
- `hooks/hooks.json`
- `install/lib/hooks.py`
- `install/install.py`
- `skills/idea-refine/SKILL.md`
- `agents/html-generator.md`
- 可能: `skills/html-anything/SKILL.md` (仅当 prompts 验证失败时)
