# raffle-winner-picker

## 定位

从列表、CSV、Excel 或 Google Sheets 中随机抽取获奖者，使用加密安全的随机算法，确保公平、无偏、透明。

## 触发时机

- 举办社交媒体抽奖活动需要选出获奖者时
- 活动现场抽取 raffle 获奖者时
- 随机选择调查参与者或测试用户时
- 从投稿作品中选出获奖作品时
- 公平分配有限名额或资源时
- **不适用**：需要按特定条件（如成绩、活跃度）加权评选时

## 核心能力

1. **加密安全随机**：使用密码学安全的随机数生成，无偏见、无模式
2. **多数据源**：支持 CSV、Excel、Google Sheets、纯文本列表
3. **多获奖者**：可一次性抽取 1 个或多个获奖者
4. **防重复**：确保同一人不会中奖两次
5. **透明过程**：清晰展示选择过程和时间戳
6. **排除机制**：可排除已中奖者或不符合条件的条目

## 指令流程概览

1. **加载数据**：从指定来源读取所有参与条目
2. **统计报告**：输出总条目数
3. **随机抽取**：使用加密安全算法选择获奖者
4. **展示结果**：显示获奖者详情（行号、姓名、邮箱等）
5. **后续操作**：可选抽取 runner-up 或导出结果

## 输出示例

```
Accessing Google Sheet...
Total entries found: 247

Randomly selecting winner...

🎉 WINNER SELECTED! 🎉

Row #142
Name: Sarah Johnson
Email: sarah.j@email.com
Entry Date: March 10, 2024

Selection method: Cryptographically random
Timestamp: 2024-03-15 14:32:18 UTC
```

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 中无随机选择类 skill，`raffle-winner-picker` 填补了「公平随机选择」的工具空白
- **借鉴价值**：其「加密安全随机 + 透明审计日志」的设计是任何涉及随机选择的场景（如 A/B 测试分组、样本抽样）的安全基准
- **搬运建议**：低价值。功能简单，使用频率有限。但可作为通用工具 skill 的一部分保留

## 元信息

- 来源：`refer/awesome-claude-skills/raffle-winner-picker/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
