---
name: create-guide
description: Use when the user asks to understand code, create a learning guide, write examples for understanding, or says a module feels like "someone else's code" they need to internalize. Also triggers when the user asks for usage examples, documentation for comprehension, or runnable tutorials for a codebase module.
---

# Create Guide

## Overview

为代码模块创建一组可运行的、带详细注释的示例文件 + README，帮助人类深入理解设计意图。输出放在 `examples/<module>-guide/` 或 `docs/guides/<module>/`，绝不混入生产代码。

## RED — 基线失败

没有本 skill 时，agent 在"帮助理解代码"场景下的典型错误：

| # | 错误行为 | Agent 的借口 |
|---|---------|-------------|
| 1 | 把 guide 写成生产代码的 docstring | "加 docstring 是标准文档方式" |
| 2 | 只展示公共 API | "用户不需要知道内部实现" / "封装就是要隐藏细节" |
| 3 | 用抽象示例（foo/bar） | "通用示例更复用" / "具体场景太局限" |
| 4 | 不可运行 | "用户自己会跑" / "Mock 数据是额外工作" |
| 5 | 英文注释 | "代码注释应该统一用英文" |
| 6 | 不写设计哲学 | "用户只想知道怎么用，不想知道为什么" |

## GREEN — 核心模式

```
examples/<module-name>-guide/
├── README.md               # 设计哲学 + 阅读顺序 + 维护规则
├── 01_<topic>.<ext>        # 核心类型 / 数据结构
├── 02_<topic>.<ext>        # 消息 / 接口
├── 03_<topic>.<ext>        # 调用方式
├── 04_<topic>.<ext>        # 流式 / 事件
└── ...                     # 完整生命周期（如 tool call、auth 适配）
```

**文件数量：** 5–8 个示例文件 + 1 个 README。每课一个概念，逐步依赖。

## 快速参考

| 任务 | 规则 |
|------|------|
| 位置 | `examples/` 或 `docs/guides/`，绝不放入 `src/` |
| 可运行 | 每个文件必须能用 mock 数据独立运行 |
| 注释 | 中文解释**设计意图**，不重复代码在做什么 |
| 内部细节 | 故意暴露私有函数（如 `_assemble_response`） |
| README | 必须包含：设计哲学、架构图、阅读顺序、运行方式、维护规则 |
| 示例 | 用具体场景（"天气查询"），不用抽象（foo/bar） |
| 语言 | 匹配模块语言，不限 Python |

## 实现步骤

### 文件头模板

```python
"""01 - 主题名称

本课介绍：
- 核心概念是什么？
- 为什么这样设计？（对比其他方案的 tradeoff）
- 与上一课的关系
"""
```

### 可运行骨架

每个文件必须包含执行骨架 + mock 数据：

```python
if __name__ == "__main__":
    # 用假数据演示 — 无需 API Key，无需网络
    demo_core_concept()
```

### 注释风格

**解释设计意图：**
```python
# 设计意图：提供工厂方法让构造更简洁，
# 避免写 ModelRequest(parts=(SystemPromptPart(...),)) 这种冗长形式
```

**不要复述代码：**
```python
# 不好的：创建一个 system request
```

### README 必须章节

1. **Design Philosophy** — 为什么这样设计？相比其他方案的 tradeoff？
2. **Architecture Diagram** — Mermaid 或 ASCII 图
3. **Reading Order Table** — 文件、主题、前置知识、核心收获
4. **Quick Index** — "我想理解 X → 读 Y"
5. **Run Instructions** — 如何运行每个示例
6. **Maintenance Rules** — 生产代码变化时何时更新本 guide

## REFACTOR — 借口表

| 借口 | 现实 |
|------|------|
| "加 docstring 是标准方式" | Guide 是学习材料，不是 API 文档。混进生产代码污染源码，也教不会设计意图。 |
| "用户不需要知道内部" | 理解 _为什么_ 需要看到 _怎么做_。私有函数暴露核心算法。 |
| "通用示例更复用" | 具体场景锚定抽象概念。"天气查询"比 `foo()` 教得更好。 |
| "用户自己会跑" | 跑不通 = 坏文档。Mock 数据花 2 分钟，省 20 分钟。 |
| "注释应该统一用英文" | 用户要的是理解。解释用用户语言，标识符保留英文。 |
| "用户只想知道怎么用" | 没有"为什么"，用户无法调试、扩展、适配。设计哲学是用好和吃透的分水岭。 |

## Red Flags — 停下检查

- "我就往源码里加点注释" → 单独建 guide 目录
- "这个模块太简单不需要 guide" → 再简单的模块也有 runnable 示例的价值
- "我用通用示例保持抽象" → 具体场景教得更好

