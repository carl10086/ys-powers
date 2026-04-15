---
name: teach-code
description: "带你由浅入深理解任意代码模块的源码。先宏观再细节，用伪代码和文字说明讲懂，不讲语法细节。"
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

```
讲解一个完整的意思 → 停下来 → 问一个问题 → 等待用户回应 → 再讲下一个
```

**NEVER:**
- 一次性讲完所有内容再问问题
- 连续输出超过一段内容不互动
- 讲完所有层（概览→概念→设计→细节）再问问题
- 问"你理解了吗"这种无效问题

---

## 讲解规则：从功能到实现

### 层级一：模块是做什么的

用一两句话讲清楚：
- 这个模块的**核心功能**是什么
- 它在系统中**扮演什么角色**

### 层级二：怎么组织的

讲清楚**设计思路**：
- 它由哪几个部分组成
- 这些部分之间**什么关系**
- 数据/控制**怎么流动**

### 层级三：具体怎么实现的

用**伪代码或文字描述**讲逻辑：
- 不需要逐行讲语法
- 用"先做什么，再做什么，最后做什么"的方式讲
- 关注**流程和逻辑**，不关注 TypeScript 语法细节

---


## 问什么问题

**好问题（引发思考）：**
- "为什么要这样设计？"
- "这样设计有什么缺点？"
- "有什么替代方案？"
- "如果不用这个设计，会怎样？"
- "这部分和刚才讲的那个有什么关系？"

**NEVER 问：**
- "你知道这个 TypeScript 语法是什么意思吗"（你又没看过代码）
- "你理解了吗"
- "记住了吗"

---

## 用户可以随时

- 追问任何细节
- 说"继续"进入下一段
- 要求深入某个点
- 跳过不关心的内容

---

## 总结

讲完后生成代码理解笔记，保存到 `docs/superpowers/specs/YYYY-MM-DD-<模块名>-read.md`
