# doubt-driven-development Skill 逐段精读分析

## 分析概要

### 文档定位
这是一份 **agent skill 文档**，定义了 `doubt-driven-development`（质疑驱动开发）的方法论，属于 `agent-skills` 框架中 Build 阶段的**飞行中审查** skill。它不是 `/review`（事后 verdict），而是在编码过程中对每一个非平凡决策进行对抗性审查。

### 核心主张
**"A confident answer is not a correct one"** — 长会话中上下文会悄悄把假设变成"事实"。Doubt-driven development 是在任何非平凡输出成立之前，实例化一个 fresh-context reviewer（偏见是**证伪**，不是批准）。

### 结构骨架

| 章节 | 内容 |
|------|------|
| Overview + When to Use | Skill 定位、"非平凡决策"定义、显式排除场景 |
| Loading Constraints | 仅适用于 main-session orchestrator，禁止在 persona/subagent 中使用 |
| The Process (5 Steps) | CLAIM → EXTRACT → DOUBT → RECONCILE → STOP |
| Cross-model Escalation | 交互式会话中必须提供跨模型 second opinion 选项 |
| Common Rationalizations | 反驳"跳过质疑步骤"的借口 |
| Red Flags | 危险信号：doubt theater、loop >3 cycles、silently skip cross-model |
| Interaction with Other Skills | 与 /review、SDD、TDD、debugging 的衔接关系 |
| Verification | 执行后的验收清单 |

### 关键洞察

1. **This is not `/review`** — `/review` 是对 finished artifact 的 verdict；doubt-driven 是 in-flight posture，在 course-correction 还便宜时 catch wrong direction
2. **Fresh-context reviewer must NOT receive the CLAIM** — 只给 ARTIFACT + CONTRACT，不给你的结论，否则 reviewer 会偏向 agreement
3. **Bounded loop, not recursion** — 3 cycles 封顶， escalating to user，不要独自 grinding 第四轮
4. **Cross-model is part of the skill's value** — 不是 optional friction，而是 single-model blind spot 的补充

---

## 逐段精读

### 段落 1: Frontmatter

**原文:**
```yaml
---
name: doubt-driven-development
description: Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production, security-sensitive logic, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later.
---
```

**翻译:**
```yaml
---
name: doubt-driven-development
description: 对每个非平凡决策进行 fresh-context 对抗性审查，在它成立之前。在正确性比速度重要时、在不熟悉的代码中工作时、在 stakes 高时（生产环境、安全敏感逻辑、不可逆操作），或任何"现在验证比以后调试更便宜"的时候使用。
---
```

**要点:**
- **触发条件四重门**：(1) correctness > speed (2) unfamiliar code (3) high stakes (4) confident output
- **"before it stands"** — 不是事后审查，而是决策成立前的 gate
- **与 /review 的区别在 frontmatter 中就明确了** — /review 是 verdict，ddt 是 pre-stand gate

---

### 段落 2: Overview

**原文核心:**
> A confident answer is not a correct one. Long sessions accumulate context that quietly turns assumptions into "facts" without anyone noticing.

> This is not `/review`. `/review` is a verdict on a finished artifact. This is an in-flight posture: non-trivial decisions get cross-examined while course-correction is still cheap.

**要点:**
- **Context rot 是核心问题** — 长会话中假设悄悄变成"事实"
- **"In-flight" vs "post-hoc"** — 关键时间窗口差异：飞行中修正便宜，PR 时修正贵
- **Biased to disprove, not approve** — reviewer 的任务是证伪，不是 balanced verdict

---

### 段落 3: When to Use — Non-trivial Decision Definition

**原文核心:**
A decision is **non-trivial** when at least one of these is true:
- Introduces or modifies branching logic
- Crosses a module or service boundary
- Asserts a property the type system cannot verify (thread safety, idempotence, ordering, invariants)
- Correctness depends on context the future reader cannot see
- Blast radius is irreversible (production deploy, data migration, public API change)

**要点:**
- **明确排除 mechanical operations** — renaming/formatting/file moves 不需要 doubt
- **Type system无法验证的属性** — thread safety、idempotence、ordering 是重点
- **"Future reader cannot see"** — 隐性上下文依赖是主要风险源
- **Irreversible blast radius** — production deploy、data migration、public API change

---

### 段落 4: Loading Constraints

**原文核心:**
> Do NOT add this skill to a persona's `skills:` frontmatter. A persona that follows Step 3 would spawn another persona — the orchestration anti-pattern explicitly forbidden by `references/orchestration-patterns.md` ("personas do not invoke other personas").

