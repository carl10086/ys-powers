---
title: "SOP: 重构 sop-add 命令设计"
created: 2026-04-19
tags: [refactor, 2026-04-19-18, brainstorm, design]
project: ys-powers
---

## 背景

在 ys-powers 项目中，需要重构 sop-add 命令设计，改进标签生成逻辑，添加伪代码步骤描述，完善关键信息结构。

## 解决方案

### 伪代码步骤

1. 分析当前 sop-add 命令的问题：标签定义不合理、文档结构混乱
2. 参考 brainstorming skill 的设计风格，确立新的设计原则
3. 逐个与用户确认各 section 的生成规则：背景、解决方案、关键信息
4. 确定解决方案使用算法描述型伪代码
5. 确定关键信息按文件组织：文件 > 类 > 函数
6. 确定标签必选日期标签（精确到小时）
7. 确定文件命名格式：sop-YYYYMMDD-NNN-{keyword}.md
8. 更新 sop-add.md 命令文件

### 关键信息

- commands/sop-add.md
  - 更新标签规则
  - 更新 SOP 格式模板
  - 更新文件命名规则

### 关键命令

```bash
git add . && git commit -m "docs: add sop-add command design spec"
```

### 关键决策

- 标签由 LLM 自由提取 + 预定义分类 + 必选日期标签
- 解决方案用算法描述型伪代码，不用代码片段型
- 关键信息按文件组织：file > class > function
- 文件名加标题关键词：sop-YYYYMMDD-NNN-{keyword}.md
