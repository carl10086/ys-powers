## Step 1: 逐段精读

### workflows/plan-phase.md

#### 段落 1: purpose

**原文:**
```xml
<purpose>
Create executable phase prompts (PLAN.md files) for a roadmap phase with integrated research and verification. Default flow: Research (if needed) -> Plan -> Verify -> Done. Orchestrates gsd-phase-researcher, gsd-planner, and gsd-plan-checker agents with a revision loop (max 3 iterations).
</purpose>
```

**翻译:**
为路线图阶段创建可执行的阶段提示（PLAN.md 文件），集成研究和验证。默认流程：研究（如需要）→ 规划 → 验证 → 完成。编排 gsd-phase-researcher、gsd-planner 和 gsd-plan-checker agent，并包含修订循环（最多 3 次迭代）。

**要点:**
- **可执行提示（executable prompts）** 是关键概念：PLAN.md 不是给人读的文档，而是给 Claude executor 执行的指令
- **三 agent 架构**：研究者（调研技术方案）→ 规划者（拆分为任务）→ 检查者（验证质量），形成完整的规划流水线
- **修订循环上限 3 次**：防止无限循环，体现对效率和收敛性的控制

---

#### 段落 2: required_reading

**原文:**
```xml
<required_reading>
Read all files referenced by the invoking prompt's execution_context before starting.

@~/.claude/get-shit-done/references/ui-brand.md
@~/.claude/get-shit-done/references/revision-loop.md
@~/.claude/get-shit-done/references/gate-prompts.md
@~/.claude/get-shit-done/references/agent-contracts.md
@~/.claude/get-shit-done/references/gates.md
</required_reading>
```

**翻译:**
在开始之前，读取调用提示的 execution_context 中引用的所有文件。
[列出 5 个参考文件]

**要点:**
- **依赖注入模式**：工作流不直接包含所有规则，而是通过引用加载外部定义，实现规则复用和独立更新
- **5 个核心参考**：UI 品牌规范、修订循环逻辑、门控提示模板、agent 契约、门控定义 — 这些是工作流的"宪法"
- **为什么重要**：确保工作流执行者加载完整上下文，避免因规则缺失导致的决策偏差

---

#### 段落 3: available_agent_types

**原文:**
```xml
<available_agent_types>
Valid GSD subagent types (use exact names — do not fall back to 'general-purpose'):
- gsd-phase-researcher — Researches technical approaches for a phase
- gsd-pattern-mapper — Analyzes codebase for existing patterns, produces PATTERNS.md
- gsd-planner — Creates detailed plans from phase scope
- gsd-plan-checker — Reviews plan quality before execution
</available_agent_types>
```

**翻译:**
有效的 GSD 子 agent 类型（使用确切名称 — 不要回退到 'general-purpose'）：
- gsd-phase-researcher — 为阶段研究技术方案
- gsd-pattern-mapper — 分析代码库中的现有模式，生成 PATTERNS.md
- gsd-planner — 从阶段范围创建详细计划
- gsd-plan-checker — 在执行前审查计划质量

**要点:**
- **4 种专业 agent**：研究者、模式映射器、规划者、检查者，每种有明确分工
- **禁用通用 agent**：强制使用专业 agent，避免"通用目的"带来的能力稀释
- **模式映射器（pattern-mapper）是可选的**：在步骤 7.8 中条件触发，用于提取代码库中的现有模式作为参考

---

#### 段落 4: process - 步骤 1 Initialize（初始化）

**原文:**
（第 23-50 行，包含 bash 命令和 JSON 解析逻辑）

**翻译:**
通过一次调用加载所有上下文（仅路径以最小化编排器上下文）：
- 调用 `gsd-tools.cjs init plan-phase` 获取初始化数据
- 获取各 agent 的技能配置
- 获取上下文窗口大小、TDD 模式等配置
- 解析 JSON 提取：研究者模型、规划者模型、检查者模型、研究启用状态、检查器启用状态、Nyquist 验证启用状态、提交文档配置、文本模式、阶段信息、文件路径等
- 如果 `planning_exists` 为 false：报错，要求先运行 `/gsd-new-project`

**要点:**
- **单点初始化**：通过 `gsd-tools.cjs init` 一次性获取所有上下文，避免多次系统调用
- **模型分离**：研究者、规划者、检查者可以使用不同模型（如研究用轻量级，规划用强模型）
- **大上下文优化**：当上下文窗口 ≥ 500K 时，自动加载最近 3 个阶段的 CONTEXT.md 和 SUMMARY.md，利用历史上下文提升规划一致性
- **前置检查**：如果没有 `.planning/` 目录，直接报错 — 不假设环境已就绪

---

#### 段落 5: process - 步骤 2 Parse and Normalize Arguments（参数解析）

**原文:**
（第 52-66 行）

**翻译:**
从 `$ARGUMENTS` 提取：阶段编号（整数或小数如 `2.1`）、标志（`--research`、`--skip-research`、`--gaps`、`--skip-verify`、`--skip-ui`、`--prd <filepath>`、`--reviews`、`--text`、`--bounce`、`--skip-bounce`）。

如果 `$ARGUMENTS` 中有 `--text` 或 init JSON 中 `text_mode` 为 true：设置 `TEXT_MODE=true`，将所有 `AskUserQuestion` 替换为纯文本编号列表。

提取 `--prd <filepath>`。

如果没有阶段编号：从路线图检测下一个未规划阶段。

如果 `phase_found` 为 false：验证阶段是否存在于 ROADMAP.md，如果有效则创建目录。

**要点:**
- **丰富的标志系统**：12 个不同的命令行标志，支持精细控制流程行为
- **TEXT_MODE 设计**：为远程会话（如 `/rc` 模式）提供降级方案，因为 TUI 菜单在 Claude App 远程会话中无法工作
- **PRD 快速路径**：支持直接从 PRD 文件生成 CONTEXT.md，跳过 discuss-phase
- **自动检测**：未提供阶段编号时自动推断，减少用户输入负担

---

#### 段落 6: process - 步骤 2.5 Validate --reviews Prerequisite

**原文:**
（第 68-84 行）

**翻译:**
如果 `--reviews` 和 `--gaps` 同时存在：报错 — 不能组合使用，这是冲突模式。

如果 `--reviews` 存在但 `has_reviews` 为 false（阶段目录中没有 REVIEWS.md）：报错并提示先运行 `/gsd-review --phase {N}`，然后重新运行 `/gsd-plan-phase {N} --reviews`。

**要点:**
- **互斥模式检查**：`--reviews`（基于反馈重新规划）和 `--gaps`（修复验证差距）不能同时使用，防止逻辑冲突
- **前置条件验证**：`--reviews` 要求必须先有 REVIEWS.md，不假设文件存在
- **明确的错误恢复路径**：错误信息包含下一步命令，用户知道如何修复

---

#### 段落 7: process - 步骤 3 Validate Phase

**原文:**
（第 86-92 行）

**翻译:**
调用 `gsd-tools.cjs roadmap get-phase` 验证阶段。

如果 `found` 为 false：报错并列出可用阶段。
如果 `found` 为 true：提取阶段编号、阶段名称、目标。

**要点:**
- **严格的阶段验证**：不依赖用户输入的阶段编号，而是查询路线图验证其有效性
- **失败时提供可用选项**：报错信息包含可用阶段列表，帮助用户纠正

---

#### 段落 8: process - 步骤 3.5 Handle PRD Express Path

**原文:**
（第 96-196 行）

**翻译:**
如果提供了 `--prd <filepath>`：
1. 读取 PRD 文件内容
2. 显示 "PRD EXPRESS PATH" 横幅
3. 解析 PRD 内容并生成 CONTEXT.md：
   - 提取所有需求、用户故事、验收标准和约束
   - 映射为锁定决策（PRD 中的一切都被视为锁定决策）
   - 识别 PRD 未覆盖的区域并标记为 "Claude's Discretion"
   - **提取规范引用** — 从 ROADMAP.md 和 PRD 中引用的规范/ADR 扩展为完整文件路径（强制）
   - 在阶段目录中创建 CONTEXT.md
4. 提交 CONTEXT.md
5. 设置 `context_content` 并跳到步骤 5（跳过后续 CONTEXT.md 加载）

**要点:**
- **PRD 直通模式**：允许用户直接提供产品需求文档，自动转换为规划所需的 CONTEXT.md 格式
- **所有 PRD 内容视为锁定决策**：体现了对用户输入的尊重 — 用户提供的就是"法律"
- **强制提取规范引用**：确保下游 agent 能看到所有相关设计文档，不遗漏架构约束
- **完全绕过 discuss-phase**：当用户已有明确 PRD 时，不需要再讨论 — 直接规划

---

#### 段落 9: process - 步骤 4 Load CONTEXT.md

**原文:**
（第 198-246 行）

**翻译:**
如果使用了 PRD 快速路径：跳过此步骤（CONTEXT.md 已在步骤 3.5 创建）。

检查 `context_path`。如果不为 null：显示使用路径。

如果为 null（没有 CONTEXT.md）：
- 读取 discuss 模式配置
- 如果 TEXT_MODE：显示纯文本选项
- 否则使用 AskUserQuestion：
  - "Continue without context" — 仅使用研究+需求进行规划
  - "Gather context (assumptions mode)" 或 "Run discuss-phase first" — 先捕获设计决策

如果选择 "Run discuss-phase first"：**重要**：不要作为嵌套 Skill/Task 调用 — AskUserQuestion 在嵌套子上下文中无法正常工作。而是显示命令并退出，让用户作为顶层命令运行。

**要点:**
- **Context 是可选但推荐的**：允许无 CONTEXT.md 继续，但明确告知用户设计偏好不会被包含
- **嵌套调用限制**：明确指出 AskUserQuestion 在嵌套 Task 中不工作（#1009），这是 Claude Code 运行时限制
- **不自动调用 discuss-phase**：工作流在此处退出，让用户主动运行 — 保持用户控制权

---

#### 段落 10: process - 步骤 4.5 Check AI-SPEC

**原文:**
（第 248-286 行）

**翻译:**
如果 `ai_integration_phase_enabled` 为 false 或提供了 `--skip-ai-spec`：跳过。

检查阶段目录中是否有 `*-AI-SPEC.md`。如果没有：检查阶段目标是否包含 AI 关键词（agent、llm、rag、chatbot、embedding 等）。

如果检测到 AI 关键词且没有 AI-SPEC：提示用户考虑运行 `/gsd-ai-integration-phase {N}`。

