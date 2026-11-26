# `disable-model-invocation` 与 pstack `teach` 的跨 skill 调用

## 问题

`disable-model-invocation: true` 是只关闭自动匹配，还是也阻止另一个 skill/agent 按名字调用？ys-powers 能否原样保留 pstack `teach`，并期待它在 Cursor、Claude Code 与 OMP 中调用 `how`、`why`、`unslop`？

## 短答案

**不能跨三个 runtime 一概期待。** 这个字段不属于 Agent Skills 核心规范，而是 runtime extension；核心规范当前只列出 `name`、`description`、`license`、`compatibility`、`metadata` 与 experimental `allowed-tools`。[Agent Skills specification，commit `83021e2`，`docs/specification.mdx` frontmatter table](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx#frontmatter)

| Runtime | 自动匹配 | 用户显式调用 | `teach` 原样跨调 `how` / `why` / `unslop` |
|---|---|---|---|
| Cursor | 关闭 | `/skill-name` 保留 | **不能可靠期待。** 官方只承诺用户输入 slash command；pstack 自己后来用“已知相对路径 + 直接读文件”绕过，而当前 `teach` 没有这条路径指引。[Cursor docs: Disabling automatic invocation](https://cursor.com/docs/skills#disabling-automatic-invocation) · [pstack PR #577](https://github.com/cursor/plugins/pull/577) · [`teach` lines 11–19 at pinned HEAD](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/teach/SKILL.md#L11-L19) |
| Claude Code | 关闭，并由 runtime 阻止未经用户授权的 Skill call | `/name` 保留；用户在消息中单独写 `/name` 可授权该 turn | **vanilla 不行。** pstack 的 Claude adapter 明确改成 `Read .../SKILL.md`；只有带这个 adapter 的 generated plugin 才有预期路径。[Claude Code docs: Control who invokes a skill](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) · [adapter lines 7–13](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/docs/harness/claude-code.md#L7-L13) |
| OMP 19.2.1 | 从 model catalog 隐藏 | `/skill:<name>` 保留 | **机制允许，但原文不构成强保证。** hidden skill 仍可通过 `skill://<name>` 读取；`teach` 已给出名字，因此 agent 可以加载。官方没有定义“skill A invoke skill B”的专门契约，`run how` 是否被稳定翻译为 `read skill://how` 仍依赖 prompt/model。[OMP 19.2.1 `Skill` contract lines 45–59](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/packages/coding-agent/src/extensibility/skills.ts#L45-L59) · [OMP docs: Frontmatter](https://omp.sh/docs/skills#frontmatter) |

因此，若“原样”表示**只复制 canonical `teach/SKILL.md`，不加 runtime adapter 或显式 load 指令**，答案是 **no**。若允许保留 `teach` 的正文，同时在 runtime 层适配，则 Claude Code 已有第一方范例；OMP 可把名字解析为 `skill://`；Cursor 则应采用 pstack 已为 `poteto-mode` 使用的直接文件读取方案，而不能把 disabled target 当作普通 Skill-tool invocation。[pstack Claude adapter lines 1–13](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/docs/harness/claude-code.md#L1-L13) · [`poteto-mode` lines 9–20](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/poteto-mode/SKILL.md#L9-L20)

## 按 runtime 的证据

### Agent Skills 核心规范

核心规范描述 progressive disclosure：启动时暴露 metadata，skill activated 后加载完整 `SKILL.md`；它没有定义 `disable-model-invocation`，也没有定义跨 skill invocation。客户端集成指南只把该字段举作“opted out of model-driven activation”的过滤例子，并建议把这类 skill 完全移出 model catalog；用户显式 activation 则由 harness 拦截 slash/mention 并注入正文。[Specification: Progressive disclosure](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx#progressive-disclosure) · [Client guide: Filtering and User-explicit activation](https://agentskills.io/client-implementation/adding-skills-support#filtering)

结论：字段与“显式”的具体边界由 Cursor、Claude Code、OMP 各自决定，不能从开放格式推导统一语义。[Agent Skills specification frontmatter](https://agentskills.io/specification#frontmatter)

### Cursor

Cursor 官方定义有三层，措辞都指向同一边界：

1. 正常情况下，Agent 看见 skills 并按 context 决定何时使用；手动路径是用户在 Agent chat 输入 `/` 并选择 skill。[Cursor docs: How skills work](https://cursor.com/docs/skills#how-skills-work)
2. frontmatter table 说 `true` 时，skill “only included when explicitly invoked via `/skill-name`”，Agent 不按 context 自动应用。[Cursor docs: Frontmatter fields](https://cursor.com/docs/skills#frontmatter-fields)
3. “Disabling automatic invocation” 更具体地说，只有当 **you explicitly type** `/skill-name` 时才把正文放进 context。[Cursor docs: Disabling automatic invocation](https://cursor.com/docs/skills#disabling-automatic-invocation)

官方 Cursor 文档没有定义 agent-issued Skill call，也没有说 skill A 的正文提到 skill B 就等价于用户输入 `/B`。所以能确定的是“自动 selection 关闭、用户 slash invocation 保留”；“另一个 skill 的 named invocation 可绕过”没有第一方 specification 支持。[Cursor docs: Agent Skills](https://cursor.com/docs/skills)

pstack 自己提供了更直接的 runtime evidence。2026-10 的 issue #527 记录 disabled leaves 不在 agent skill list、Skill tool 会拒绝，随后 maintainer 合并 PR #577 修复：**不是**移除 flag，而是在 `poteto-mode` 中加入 `../<name>/SKILL.md`，让 agent 直接读取 leaf 文件；当前 pinned `poteto-mode` 仍保留该行。[Issue #527](https://github.com/cursor/plugins/issues/527) · [PR #577](https://github.com/cursor/plugins/pull/577) · [`poteto-mode` lines 9–20, commit `41e4009`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/poteto-mode/SKILL.md#L9-L20)

这也给出对 `teach` 的实际判定：当前 `teach` 只说 “run `how`”、 “run `why`” 与 “through the **unslop** skill”，没有 `../<name>/SKILL.md` 或其他 file-load 指令；而三个 target 都在 line 4 设置该 flag。[`teach` lines 11–19](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/teach/SKILL.md#L11-L19) · [`how` lines 1–5](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/how/SKILL.md#L1-L5) · [`why` lines 1–5](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/why/SKILL.md#L1-L5) · [`unslop` lines 1–5](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/unslop/SKILL.md#L1-L5)

### Claude Code

Claude Code 把两个 invocation axis 分开：默认用户与 Claude 都能调用；`disable-model-invocation: true` 后，“Claude can't invoke the skill on its own”，description 不进入 Claude context，但用户仍可调用。若用户消息没有把 `/name` 作为无标点的独立词写入，Claude Code 会 block Claude 的 call；写在消息开头直接运行，写在普通文本之后只授权当前消息，由 Claude 决定是否调用。[Claude Code docs: Control who invokes a skill](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) · [Where you write the skill's name](https://code.claude.com/docs/en/skills#where-you-write-the-skills-name)

因此，已经注入的 `teach` body 说 “run `how`” 不等于**用户消息**授权 `/how`，也不授权 `/why` 或 `/unslop`；vanilla Skill tool 不能以“显式 named invocation”为理由越过 flag。[Claude Code docs: invocation matrix and blocking behavior](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill)

pstack 对 Claude Code 的第一方解决方案再次是直接读文件：adapter line 12 明说 Skill tool 拒绝多数 pstack skills，并把“run another pstack skill”映射到 `Read <pstack>/skills/<name>/SKILL.md`。generated `teach` copy 还会在标题下增加“先读 adapter”的 line，因此它不是仅复制 canonical file 后依赖 Claude Code 原生 invocation。[Adapter lines 1–13](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/harness/pstack/claude-code/docs/harness/claude-code.md#L1-L13) · [generated `teach` lines 7–13](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/harness/pstack/claude-code/skills/teach/SKILL.md#L7-L13) · [PR #637 packaging rationale](https://github.com/cursor/plugins/pull/637)

### OMP 19.2.1

OMP 将 kebab-case 字段 normalize 为 `disableModelInvocation`，再映射为 `Skill.hide`；system prompt 构建时过滤 `hide === true`。这正是“关闭 automatic catalog exposure”，不是 unload 或 access denial。[OMP `skills.ts` lines 280–289, commit `b55cd1b`](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/packages/coding-agent/src/extensibility/skills.ts#L280-L289) · [`system-prompt.ts` lines 1069–1077](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/packages/coding-agent/src/system-prompt.ts#L1069-L1077)

同一个 `Skill` interface 明确写 hidden skill 仍 loaded，并可经 `skill://<name>` 与启用时的 `/skill:<name>` 访问；URI resolver 按 exact name 在完整 loaded list 中查找，没有检查 `hide`。[OMP `Skill` interface lines 45–59](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/packages/coding-agent/src/extensibility/skills.ts#L45-L59) · [`skill-protocol.ts` lines 65–97](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/packages/coding-agent/src/internal-urls/skill-protocol.ts#L65-L97) · [OMP docs: hidden and explicit invocation](https://omp.sh/docs/skills#find-and-use-an-installed-skill)

所以 OMP 中另一个已加载的 skill 只要知道名字，技术上可以 `read skill://how`、`read skill://why`、`read skill://unslop`；flag 不会拦截。但 OMP 文档只定义 model matching、用户 `/skill:` 与 `skill://` reachability，没有定义看到自然语言 “run `how`” 时必须做该 read。结论应标为“可实现、未保证”，而不是把 model inference 写成 runtime contract。[OMP docs: Runtime usage behavior](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/docs/skills.md#runtime-usage-behavior)

## pstack 的意图与历史

pstack 的 author intent 很清楚，但 intent 与 runtime enforcement 不是一回事：

- `teach` 在 commit [`8f008c4`](https://github.com/cursor/plugins/commit/8f008c41981dca484d5beaf688d3aa2ea4ecf89b) / [PR #153](https://github.com/cursor/plugins/pull/153) 引入时就把组合写成 “real skill invocations”，并要求并行跑 `how`、`why`，最后通过 `unslop` 写作；`teach` 自己从第一版起就是 manual-only。[Introduction diff](https://github.com/cursor/plugins/commit/8f008c41981dca484d5beaf688d3aa2ea4ecf89b#diff-beea0ff19d3a7c1dfce83ea0791a58f92d942943f6e2552958065519e271be49)
- `how`、`why`、`unslop` 后来才在 commit [`73f8be4`](https://github.com/cursor/plugins/commit/73f8be4873ea4ba2b7378243a036d3360c69e04d) / [PR #300](https://github.com/cursor/plugins/pull/300) 一起得到 `disable-model-invocation: true`；PR 只说明加 flag，没有给 cross-skill exception。[PR #300 summary](https://github.com/cursor/plugins/pull/300)
- 后续 pstack 没有建立“model 命名就算显式 invocation”的特权。相反，PR #577 明说 leaves 因该 flag 不向 agent 暴露 path，并用直接读取相对路径修复 hub routing。[PR #577 summary and test plan](https://github.com/cursor/plugins/pull/577)
- 当前 pinned HEAD `41e400932eca14f289e7db717a70455256b6d388` 中，`teach` 的组合文字仍在，四个 skills 都有 flag，但只有 `poteto-mode` 有 bundled-leaf path guidance。[`teach`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/teach/SKILL.md) · [`poteto-mode` lines 9–12](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/poteto-mode/SKILL.md#L9-L12)

最保守的解释是：pstack **意图**让 `teach` 组合三个 leaves，但 canonical Cursor `teach` 没跟上 pstack 后来确立的 file-read composition mechanism。不能用作者意图覆盖 host 的 invocation gate。[PR #153](https://github.com/cursor/plugins/pull/153) · [PR #577](https://github.com/cursor/plugins/pull/577)

## 对 ys-powers 的含义

1. **不要宣称 canonical `teach` 原样跨 runtime 可用。** Cursor 与 vanilla Claude Code 都不支持该宣称；OMP 只提供可达机制，没有自然语言跨调保证。[Cursor invocation docs](https://cursor.com/docs/skills#disabling-automatic-invocation) · [Claude invocation docs](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) · [OMP frontmatter docs](https://omp.sh/docs/skills#frontmatter)
2. **若必须保持 canonical body 不变，把差异放在 runtime adapter。** Claude Code 已这样做；adapter 将 pstack skill reference 转成直接 `Read`，generated copy 只增加 adapter bootstrap line。[pstack Claude adapter](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/harness/pstack/claude-code/docs/harness/claude-code.md#L1-L13) · [generated `teach`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/harness/pstack/claude-code/skills/teach/SKILL.md#L7-L13)
3. **若目标是最小且确定的移植，显式写 load mechanism。** Cursor 用 sibling `SKILL.md` path，Claude Code 用 adapter `Read`，OMP 用 `read skill://<name>`。这不是为了绕过安全权限；它是在 host 已加载 skill package 的前提下选择已知文件，而各 runtime 对 disabled target 的原生 Skill invocation 语义仍保持不变。[pstack PR #577](https://github.com/cursor/plugins/pull/577) · [OMP skill URI contract](https://github.com/can1357/oh-my-pi/blob/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac/packages/coding-agent/src/extensibility/skills.ts#L45-L59)

## Sources

- Cursor: [Agent Skills official documentation](https://cursor.com/docs/skills).
- Claude Code: [Extend Claude with skills](https://code.claude.com/docs/en/skills).
- Agent Skills: [specification at commit `83021e2`](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx) and [client implementation guide](https://agentskills.io/client-implementation/adding-skills-support).
- OMP: [official Skills docs](https://omp.sh/docs/skills) and [v19.2.1 source, commit `b55cd1b`](https://github.com/can1357/oh-my-pi/tree/b55cd1bb664d8ab46ddc77f2a34eb47555dbf1ac).
- pstack: pinned local upstream [`refer/cursor-plugins` at `41e4009`](https://github.com/cursor/plugins/tree/41e400932eca14f289e7db717a70455256b6d388), especially [`teach`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/teach/SKILL.md), [`how`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/how/SKILL.md), [`why`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/why/SKILL.md), [`unslop`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/unslop/SKILL.md), [PR #153](https://github.com/cursor/plugins/pull/153), [PR #577](https://github.com/cursor/plugins/pull/577), and the [Claude adapter](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/docs/harness/claude-code.md).
