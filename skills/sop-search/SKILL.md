---
name: searching-sops
description: Use when the user asks about past experiences, previous solutions, or historical decisions. Use when starting a task that may have been solved before. Use when the user mentions "before", "last time", "previously", or "how did we". Use when encountering auth, api, database, or domain-specific problems that may have historical SOP records.
---

# Searching SOPs

搜索 `sop/` 目录下的历史 SOP 文档并从中学习。

## 核心原则

**SOP 记录我们实际做了什么。** Skill 和 rule 告诉我们应该做什么。在解决新问题前，先检查是否解决过。

## 适用场景

- 用户问："之前我们是怎么处理 X 的？"
- 用户问："我们之前对 Y 的做法是什么？"
- 开始一个已有 SOP 记录的领域的任务（auth、api、database 等）
- 用户提到 "last time"、"before"、"previously"
- 存在多个可行方案，历史上下文有助于决策

## 不适用场景

- 用户询问通用最佳实践（使用 skill/rule 代替）
- 用户问 "how should I"（面向未来，不是历史）
- 项目中不存在 `sop/` 目录

## 搜索流程

**严格限定：只搜索 `sop/` 目录。不要搜索 skills/、commands/、docs/ 或其他目录。**

### 第一步：文件名搜索（最高优先级）

```bash
ls -lt sop/*<keyword>* 2>/dev/null
```

文件名匹配通常最相关。

### 第二步：内容搜索（补充）

```bash
rg -l -i <keyword> sop/ 2>/dev/null
```

内容搜索捕获关键词在正文中但不在文件名中的 SOP。

### 第三步：合并排序

1. 合并第一步和第二步的结果
2. 去重
3. 按修改时间排序（`ls -lt`）：**新文件优先**

### 第四步：读取学习

读取前 2-3 个最相关且最新的 SOP。提取：

- **背景**：什么场景触发了这个 SOP？
- **伪代码步骤**：解决方案的思路是什么？
- **关键决策**：为什么选择这个方案？

## 应用学到的知识

读取 SOP 后：

1. 向用户总结相关的历史经验
2. 将学到的教训应用到当前任务
3. 如果历史方案直接适用，明确说明
4. 如果历史方案已过时或部分相关，解释差异

## 常见错误

| 错误 | 修复 |
|------|------|
| 搜索 skills/ 或 commands/ 而非 sop/ | **严格限定 sop/**。其他目录包含通用指导，不是历史经验。 |
| 只检查文件名 | 始终同时做**文件名和内容**搜索 |
| 忽略文件时间 | 始终按 **mtime 排序** — 更新的 SOP 代表更近的经验 |
| 用户问历史时推荐 skill | 用户问 "what did we do" → 搜索 SOP。用户问 "what should I do" → 使用 skill/rule。 |
