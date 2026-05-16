# skill-share

## 定位

创建新的 Claude Skill 并自动通过 Slack 分享给团队，实现 Skill 开发 → 验证 → 打包 → 通知的一体化流程。

## 触发时机

- 创建新 Skill 后需要分发给团队成员时
- 需要验证 Skill 结构是否符合规范时
- 希望将 Skill 打包为可分发格式（zip）时
- 需要自动化 Skill 开发和团队通知流程时
- **不适用**：Skill 仅个人使用、无需团队协作时

## 核心能力

1. **Skill 创建**：自动生成标准目录结构（SKILL.md、scripts/、references/、assets/）和 YAML frontmatter
2. **结构验证**：检查 SKILL.md 格式、必填字段和命名规范（hyphen-case）
3. **自动打包**：生成包含所有资源和文档的可分发 zip 文件
4. **Slack 集成**：通过 Rube 自动将 Skill 信息发送到指定 Slack 频道

## 指令流程概览

1. **初始化**：提供 Skill 名称和描述
2. **创建**：生成标准 Skill 目录结构
3. **验证**：检查元数据和命名规范
4. **打包**：创建 zip 分发包
5. **通知**：通过 Slack 向团队发送 Skill 创建通知

## Slack 集成能力

通过 Rube 调用以下工具：
- `SLACK_SEND_MESSAGE` — 发送 Skill 基本信息
- `SLACK_POST_MESSAGE_WITH_BLOCKS` — 分享格式化的 Skill 元数据
- `SLACK_FIND_CHANNELS` — 发现目标频道

## 使用示例

```
Create a skill called "pdf-analyzer"
```

执行流程：
1. 创建 `/skill-pdf-analyzer/` 目录
2. 生成 SKILL.md 模板
3. 创建 scripts/、references/、assets/ 子目录
4. 验证结构
5. 打包为 zip
6. Slack 通知："New Skill Created: pdf-analyzer — Advanced PDF analysis capabilities"

## 与 ys-powers 的关联

- **与 skill-creator 的关系**：`skill-creator` 是「Skill 开发指南」，`skill-share` 是「Skill 分发工具」。两者配套使用：先用 skill-creator 设计，再用 skill-share 分发
- **借鉴价值**：其「创建 → 验证 → 打包 → 通知」的流水线是任何内部工具分发流程的参考模板
- **搬运建议**：中等价值。适合需要团队协作维护 Skill 库的组织。依赖 Rube/Slack 集成

## 元信息

- 来源：`refer/awesome-claude-skills/skill-share/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
