---
name: SOP-ADD
description: Extracts key information from current session history and generates structured SOP files. Use when a task is completed and the user wants to capture the experience for future reference, or when the user explicitly asks to "document this" or "save as SOP".
---

# SOP-ADD

将已完成的 session 经验自动沉淀为可检索的结构化文档。

## 与 skills/rules 的边界

| 内容 | 归属 | 示例 |
|------|------|------|
| 具体案例的解决过程 | **SOP** | "本次 JWT 过期 bug 的修复步骤" |
| 可复用的 Claude 指令 | **Skill** | "处理 JWT 过期的通用模式" |
| 强制性项目规范 | **Rule** | "所有 token 必须用 httpOnly cookie" |

**原则**：SOP 记录"这次实际做了什么"，Skill 指导"下次应该怎么做"。

## 触发时机

1. **自动提示**：任务完成后询问用户"是否生成 SOP 沉淀这次经验？"
2. **手动调用**：用户说"生成 SOP"、"记录下来"、"文档化这次经验"

## 自动提取规则

Claude 自动从 session 历史提取，用户仅需审阅确认。

### 1. 基础信息（自动推断）

| 字段 | 提取规则 |
|------|----------|
| title | 从用户最初的问题描述提取，格式：`SOP: {问题/需求}` |
| created | 当前日期 `YYYY-MM-DD` |
| project | 当前工作目录的 git 仓库名 |
| type | 从问题描述推断：`bug-fix` \| `feature` \| `refactor` \| `config` \| `deploy` \| `testing` |
| domain | 从涉及文件路径推断：`auth` \| `api` \| `database` \| `frontend` \| `ci-cd` \| `other` |
| date | `YYYY-MM-DD`（天级，非小时级） |

### 2. 背景（自动提取）

- 提取来源：session 前 3 轮对话 + 用户的初始问题描述
- 格式：`在 [场景] 中，[遇到的问题/需求]`

### 3. 伪代码步骤（核心）

**定义**：从具体实现中抽象出的算法描述型步骤。不是操作手册，而是逻辑意图的提炼。

**提取来源**：
1. 用户原始需求 → 初始目标
2. Claude 的 plan → 关键阶段
3. 实际执行中的关键转折点 → 决策节点

**抽象规则**：

| 级别 | 做法 | 示例 |
|------|------|------|
| 保留 | 逻辑意图、算法结构、关键判断 | "检查 token 是否过期" |
| 去除 | 具体命令、临时路径、试错过程 | "运行 `cat package.json`"、"先改了 A 又改回 B" |

**质量标准**：
- 每一步应能对应到代码中的核心逻辑片段
- 步骤之间应有清晰的因果/顺序关系
- 应包含关键判断（if/else）和循环（while/for）结构

### 4. 关键信息（自动提取）

- 提取来源：session 中编辑/涉及的所有文件
- 组织方式：按文件组织，层级为 `file > class > function`
- 规则：只列出与解决方案直接相关的符号，未涉及类/函数可省略层级

### 5. 关键命令（自动提取）

- 提取来源：session 中实际运行的 bash 命令
- 处理：去重，保留可复用的命令（去除临时路径、敏感参数）

### 6. 关键决策（自动提取）

- 提取来源：session 中 Claude 提出的"建议"、"权衡"、"我们选择"等语句
- 标准：必须回答"为什么这么做"

## 标签体系

```yaml
tags:
  - <type>        # bug-fix | feature | refactor | config | deploy | testing
  - <domain>      # auth | api | database | frontend | ci-cd | other
  - <date>        # YYYY-MM-DD
  - <custom>      # 可选，如"双token"、"性能优化"等关键词
```

## SOP 输出格式

```yaml
---
title: "SOP: {自动提取的问题描述}"
created: YYYY-MM-DD
tags: [<type>, <domain>, <date>, <optional-custom>]
project: <repo-name>
---

## 背景

在 [场景] 中，[遇到的问题/需求]。

## 解决方案

### 伪代码步骤

1. [步骤1]
2. [步骤2]
3. [步骤3]

### 关键信息

- path/to/file.ts
  - class ClassName
    - methodName()
  - functionName()

### 关键命令

```bash
npm test auth/session
```

### 关键决策

- [决策点及原因]
```

## 文件命名

```
sop/sop-{日期}-{序号}-{关键词}.md

# 示例
sop/sop-20260428-001-auth-fix.md
sop/sop-20260428-002-api-refactor.md
```

- 关键词从 title 自动提取，kebab-case
- 序号按当日已有文件数量自动递增

## 相似性检查

生成前执行：

```bash
grep -r "<domain>\|<关键词>" sop/ --include="*.md" -l
```

若找到相似 SOP，提示用户：
> 发现相似文档：`sop-20260420-001-auth-fix.md`。是否合并更新，还是创建新文档？

## 验证步骤

生成后、保存前逐项检查：

- [ ] title 是否准确概括问题？
- [ ] 伪代码步骤是否抽象到逻辑意图层面（而非具体操作）？
- [ ] 伪代码步骤是否包含关键判断和循环结构？
- [ ] key commands 是否可复制粘贴直接运行？
- [ ] key decisions 是否回答了"为什么这么做"？
- [ ] 是否包含敏感信息（API key、密码、内部路径）？
- [ ] 用户确认后再保存