使用 AskUserQuestion：
- "Continue — plan without AI-SPEC"
- "Stop — I'll run /gsd-ai-integration-phase {N} first"

如果 AI-SPEC 存在：提取框架信息传递给规划者。

**要点:**
- **AI 项目特殊处理**：识别涉及 AI 系统开发的阶段，强制要求 AI 设计规范
- **非阻塞但明确建议**：用户可以选择继续，但系统明确告知风险
- **关键词检测**：通过 grep 检测阶段目标中的 AI 相关术语，自动触发检查

---

#### 段落 11: process - 步骤 5 Handle Research（处理研究）

**原文:**
（第 288-379 行）

**翻译:**
如果 `--gaps` 或 `--skip-research` 或 `--reviews`：跳过。

如果 `has_research` 为 true 且没有 `--research`：使用现有研究，跳到步骤 6。

如果 RESEARCH.md 缺失或有 `--research`：
- 如果没有显式标志且不是 `--auto`：询问用户是否研究
  - TEXT_MODE：显示纯文本选项
  - 否则 AskUserQuestion："Research first (Recommended)" vs "Skip research"
- 如果用户选择 "Skip research"：跳到步骤 6
- 如果 `--auto` 且 `research_enabled` 为 false：静默跳过

显示 "RESEARCHING PHASE" 横幅。

生成研究提示并生成 gsd-phase-researcher：
- 目标：研究如何实现该阶段，回答"要做好规划，我需要知道什么？"
- 读取文件：context_path、requirements_path、state_path
- 附加 agent 技能配置
- 输出到 `{phase_dir}/{phase_num}-RESEARCH.md`

**要点:**
- **研究是默认行为**：除非用户明确跳过或已有研究，否则默认进行研究
- **上下文化建议**：根据阶段类型给出建议（新功能/不熟悉的集成 → 研究；bug 修复/简单重构 → 跳过）
- **自动化兼容**：`--auto` 模式下尊重 `research_enabled` 配置，静默决策不中断流水线
- **问题驱动**：研究目标不是"了解一切"，而是"为了规划好，我需要知道什么" — 聚焦且实用

---

#### 段落 12: process - 步骤 5.5 Create Validation Strategy

**原文:**
（第 386-414 行）

**翻译:**
如果 `nyquist_validation_enabled` 为 false 或 `research_enabled` 为 false：跳过。

如果研究未启用且 Nyquist 启用：警告"Nyquist 验证启用但研究禁用 — 没有 RESEARCH.md 无法创建 VALIDATION.md"。

检查 RESEARCH.md 中是否有 "## Validation Architecture"。

如果有：
1. 读取模板 `templates/VALIDATION.md`
2. 写入 `${PHASE_DIR}/${PADDED_PHASE}-VALIDATION.md`
3. 验证文件创建成功
4. 如果失败：停止，不继续到步骤 6
5. 如果 `commit_docs`：提交

如果没有：警告并继续 — 计划可能无法通过 Dimension 8。

**要点:**
- **Nyquist 验证框架**：一个 8 维度的验证框架（Dimension 8 是验证架构）
- **依赖研究的验证策略**：VALIDATION.md 基于 RESEARCH.md 中的验证架构生成
- **硬失败（Hard Fail）**：如果 VALIDATION.md 创建失败，工作流停止 — 不继续到规划阶段

---

#### 段落 13: process - 步骤 5.55 Security Threat Model Gate

**原文:**
（第 416-440 行）

**翻译:**
如果 `workflow.security_enforcement` 显式为 `false`：跳过。不存在（absent）= 启用。

读取安全配置：`security_enforcement`、`security_asvs_level`（默认 L1）、`security_block_on`（默认 high）。

如果启用：显示"SECURITY THREAT MODEL REQUIRED"横幅，告知每个 PLAN.md 必须包含 `<threat_model>` 块，拦截严重级别威胁。

继续到步骤 5.6。安全配置在步骤 8 传递给规划者。

**要点:**
- **安全默认启用**：不配置 = 启用，符合"安全默认"最佳实践
- **ASVS 分级**：支持 OWASP ASVS L1/L2/L3 级别
- **威胁拦截配置**：可配置拦截严重级别（high/medium/low）
- **下游传递**：安全要求不是由工作流检查，而是传递给规划者强制执行

---

#### 段落 14: process - 步骤 5.6 UI Design Contract Gate

**原文:**
（第 442-506 行）

**翻译:**
如果 `workflow.ui_phase` 和 `workflow.ui_safety_gate` 都显式为 `false`：跳过。键不存在 = 启用。

检查阶段是否有前端指标（UI、interface、frontend、component 等关键词）。

如果有前端指标：
- 检查是否存在 UI-SPEC.md
- 如果存在：设置路径，继续
- 如果缺失且 `--skip-ui`：静默跳过
- 如果缺失且 `UI_GATE_CFG` 为 true：
  - 检查是否在 auto-chain 中：
    - 如果是：自动运行 `gsd-ui-phase` 生成 UI-SPEC
    - 如果不是：显示警告并**退出工作流**，建议运行 `/gsd-ui-phase {N}`

如果没有前端指标：静默跳过。

**要点:**
- **UI 安全门控**：前端阶段必须有 UI 设计契约，防止"先写代码后想设计"的反模式
- **自动链中的特殊处理**：在 `--chain` 或 `--auto` 流水线中，自动调用 UI 阶段而不中断流水线
- **手动模式下的硬退出**：如果用户手动运行且缺少 UI-SPEC，工作流停止 — 强制用户先完成设计

---

#### 段落 15: process - 步骤 5.7 Schema Push Detection Gate

**原文:**
（第 509-568 行）

**翻译:**
检测阶段范围中的 schema 相关文件，并注入强制的 `[BLOCKING]` schema push 任务到计划中。

扫描阶段目标、CONTEXT.md、RESEARCH.md 中匹配 ORM 模式的文件路径：
- Payload CMS: `src/collections/**/*.ts`
- Prisma: `prisma/schema.prisma`
- Drizzle: `drizzle/schema.ts`
- Supabase: `supabase/migrations/*.sql`
- TypeORM: `src/entities/**/*.ts`

如果检测到 schema 相关文件：
- 设置 `SCHEMA_PUSH_REQUIRED=true`
- 确定对应 ORM 的 push 命令和非 TTY 变通方案
- 向规划者提示中注入约束：必须包含 `[BLOCKING]` 任务，在 schema 文件修改后、验证前运行数据库 schema push
- 显示检测信息

如果没有检测到：静默跳过。

**要点:**
- **假阳性预防**：build/type 检查通过可能是因为 TypeScript 类型来自配置而非实时数据库 — 这是一个常见的验证陷阱
- **ORM 感知**：支持 5 种主流 ORM，每种有特定的 push 命令和变通方案
- **[BLOCKING] 强制注入**：不是建议，而是强制要求 — 规划者必须在计划中包含此任务
- **自动化与手动的区分**：如果 push 需要无法抑制的交互式提示，标记为 `autonomous: false`

---

#### 段落 16: process - 步骤 6 Check Existing Plans

**原文:**
（第 571-579 行）

**翻译:**
列出阶段目录中的 `*-PLAN.md` 文件。

如果存在且 `--reviews`：跳过提示 — 直接重新规划。
如果存在且没有 `--reviews`：提供选项：1) 添加更多计划，2) 查看现有计划，3) 从头重新规划。

**要点:**
- **增量规划支持**：允许在现有计划基础上添加，而非总是从头开始
- **`--reviews` 模式特殊处理**：当有跨 AI 审查反馈时，直接进入重新规划流程

---

#### 段落 17: process - 步骤 7 Use Context Paths from INIT

**原文:**
（第 581-596 行）

**翻译:**
从 INIT JSON 提取所有上下文文件路径：
state_path、roadmap_path、requirements_path、research_path、verification_path、uat_path、context_path、reviews_path、patterns_path。

使用辅助函数 `_gsd_field` 从 JSON 中提取字段值。

**要点:**
- **路径统一来源**：所有文件路径来自 init 调用，避免在工作流中硬编码路径逻辑
- **空值处理**：如果文件不存在，路径为 null，下游代码需要处理这种情况

---

#### 段落 18: process - 步骤 7.5 Verify Nyquist Artifacts

**原文:**
（第 598-620 行）

**翻译:**
如果 `nyquist_validation_enabled` 为 false 或 `research_enabled` 为 false：跳过。

如果研究未启用且 Nyquist 仍启用：询问用户：
1. 重新运行：`/gsd-plan-phase {PHASE} --research`
2. 禁用 Nyquist
3. 继续（计划将无法通过 Dimension 8）

检查 VALIDATION.md 是否存在。如果缺失且 Nyquist 仍启用/适用：询问用户。

**要点:**
- **Nyquist 验证的严格性**：研究是 Nyquist 验证的前提，没有研究就没有验证策略
- **用户选择权**：提供重新运行、禁用或继续三种选项，不强制单一行为

---

#### 段落 19: process - 步骤 7.8 Spawn gsd-pattern-mapper Agent

**原文:**
（第 622-678 行）

**翻译:**
如果 `workflow.pattern_mapper` 显式为 `false`：跳过。也跳过如果没有 CONTEXT.md 和 RESEARCH.md。

如果 PATTERNS.md 已存在：跳过（使用现有）。

显示 "PATTERN MAPPING" 横幅。

生成模式映射提示：
- 从 CONTEXT.md 和 RESEARCH.md 提取要创建/修改的文件列表
- 对每个文件：按角色和数据流分类，在代码库中找到最接近的现有类比
- 提取具体代码片段
- 生成 PATTERNS.md

生成 gsd-pattern-mapper，使用 researcher_model。

**要点:**
- **代码库模式复用**：避免重新发明轮子，利用现有代码模式指导新实现
- **类比学习**：找到"最接近的现有类比" — 这是基于案例的推理（Case-Based Reasoning）
- **非阻塞**：模式映射失败时不停止工作流，只是警告并继续

---

#### 段落 20: process - 步骤 8 Spawn gsd-planner Agent

**原文:**
（第 680-793 行）

**翻译:**
显示 "PLANNING PHASE" 横幅。

