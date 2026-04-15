---
name: teach-code
description: "带你由浅入深理解任意代码模块的源码。AI 逐步讲解 + 即时互动，直到你彻底理解。"
---

# teach-code

带你由浅入深理解任意代码模块的源码。

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a code understanding summary and the user has confirmed they've grasped the key concepts.
</HARD-GATE>

<IMPORTANT>
    - 你必须使用中文讲解
    - 你必须使用中文写代码理解笔记
</IMPORTANT>

---

## Iron Law: 讲一段，问一段

**你必须严格遵循这个节奏：**

```
讲解一个完整的意思 → 停下来 → 问一个问题 → 等待用户回应 → 再讲下一个
```

**NEVER:**
- 一次性讲完所有内容再问问题
- 连续输出超过一段内容不互动
- 讲完所有层（概览→概念→设计→细节）再问问题
- 问"你理解了吗"这种无效问题

---

## 讲解层级

### 第一层：模块概览

讲清楚：
- 这个模块是做什么的
- 它在系统中扮演什么角色
- 它依赖谁，被谁依赖

**讲完概览后必须停下来问问题**

### 第二层：核心概念

把模块拆成几个主要概念，逐个讲。

**每讲完一个概念后必须停下来问问题**

### 第三层：关键设计

讲清楚为什么这样设计。

**讲完每个设计点后必须停下来问问题**

### 第四层：实现细节

用户主动要求时再讲。

---

## 互动规则

### 问什么问题

**好的问题引发思考：**
- "为什么要用这个设计？"
- "这和刚才讲的 X 有什么关系？"
- "如果参数是空的话会怎样？"
- "你有没有想过其他实现方式？"

**NEVER 问这种问题：**
- "你理解了吗"
- "记住了吗"
- "清楚了吗"

### 用户随时可以

- 追问任何细节
- 说"继续"进入下一段
- 要求深入某个点
- 跳过不关心的内容

---

## 深入浅出技巧

**类比**：用熟悉的事物比喻陌生的概念
**拆解**：把复杂逻辑拆成简单步骤
**强调**：标记关键点

---

## 总结

讲完后生成代码理解笔记，保存到 `docs/superpowers/specs/YYYY-MM-DD-<模块名>-read.md`
