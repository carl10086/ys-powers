# internal-comms

## 定位

一套公司内部沟通文档的写作资源库，覆盖 3P 更新、公司简报、FAQ、状态报告、项目更新等常见内部沟通场景，确保格式和语调符合公司规范。

## 触发时机

- 需要撰写 3P 更新（Progress, Plans, Problems）时
- 编写公司级或团队级 newsletter 时
- 回应内部常见问题（FAQ）时
- 准备领导层汇报或项目状态报告时
- 撰写事故报告（incident report）时
- **不适用**：对外公开的新闻稿、客户沟通或法律文件

## 核心能力

1. **类型识别**：自动判断沟通文档的类型（3P 更新、简报、FAQ、事故报告等）
2. **格式规范**：每种类型有独立的 guideline 文件，定义结构、语调和内容要求
3. **语调一致**：保持公司内部统一的沟通风格
4. **模板套用**：从 `examples/` 目录加载对应模板并按规范填充内容

## 支持的沟通类型

| 类型 | Guideline 文件 | 适用场景 |
|------|---------------|---------|
| 3P 更新 | `examples/3p-updates.md` | 团队周会、进度同步 |
| 公司简报 | `examples/company-newsletter.md` | 全员通知、月度总结 |
| FAQ 回复 | `examples/faq-answers.md` | 回应常见内部问题 |
| 通用沟通 | `examples/general-comms.md` | 不匹配以上类型的其他内部沟通 |

## 指令流程概览

1. **识别沟通类型**：从用户请求中提取文档类型关键词
2. **加载 Guideline**：从 `examples/` 目录读取对应类型的格式和语调规范
3. **收集内容**：按 guideline 要求的结构收集信息（进度、计划、问题等）
4. **撰写文档**：遵循规范生成符合公司风格的内部沟通文稿

## 与 ys-powers 的关联

- **与 content-research-writer 的关系**：`content-research-writer` 面向外部内容创作（博客、案例研究），`internal-comms` 面向内部沟通。两者互补
- **借鉴价值**：其「类型识别 → 模板加载 → 规范输出」的模式可复用到任何需要「按固定格式生成文档」的场景（如会议纪要、周报、Checklist）
- **搬运建议**：中等价值。若 ys-powers 的使用者需要维护团队/公司内部的沟通规范，可搬运并替换 `examples/` 中的模板为自有规范

## 元信息

- 来源：`refer/awesome-claude-skills/internal-comms/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
