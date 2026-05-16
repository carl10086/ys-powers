# changelog-generator

## 定位

将技术性的 Git 提交历史自动转换为用户友好的发布日志（changelog），把开发语言翻译成客户语言，减少手动整理发布说明的时间。

## 触发时机

- 准备新版本发布说明时
- 需要写周报、月报形式的产品更新摘要时
- 向客户或用户文档化变更时
- 为应用商店提交或更新通知撰写 changelog 时
- 维护公开的 changelog 或产品更新页面时
- **不适用**：内部纯技术重构、无用户可见变更的提交

## 核心能力

1. **扫描 Git 历史**：分析特定时间段或版本之间的提交记录
2. **智能分类**：将提交自动归入 Features、Improvements、Bug Fixes、Breaking Changes、Security 等类别
3. **技术 → 用户语言翻译**：将开发者提交信息转换为面向客户的清晰描述
4. **噪声过滤**：自动排除内部提交（重构、测试、CI 等无用户价值的内容）
5. **品牌语调适配**：可结合品牌风格指南统一输出语气

## 指令流程概览

1. 确定时间范围或版本区间（如 "自上次发布以来"、"过去一周"、"v2.4.0 到 v2.5.0"）
2. 扫描对应区间的 Git 提交历史
3. 按类别分组并过滤内部提交
4. 将技术描述翻译为客户语言
5. 格式化输出为结构化 changelog（Markdown 格式）

## 使用方式

```
Create a changelog from commits since last release
Generate changelog for all commits from the past week
Create release notes for version 2.5.0
Create a changelog for commits since v2.4.0, using my changelog guidelines from CHANGELOG_STYLE.md
```

## 输出示例

```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different projects.
- **Keyboard Shortcuts**: Press ? to see all available shortcuts.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents
```

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 有 `git-workflow-and-versioning` skill 和 `shipping-and-launch` skill，但无专门的 changelog 生成能力。`changelog-generator` 可补全发布流程中的「内容生产」环节
- **借鉴价值**：其「技术提交 → 用户语言」的翻译模式可复用到任何需要将内部技术输出转化为外部-facing 文档的场景
- **搬运建议**：高价值，发布流程中非常实用，建议搬运到 ys-powers 的 `skills/` 中

## 元信息

- 来源：`refer/awesome-claude-skills/changelog-generator/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
