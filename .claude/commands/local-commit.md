---
name: local-commit
description: 本地项目极简提交：暂存、生成 message、确认、一步完成
---

## 安全红线

- 不 force push
- 不提交密钥/token/credentials
- 不跳过用户确认直接提交
- 不自动包含 `.claude/`、`.env`、日志文件

## Commit 格式

```
type(scope): 简短描述（≤50字）

- 变更点 1
- 变更点 2
```

**type 选项：** feat | update | fix | refactor | chore

## Workflow

复制此清单并逐项勾选：

```
- [ ] 1. 预检工作区 → verify: git status 有变更
- [ ] 2. 展示变更摘要并确认范围 → verify: 用户选择全部/部分/取消
- [ ] 3. 生成 commit message → verify: message 准确反映变更
- [ ] 4. 用户确认 message → verify: Y/n/e
- [ ] 5. 执行提交 → verify: commit 成功
```

### 1. 预检工作区

```bash
git status --short
```

**输出为空？** → 工作区干净，终止流程：
> 工作区干净，无变更可提交。

**输出非空？** → 继续 Step 2。

### 2. 展示变更并确认范围

展示 `git status --short` 结果：

```
检测到以下变更：
 M resume/resume.md
 M review/kafka.md

处理方式：
1. 全部提交（默认）
2. 部分提交，让我选择文件
3. 取消提交
```

**检测到不应提交的文件时主动提示：**
- `.claude/`、`.env`、日志文件、临时文件
- 询问："检测到 X 文件，是否纳入本次提交？"

### 3. 生成 Commit Message

执行 `git diff --cached`，基于 diff 总结主题：

1. **判断 type**：看主要变更性质（新增/修改/删除/重构）
2. **确定 scope**：看涉及哪个目录或文件类型
3. **提炼主题**：用 5-10 字概括核心变更
4. **列出变更点**：逐条列出具体修改

生成 message：

```
type(scope): 简短描述（≤50字）

- 变更点 1
- 变更点 2
```

### 4. 用户确认 Message

展示建议的 message：

```
建议的 commit message：

update(resume): 补充工作经历，修复格式问题

- 新增与爱为舞经历
- 删除电商项目描述
- 统一标点符号

确认提交？ [Y/n/e(dit)]
```

- **Y**（默认）→ 继续 Step 5
- **n** → 终止流程
- **e** → 用户输入自定义 message，验证非空后提交

### 5. 执行提交

```bash
git add .
git commit -m "message"
```

成功后展示结果：
```
[main a1b2c3d] update(resume): 补充工作经历，修复格式问题
 2 files changed, 15 insertions(+), 8 deletions(-)
```

## 异常情况处理

| 情况 | 处理 |
|------|------|
| 工作区干净 | 提示"无变更可提交"，终止 |
| 非 Git 仓库 | 提示"当前目录不是 Git 仓库"，终止 |
| 用户取消 | 终止，不执行任何操作 |
| 自定义 message 为空 | 提示"message 不能为空"，重新输入 |
| 不应提交的文件在列表中 | 主动询问是否纳入 |

## 执行后自检

- [ ] 工作区已预检，不是干净状态
- [ ] 用户已确认提交范围
- [ ] commit message 准确反映变更内容
- [ ] 用户已确认 message（Y 或自定义）
- [ ] 没有 `.claude/`、`.env`、密钥文件被误提交
