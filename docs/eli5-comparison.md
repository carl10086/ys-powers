# ELI5 三个来源的差异核对

> **研究对象**：
> 1. 文章：[ELI5スキルとは｜/eli5の中身は全文3行、もう一つのeli5とeli10の実在、自動起動を止める1行まで実測](https://ai-heartland.com/explain/eli5-skill-claude-code)
> 2. DreambigOu/ELI5：[`skills/eli5/SKILL.md`](https://github.com/DreambigOu/ELI5/blob/main/skills/eli5/SKILL.md) 及其 [README](https://github.com/DreambigOu/ELI5/blob/main/README.md)
> 3. Anthropic 社区插件仓库中的原始版：[`eli5/skills/eli5/SKILL.md`](https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md)
>
> **口径**：本文所称“Anthropic 原始版”特指上面这个路径；它位于 `anthropics/claude-plugins-community`，而不是 `anthropics/skills`。该仓库 README 明确称自己是社区插件市场的只读镜像，并将 `claude-plugins-official` 列为另一个 Anthropic-maintained 仓库。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/README.md)

## 结论先行

- **Anthropic 原始版**是一个极小的“输出形态”技能：将主题解释成 HTML artifact，强调大图、少字；它并不建立受众分类、步骤化教学或领域校准规则。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/skills/eli5/SKILL.md)
- **DreambigOu 版**是一个“受众适配框架”：先识别年龄、教育程度、职业或关系，再按受众选择词汇、类比、语气、深度和 framing；还要求先读懂源材料，并规定解释结构。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md)
- **文章**的核心贡献不是另一份实现，而是把 Anthropic 原始版的真实尺寸、提交历史、安装/触发实验，以及同名 DreambigOu 版放在一起辨析。文章把两者概括为“HTML 图解输出”与“受众/语气调节”两种不同用途。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code)
- 因此，二者不是简单的“新旧版本”关系：**DreambigOu 是功能扩展/设计分叉，而不是对原始版的逐字重写**。[推断·由两份 `SKILL.md` 的内容差异得出]

## 差异矩阵