生成规划者提示，包含：
- **规划上下文**：阶段编号、模式（standard/gap_closure/reviews）
- **files_to_read**：所有上下文文件路径（STATE、ROADMAP、REQUIREMENTS、CONTEXT、RESEARCH、PATTERNS、VERIFICATION、UAT、REVIEWS、UI_SPEC）
- **跨阶段上下文**（1M 模型增强）：加载最近 3 个阶段的 CONTEXT.md 和 SUMMARY.md，以及显式依赖阶段
- **Agent 技能配置**：`${AGENT_SKILLS_PLANNER}`
- **阶段需求 ID**：每个 ID 必须出现在某个计划的 `requirements` 字段中
- **TDD 模式**：如果启用，应用 TDD 启发式规则
- **下游消费者信息**：说明输出被 `/gsd-execute-phase` 消费，需要特定格式
- **深度工作规则（MANDATORY）**：
  - 每个任务必须有 `<read_first>` — 执行者必须先读取的文件
  - 每个任务必须有 `<acceptance_criteria>` — 可用 grep/命令验证的条件
  - 每个 `<action>` 必须包含具体值，不能是"对齐 X 和 Y"这类模糊指令
- **质量门控**：检查清单确保 PLAN.md 文件、有效 frontmatter、具体任务、依赖关系、Wave 分配等

生成 gsd-planner，使用 planner_model。

**要点:**
- **上下文丰富度**：规划者接收几乎所有可用上下文 — 这是"给承包商的蓝图"而非"给我建个房子"
- **深度工作规则强制**：三个必填字段（read_first、acceptance_criteria、具体 action）解决 executor agent 常见的"浅层执行"问题
- **大上下文优化**：1M 上下文模型加载更多历史阶段，保持跨阶段一致性
- **需求追溯性**：每个需求 ID 必须被某个计划覆盖，确保无遗漏

---

#### 段落 21: process - 步骤 9 Handle Planner Return

**原文:**
（第 795-802 行）

**翻译:**
处理规划者返回的不同状态：
- `## PLANNING COMPLETE`：显示计划数量，如果 `--skip-verify` 或检查器禁用：跳到步骤 13，否则：步骤 10
- `## PHASE SPLIT RECOMMENDED`：阶段超过上下文预算，在步骤 9b 处理
- `## ⚠ Source Audit: Unplanned Items Found`：多源覆盖审计发现未规划项，在步骤 9c 处理
- `## CHECKPOINT REACHED`：呈现给用户，获取响应，生成续集（步骤 12）
- `## PLANNING INCONCLUSIVE`：显示尝试，提供选项

**要点:**
- **结构化返回码**：规划者不返回自由文本，而是使用特定标题的状态码
- **三种特殊状态**：阶段拆分建议、源代码审计缺口、检查点 — 都需要特殊处理

---

#### 段落 22: process - 步骤 9b Handle Phase Split Recommendation

**原文:**
（第 804-834 行）

**翻译:**
当规划者返回 `## PHASE SPLIT RECOMMENDED` 时：

提取：提议的子阶段、每个子阶段的源项目、拆分的必要原因。

呈现给用户：
- **选项 1：拆分为子阶段** — 如 Phase Xa、Xb
- **选项 2：继续** — 质量可能下降
- **选项 3：优先排序** — 用户选择现在实现哪些，其余作为后续阶段

使用 AskUserQuestion 呈现 3 个选项。

如果 "Split"：使用 `/gsd-insert-phase` 创建子阶段，然后重新规划每个。
如果 "Proceed"：返回规划者，指示尝试所有项目。
如果 "Prioritize"：使用 AskUserQuestion（multiSelect）让用户选择，为每个子阶段创建 CONTEXT.md。

**要点:**
- **上下文预算管理**：当阶段太大时，不强行压缩质量，而是建议拆分
- **用户主导决策**：3 种明确选项，用户决定如何处理范围
- **自动化子阶段创建**：选择拆分后，使用 `/gsd-insert-phase` 自动创建子阶段

---

#### 段落 23: process - 步骤 9c Handle Source Audit Gaps

**原文:**
（第 836-862 行）

**翻译:**
当规划者返回 `## ⚠ Source Audit: Unplanned Items Found` 时：

提取：每个未规划项及其源工件和章节、规划者建议的选项。

对每个未规划项呈现给用户：
- **选项 1：添加计划覆盖此项**（推荐）
- **选项 2：拆分阶段 — 将相关项移到子阶段
- **选项 3：推迟 — 添加到待办事项（开发者确认这是故意的）**

如果 "Add plan"：返回规划者（步骤 8），指示添加覆盖缺失项的计划。
如果 "Split"：使用 `/gsd-insert-phase`。
如果 "Defer"：记录到 CONTEXT.md `## Deferred Ideas`，继续到步骤 10。

**要点:**
- **覆盖审计强制**：规划者必须审计所有 4 种源类型（GOAL、REQ、RESEARCH、CONTEXT），不能静默遗漏
- **逐项处理**：每个缺口单独呈现，用户可以逐个决定
- **审计追踪**：推迟的项记录到 CONTEXT.md，有明确的审计线索

---

#### 段落 24: process - 步骤 10 Spawn gsd-plan-checker Agent

**原文:**
（第 864-910 行）

**翻译:**
显示 "VERIFYING PLANS" 横幅。

生成检查者提示：
- **验证上下文**：阶段编号、阶段目标
- **files_to_read**：所有 PLAN.md、ROADMAP、REQUIREMENTS、CONTEXT、RESEARCH
- **Agent 技能配置**：`${AGENT_SKILLS_CHECKER}`
- **阶段需求 ID**：必须全部覆盖
- **期望输出**：`## VERIFICATION PASSED` 或 `## ISSUES FOUND`

生成 gsd-plan-checker，使用 checker_model。

**要点:**
- **独立验证**：检查者是独立 agent，不是规划者的自检 — 避免确认偏误
- **完整上下文**：检查者也能访问所有源文件，验证计划是否忠实于需求

---

#### 段落 25: process - 步骤 11 Handle Checker Return

**原文:**
（第 912-935 行）

**翻译:**
- `## VERIFICATION PASSED`：显示确认，继续到步骤 13
- `## ISSUES FOUND`：显示问题，检查迭代次数，继续到步骤 12

**条件性思考伙伴**：如果 `features.thinking_partner` 启用，扫描检查者的问题中的架构权衡关键词（architecture、approach、strategy、pattern、vs、alternative）。如果找到：
- 提供简要分析（选项 A、选项 B、推荐）
- 询问是否应用到修订

**要点:**
- **思考伙伴功能**：可选的架构权衡分析，帮助用户理解复杂决策
- **条件触发**：仅当问题涉及架构权衡时才触发，不干扰简单问题

---

#### 段落 26: process - 步骤 12 Revision Loop (Max 3 Iterations)

**原文:**
（第 937-1000 行）

**翻译:**
跟踪 `iteration_count`（初始计划 + 检查后从 1 开始）。
跟踪 `prev_issue_count`（循环开始前初始化为 Infinity）。
跟踪 `stall_reentry_count`（从 0 开始；每次 "Adjust approach" 重新进入步骤 8 时递增）。

如果 `iteration_count < 3`：
- 解析检查者返回中的问题计数（BLOCKER + WARNING）
- 如果检查者返回中没有 YAML 问题块（即计划通过无问题）：`issue_count` = 0，跳过停滞检查
- 显示：`Revision iteration {N}/3 -- {blocker_count} blockers, {warning_count} warnings`

**停滞检测**：如果 `issue_count >= prev_issue_count`：
- 显示：修订循环停滞 — 问题计数未减少
- 如果 `stall_reentry_count < 2`：询问用户"Issues remain after {N} revision attempts with no progress. Proceed with current output?" 选项："Proceed anyway" | "Adjust approach"
  - "Proceed anyway"：接受当前计划，继续到步骤 13
  - "Adjust approach"：递增 `stall_reentry_count`，开放自由讨论，然后重新进入步骤 8（完全重新规划）
- 如果 `stall_reentry_count >= 2`：显示停滞持续，列出剩余问题，建议手动解决或运行 `/gsd-debug`

设置 `prev_issue_count = issue_count`。

生成修订提示，调用规划者进行修订。
规划者返回后 -> 再次生成检查者（步骤 10），递增 iteration_count。

如果 `iteration_count >= 3`：显示最大迭代次数已达到，提供选项：1) 强制继续，2) 提供指导并重试，3) 放弃。

**要点:**
- **三层防停滞机制**：
  1. 问题计数检测（issue_count >= prev_issue_count）
  2. 重新规划计数限制（stall_reentry_count < 2）
  3. 最大迭代次数（3 次）
- **用户参与决策**：停滞时不自动决定，而是询问用户
- **"Adjust approach" 重置循环**：允许完全重新规划，给用户一次"重新开始"的机会

---

#### 段落 27: process - 步骤 12.5 Plan Bounce (Optional External Refinement)

**原文:**
（第 1010-1079 行）

**翻译:**
如果 `--skip-bounce`、`--gaps` 或 bounce 未激活：跳过。

激活条件：`--bounce` 标志存在或 `workflow.plan_bounce` 配置为 true。`--skip-bounce` 总是获胜（即使配置启用也禁用）。`--gaps` 也禁用 bounce。

先决条件：`workflow.plan_bounce_script` 必须设置为有效脚本路径。如果激活但未配置：显示警告并跳过。

读取 pass 次数（默认 2）和脚本路径。

对每个 PLAN.md 文件：
1. 备份到 `*-PLAN.pre-bounce.md`
2. 调用 bounce 脚本
3. 验证 bounce 后的 YAML frontmatter 完整性
4. 处理脚本失败：从备份恢复

所有计划 bounce 后：
5. 在 bounce 后的计划上重新运行 plan checker
6. 提交幸存下来的 bounce 计划

清理：删除所有备份文件。

**要点:**
- **外部精化机制**：允许用户配置自定义脚本对计划进行后处理（如格式化、增强、翻译）
- **安全回滚**：每个计划先备份，失败时自动恢复 — 防止外部脚本破坏计划
- **双重验证**：bounce 后重新运行 checker，确保精化不会降低质量

---

#### 段落 28: process - 步骤 13 Requirements Coverage Gate

**原文:**
（第 1081-1130 行）

**翻译:**
计划通过检查者后（或检查者被跳过），验证所有阶段需求是否被至少一个计划覆盖。

如果 `phase_req_ids` 为 null 或 TBD：跳过。

