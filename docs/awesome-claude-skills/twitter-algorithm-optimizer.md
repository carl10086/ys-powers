# twitter-algorithm-optimizer

## 定位

基于 Twitter 开源推荐算法的核心原理（Real-graph、SimClusters、TwHIN、Tweepcred），分析和优化推文以获得最大曝光和互动。

## 触发时机

- 需要优化推文草稿以提高算法推荐概率时
- 理解为什么某条推文表现不佳（算法层面）时
- 希望基于 Twitter 实际排名机制改写内容时
- 制定整体 Twitter 内容策略时
- **不适用**：非 Twitter/X 平台的内容优化

## 核心能力

1. **算法分析**：对照 Twitter 核心推荐模型评估推文：
   - **Real-graph**：预测粉丝互动可能性
   - **SimClusters**：识别社区共鸣度
   - **TwHIN**：用户与内容主题的知识图谱匹配
   - **Tweepcred**：用户信誉/权威度评分

2. **信号识别**：分析显性和隐性互动信号：
   - 显性：点赞、回复、转发、引用推文
   - 隐性：个人主页访问、点击、停留时间、收藏
   - 负面：屏蔽、举报、静音、快速划走

3. **内容改写**：基于算法洞察优化推文文案
4. **策略建议**：提供基于算法机制的增长策略

## Twitter 推荐流程

1. **候选检索**：多源发现候选推文（搜索索引、时间线关系图、趋势内容）
2. **排名预测**：ML 模型预测互动概率（该用户是否会互动？多快？会传播吗？）
3. **过滤**：移除屏蔽内容，应用偏好设置
4. **投放**：向用户展示排序后的时间线

## 优化策略

| 策略 | 核心动作 |
|------|---------|
| 最大化 Real-graph | 发布粉丝愿意互动的内容，提问比陈述获得更多回复 |
| 利用 SimClusters | 创作紧密社区共鸣的内容，清晰信号主题归属 |
| 提升 TwHIN 匹配 | 保持在垂直领域或清晰标记主题转换 |
| 积累 Tweepcred | 通过持续互动建立信誉，高信誉账户获得更多分发 |

## 与 ys-powers 的关联

- **与 content-research-writer 的关系**：`content-research-writer` 面向长内容创作，`twitter-algorithm-optimizer` 面向短内容算法优化。两者互补
- **借鉴价值**：其「算法拆解 → 信号映射 → 策略输出」的分析框架可复用到任何需要理解平台推荐机制的场景（如 LinkedIn、YouTube、TikTok）
- **搬运建议**：中等价值。适合有社交媒体运营需求的用户。注意算法细节可能随 Twitter/X 更新而变化

## 元信息

- 来源：`refer/awesome-claude-skills/twitter-algorithm-optimizer/SKILL.md`
- 维护者：Composio / 社区
- 许可证：AGPL-3.0（引用 Twitter 开源算法源码）