> If you find yourself applying this skill from inside a subagent context: the preferred path is to surface to the user that doubt-driven cannot run nested and let the main session handle it.

**要点:**
- **严禁在 persona frontmatter 中使用** — persona 调用 persona 是 orchestration anti-pattern
- **Subagent 中无法 spawn fresh-context reviewer** — 优先 escalate 到 main session
- **Degraded fallback 存在但需标注** — self-questioning 不是 fresh-context review，必须 flag 为 degraded

---

### 段落 5: The Process — Step 1 (CLAIM)

**原文核心:**
```
CLAIM: "The new caching layer is thread-safe under the
        read-heavy workload described in the spec."
WHY THIS MATTERS: a race here corrupts user data and is
                  hard to detect in QA.
```

**要点:**
- **如果不能 compactly write the claim，你有的不是 decision，是 vibe** — 先 surface 再 scrutinize
- **WHY THIS MATTERS 是非谈判的** — 必须说明 stakes
- **CLAIM 是给 orchestrator 自己的，不是给 reviewer 的** — Step 3 中明确禁止把 CLAIM 传给 reviewer

---

### 段落 6: The Process — Step 2 (EXTRACT)

**原文核心:**
- Code: the diff or the function — not the whole file
- Decision: the proposal in 3–5 sentences plus the constraints it has to satisfy
- Strip your reasoning. If you hand over conclusions, you'll get back validation of your conclusions.

**要点:**
- **Smallest reviewable unit** — 小到 reviewer 能一次读完
- **Strip reasoning** — 不给结论，只给 artifact + contract
- **500-line PR 必须 decompose** — 否则 reviewer 无法 hold in mind

---

### 段落 7: The Process — Step 3 (DOUBT)