步骤 1：从计划 frontmatter 收集所有需求 ID
步骤 2：与 ROADMAP 中的阶段需求对比
步骤 3：检查 CONTEXT.md 功能是否在计划目标中提到
步骤 4：报告
- 全部覆盖：显示确认，继续到步骤 14
- 有缺口：显示缺口详情，提供选项：1) 重新规划，2) 移到下一阶段，3) 接受覆盖缺口

**要点:**
- **最终覆盖率检查**：这是最后一道防线，确保没有需求被遗漏
- **双重检查**：不仅检查需求 ID，还检查 CONTEXT.md 中描述的功能是否在计划目标中体现
- **明确的缺口呈现**：表格形式展示未覆盖的需求和未提及的功能

---

#### 段落 29: process - 步骤 13b Record Planning Completion in STATE.md

**原文:**
（第 1132-1141 行）

**翻译:**
计划通过所有门控后，记录规划完成到 STATE.md：
```bash
node gsd-tools state planned-phase --phase "${PHASE_NUMBER}" --name "${PHASE_NAME}" --plans "${PLAN_COUNT}"
```

更新 STATUS 为 "Ready to execute"，设置正确计划数，记录时间戳。

**要点:**
- **状态机更新**：STATE.md 作为项目状态机，记录每个阶段的当前状态
- **自动化状态转换**：从 "Planned" 到 "Ready to execute"，无需手动更新

---

#### 段落 30: process - 步骤 14 Present Final Status

**原文:**
（第 1143 行）

**翻译:**
根据标志/配置路由到 `<offer_next>` 或 `auto_advance`。

**要点:**
- **路由决策点**：根据用户配置决定下一步行为 — 手动模式下显示选项，自动模式下自动前进

---

#### 段落 31: process - 步骤 15 Auto-Advance Check

**原文:**
（第 1147-1208 行）

**翻译:**
检查自动前进触发条件：
1. 解析 `--auto` 和 `--chain` 标志
2. **同步链标志与意图**：如果用户手动调用（无 `--auto` 和 `--chain`），清除之前的临时链标志
3. 读取链标志和用户偏好

如果 `--auto` 或 `--chain` 存在且 `AUTO_CHAIN` 不为 true：持久化链标志

如果 `--auto` 或 `--chain` 或 `AUTO_CHAIN` 或 `AUTO_CFG` 为 true：
- 显示 "AUTO-ADVANCING TO EXECUTE" 横幅
- 使用 Skill 工具启动 execute-phase（避免嵌套 Task 会话导致运行时冻结）
- 添加 `--no-transition` 保持自动前进链扁平

处理 execute-phase 返回：
- PHASE COMPLETE → 显示完成摘要，提示下一个阶段
- GAPS FOUND / VERIFICATION FAILED → 显示结果，停止链

如果未启用自动：路由到 `<offer_next>`。

**要点:**
- **扁平链设计**：使用 `--no-transition` 和 Skill 工具（而非 Task）避免深层 agent 嵌套，这是 Claude Code 运行时限制（深层嵌套会导致冻结）
- **标志与配置的优先级**：`--auto`/`--chain` 标志 > `AUTO_CHAIN` 临时状态 > `AUTO_CFG` 持久配置
- **清理临时状态**：手动调用时清除 `_auto_chain_active`，防止残留状态影响后续操作
- **错误时停止链**：执行失败时不自动继续，让用户审查

---

#### 段落 32: offer_next

**原文:**
（第 1212-1248 行）

**翻译:**
直接输出 markdown（不作为代码块）：
- 显示 "PHASE {X} PLANNED ✓" 横幅
- 阶段信息和计划统计
- Wave 结构表格
- 研究和验证状态
- **Next Up**：提示执行阶段命令 `/gsd-execute-phase {X}`
- **Also available**：查看计划、重新研究、同行审查、基于反馈重新规划等选项

**要点:**
- **清晰的下一步指引**：默认下一步是执行，但不自动执行 — 给用户确认权
- **`/clear` 建议**：提示用户在执行前清除上下文窗口，为执行阶段释放空间
- **多种后续选项**：不只提供执行，还提供审查、研究、重新规划等替代路径

---

#### 段落 33: windows_troubleshooting

**原文:**
（第 1250-1272 行）

**翻译:**
**Windows 用户**：如果 plan-phase 在 agent 生成期间冻结（Windows 上常见，由于 MCP 服务器的 stdio 死锁）：
1. 强制终止：关闭终端（Ctrl+C 可能无效）
2. 清理孤儿进程：PowerShell 命令杀死过时的 node 进程
3. 清理过时任务目录：删除 `~\.claude\tasks\*` 
4. 减少 MCP 服务器数量
5. 重试：重启 Claude Code 重新运行

如果持续冻结，尝试 `--skip-research` 将 agent 链从 3 减少到 2 个。

**要点:**
- **平台特定问题**：Windows 上 MCP 服务器的 stdio 死锁是已知问题（anthropics/claude-code#28126）
- **应急恢复步骤**：提供完整的恢复流程，包括进程清理和目录清理
- **降级方案**：`--skip-research` 减少 agent 数量作为临时规避措施

---

#### 段落 34: success_criteria

**原文:**
（第 1274-1288 行）

**翻译:**
- [ ] .planning/ 目录已验证
- [ ] 阶段已对照路线图验证
- [ ] 阶段目录已按需创建
- [ ] CONTEXT.md 早期加载（步骤 4）并传递给所有 agent
- [ ] 研究完成（除非 --skip-research 或 --gaps 或已存在）
- [ ] gsd-phase-researcher 已生成并带有 CONTEXT.md
- [ ] 现有计划已检查
- [ ] gsd-planner 已生成并带有 CONTEXT.md + RESEARCH.md
- [ ] 计划已创建（PLANNING COMPLETE 或 CHECKPOINT 已处理）
- [ ] gsd-plan-checker 已生成并带有 CONTEXT.md
- [ ] 验证通过或用户覆盖或最大迭代次数且用户决定
- [ ] 用户在 agent 生成之间看到状态
- [ ] 用户知道下一步

**要点:**
- **14 项检查清单**：覆盖从目录验证到用户沟通的完整流程
- **Context 传递强调**：多次提到 CONTEXT.md 必须传递给所有 agent — 这是避免"丢失用户决策"的关键
- **用户可见性**：要求用户在 agent 生成之间看到状态 — 不透明的工作流会降低信任

---

### commands/gsd/plan-phase.md

#### 段落 35: Frontmatter

**原文:**
```yaml
---
name: gsd:plan-phase
description: Create detailed phase plan (PLAN.md) with verification loop
argument-hint: "[phase] [--auto] [--research] [--skip-research] [--gaps] [--skip-verify] [--prd <file>] [--reviews] [--text] [--tdd]"
agent: gsd-planner
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - WebFetch
  - mcp__context7__*
---
```

**翻译:**
名称：gsd:plan-phase
描述：创建详细的阶段计划（PLAN.md）并带验证循环
参数提示：[阶段] [--auto] [--research] [--skip-research] [--gaps] [--skip-verify] [--prd <文件>] [--reviews] [--text] [--tdd]
Agent：gsd-planner
允许工具：Read、Write、Bash、Glob、Grep、Task、AskUserQuestion、WebFetch、mcp__context7__*

**要点:**
- **命令即接口**：这是用户直接交互的命令定义，frontmatter 描述了 CLI 接口
- **11 个命令行标志**：提供精细的流程控制
- **Agent 声明**：指定使用 gsd-planner 作为执行 agent，但工作流中还会生成其他 agent（researcher、checker）
- **工具权限**：明确列出允许的工具，遵循最小权限原则

---

#### 段落 36: objective

**原文:**
```xml
<objective>
Create executable phase prompts (PLAN.md files) for a roadmap phase with integrated research and verification.

**Default flow:** Research (if needed) → Plan → Verify → Done

**Orchestrator role:** Parse arguments, validate phase, research domain (unless skipped), spawn gsd-planner, verify with gsd-plan-checker, iterate until pass or max iterations, present results.
</objective>
```

**翻译:**
为路线图阶段创建可执行的阶段提示（PLAN.md 文件），集成研究和验证。

默认流程：研究（如需要）→ 规划 → 验证 → 完成

编排器角色：解析参数、验证阶段、研究领域（除非跳过）、生成 gsd-planner、用 gsd-plan-checker 验证、迭代直到通过或最大迭代次数、呈现结果。

**要点:**
- **编排器（Orchestrator）模式**：这个命令本身不直接执行规划，而是协调多个子 agent 完成工作
- **默认流程 vs 编排器角色**：前者描述数据流，后者描述控制流 — 合起来就是完整的流程定义

---

#### 段落 37: execution_context

**原文:**
```xml
<execution_context>
@~/.claude/get-shit-done/workflows/plan-phase.md
@~/.claude/get-shit-done/references/ui-brand.md
</execution_context>
```

**翻译:**
执行上下文：
- plan-phase 工作流文件
- UI 品牌参考

**要点:**
- **分离命令定义和工作流逻辑**：命令文件是"接口"，工作流文件是"实现"
- **UI 品牌参考**：即使是命令定义也引用 UI 品牌规范，确保输出一致性

---

#### 段落 38: IMPORTANT 约束

**原文:**
```xml
<IMPORTANT>
    - 必须阅读关键文件的内容，不能只做 `ls` 和 `find`
    - 每个架构描述必须包含具体的文件路径（用反引号包裹）
    - 至少阅读 3-5 个关键文件的完整内容
</IMPORTANT>
```

**翻译:**
重要约束：
- 必须阅读关键文件的内容，不能只做 `ls` 和 `find`
- 每个架构描述必须包含具体的文件路径（用反引号包裹）
- 至少阅读 3-5 个关键文件的完整内容

**要点:**
- **深度阅读要求**：禁止浅层目录扫描，强制要求阅读文件内容 — 这是保证规划质量的基础
- **具体路径要求**：每个描述必须包含 `path/to/file` 格式的具体路径，不能模糊表述

---

### agents/gsd-planner.md

#### 段落 39: Frontmatter and Role

**原文:**
```yaml
---
name: gsd-planner
description: Creates executable phase plans with task breakdown, dependency analysis, and goal-backward verification. Spawned by /gsd-plan-phase orchestrator.
tools: Read, Write, Bash, Glob, Grep, WebFetch, mcp__context7__*
color: green
---

<role>
You are a GSD planner. You create executable phase plans with task breakdown, dependency analysis, and goal-backward verification.

Spawned by:
- `/gsd-plan-phase` orchestrator (standard phase planning)
- `/gsd-plan-phase --gaps` orchestrator (gap closure from verification failures)
- `/gsd-plan-phase` in revision mode (updating plans based on checker feedback)
- `/gsd-plan-phase --reviews` orchestrator (replanning with cross-AI review feedback)

Your job: Produce PLAN.md files that Claude executors can implement without interpretation. Plans are prompts, not documents that become prompts.
</role>
```

