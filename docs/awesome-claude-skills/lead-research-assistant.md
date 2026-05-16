# lead-research-assistant

## 定位

通过分析产品定位和理想客户画像（ICP），识别高质量潜在客户，提供按匹配度排序的线索列表和个性化的接触策略。

## 触发时机

- 需要为产品或服务寻找潜在客户时
- 准备合作伙伴或目标公司的 outreach 名单时
- 进行销售拓展（sales outreach）前需要调研目标账户时
- 需要验证某个市场领域是否存在足够多的匹配客户时
- **不适用**：B2C 场景、或产品定位尚不明确的早期探索阶段

## 核心能力

1. **业务理解**：分析产品价值主张、核心功能和解决的问题
2. **ICP 定义**：基于行业、公司规模、地理位置、技术栈、痛点等维度定义理想客户
3. **线索搜索**：根据 ICP 搜索匹配的公司，利用招聘动态、技术栈、融资新闻等信号判断需求
4. **优先级排序**：按匹配度（1-10 分）排序，考虑需求紧迫性、预算、竞争格局等
5. **接触策略**：为每个线索提供个性化的 outreach 建议、决策人角色和 conversation starters
6. **数据丰富**：收集决策人信息和公司上下文

## 指令流程概览

1. **理解产品**：分析代码库（如在项目目录中运行）或产品描述，提取价值主张和核心功能
2. **定义 ICP**：确定目标行业、公司规模、地理位置、痛点和技术要求
3. **搜索线索**：基于 ICP 搜索匹配公司，利用公开信号（招聘、融资、技术栈）验证需求
4. **评分排序**：为每个线索计算匹配度分数并排序
5. **生成输出**：为每个线索提供公司名称、匹配理由、优先级、决策人、接触策略和价值主张

## 输出格式

```markdown
# Lead Research Results

## Summary
- Total leads found: [X]
- High priority (8-10): [X]
- Medium priority (5-7): [X]

## Top Leads

### 1. [Company Name]
- **Website**: [URL]
- **Why Fit**: [具体匹配理由]
- **Priority**: [分数]/10
- **Decision Maker**: [目标角色]
- **Contact Strategy**: [个性化 outreach 建议]
- **Value Prop**: [针对该公司的产品价值]
```

## 与 ys-powers 的关联

- **与 competitive-ads-extractor 的关系**：`competitive-ads-extractor` 分析竞品广告策略，`lead-research-assistant` 分析潜在客户。两者都属于市场情报范畴，方向互补
- **借鉴价值**：其「产品分析 → ICP 定义 → 信号搜索 → 评分排序 → 策略输出」的五步流程是通用的 B2B 销售研究方法论
- **搬运建议**：中等价值。适合有销售或 BD 需求的团队。注意线索数据的准确性依赖公开信息源

## 元信息

- 来源：`refer/awesome-claude-skills/lead-research-assistant/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
