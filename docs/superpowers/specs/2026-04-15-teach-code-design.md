# teach-code 命令设计

## 背景

用户希望创建一个交互式代码理解命令，能够通过文档说明 + 交互式提问的方式，带你一步步理解任意代码模块的源码。命令最终取名 `teach-code`。

## 目标

- 用户随意指定文件/目录/模块作为起点
- AI 根据代码复杂度自动决定深入程度
- 通过 brainstorming skill 的交互式问答框架引导理解
- 复杂场景支持可视化辅助（chrome-devtools MCP）
- 最终产出代码理解笔记

## 设计决策

### 命令名称

`teach-code`：语义清晰，表明"教我理解这段代码"

### 核心流程

```
用户输入：/teach-code <文件/目录/模块路径>

Step 1: 探索上下文
  → AI 读取指定路径的代码，分析文件结构、核心模块、依赖关系
  → 生成整体概览（用中文输出）

Step 2: 交互式问答引导
  → AI 根据代码复杂度提出关键问题
  → 一次一问，用户回答后逐步深入
  → 复杂调用链/分支逻辑提供可视化辅助（chrome-devtools）

Step 3: 总结
  → 生成简短代码理解笔记
  → 保存到 docs/superpowers/specs/YYYY-MM-DD-<模块名>-read.md
```

### brainstorming skill 的角色

command 中指定使用 brainstorming skill，借助它的：
- 交互式问答框架（一次一问，循序渐进）
- 用户意图澄清能力
- 设计文档产出流程（用于生成理解笔记）

brainstorming skill 的 CheckList 在此场景下适配为：
1. 探索项目上下文 → 读取并分析代码
2. 提问 → 交互式问答引导
3. 方案建议 → 可视化辅助（如需要）
4. 设计文档 → 代码理解笔记

### brainstorming skill 调用方式

command 文件开头 frontmatter 指定：
```yaml
---
description: 使用 brainstorming skill 进行交互式代码理解
requires: brainstorming
---
```

## 命令文件结构

`commands/teach-code.md`

```yaml
---
description: 使用 brainstorming skill 进行交互式代码理解，带你一步步理解任意代码模块的源码
requires: brainstorming
---

# teach-code

## 使用方式

/teach-code <文件/目录/模块路径>

## 流程

### Step 1: 探索上下文
读取指定路径代码，分析文件结构、核心模块、依赖关系，生成整体概览。

### Step 2: 交互式问答引导
根据代码复杂度，AI 提出关键问题引导深入理解。规则：
- 一次一问，循序渐进
- 复杂调用链/分支逻辑提供可视化辅助

### Step 3: 总结
生成代码理解笔记，保存到 docs/superpowers/specs/YYYY-MM-DD-<模块名>-read.md
```

## 验证标准

- `commands/teach-code.md` 文件存在
- frontmatter 中指定 `requires: brainstorming`
- 命令流程清晰，可直接使用