**翻译:**
名称：gsd-planner
描述：创建可执行的阶段计划，包含任务拆分、依赖分析和目标逆向验证。由 /gsd-plan-phase 编排器生成。

角色：
你是 GSD 规划者。你创建可执行的阶段计划，包含任务拆分、依赖分析和目标逆向验证。

由以下生成：
- 标准阶段规划
- 差距修复模式
- 修订模式（基于检查者反馈更新计划）
- 基于跨 AI 审查反馈重新规划

你的工作：生成 Claude 执行者无需解释即可实现的 PLAN.md 文件。计划是提示，不是变成提示的文档。

**要点:**
- **4 种生成模式**：标准、差距修复、修订、审查反馈 —  planner 需要适应不同上下文
- **关键区分**："Plans are prompts, not documents that become prompts" — 计划直接就是提示，不需要二次转换
- **绿色标识**：color: green 可能用于日志或 UI 中的颜色编码

---

#### 段落 40: Core Responsibilities

**原文:**
```xml
**Core responsibilities:**
- **FIRST: Parse and honor user decisions from CONTEXT.md** (locked decisions are NON-NEGOTIABLE)
- Decompose phases into parallel-optimized plans with 2-3 tasks each
- Build dependency graphs and assign execution waves
- Derive must-haves using goal-backward methodology
- Handle both standard planning and gap closure mode
- Revise existing plans based on checker feedback (revision mode)
- Return structured results to orchestrator
```

**翻译:**
核心职责：
- **首先：解析并遵守 CONTEXT.md 中的用户决策**（锁定决策不可协商）
- 将阶段分解为并行优化的计划，每个计划 2-3 个任务
- 构建依赖图并分配执行 wave
- 使用目标逆向方法论推导 must-haves
- 处理标准规划和差距修复模式
- 基于检查者反馈修订现有计划（修订模式）
- 向编排器返回结构化结果

**要点:**
- **用户决策优先**："FIRST" 大写强调，锁定决策是不可协商的硬约束
- **并行优化**：目标不是生成顺序任务列表，而是最大化并行性
- **目标逆向**：从目标倒推需要做什么，而非从现状正推能做什么

---

#### 段落 41: Context Fidelity

**原文:**
（第 63-92 行，上下文保真度规则）

**翻译:**
在创建任何任务之前，验证：

1. **锁定决策（来自 `## Decisions`）** — 必须完全按指定实现
   - 如果用户说 "use library X" → 任务必须使用 library X，不能用替代方案
   - 如果用户说 "card layout" → 任务必须实现卡片，不能用表格
   - 如果用户说 "no animations" → 任务不能包含动画
   - 在任务 action 中引用决策 ID（D-01, D-02 等）以提供可追溯性

2. **推迟想法（来自 `## Deferred Ideas`）** — 不能出现在计划中
   - 如果用户推迟了 "search functionality" → 计划中不能有搜索任务
   - 如果用户推迟了 "dark mode" → 计划中不能有暗黑模式任务

3. **Claude 的自由裁量（来自 `## Claude's Discretion`）** — 使用你的判断
   - 做出合理选择并在任务 action 中记录

自检：
- [ ] 每个锁定决策（D-01, D-02 等）都有实现它的任务
- [ ] 任务 action 引用它们实现的决策 ID（如 "per D-03"）
- [ ] 没有任务实现推迟的想法
- [ ] 自由裁量区域得到合理处理

如果存在冲突（如研究建议 library Y 但用户锁定 library X）：
- 遵守用户的锁定决策
- 在任务 action 中注明："Using X per user decision (research suggested Y)"

**要点:**
- **三层决策分类**：锁定（必须做）、推迟（必须不做）、自由裁量（可做可不做）— 这是需求管理的核心模式
- **可追溯性要求**：每个任务必须引用决策 ID，实现"需求 → 任务"的追踪
- **冲突解决规则**：用户决策优先于研究建议 — 尊重用户主权

---

#### 段落 42: Scope Reduction Prohibition

**原文:**
（第 94-125 行，范围缩减禁止规则）

**翻译:**
**禁止的语言/模式：**
- "v1", "v2", "simplified version", "static for now", "hardcoded for now"
- "future enhancement", "placeholder", "basic version", "minimal implementation"
- "will be wired later", "dynamic in future phase", "skip for now"
- 任何将源工件决策缩减到低于指定范围的语言

**规则：**如果 D-XX 说 "display cost calculated from billing table in impulses"，计划必须交付从 billing table 计算出的 impulses 成本。不能是 "static label /min" 作为 "v1"。

**当计划集无法覆盖所有源项目时：**

不要静默省略功能。而是：
1. **创建多源覆盖审计**（见下文）覆盖所有四种工件类型
2. **如果任何项目无法放入**计划预算（上下文成本超过容量）：
   - 向编排器返回 `## PHASE SPLIT RECOMMENDED`
   - 提议如何拆分：哪些项目组形成自然子阶段
3. 编排器将拆分呈现给用户批准
4. 批准后，在预算内规划每个子阶段

**多源覆盖审计（每个计划集强制）**
审计所有四种源类型：GOAL（ROADMAP 阶段目标）、REQ（REQUIREMENTS.md 的 phase_req_ids）、RESEARCH（RESEARCH.md 功能/约束）、CONTEXT（CONTEXT.md 的 D-XX 决策）。

每个项目必须被计划覆盖。如果任何项目缺失 → 向编排器返回 `## ⚠ Source Audit: Unplanned Items Found`。

**要点:**
- **反简化文化**：明确禁止使用"先简单做后面再改"的语言 — 这是对质量滑坡的预防
- **四种源类型审计**：目标、需求、研究、上下文 — 确保不遗漏任何输入
- **不静默省略**：不能偷偷删掉做不完的功能，必须明确建议拆分
- **拆分推荐**：当范围太大时，不是砍功能，而是建议拆分子阶段

---

#### 段落 43: Planner Authority Limits

**原文:**
（第 127-140 行，规划者权限限制）

**翻译:**
规划者无权判断功能"太难"、因看似有挑战性而省略功能，或使用"复杂/困难/非平凡"来证明范围缩减。

**只有三个合法的分拆或标记原因：**
1. **上下文成本**：实现将消耗单个 agent 上下文窗口的 >50%
2. **信息缺失**：任何源工件中都不存在所需数据
3. **依赖冲突**：功能必须等到另一个阶段交付后才能构建

如果一个功能没有这三个约束，就必须规划。句号。

**要点:**
- **禁止以难度为由缩减范围**：规划者不能替用户决定"这个太难了做不完" — 这是用户或架构师的决策
- **三个合法原因**：上下文限制（客观）、信息缺失（可解决）、依赖冲突（时序问题）
- **句号（Period.）**：强调没有例外 — 难度不是省略功能的理由

---

#### 段落 44: Philosophy

**原文:**
（第 142-181 行，哲学部分）

**翻译:**
## 独立开发者 + Claude 工作流

为一个人（用户）和一个实现者（Claude）规划。
- 没有团队、利益相关者、仪式、协调开销
- 用户 = 远见者/产品负责人，Claude = 构建者
- 以上下文窗口成本估算工作量，而非时间

## 计划是提示

PLAN.md 就是提示（不是变成提示的文档）。包含：
- 目标（做什么和为什么）
- 上下文（@file 引用）
- 任务（带验证标准）
- 成功标准（可测量）

## 质量降级曲线

| 上下文使用 | 质量 | Claude 状态 |
|-----------|------|------------|
| 0-30% | 峰值 | 彻底、全面 |
| 30-50% | 良好 | 自信、扎实 |
| 50-70% | 降级 | 效率模式开始 |
| 70%+ | 差 | 仓促、最小化 |

**规则：**计划应在 ~50% 上下文中完成。更多计划，更小范围，一致的质量。每个计划：最多 2-3 个任务。

## 快速交付

Plan -> Execute -> Ship -> Learn -> Repeat

**反企业模式（如果看到就删除）：**
- 团队结构、RACI 矩阵、利益相关者管理
- Sprint 仪式、变更管理流程
- 以人类单位估算时间
- 以复杂/困难作为范围理由
- 为文档而文档

**要点:**
- **单人团队优化**：不为多人团队协作设计，而是为"1 人 + 1 AI"优化
- **上下文预算替代时间估算**：用上下文消耗量衡量工作量，这是 AI 时代的独特指标
- **50% 规则**：计划的目标消耗是 50% 上下文，留有余量应对意外复杂性
- **反企业宣言**：明确反对传统企业开发模式（RACI、Sprint 仪式等）

---

#### 段落 45: Discovery Levels

**原文:**
（第 183-212 行，发现层级）

**翻译:**
## 强制发现协议

除非能证明当前上下文已存在，否则发现是强制的。

**Level 0 - 跳过**（纯内部工作，仅现有模式）
- 所有工作遵循已建立的代码库模式（grep 确认）
- 没有新的外部依赖
- 示例：添加删除按钮、添加字段到模型、创建 CRUD 端点

**Level 1 - 快速验证**（2-5 分钟）
- 单个已知库，确认语法/版本
- 行动：Context7 resolve-library-id + query-docs，不需要 DISCOVERY.md

**Level 2 - 标准研究**（15-30 分钟）
- 在 2-3 个选项中选择，新的外部集成
- 行动：路由到发现工作流，生成 DISCOVERY.md

**Level 3 - 深度探索**（1+ 小时）
- 具有长期影响的架构决策，新颖问题
- 行动：带 DISCOVERY.md 的完整研究

**深度指标：**
- Level 2+：package.json 中没有的新库、外部 API、描述中的 "choose/select/evaluate"
- Level 3："architecture/design/system"、多个外部服务、数据建模、认证设计

对于利基领域（3D、游戏、音频、着色器、ML），建议在 plan-phase 前运行 `/gsd-research-phase`。

**要点:**
- **四层发现协议**：从跳过到深度探索，根据工作类型自动选择
- **举证责任**："除非能证明当前上下文已存在，否则发现是强制的" — 默认要做发现
- **领域特殊处理**：3D、游戏、音频等利基领域建议前置研究阶段
- **时间估算**：给出大致时间范围（2-5 分钟、15-30 分钟、1+ 小时）帮助判断

