# skill-creator

## 定位

指导开发者创建高质量的 Claude Skill，涵盖 Skill 的结构设计、渐进式加载原则、元数据编写和打包分发。

## 触发时机

- 需要为特定工作流或领域创建自定义 Claude Skill 时
- 评估或改进现有 Skill 的质量时
- 理解 Claude Skill 的架构和最佳实践时
- **不适用**：仅需一次性提示词（prompt）而无需复用结构的场景

## 核心能力

1. **Skill 架构指导**：解释 Skill 的组成（SKILL.md + scripts/ + references/ + assets/）
2. **元数据优化**：指导如何编写高质量的 `name` 和 `description`，确保 Claude 在正确时机触发 Skill
3. **渐进式加载设计**：利用三级加载系统管理上下文效率：
   - **Level 1: 元数据**（~100 词）— 始终在上下文中
   - **Level 2: SKILL.md 正文**（< 5000 词）— Skill 触发时加载
   - **Level 3: Bundle 资源** — 按需加载，无上限
4. **资源组织**：区分 scripts/（可执行代码）、references/（参考文档）、assets/（输出资源）
5. **验证与迭代**：通过具体用例验证 Skill 设计，基于反馈迭代

## Skill 解剖结构

```
skill-name/
├── SKILL.md              # 必需：YAML frontmatter + Markdown 指令
│   ├── name:             # 必需：skill 名称
│   └── description:      # 必需：触发时机描述
├── scripts/              # 可选：可执行脚本（Python/Bash 等）
├── references/           # 可选：参考文档（按需加载）
└── assets/               # 可选：输出资源（模板、图标、字体等）
```

## 关键设计原则

| 原则 | 说明 |
|------|------|
| **元数据质量** | `name` 和 `description` 决定 Skill 何时被使用，使用第三人称（"This skill should be used when..."） |
| **避免重复** | 信息应只存在于 SKILL.md 或 references 之一，优先将详细内容放入 references |
| **Script 黑盒化** | 脚本可在不读入上下文的情况下执行，适合确定性和重复性任务 |
| **References 按需加载** | > 10k 词的参考文件应在 SKILL.md 中提供 grep 搜索模式 |

## 与 ys-powers 的关联

- **与 mcp-builder 的关系**：`mcp-builder` 教「如何构建 MCP Server」，`skill-creator` 教「如何构建 Claude Skill」。两者是不同层面的能力扩展：MCP 用于连接外部系统，Skill 用于封装工作流知识
- **借鉴价值**：其「渐进式加载」设计是管理大上下文的核心技术，直接适用于 ys-powers 自身的 Skill 设计；其「元数据驱动触发」机制解释了为什么好的 description 至关重要
- **搬运建议**：极高价值。这是 Skill 生态的「元 skill」，所有 ys-powers 的 Skill 开发者都应参考

## 元信息

- 来源：`refer/awesome-claude-skills/skill-creator/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
