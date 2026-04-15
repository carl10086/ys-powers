# teach-code 命令设计

## 背景

用户希望创建一个交互式代码理解命令，能够通过文档说明 + 交互式提问的方式，带你一步步理解任意代码模块的源码。命令取名 `teach-code`。

## 目标

- 用户随意指定文件/目录/模块作为起点
- AI 根据代码复杂度自动决定深入程度
- 通过独立的 `teach-code` skill 进行"由浅入深"的交互式问答引导
- 复杂场景支持可视化辅助（chrome-devtools MCP）
- 最终产出代码理解笔记

## 设计决策

### 核心结构

1. **`skills/teach-code/`** — 独立的 skill，基于 `skills/brainstorming/` 改造，专注于"由浅入深理解代码"流程
2. **`commands/teach-code.md`** — command 文件，指定 `requires: teach-code`

### skill 改造要点

brainstorming 的 CheckList（9步）改造为"代码理解"版本：

| 原 brainstorming 步骤 | 改造后步骤 |
|----------------------|------------|
| Explore project context | 读取并分析代码，生成整体概览 |
| Offer visual companion | 提供可视化辅助（可选） |
| Ask clarifying questions | 提出关键理解问题（一次一问） |
| ~~Propose 2-3 approaches~~ | **删除**（无方案选择环节） |
| ~~Present design~~ | **删除**（无设计方案产出） |
| ~~Write design doc~~ | **替换为** 生成代码理解笔记 |
| Spec self-review | 自我检查笔记完整性 |
| User reviews spec | 用户确认理解笔记 |
| ~~Transition to implementation~~ | **删除**（不需要 implementation plan） |

**最终产物**：代码理解笔记（而非设计文档）

### brainstorming skill 的角色

以 brainstorming 为框架，复用其：
- 交互式问答框架（一次一问，循序渐进）
- 用户意图澄清能力
- 文档产出流程

### 命令调用流程

```
用户输入：/teach-code <文件/目录/模块路径>

Step 1: 探索上下文
  → AI 读取指定路径代码，分析文件结构、核心模块、依赖关系
  → 生成整体概览（中文输出）

Step 2: 交互式问答引导
  → AI 根据代码复杂度提出关键问题
  → 一次一问，用户回答后逐步深入
  → 遇到复杂调用链或分支逻辑时提供可视化辅助
  → AI 自动决定深入程度

Step 3: 总结
  → 生成代码理解笔记
  → 保存到 docs/superpowers/specs/YYYY-MM-DD-<模块名>-read.md
```

### 文件结构

```
ys-powers/
├── skills/
│   └── teach-code/
│       ├── SKILL.md          # 改造后的 skill，复用 brainstorming 框架
│       └── (其他辅助文件，如 visual-companion.md 如有需要)
├── commands/
│   └── teach-code.md         # command 文件，requires: teach-code
└── docs/superpowers/specs/
    └── YYYY-MM-DD-teach-code-design.md  # 本设计文档
```

## 验证标准

- `skills/teach-code/SKILL.md` 存在，且 checklist 适配代码理解流程
- `commands/teach-code.md` 存在，frontmatter 指定 `requires: teach-code`
- 命令流程完整：探索上下文 → 交互式问答 → 总结产出笔记