---

#### 段落 46: Task Breakdown

**原文:**
（第 214-340 行，任务拆分详细规则）

**翻译:**
## 任务解剖

每个任务有四个必需字段：

**<files>：** 创建或修改的确切文件路径。
- 好：`src/app/api/auth/login/route.ts`、`prisma/schema.prisma`
- 坏："the auth files"、"relevant components"

**<action>：** 具体实现指令，包括要避免什么和为什么。
- 好："Create POST endpoint accepting {email, password}, validates using bcrypt against User table, returns JWT in httpOnly cookie with 15-min expiry. Use jose library (not jsonwebtoken - CommonJS issues with Edge runtime)."
- 坏："Add authentication"、"Make login work"

**<verify>：** 如何证明任务完成。
- 好：具体的自动化命令，< 60 秒内运行
- 坏："It works"、"Looks good"、仅手动验证
- 简单格式也可接受：`npm test` passes、`curl -X POST /api/auth/login` returns 200

**Nyquist 规则：** 每个 `<verify>` 必须包含 `<automated>` 命令。如果还没有测试，设置 `<automated>MISSING — Wave 0 must create {test_file} first</automated>` 并创建 Wave 0 任务生成测试脚手架。

**<done>：** 验收标准 — 可测量的完成状态。
- 好："Valid credentials return 200 + JWT cookie, invalid credentials return 401"
- 坏："Authentication is complete"

## 任务类型

| 类型 | 用途 | 自主性 |
|------|------|--------|
| `auto` | Claude 能独立完成的一切 | 完全自主 |
| `checkpoint:human-verify` | 视觉/功能验证 | 暂停等待用户 |
| `checkpoint:decision` | 实现选择 | 暂停等待用户 |
| `checkpoint:human-action` | 真正不可避免的手动步骤（罕见） | 暂停等待用户 |

**自动化优先规则：** 如果 Claude 能通过 CLI/API 做，Claude 必须做。检查点在自动化之后验证，而非替代它。

## 任务大小

每个任务目标 **10–30% 上下文消耗**。

| 上下文成本 | 行动 |
|-----------|------|
| < 10% 上下文 | 太小 — 与相关任务合并 |
| 10-30% 上下文 | 合适大小 — 继续 |
| > 30% 上下文 | 太大 — 拆分为两个任务 |

**上下文成本信号（使用这些，而非时间估算）：**
- 修改文件数：0-3 = ~10-15%，4-6 = ~20-30%，7+ = ~40%+（拆分）
- 新子系统：~25-35%
- 迁移 + 数据转换：~30-40%
- 纯配置/接线：~5-10%

**过大信号：** 触及 >3-5 个文件，多个不同代码块，action 段落 >1 段。

**合并信号：** 一个任务为下一个做准备，单独任务触及同一文件，单独无意义。

## 接口优先任务排序

当计划创建后续任务消费的新接口时：

1. **第一个任务：定义契约** — 创建类型文件、接口、导出
2. **中间任务：实现** — 针对已定义契约构建
3. **最后一个任务：接线** — 将实现连接到消费者

这防止"寻宝"反模式，即执行者在代码库中探索以理解契约。他们在计划本身中接收契约。

## 特异性

**测试：** 不同的 Claude 实例能否在不问澄清问题的情况下执行？如果不能，增加特异性。

## TDD 检测

**当 `workflow.tdd_mode` 启用时：** 积极应用 TDD 启发式 — 所有符合条件的任务必须使用 `type: tdd`。
**当 `workflow.tdd_mode` 禁用（默认）：** 机会性地应用 TDD 启发式 — 仅在收益明显时使用 `type: tdd`。

**启发式：** 能否在写 `fn` 之前写 `expect(fn(input)).toBe(output)`？
- 是 → 创建专用 TDD 计划（type: tdd）
- 否 → 标准计划中的标准任务

**TDD 候选（专用 TDD 计划）：** 有定义 I/O 的业务逻辑、有请求/响应契约的 API 端点、数据转换、验证规则、算法、状态机。

**标准任务：** UI 布局/样式、配置、胶水代码、一次性脚本、无业务逻辑的简单 CRUD。

**为什么 TDD 有自己的计划：** TDD 需要 RED→GREEN→REFACTOR 循环，消耗 40-50% 上下文。嵌入多任务计划会降低质量。

## 用户设置检测

对于涉及外部服务的任务，识别人工需要的配置：

外部服务指标：新 SDK（stripe、@sendgrid/mail、twilio、openai）、webhook 处理程序、OAuth 集成、process.env.SERVICE_* 模式。

对每个外部服务，确定：
1. **所需环境变量** — 来自仪表板的哪些密钥？
2. **账户设置** — 用户需要创建账户吗？
3. **仪表板配置** — 必须在外部 UI 中配置什么？

记录在 `user_setup` frontmatter 中。仅包含 Claude 确实无法做的内容。

**要点:**
- **四个必填字段**：files、action、verify、done — 每个都有具体的好/坏示例
- **Nyquist 规则**：每个 verify 必须有 automated 命令，否则标记为 MISSING 并创建前置任务
- **上下文成本估算表**：给出基于文件数量和任务类型的经验法则
- **接口优先排序**：先定义类型/接口，再实现，最后接线 — 避免"寻宝"反模式
- **TDD 模式识别**：基于"能否先写测试"的启发式判断，不是强制所有任务都用 TDD
- **用户设置检测**：外部服务需要人工配置的部分（密钥、账户、仪表板设置）

---

#### 段落 47: Dependency Graph

**原文:**
（第 342-368 行，依赖图构建）

**翻译:**
## 构建依赖图

对每个任务，记录：
- `needs`：运行前必须存在什么
- `creates`：产生什么
- `has_checkpoint`：需要用户交互？

**示例：** A→C, B→D, C+D→E, E→F(checkpoint)。Waves：{A,B} → {C,D} → {E} → {F}。

**优先垂直切片**（用户功能：模型+API+UI）而非水平分层（所有模型 → 所有 API → 所有 UI）。垂直 = 并行。水平 = 顺序。仅在需要共享基础时使用水平。

## 并行执行的文件所有权

独占文件所有权防止冲突：

```yaml
# Plan 01 frontmatter
files_modified: [src/models/user.ts, src/api/users.ts]

# Plan 02 frontmatter（无重叠 = 并行）
files_modified: [src/models/product.ts, src/api/products.ts]
```

无重叠 → 可并行运行。文件在多个计划中 → 后一个计划依赖前一个。

**要点:**
- **依赖图三要素**：needs、creates、has_checkpoint — 简洁但完整
- **垂直切片优先**：按用户功能切片（一个功能从模型到 API 到 UI）而非按层切片 — 最大化并行
- **文件所有权**：通过 frontmatter 声明文件修改，无重叠即可并行

---

#### 段落 48: Scope Estimation

**原文:**
（第 370-405 行，范围估算）

**翻译:**
## 上下文预算规则

计划应在 ~50% 上下文中完成（不是 80%）。无上下文焦虑，质量从头到尾保持一致，为意外复杂性留有余地。

**每个计划：最多 2-3 个任务。**

| 上下文权重 | 任务数/计划 | 上下文/任务 | 总计 |
|-----------|------------|-----------|------|
| 轻（CRUD、配置） | 3 | ~10-15% | ~30-45% |
| 中（认证、支付） | 2 | ~20-30% | ~40-50% |
| 重（迁移、多子系统） | 1-2 | ~30-40% | ~30-50% |

## 拆分信号

**总是拆分如果：**
- 超过 3 个任务
- 多个子系统（DB + API + UI = 单独计划）
- 任何任务修改 >5 个文件
- 检查点 + 实现在同一计划中
- 发现 + 实现在同一计划中

**考虑拆分：** >5 个文件总计、自然语义边界、单个计划上下文成本估算超过 40%。

## 粒度校准

| 粒度 | 典型计划/阶段 | 任务/计划 |
|------|-------------|----------|
| 粗 | 1-3 | 2-3 |
| 标准 | 3-5 | 2-3 |
| 细 | 5-10 | 2-3 |

从实际工作推导计划。粒度确定压缩容忍度，不是目标。

**要点:**
- **50% 规则**：不是用尽上下文，而是只用到 50%，留 50% 应对意外 — 这是对 AI 工作不确定性的缓冲
- **任务数上限 3**：强制小计划，避免大计划的质量降级
- **拆分信号清单**：明确什么时候"必须拆分"、什么时候"考虑拆分"
- **粒度是属性不是目标**：粒度由实际工作决定，不是为了细而细

---

#### 段落 49: Plan Format

**原文:**
（第 407-594 行，PLAN.md 结构规范）

**翻译:**
## PLAN.md 结构

```markdown
---
phase: XX-name
plan: NN
type: execute
wave: N                     # 执行 wave（1, 2, 3...）
depends_on: []              # 此计划所需的计划 ID
files_modified: []          # 此计划触及的文件
autonomous: true            # 如果没有检查点则为 false
requirements: []            # 必需 — 来自 ROADMAP 的需求 ID。不能空。
user_setup: []              # 人工需要的设置（如果为空则省略）

must_haves:
  truths: []                # 可观察行为
  artifacts: []             # 必须存在的文件
  key_links: []             # 关键连接
---

<objective>
[此计划完成什么]

Purpose: [为什么重要]
Output: [创建的工件]
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md

# 仅在真正需要时引用先前计划的 SUMMARY
@path/to/relevant/source.ts
</context>

<tasks>

<task type="auto">
  <name>Task 1: [Action-oriented name]</name>
  <files>path/to/file.ext</files>
  <action>[Specific implementation]</action>
  <verify>[Command or check]</verify>
  <done>[Acceptance criteria]</done>
</task>

</tasks>

<threat_model>
## 信任边界
...
## STRIDE 威胁登记
...
</threat_model>

<verification>
[Overall phase checks]
</verification>

<success_criteria>
[Measurable completion]
</success_criteria>

<output>
After completion, create `.planning/phases/XX-name/{phase}-{plan}-SUMMARY.md`
</output>
```

## Frontmatter 字段

