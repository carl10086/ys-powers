# gstack 技能全景清单

> 来源：[garrytan/gstack](https://github.com/garrytan/gstack)（MIT 许可）
> 统计时间：2026/05/25，基于 `refer/gstack/` 目录内容

---

## 分类总览

gstack 提供 **50+ 个 slash-command 技能**，按职能分为 7 大类：

| 类别 | 技能数 | 核心价值 |
|------|--------|----------|
| [规划与产品思考](#一规划与产品思考) | 7 | 在写代码前锁定正确的问题 |
| [实现与审查](#二实现与审查) | 11 | 高质量编码、调试、设计、QA |
| [发布与部署](#三发布与部署) | 7 | 从 PR 到生产验证的完整管线 |
| [运营与记忆](#四运营与记忆) | 8 | 跨会话知识积累与质量监控 |
| [浏览器与智能体集成](#五浏览器与智能体集成) | 5 | 真实浏览器环境 + 多智能体协同 |
| [iOS QA](#六ios-qa) | 5 | USB 真机测试与修复 |
| [安全与工具](#七安全与工具) | 7 | 防御性编程与实用工具 |

---

## 一、规划与产品思考

> 目标：**在写第一行代码前，确保你在解决正确的问题，用正确的方式。**

| 技能 | 一句话描述 | 工作流位置 |
|------|-----------|-----------|
| `/office-hours` | YC 风格的 6 个强制性问题，重新框定产品需求 | Think 阶段入口 |
| `/plan-ceo-review` | CEO 级范围挑战——在需求里找到 10 星产品的切入点 | Think → Plan 过渡 |
| `/plan-eng-review` | 锁定架构、数据流、ASCII 图、边界情况、测试策略 | Plan 阶段核心 |
| `/plan-design-review` | 10 维度设计评分（0-10），描述"10 分长什么样" | Plan 阶段并行 |
| `/plan-devex-review` | DX 审计：首次上手时间、魔法时刻、摩擦点（20-45 个问题） | Plan 阶段可选 |
| `/autoplan` | 一键串行执行 CEO → 设计 → 工程 → DX 四个审查 | Plan 阶段自动化 |
| `/design-consultation` | 从零构建完整设计系统，附带竞品调研 | 独立设计任务 |

**关键机制**：`autoplan` 不是简单串 prompt，而是每个步骤产出的文档（设计 PRD、工程规格、DX 报告）会写入磁盘，后续步骤自动读取。这是"过程即产物"哲学的体现。

---

## 二、实现与审查

> 目标：**让 AI 写出人级别的代码，并找到 CI 通过后仍会在生产环境崩溃的 bug。**

| 技能 | 一句话描述 | 输出物 |
|------|-----------|--------|
| `/review` |  staff engineer 级 PR 审查 | 审查报告 + 逐文件意见 |
| `/codex` | 引入 OpenAI Codex CLI 作为第二意见 | 独立审查报告 |
| `/investigate` | 系统化根因调试；铁律：没有调查就没有修复 | 调查报告 + 修复方案 |
| `/design-review` | 对线上站点进行视觉审计 + 修复循环 | 截图对比 + 原子提交 |
| `/design-shotgun` | 生成 4-6 个 AI  mockup 变体，对比板迭代 | 变体图片 + 决策记录 |
| `/design-html` | 产出可投产 Pretext 原生 HTML/CSS（30KB，零依赖） | 单文件 HTML |
| `/qa` | 打开真实浏览器，找 bug，原子修复，回归验证 | 修复 + 回归测试 |
| `/qa-only` | 同上，但只报告不修改代码 | 纯 QA 报告 |
| `/scrape` | 从网页拉取数据；原型 → 固化浏览器技能约 200ms | 数据 / 技能模板 |
| `/skillify` | 将上一次 `/scrape` 固化为可复用技能 | 永久 SKILL.md |
| `/devex-review` | 实时 DX 审计——真实走一遍 onboarding，截图记录错误 | DX 报告 + 截图 |

**关键机制**：`review` 不是简单的 diff 分析，它有 7 名专项审计员（api-contract、data-migration、maintainability、performance、red-team、security、testing），每个子专家独立运行后再汇总。这借鉴了 GPT-4 的"debate"模式。

---

## 三、发布与部署

> 目标：**从代码完成到生产验证，零手动步骤。**

| 技能 | 一句话描述 | 触发时机 |
|------|-----------|----------|
| `/ship` | 同步 main、运行测试、审计覆盖率、提升 VERSION、更新 CHANGELOG、开 PR | 功能完成时 |
| `/land-and-deploy` | 合并 PR、等待 CI/部署、端到端验证生产健康 | PR 通过后 |
| `/canary` | 部署后监控循环（控制台错误、性能回退、页面失败） | 部署完成后 |
| `/benchmark` | 基准化页面加载、Core Web Vitals、资源体积；前后对比 | 性能优化前后 |
| `/document-release` | 更新所有文档以匹配已发布内容；构建 Diataxis 覆盖图 | 发布完成后 |
| `/document-generate` | 从代码生成 Diataxis 文档（教程/指南/参考/解释） | 随时 |
| `/setup-deploy` | 一次性部署配置检测（Fly.io、Render、Vercel 等） | 项目初始化 |

**关键机制**：`ship` 会自举测试框架（如果项目没有测试）。它会检测项目类型（Node/Python/Go/Rust 等），安装对应的测试 runner，并生成第一个测试文件。这是"完整性优先"原则的体现。

---

## 四、运营与记忆

> 目标：**让知识跨会话积累，让质量可量化。**

| 技能 | 一句话描述 | 解决的问题 |
|------|-----------|-----------|
| `/context-save` | 保存工作状态（git 状态、决策、剩余工作） | Claude 上下文压缩后丢失进度 |
| `/context-restore` | 从保存的上下文恢复，跨 Conductor 工作区 | 跨会话续作 |
| `/learn` | 管理跨会话的学习记录（模式、陷阱、偏好） | 重复犯同样的错 |
| `/retro` | 每周复盘，含个人分工和 shipping streak | 缺乏系统性回顾 |
| `/health` | 代码质量仪表盘（类型检查、lint、测试、死代码）→ 0-10 分 | 质量退化不可见 |
| `/landing-report` | 只读仪表盘：工作区感知的发布队列 | 团队可见性 |
| `/benchmark-models` | 跨模型基准（Claude vs GPT vs Gemini）运行技能 | 模型选择 |
| `/setup-gbrain` | 一键配置 gbrain（PGLite 本地 / Supabase 现有 / 自动 provision） | 记忆基础设施 |
| `/sync-gbrain` | 重新索引仓库代码到 gbrain；刷新 CLAUDE.md 搜索指引 | 代码库记忆同步 |

**关键机制**：gbrain 是 gstack 的跨机器记忆系统。它支持三种后端：PGLite（本地 PostgreSQL WASM）、现有 Supabase、或自动 provision 的新 Supabase 项目。`sync-gbrain` 会把代码库向量化，让后续会话能通过语义搜索快速定位相关代码。

---

## 五、浏览器与智能体集成

> 目标：**让 AI 在真实浏览器环境中工作，并支持多智能体协同。**

| 技能 | 一句话描述 | 技术亮点 |
|------|-----------|----------|
| `/browse` | 快速 headless 浏览器（~100ms/命令，持久状态，真实 Chromium） | Bun HTTP 守护进程 |
| `/open-gstack-browser` | 启动带侧边栏、stealth、模型路由的可见 GStack Browser | 集成扩展 |
| `/setup-browser-cookies` | 从真实浏览器（Chrome/Arc/Brave/Edge）导入 Cookie 用于认证测试 | 自动检测 |
| `/pair-agent` | 配对远程 AI 智能体（OpenClaw/Codex 等）与你的浏览器，通过限定隧道 | 跨厂商智能体协同 |
| `/connect-chrome` | `open-gstack-browser` 的别名 |

**关键机制**：`/pair-agent` 是业界首个跨厂商 AI 智能体协调工具。它让 Claude Code 和 OpenClaw/Codex 共享同一个浏览器实例，通过限定 token 和标签隔离确保安全。隧道架构采用双监听器 + 表面拒绝日志。

---

## 六、iOS QA

> 目标：**在真实 iPhone 上运行端到端测试。**

| 技能 | 一句话描述 | 要求 |
|------|-----------|------|
| `/ios-qa` | 通过 USB CoreDevice + 嵌入式 StateServer 驱动真机 | macOS + Xcode + USB iPhone |
| `/ios-fix` | 自主 iOS bug 修复器，捕获回归快照 | 同上 |
| `/ios-design-review` | 10 维度 Apple HIG 审计在真机上 | 同上 |
| `/ios-clean` | 移除 DebugBridge + `#if DEBUG` 布线，准备 Release 构建 | 发布前 |
| `/ios-sync` | 针对最新上游重新生成 iOS accessor/template | 依赖更新后 |

---

## 七、安全与工具

> 目标：**防御性编程和实用工具。**

| 技能 | 一句话描述 | 场景 |
|------|-----------|------|
| `/cso` | OWASP Top 10 + STRIDE 安全审计，8/10+ 置信度门槛 | 发布前强制审查 |
| `/careful` | 在破坏性命令前警告（`rm -rf`、`DROP TABLE`、force-push） | 日常防护 |
| `/freeze` | 硬阻断对指定目录外的编辑 | 锁定范围 |
| `/guard` | 同时激活 `/careful` + `/freeze` | 高危操作 |
| `/unfreeze` | 移除编辑限制 | 解除锁定 |
| `/make-pdf` | 将任意 Markdown 转为出版质量 PDF | 文档输出 |
| `/plan-tune` | 自调优 AskUserQuestion 敏感度 | 交互优化 |
| `/gstack-upgrade` | 自更新器，带迁移支持 | 版本升级 |

**关键机制**：`cso`（Chief Security Officer）不是简单的 checklist，它运行分层安全审计：L1-L3 内容安全、L4 ML 分类器（22MB BERT-small，可选 721MB DeBERTa）、L4b 转录分类器、L5 canary token。集成阻断规则：仅当 ML 和转录分类器**都同意**时才阻断。

---

## 附录：技能目录结构约定

每个 gstack 技能遵循统一目录结构：

```
skill-name/
├── SKILL.md              # 生成的技能定义（Claude 读取）
├── SKILL.md.tmpl         # 源模板（编辑此文件，运行 gen:skill-docs）
└── [支持文件/]            # 可选：checklist、子专家目录、模板
```

**典型支持文件示例**：
- `review/checklist.md` — 审查 checklist
- `review/specialists/` — 7 名子专家审计文件
- `qa/templates/qa-report-template.md` — QA 报告模板
- `ship/TODOS-format.md` — TODO 格式规范

---

## 附录：文档体系

gstack 在 `docs/` 目录下维护完整的 Diataxis 文档体系：

| 文档 | 类型 | 用途 |
|------|------|------|
| `tutorial-document-generate.md` | Tutorial | 教用户用 `/document-generate` |
| `howto-document-a-shipped-feature.md` | How-to | 发布后补文档的工作流 |
| `howto-ios-testing-with-gstack.md` | How-to | iOS 真机测试完整 walkthrough |
| `skills.md` | Reference | 所有 45+ 技能的深度参考 |
| `OPENCLAW.md` | Reference | OpenClaw 集成协议（5 级 dispatch） |
| `ADDING_A_HOST.md` | Reference | 如何添加新 AI 智能体适配 |
| `ON_THE_LOC_CONTROVERSY.md` | Explanation | 生产力声明的方法论辩护 |
| `explanation-diataxis-in-gstack.md` | Explanation | 为什么用 Diataxis 框架 |
| `designs/*.md` | Architecture | 18 份架构决策记录（ADR） |

---

## 相关文档

- [overview.md](overview.md) — gstack 总体介绍与架构概览
- [integration-analysis.md](integration-analysis.md) — 哪些能力可以借鉴/集成到 ys-powers
