# tailored-resume-generator

## 定位

分析职位描述，提取关键要求和关键词，生成针对该职位高度定制的简历，突出最相关的经验、技能和成就，提升面试机会。

## 触发时机

- 申请特定职位需要针对性优化简历时
- 跨行业或跨角色转行需要重新包装经验时
- 需要为 ATS（Applicant Tracking System）优化简历关键词时
- 为同一候选人创建多个面向不同职位的简历版本时
- **不适用**：通用简历模板制作、无明确目标职位时

## 核心能力

1. **JD 分析**：提取职位描述中的关键要求、技能、资格和关键词
2. **优先级识别**：根据 JD 的语言和结构判断雇主最看重的要素
3. **内容定制**：重新组织和强调与职位最相关的经验、技能和成就
4. **关键词优化**：自然融入 ATS 友好的关键词
5. **专业排版**：生成适合多种格式的清晰、专业简历布局
6. **改进建议**：指出经验差距并提供弥补建议

## 指令流程概览

1. **输入收集**：接收职位描述和候选人背景（现有简历或要点列表）
2. **JD 解析**：提取硬性要求、优先技能和隐性期望
3. **匹配映射**：将候选人经历与 JD 要求一一对应
4. **内容重写**：
   - 突出最相关的成就（用量化的结果）
   - 调整技能列表的顺序以匹配 JD 优先级
   - 自然融入关键词
5. **输出生成**：生成格式化简历 + 改进建议 + 差距分析

## 使用方式

```
I'm applying for this job:
[paste job description]

Here's my background:
- 5 years as software engineer at TechCorp
- Led team of 3 developers on mobile app project
- Expert in Python, JavaScript, React
```

## 与 ys-powers 的关联

- **与 content-research-writer 的关系**：`content-research-writer` 面向外部内容创作，`tailored-resume-generator` 面向个人职业发展。两者都涉及「分析需求 → 定制输出」
- **借鉴价值**：其「JD 解析 → 经历映射 → 关键词优化 → 排版输出」的流程是通用的「需求驱动内容定制」模式
- **搬运建议**：中等价值。适合求职者或职业顾问。注意简历内容涉及个人隐私，搬运时应确保数据安全

## 元信息

- 来源：`refer/awesome-claude-skills/tailored-resume-generator/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