| 字段 | 必需 | 用途 |
|------|------|------|
| `phase` | 是 | 阶段标识符（如 `01-foundation`） |
| `plan` | 是 | 阶段内计划编号 |
| `type` | 是 | `execute` 或 `tdd` |
| `wave` | 是 | 执行 wave 编号 |
| `depends_on` | 是 | 此计划所需的计划 ID |
| `files_modified` | 是 | 此计划触及的文件 |
| `autonomous` | 是 | `true` 如果没有检查点 |
| `requirements` | 是 | **必须**列出 ROADMAP 中的需求 ID。每个路线图需求 ID 必须出现在至少一个计划中。 |
| `user_setup` | 否 | 人工需要的设置项 |
| `must_haves` | 是 | 目标逆向验证标准 |

## 执行者的接口上下文

**关键洞察：**"给承包商蓝图和告诉他们'给我建个房子'的区别。"

当计划使用现有代码或创建其他计划消费的新接口时：

### 对于使用现有代码的计划：
提取执行者需要的关键接口/类型/导出，嵌入计划的 `<context>` 部分作为 `<interfaces>` 块。

### 对于创建新接口的计划：
如果此计划创建后续计划依赖的类型/接口，包含 "Wave 0" 骨架步骤。

### 何时包含接口：
- 计划触及从其他模块导入的文件 → 提取那些模块的导出
- 计划创建新 API 端点 → 提取请求/响应类型
- 计划修改组件 → 提取其 props 接口
- 计划依赖先前计划的输出 → 提取该计划 files_modified 中的类型

### 何时跳过：
- 计划自包含（从无到有创建一切，无导入）
- 纯配置（无代码接口涉及）
- Level 0 发现（所有模式已建立）

## 上下文部分规则

仅当真正需要时才包含先前计划的 SUMMARY 引用。

**反模式：** 反射性链接（02 引用 01，03 引用 02...）。独立计划不需要先前 SUMMARY 引用。

## 用户设置 Frontmatter

当涉及外部服务时：

```yaml
user_setup:
  - service: stripe
    why: "Payment processing"
    env_vars:
      - name: STRIPE_SECRET_KEY
        source: "Stripe Dashboard -> Developers -> API keys"
    dashboard_config:
      - task: "Create webhook endpoint"
        location: "Stripe Dashboard -> Developers -> Webhooks"
```

仅包含 Claude 确实无法做的内容。

**要点:**
- **严格的 frontmatter 模式**：10 个字段，其中 8 个必需 — 确保每个计划都有完整的元数据
- **需求追溯性**：`requirements` 字段不能空，且每个 ROADMAP 需求 ID 必须出现在至少一个计划中 — 这是需求覆盖的最终保障
- **接口上下文提取**：为执行者预提取类型定义和接口，避免"寻宝" — 这是提高执行效率的关键设计
- **反模式识别**：明确反对"反射性链接"（每个计划都引用前一个）— 独立计划应该独立
- **威胁模型块**：当 security_enforcement 启用时，每个计划必须包含 STRIDE 威胁登记

---

#### 段落 50: Goal-Backward Methodology

**原文:**
（第 596-698 行，目标逆向方法论）

**翻译:**
## 目标逆向方法论

**正向规划：**"我们应该构建什么？" → 产生任务。
**目标逆向：**"目标要实现，什么必须为真？" → 产生任务必须满足的要求。

## 过程

**步骤 0：提取需求 ID**
从 ROADMAP.md 读取此阶段的 `**Requirements:**` 行。分发需求 ID 到各计划 — 每个计划的 `requirements` frontmatter 字段必须列出其任务处理的需求 ID。**关键：** 每个需求 ID 必须出现在至少一个计划中。`requirements` 字段为空的计划无效。

**安全（当 `security_enforcement` 启用时 — 不存在 = 启用）：** 识别此阶段范围内的信任边界。从 RESEARCH.md 安全域将 STRIDE 类别映射到适用的技术栈。对每个威胁：分配处置（如果 ASVS L1 要求则缓解，如果低风险则接受，如果第三方则转移）。当 security_enforcement 启用时，每个计划必须包含 `<threat_model>`。

**步骤 1：陈述目标**
从 ROADMAP.md 获取阶段目标。必须是结果导向的，而非任务导向的。
- 好："Working chat interface"（结果）
- 坏："Build chat components"（任务）

**步骤 2：推导可观察真理**
"目标要实现，什么必须为真？" 从用户视角列出 3-7 条真理。

对于 "working chat interface"：
- 用户可以看到现有消息
- 用户可以输入新消息
- 用户可以发送消息
- 发送的消息出现在列表中
- 消息在页面刷新后持久化

**测试：** 每条真理都能被使用应用的人验证。

**步骤 3：推导必需工件**
对每条真理："这条为真，什么必须存在？"

"User can see existing messages" 需要：
- Message list component（渲染 Message[]）
- Messages state（从某处加载）
- API route 或 data source（提供消息）
- Message type definition（塑造数据）

**测试：** 每个工件 = 特定文件或数据库对象。

**步骤 4：推导必需接线**
对每个工件："这个功能，什么必须连接？"

Message list component 接线：
- 导入 Message type（不使用 `any`）
- 接收 messages prop 或从 API 获取
- 遍历 messages 渲染（非硬编码）
- 处理空状态（不只是崩溃）

**步骤 5：识别关键链接**
"这最可能在哪里损坏？" 关键链接 = 损坏导致级联故障的关键连接。

对于 chat interface：
- Input onSubmit -> API call（如果损坏：打字有效但发送无效）
- API save -> database（如果损坏：看起来发送了但不持久化）
- Component -> real data（如果损坏：显示占位符，非消息）

## Must-Haves 输出格式

```yaml
must_haves:
  truths:
    - "User can see existing messages"
    - "User can send a message"
    - "Messages persist across refresh"
  artifacts:
    - path: "src/components/Chat.tsx"
      provides: "Message list rendering"
      min_lines: 30
    - path: "src/app/api/chat/route.ts"
      provides: "Message CRUD operations"
      exports: ["GET", "POST"]
    - path: "prisma/schema.prisma"
      provides: "Message model"
      contains: "model Message"
  key_links:
    - from: "src/components/Chat.tsx"
      to: "/api/chat"
      via: "fetch in useEffect"
      pattern: "fetch.*api/chat"
    - from: "src/app/api/chat/route.ts"
      to: "prisma.message"
      via: "database query"
      pattern: "prisma\\.message\\.(find|create)"
```

## 常见失败

**真理太模糊：**
- 坏："User can use chat"
- 好："User can see messages", "User can send message", "Messages persist"

**工件太抽象：**
- 坏："Chat system", "Auth module"
- 好："src/components/Chat.tsx", "src/app/api/auth/login/route.ts"

**缺少接线：**
- 坏：列出组件但不说明如何连接
- 好："Chat.tsx fetches from /api/chat via useEffect on mount"

**要点:**
- **五步目标逆向**：提取需求 → 陈述目标 → 推导真理 → 推导工件 → 推导接线 → 识别关键链接
- **结果导向的目标**："Working chat interface" 而非 "Build chat components" — 关注交付价值而非执行任务
- **真理的可验证性**：每条真理必须能被最终用户验证 — 这是验收测试的基础
- **工件的特异性**：每个工件必须是具体文件路径，不能是抽象模块名
- **关键链接的风险识别**：主动识别最可能断裂的连接，在计划中重点关照

---

#### 段落 51: Checkpoints

**原文:**
（第 700-760 行，检查点类型）

**翻译:**
## 检查点类型

**checkpoint:human-verify（90% 的检查点）**
人工确认 Claude 的自动化工作正确运行。

用于：视觉 UI 检查、交互流程、功能验证、动画/可访问性。

**checkpoint:decision（9% 的检查点）**
人工做出影响方向的实现选择。

用于：技术选择、架构决策、设计选择。

**checkpoint:human-action（1% — 罕见）**
动作没有 CLI/API，需要纯人工交互。

仅用于：邮件验证链接、短信 2FA 码、手动账户审批、信用卡 3D Secure 流程。

不要用于：部署（用 CLI）、创建 webhook（用 API）、创建数据库（用提供商 CLI）、运行构建/测试（用 Bash）、创建文件（用 Write）。

## 认证门控

当 Claude 尝试 CLI/API 并得到认证错误时 → 创建检查点 → 用户认证 → Claude 重试。认证门控动态创建，不预先规划。

## 写作指南

**做：** 在检查点前自动化一切，具体（"访问 https://myapp.vercel.app" 而非 "check deployment"），编号验证步骤，陈述预期结果。

**不做：** 让人做 Claude 能自动化的事，混合多个验证，在自动化完成前放置检查点。

## 反模式和扩展示例

检查点反模式、特异性比较表、上下文部分反模式和范围缩减模式：
@~/.claude/get-shit-done/references/planner-antipatterns.md

**要点:**
- **检查点 90-9-1 分布**：绝大多数是验证（90%），少数是决策（9%），极少是人工操作（1%）— 体现自动化优先哲学
- **认证门控动态创建**：不是预先规划，而是在执行中遇到认证错误时动态创建 — 更灵活
- **自动化优先**：检查点验证 AFTER 自动化，不是替代自动化
- **外部参考**：详细反模式放在单独文件中，保持主文档聚焦

---

#### 段落 52: TDD Integration

**原文:**
（第 762-807 行，TDD 集成）

**翻译:**
## TDD 计划结构

TDD 候选在 task_breakdown 中被识别，获得专用计划（type: tdd）。一个功能一个 TDD 计划。

```markdown
---
phase: XX-name
plan: NN
type: tdd
---

<objective>
[什么功能和为什么]
Purpose: [TDD 对此功能的设计收益]
Output: [工作的、经过测试的功能]
</objective>

<feature>
  <name>[Feature name]</name>
  <files>[source file, test file]</files>
  <behavior>
    [以可测试术语描述的预期行为]
    Cases: input -> expected output
  </behavior>
  <implementation>[测试通过后如何实现]</implementation>
</feature>
```

## Red-Green-Refactor 循环

**RED：** 创建测试文件 → 写描述预期行为的测试 → 运行测试（必须失败）→ 提交：`test({phase}-{plan}): add failing test for [feature]`

**GREEN：** 写最小代码通过 → 运行测试（必须通过）→ 提交：`feat({phase}-{plan}): implement [feature]`

**REFACTOR（如需要）：** 清理 → 运行测试（必须通过）→ 提交：`refactor({phase}-{plan}): clean up [feature]`

每个 TDD 计划产生 2-3 个原子提交。

## TDD 的上下文预算

