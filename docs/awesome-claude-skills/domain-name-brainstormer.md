# domain-name-brainstormer

## 定位

为新项目、产品或公司生成创意域名建议，并实时检查 `.com`、`.io`、`.dev`、`.ai` 等多 TLD 的可用性，将数小时的头脑风暴和手动查询压缩为几分钟。

## 触发时机

- 启动新项目或公司需要域名时
- 为产品、服务或个人品牌寻找在线标识时
- 首选域名已被注册，需要寻找替代方案时
- 需要检查特定关键词组合的域名可用性时
- **不适用**：已有确定域名、仅需注册的场景

## 核心能力

1. **项目理解**：分析项目定位和目标受众，生成相关性高的命名方向
2. **创意生成**：创建 memorable、品牌感强的域名选项
3. **可用性检查**：实时验证 `.com`、`.io`、`.dev`、`.ai`、`.app` 等 TLD 的注册状态
4. **替代建议**：当首选被占用时，提供变体、组合词或创意拼写方案
5. **品牌洞察**：解释每个建议名称的优势和目标受众的感知效果
6. **价格提示**：标注已被占用域名的预估收购价格（如有）

## 指令流程概览

1. **理解项目**：解析用户描述的项目类型、目标受众和核心关键词
2. **生成候选**：基于语义关联、行业惯例和语言创意生成 10-15 个候选名称
3. **检查可用性**：逐一查询各 TLD 的注册状态（可用 / 被占用 / 溢价）
4. **分级推荐**：
   - 首选推荐：短、易记、高度相关的可用域名
   - 备选方案：不同 TLD 或轻微变体
   - 创意方案：组合词、造词或隐喻式命名
5. **品牌分析**：为每个推荐解释其品牌传播价值

## 使用示例

```
I'm building a tool for developers to share code snippets. Suggest domain names.

I need a domain name for my AI writing assistant.
Prefer short names with .ai or .io extension.

Suggest domain names using the words "pixel" or "studio"
for my design agency
```

## 输出示例

```
🎯 Domain Name Suggestions

## Available (.com)
1. ✓ snippetbox.com — Clear, memorable, available!
2. ✓ codeclip.com — Short and snappy (8 characters)
3. ✓ devpaste.com — Developer-focused

## Available (Alternative TLDs)
4. ✓ snippet.dev — Perfect for developer audience
5. ✓ codebox.io — Tech-forward
6. ✓ sharecode.app — Descriptive

## Premium / Taken
- codeshare.com (Taken, est. $2,500)
- snippets.com (Taken, premium domain)

🏆 Top Pick: snippet.dev
🥈 Runner-up: snippetbox.com
```

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 中无品牌命名或域名相关 skill，`domain-name-brainstormer` 填补了「产品启动」阶段的工具空白
- **借鉴价值**：其「关键词提取 → 语义扩展 → 可用性验证 → 品牌分析」的四步流程可复用到任何命名场景（变量命名、项目命名、API 端点命名）
- **搬运建议**：中等价值。适合独立开发者、创业者或产品团队。若 ys-powers 的使用者群体包含大量初创项目，值得搬运

## 元信息

- 来源：`refer/awesome-claude-skills/domain-name-brainstormer/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
