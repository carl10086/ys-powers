# competitive-ads-extractor

## 定位

从 Facebook Ad Library、LinkedIn 等广告库中提取竞品广告，分析其 messaging、痛点定位和创意策略，为自身广告活动提供数据驱动的灵感。

## 触发时机

- 研究竞品广告策略和定位时
- 为新产品广告寻找创意灵感时
- 需要理解市场主流 messaging 和痛点表达时
- 分析特定行业或平台的广告趋势时
- 规划广告活动并希望基于已验证的概念时
- **不适用**：无明确竞品、或广告平台不可访问的场景

## 核心能力

1. **广告抓取**：从 Facebook Ad Library、LinkedIn 等平台抓取活跃广告
2. **截图存档**：保存所有广告的可视化副本到本地目录
3. **Messaging 分析**：提取竞品强调的问题、使用场景和价值主张
4. **主题分类**：按主题、受众或格式对广告进行分组
5. **模式识别**：发现共同的成功广告手法和创意模式
6. **效果洞察**：解释为什么某些广告可能表现良好（基于结构、文案、视觉等维度）

## 指令流程概览

1. 指定竞品名称和目标平台（Facebook / LinkedIn）
2. 抓取该竞品在广告库中的所有活跃广告
3. 保存截图到 `competitor-ads/<competitor-name>/` 目录
4. 分析 messaging：痛点、使用场景、价值主张
5. 分类整理并输出洞察报告

## 使用方式

```
Extract all current ads from [Competitor Name] on Facebook Ad Library
Scrape ads from [Company] and analyze their messaging
Extract ads from these 5 competitors: [list]. Compare their approaches.
Get LinkedIn ads from [Competitor] and analyze their B2B positioning strategy
```

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 中无竞品分析类 skill，`competitive-ads-extractor` 填补了市场研究领域的空白
- **借鉴价值**：其「抓取 → 截图存档 → 结构化分析」的三段式流程可复用到任何竞品情报收集场景
- **搬运建议**：价值中等，适合有营销/增长团队的组织。若 ys-powers 的使用者常涉及市场分析，可搬运

## 元信息

- 来源：`refer/awesome-claude-skills/competitive-ads-extractor/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