TDD 计划目标 ~40% 上下文（低于标准的 50%）。RED→GREEN→REFACTOR 来回比线性执行更重。

**要点:**
- **专用 TDD 计划**：不是将 TDD 嵌入标准计划，而是为每个 TDD 候选创建独立计划 — 避免质量降级
- **三阶段提交规范**：test → feat → refactor，每个阶段单独提交 — 清晰的演进历史
- **更低的上下文预算**：40% vs 50%，因为 TDD 的迭代更消耗上下文

---

#### 段落 53: Execution Flow Steps

**原文:**
（第 825-1031 行，执行流程步骤）

**翻译:**
包含以下步骤的详细执行流程：
- load_project_state：加载规划上下文（init、STATE.md）
- load_mode_context：检查调用模式并加载相关参考文件
- load_codebase_context：检查代码库映射，按阶段类型加载相关文档
- identify_phase：读取 ROADMAP.md，识别阶段
- mandatory_discovery：应用发现层级协议
- read_project_history：两步上下文组装 — 先生成摘要索引，再选择性读取完整 SUMMARY
- inject_global_learnings：如果启用，查询先前项目经验
- gather_phase_context：加载阶段上下文文件（CONTEXT.md、RESEARCH.md、DISCOVERY.md）
- break_into_tasks：将阶段分解为任务
- build_dependency_graph：显式映射依赖关系
- assign_waves：计算 wave 编号
- group_into_plans：按 wave 和文件冲突分组
- derive_must_haves：应用目标逆向方法论
- reachability_check：验证每个 must-have 工件有具体创建路径
- estimate_scope：验证每个计划符合上下文预算
- confirm_breakdown：在交互模式下呈现拆分等待确认
- write_phase_prompt：使用 Write 工具创建 PLAN.md 文件（严格命名约定）
- validate_plan：使用 gsd-tools 验证 frontmatter 和结构
- update_roadmap：更新 ROADMAP.md 中的阶段占位符
- git_commit：提交计划文件
- offer_next：向编排器返回结构化规划结果

**要点:**
- **19 个详细步骤**：从加载上下文到提交计划，每个步骤有具体命令和验证
- **严格命名约定**：`{padded_phase}-{NN}-PLAN.md` — 错误命名会破坏 gsd-tools 检测
- **验证前置**：提交前先验证 frontmatter 和结构，不合格的 plan 不提交
- **两步历史读取**：先生成摘要索引（低成本），再选择性读取完整 SUMMARY（高成本）— 优化上下文使用

---

#### 段落 54: Structured Returns

**原文:**
（第 1033-1088 行，结构化返回）

**翻译:**
## 规划完成

返回格式：
```markdown
## PLANNING COMPLETE

**Phase:** {phase-name}
**Plans:** {N} plan(s) in {M} wave(s)

### Wave Structure

| Wave | Plans | Autonomous |
|------|-------|------------|
| 1    | {plan-01}, {plan-02} | yes, yes |
| 2    | {plan-03}     | no (has checkpoint) |

### Plans Created

| Plan | Objective | Tasks | Files |
|------|-----------|-------|-------|
| {phase}-01 | [brief] | 2 | [files] |
| {phase}-02 | [brief] | 3 | [files] |

### Next Steps

Execute: `/gsd-execute-phase {phase}`

<sub>`/clear` first - fresh context window</sub>
```

## 差距修复计划已创建

## 检查点到达 / 修订完成

遵循检查点和 revision_mode 部分各自的模板。

**要点:**
- **标准化返回格式**：编排器解析规划者的返回，需要严格的结构化输出
- **Wave 结构表格**：清晰展示并行性（Wave 1 的计划可以并行执行）
- **下一步指引**：默认下一步是执行，但提醒 `/clear` 释放上下文

---

#### 段落 55: Success Criteria

**原文:**
（第 1090-1126 行，成功标准）

**翻译:**
## 标准模式

阶段规划完成当：
- [ ] STATE.md 已读取，项目历史已吸收
- [ ] 强制发现已完成（Level 0-3）
- [ ] 先前决策、问题、顾虑已综合
- [ ] 依赖图已构建（每个任务的 needs/creates）
- [ ] 任务已按 wave 分组（非按顺序）
- [ ] PLAN 文件存在且带 XML 结构
- [ ] 每个计划：frontmatter 中有 depends_on、files_modified、autonomous、must_haves
- [ ] 每个计划：如果涉及外部服务则声明 user_setup
- [ ] 每个计划：Objective、context、tasks、verification、success criteria、output
- [ ] 每个计划：2-3 个任务（~50% 上下文）
- [ ] 每个任务：Type、Files（如果是 auto）、Action、Verify、Done
- [ ] 检查点正确结构化
- [ ] Wave 结构最大化并行性
- [ ] PLAN 文件已提交到 git
- [ ] 用户知道下一步和 wave 结构
- [ ] `security_enforcement` 启用时 `<threat_model>` 存在且带 STRIDE 登记
- [ ] 每个威胁有处置（mitigate / accept / transfer）
- [ ] 缓解措施引用具体实现（非通用建议）

## 差距修复模式

规划完成当：
- [ ] VERIFICATION.md 或 UAT.md 已加载且缺口已解析
- [ ] 现有 SUMMARY 已读取以获取上下文
- [ ] 缺口已聚类为聚焦计划
- [ ] 计划编号在现有之后连续
- [ ] PLAN 文件存在且带 gap_closure: true
- [ ] 每个计划：任务从 gap.missing 项推导
- [ ] PLAN 文件已提交到 git
- [ ] 用户知道接下来运行 `/gsd-execute-phase {X}`

**要点:**
- **20 项检查清单（标准模式）**：覆盖从上下文加载到安全威胁模型的完整流程
- **安全威胁模型强制**：security_enforcement 启用时，每个计划必须有 threat_model 块
- **差距修复模式有单独标准**：更聚焦，只关注缺口修复

---

## Step 2: 引用文件分析

### 引用文件清单

| 引用文件 | 类型 | 作用 |
|---------|------|------|
| `references/ui-brand.md` | 样式规范 | UI 输出的一致性规范 |
| `references/revision-loop.md` | 流程规范 | 修订循环的详细规则 |
| `references/gate-prompts.md` | 提示模板 | 门控检查点的提示模板 |
| `references/agent-contracts.md` | 契约定义 | Agent 间的接口契约 |
| `references/gates.md` | 门控定义 | 各种门控的条件和行为 |
| `references/planner-source-audit.md` | 审计规范 | 多源覆盖审计的格式和规则 |
| `references/planner-gap-closure.md` | 修复模式 | 差距修复模式的详细规则 |
| `references/planner-revision.md` | 修订模式 | 基于反馈修订计划的规则 |
| `references/planner-reviews.md` | 审查模式 | 跨 AI 审查反馈的处理规则 |
| `references/planner-antipatterns.md` | 反模式 | 规划反模式和示例对比 |
| `references/tdd.md` | TDD 规范 | TDD 模式启用时的门控执行规则 |
| `references/thinking-models-planning.md` | 思维模型 | 规划时的结构化推理模型 |
| `workflows/execute-plan.md` | 执行工作流 | 下游消费者（执行者）的工作流 |

### 关键洞察

这些引用文件实现了**关注点分离**：
- 主工作流（plan-phase.md）定义"什么时候做什么"
- 引用文件定义"怎么做"和"做到什么标准"
- Agent 定义（gsd-planner.md）定义"谁来做"和"产出的格式"

这种分离使得：
1. **规则可以独立更新**：修改 TDD 规则不需要改动工作流
2. **Agent 可以复用**：gsd-planner 在不同模式（标准/差距/修订）下使用相同核心能力
3. **工作流保持清晰**：不被细节淹没，聚焦控制流

---

## Step 3: 整体总结

### 核心概念

| 概念 | 定义 | 重要性 |
|------|------|--------|
| **PLAN.md** | 可执行提示文件，不是给人读的文档 | 直接给 Claude executor 执行，无需解释 |
| **Wave** | 并行执行组，同 wave 的计划无文件冲突 | 最大化并行性，减少总执行时间 |
| **Context Budget** | 上下文窗口的使用预算（目标 50%） | 防止质量降级，留有余量应对意外 |
| **Goal-Backward** | 从目标倒推需要做什么 | 确保每个任务都服务于最终目标 |
| **Locked Decision** | 用户在 CONTEXT.md 中锁定的不可协商决策 | 保障用户主权，防止 AI 擅自更改 |
| **Source Audit** | 审计所有源工件是否被计划覆盖 | 防止需求遗漏 |
| **Checkpoint** | 需要用户交互的暂停点 | 在关键节点获得人类确认 |
| **Vertical Slice** | 按用户功能切片（模型+API+UI） | 最大化并行，减少依赖等待 |

### 工作流程

```
初始化 → 参数解析 → 阶段验证 → 上下文加载 → 研究（可选）→ 
模式映射（可选）→ 规划（gsd-planner）→ 检查（gsd-plan-checker）→ 
修订循环（最多 3 轮）→ 需求覆盖检查 → 状态更新 → 下一步指引
```

**关键门控点：**
1. **安全威胁模型门控** — 确保 AI 系统有安全设计
2. **UI 设计契约门控** — 确保前端阶段有设计规范
3. **Schema Push 门控** — 防止数据库相关的假阳性验证
4. **需求覆盖门控** — 确保所有需求都被计划覆盖

### 关键文件

| 文件 | 作用 | 大小 |
|------|------|------|
| `commands/gsd/plan-phase.md` | 用户-facing 命令定义 | ~53 行 |
| `get-shit-done/workflows/plan-phase.md` | 完整工作流编排 | ~1289 行 |
| `agents/gsd-planner.md` | 规划 Agent 角色和能力 | ~1227 行 |
| `get-shit-done/references/*.md` | 专业规则参考 | 多个文件 |

### 设计哲学

1. **计划是提示，不是文档** — 直接可执行，无需二次转换
2. **上下文预算意识** — 用上下文消耗量衡量工作量，不是时间
3. **用户决策不可协商** — 锁定决策必须完全遵守
4. **质量优于速度** — 50% 上下文规则确保质量稳定
5. **并行优于顺序** — 垂直切片和 Wave 分配最大化并行
6. **验证内建** — 不是事后检查，而是规划的一部分
7. **反企业模式** — 为单人+AI 优化，反对传统团队协作开销

---

*分析完成于 2026-04-25*
*文档：gsd-plan-phase 工作流分析（命令 + 工作流 + Agent）*