| 维度 | Anthropic 原始版 | DreambigOu/ELI5 | 文章如何描述/核对结果 |
|---|---|---|---|
| **核心目标** | “像对完全不了解该主题的人解释”，并产出 HTML artifact、big pictures、few words。 | “让任何受众都能理解”，核心是根据背景、词汇和兴趣调整解释。 | **一致**：文章将前者概括为“形式/密度固定”，将 DreambigOu 概括为“相手に合わせて語調を変える”。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) |
| **触发描述** | `Use when the user types /eli5 <topic> or asks for a dead-simple picture explainer of how something works.` | 列出 `explain like I am`、`ELI5`、`explain this to my`、`break this down for` 等大量短语，并覆盖“给 manager、mom、5th grader”等部分匹配。 | **原始版窄、DreambigOu 宽**；这是 frontmatter 的直接差异，不是仅凭仓库名推断。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/skills/eli5/SKILL.md) · [事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **未指定受众时** | 正文只说面向“对主题一无所知的人”；没有规定默认年龄。 | 明确规定默认到 `Age 5`（classic ELI5）。 | 文章特别指出原始版正文是 “someone who knows nothing about this topic”，不能据此断言一定按真实五岁儿童输出；DreambigOu 则确实写了 Age 5 默认。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **受众模型** | 只有“知识为零”这一抽象受众。 | 三组显式分类：年龄（5/10/15/20–30/40+）、教育程度（5th grade 至 Graduate school）、职业（Manager/Engineer/Designer/Director/Product Manager/Colleague）、关系（家庭/朋友）。 | 文章把 DreambigOu 列为第二种 eli5；当前文件的四组表格直接证实这一点。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **输出载体与密度** | 明确要求 `HTML artifact`、`big pictures`、`few words`；README 也说会产生 HTML artifact。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/README.md) | 没有 HTML、artifact、图片或固定字数要求；按受众选择表达方式和长度。 | 文章用“大きな絵＋少ない言葉”解释原始版的差异化；“DreambigOu 不以 HTML artifact 为主”与当前 `SKILL.md` 的无此要求相符。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **解释流程** | 只有一条正文指令，随后写入 `Topic: $ARGUMENTS`；没有“先理解材料、再组织解释”的分步规则。 | 明确三步：`Identify the Audience` → `Read the Source Material` → `Craft the Explanation`。 | **DreambigOu 把教学过程显式化**；这是对文本的直接比较。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) · [事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/skills/eli5/SKILL.md) |
| **解释结构** | 未规定章节顺序，只规定视觉/文字密度。 | 固定建议：先一句话说明 “what”、再用 analogy、补充 details、最后回答 “so what”。 | **DreambigOu 更像可复用的教学 rubric**；“更像 rubric”是推断，四步本身是文件事实。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **类比与语言校准** | 只要求大图和少字，没有按受众规定类比类型、术语策略或句子长度。 | 年龄/职业/关系各有类比与词汇规则；简单受众要求零 jargon、必要术语立即定义、每句一个想法；技术受众保留术语并讨论 trade-offs/edge cases；商业受众聚焦 impact、outcomes、decision。 | 文章将这一区别概括为“原始版解决形式，不是解释质量”；DreambigOu 的具体规则支持这一概括。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **准确性/简化立场** | 原始正文没有准确性、根因分析或简化边界的额外声明。 | 要求先理解代码/概念/错误/技术文档；并写明复杂主题可“ruthlessly”简化，80% 能让受众理解优于 100% 但失去受众。 | 这是 DreambigOu 的额外设计；“更容易产生可校准的长解释”是推断，不能从静态文件推出实际模型效果。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) |
| **示例覆盖** | SKILL.md 没有示例，只保留 `Topic: $ARGUMENTS`。插件 README 给出 `/eli5 how does DNS work`。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/README.md) | SKILL.md 给出数据库 index、API rate limiting 给 manager、React `useEffect` 给 college student 三个示例；README 还列出 merge conflicts、error、designer 等用法。 | DreambigOu 的示例用于展示“按受众变化”，原始版 README 示例用于展示“按主题生成图解”。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md) · [事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/README.md) |
| **评估材料** | 插件目录包含 README、plugin manifest 和 `skills/eli5/SKILL.md`；原始 `SKILL.md` 本身没有 eval 规则。[事实·目录](https://api.github.com/repos/anthropics/claude-plugins-community/contents/eli5) | 仓库附带 `eli5-workspace/evals.json`、`eval-results.md`、运行脚本和测试；3 个场景对比 with-skill/baseline。 | DreambigOu 额外交付了评估工作区。其结果（skill 91.7% vs baseline 33.3%）是**仓库自报的 LLM 评估结果，不是本次独立复测**。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/eli5-workspace/eval-results.md) |
| **发布形态** | 社区插件：有 `eli5/.claude-plugin/plugin.json`（版本 1.0.0、作者 Thariq Shihipar、MIT）并可通过 marketplace 安装。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/.claude-plugin/plugin.json) | 普通 GitHub skill 仓库；README 给出的安装方式是 clone 后把 `skills/eli5` 复制到 `~/.claude/skills/eli5`，没有与原始版同形的 plugin manifest。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/README.md) | 文章核对了原始版的 marketplace 安装命令，并提醒 `anthropics/claude-plugins-community` 是社区市场只读镜像，不等于 Anthropic 官方维护插件集。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) |
| **规模与历史** | 文章报道当前文件全长 321 bytes、正文实质 3 行；Git 历史显示约 5 分 44 秒内经历“添加插件”→“HTML page 改为 HTML artifact”→“an idiot 改为 someone”的三次提交。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·提交历史](https://api.github.com/repos/anthropics/claude-plugins-community/commits?path=eli5/skills/eli5/SKILL.md&per_page=20) | GitHub Contents API 报告 `skills/eli5/SKILL.md` 为 7,965 bytes；初始提交将该文件作为 116 行新增内容，并同时加入 eval workspace。[事实·API](https://api.github.com/repos/DreambigOu/ELI5/contents/skills/eli5/SKILL.md?ref=main) · [事实·提交](https://api.github.com/repos/DreambigOu/ELI5/commits/591c8590fb71174db8229a0d3a0e728eabc99fe2) | 文章用“3 行 vs 3,242 bytes”等数字强调同名技能的规模/用途差异；其中 3,242 bytes 是文章对另一版本的测量口径，不能替换本次 GitHub API 当前报告的 7,965 bytes。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·API](https://api.github.com/repos/DreambigOu/ELI5/contents/skills/eli5/SKILL.md?ref=main) |

## 文章与文件之间需要保留的限定

1. **“Anthropic 原始版”不等于“官方维护技能集”。** 文章称它不是 `anthropics/skills` 或 `claude-plugins-official` 中的官方技能；社区仓库自己的 README 也说明这是社区插件市场只读镜像。可以说作者是 Anthropic 工程师、插件通过社区分发，但不应把它简称成 Anthropic 官方技能。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code) · [事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/README.md)
2. **文章的实验结论与静态文件事实要分开。** 例如文章报告常驻约 39 tokens、`disable-model-invocation: true` 的 A/B 结果、以及 show-me 的触发波动；这些是文章描述的特定 Claude Code 版本/运行条件，不是仅凭 `SKILL.md` 可以推出的普遍行为。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code)
3. **DreambigOu 的评估数字不能当成跨模型基准。** 仓库明确记录了 3 个测试、每个测试 with/without skill 的比较和 LLM grader；91.7% vs 33.3% 是该仓库自己的实验结果，且 `eval-results.md` 自己指出 LLM grading 存在波动。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/eli5-workspace/eval-results.md)
4. **“功能扩展”是比较结论，不是作者自称 fork。** 两份 `SKILL.md` 的命名相同，但 DreambigOu 的提交历史显示其 2026-03-17 是一个独立仓库的初始提交；现有来源没有证明它从 Anthropic 文件复制而来。因此更稳妥的说法是“同名、独立实现、用途不同”。[事实·提交](https://api.github.com/repos/DreambigOu/ELI5/commits/591c8590fb71174db8229a0d3a0e728eabc99fe2)；“用途不同/扩展”属于[推断]。

## 使用选择

- **要一张低文字量、视觉化的 HTML 图解**：选 Anthropic 原始版；它的正文直接把 HTML artifact、big pictures、few words 写成输出约束。[事实·文件](https://raw.githubusercontent.com/anthropics/claude-plugins-community/main/eli5/skills/eli5/SKILL.md)
- **要把同一主题讲给 manager、engineer、孩子或家人，并改变词汇、语气、关注点**：选 DreambigOu 版；其受众表和语言校准规则是专门为此设计的。[事实·文件](https://raw.githubusercontent.com/DreambigOu/ELI5/main/skills/eli5/SKILL.md)
- **要理解“为什么这两个都叫 eli5”**：文章提供了辨名背景，但实际选择应以 marketplace/repository/path 为准，不能只按 `eli5` 搜索结果判断。[事实·文章](https://ai-heartland.com/explain/eli5-skill-claude-code)

## 来源索引

- 文章原文：https://ai-heartland.com/explain/eli5-skill-claude-code
- DreambigOu skill：`DreambigOu/ELI5 → skills/eli5/SKILL.md`  
  https://github.com/DreambigOu/ELI5/blob/main/skills/eli5/SKILL.md
- DreambigOu README：`DreambigOu/ELI5 → README.md`  
  https://github.com/DreambigOu/ELI5/blob/main/README.md
- DreambigOu eval：`DreambigOu/ELI5 → eli5-workspace/eval-results.md`  
  https://github.com/DreambigOu/ELI5/blob/main/eli5-workspace/eval-results.md
- Anthropic 原始 skill：`anthropics/claude-plugins-community → eli5/skills/eli5/SKILL.md`  
  https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md
- Anthropic 插件 README：`anthropics/claude-plugins-community → eli5/README.md`  
  https://github.com/anthropics/claude-plugins-community/blob/main/eli5/README.md
- Anthropic 插件 manifest：`anthropics/claude-plugins-community → eli5/.claude-plugin/plugin.json`  
  https://github.com/anthropics/claude-plugins-community/blob/main/eli5/.claude-plugin/plugin.json
- Anthropic skill 提交历史：
  https://api.github.com/repos/anthropics/claude-plugins-community/commits?path=eli5/skills/eli5/SKILL.md&per_page=20