**原文核心:**
```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

**要点:**
- **Prompt must be adversarial** — "Find what is wrong" 不是 "Is this good?"
- **Do NOT validate. Do NOT summarize.** — 明确禁止 balanced verdict
- **Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM.** — 给结论会 bias reviewer toward agreement
- **Persona default response shape 必须被覆盖** — code-reviewer persona 默认产 balanced verdict，需要显式 override

---

### 段落 8: Cross-model Escalation

**原文核心:**
> A single-model reviewer shares blind spots with the original author — a colder, different-architecture model catches them.

> **Interactive sessions: always offer. Never silently skip.**

> After the single-model review in Step 3 above, but before RECONCILE, pause and ask:
> "Single-model review complete. Want a cross-model second opinion? Options: Gemini CLI, Codex CLI, manual external review (you paste it elsewhere), or skip."

**要点:**
- **Cross-model 不是 optional，是 skill value 的一部分** — 在 non-trivial decision 的 scope 内
- **Mandatory in every interactive doubt cycle** — 即使 stakes feel low
- **User decides, agent surfaces** — 代理的职责是呈现选择，不是 gate
- **CLI 调用前的安全检查**：PATH check → working-binary test → syntax confirmation → explicit authorization
- **Never interpolate artifact into shell-quoted argument** — 用 stdin pipe，避免 shell injection
- **Read-only sandbox 是 load-bearing detail** — 防止 artifact 中的 prompt injection 执行

---

### 段落 9: The Process — Step 4 (RECONCILE)

**原文核心:**
For each finding, classify in this **precedence order** (first matching class wins):
1. **Contract misread** — CONTRACT unclear/incomplete. Fix contract, re-classify next cycle.
2. **Valid + actionable** — real issue. Change artifact, re-loop.
3. **Valid trade-off** — real issue but cost > benefit. Document explicitly.
4. **Noise** — reviewer lacks context. Note, move on, ask: would adding context to contract prevent false flag?

**要点:**
- **You are still the orchestrator** — reviewer output 是 data 不是 verdict
- **Precedence order 是关键** — contract misread > actionable > trade-off > noise
- **Fresh reviewer can be wrong** — 不要因为"fresh"就 defer

---

### 段落 10: The Process — Step 5 (STOP)

**原文核心:**
Stop when:
- Next iteration returns only trivial or already-considered findings, **or**
- 3 cycles completed (escalate to user, don't grind a fourth alone), **or**
- User explicitly says "ship it"

> If after 3 cycles the reviewer still surfaces substantive issues, the artifact may not be ready. Surface this to the user — three unresolved cycles is information about the artifact, not a reason to keep looping.

**要点:**
- **3 cycles 是硬上限** — escalate to user，不要独自 grinding
- **如果 3 cycles 显然不够因为 artifact 太大** → artifact too big，return to Step 2 and decompose
- **Do not lift the bound** —  bound 不是 negotiable

---

### 段落 11: Red Flags

| 危险信号 | 含义 |
|---------|------|
| Spawning fresh-context for one-line rename | 过度使用，浪费资源 |
| Treating reviewer output as authoritative | 忘记自己是 orchestrator |
| Looping >3 cycles without escalating | 违反 STOP 规则 |
| Prompting "is this good?" instead of "find issues" | 非对抗性，失去 skill 价值 |
| Skipping doubt under time pressure on high-stakes | 最不该 skip 的时候 skip |
| Re-spawning on unchanged artifact | Stalling，会得相同 findings |
| **Doubt theater** | 2+ cycles 有 substantive findings 但 0 个 classified as actionable — 你在 validating，不是 doubting |
| Doubting only after committing | 那是 `/review`，不是 doubt-driven |
| Hardcoding external CLI without confirming | 工具可能不存在或 syntax 不同 |
| **Silently skipping cross-model** | 即使不推荐，offer 必须 visible |
| Falling back silently when CLI errors | Surface failure，let user redirect |
| Passing CLAIM to reviewer | Biases toward agreement |

---

## 与 ys-powers 现有 workflow 的对比

### 当前 ys-powers 链路
```
/spec → /plan → /build (incremental-implementation + test-driven-development)
```

### doubt-driven-development 的插入点

**在 /build 阶段内部**：
- `incremental-implementation` 的每个 increment 完成后，如果有非平凡决策，触发 doubt-driven
- `test-driven-development` 的 RED step 本身就是 doubt made concrete — 一个 failing test 是对 behavior claim 的 disproof attempt

**在 /review 之前**：
- `/review`（code-review-and-quality）是 post-hoc PR verdict
- doubt-driven 是 in-flight per-decision
- 两者互补，不是替代

### 与现有 skill 的关系

| 现有 skill | 与 ddt 的关系 |
|-----------|-------------|
| code-review-and-quality / `/review` | 互补 — `/review` 事后，ddt 飞行中 |
| source-driven-development | SDD 验证 framework facts，ddt 验证 reasoning about artifact |
| test-driven-development | TDD 的 RED step = doubt made concrete；当 TDD 适用时，failing test 满足 ddt 的 fresh-context review 要求 |
| debugging-and-error-recovery | Reviewer 发现 real failure mode 时，drop into debugging skill |

---

## 同步决策

### 已同步内容
- `skills/doubt-driven-development/SKILL.md` — 完整搬运，已加入 ys-powers skill 集
- `skills/using-agent-skills/SKILL.md` — 决策树已新增 ddt 入口（"Stakes high / unfamiliar code? → doubt-driven-development"）

### 与现有 workflow 的衔接建议

**选项 A：集成到 /build（推荐）**
- 在 `incremental-implementation` 的每个 increment 中，如果涉及非平凡决策，自动触发 ddt
- 触发条件：branching logic、cross-module boundary、type system 无法验证的断言
- 产物：doubt cycle 的结果（CLAIM + reviewer findings + reconciliation）作为 increment 的一部分

**选项 B：作为独立 skill，用户显式调用**
- 用户在想"这个决策对吗？"时显式调用 `/doubt-driven-development`
- 与当前状态一致（已存在于 skill 集）
- 风险：用户可能忘记在关键时刻调用

**选项 C：集成到 /review**
- 在 `/review` 命令中增加 ddt 作为前置步骤
- 风险：混淆了 in-flight 和 post-hoc 的界限

### 建议
采用 **选项 B（当前状态）+ 在 /build 中增加可选触发提示**：
- ddt 作为独立 skill 存在，用户显式调用
- 在 `incremental-implementation` 的 Verification 清单中增加一项："如果本 increment 涉及非平凡决策，考虑调用 doubt-driven-development"
- 这样既不强制（避免过度使用），又提醒（避免遗漏）

---

## Verification（执行后的验收清单）

- [ ] 每个非平凡决策都被显式命名为 CLAIM
- [ ] 至少一次 fresh-context review per non-trivial artifact（TDD 的 RED step 可替代 behavioral claims）
- [ ] Reviewer 收到 ARTIFACT + CONTRACT — NOT CLAIM，NOT reasoning
- [ ] Reviewer prompt 是对抗性（"find issues"）不是验证性（"is it good"）
- [ ] Findings 按 precedence 分类：contract misread / actionable / trade-off / noise
- [ ] 停止条件满足：trivial findings / 3 cycles / user override
- [ ] 交互模式：cross-model 被显式 offer（无论 artifact stakes）
- [ ] 非交互模式：cross-model skip 被 announce
- [ ] 任何外部 CLI 调用前有 PATH check + working-binary test + syntax confirmation + explicit authorization
