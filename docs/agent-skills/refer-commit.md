# agent-skills Refer Commit Log

## §1 当前快照

- refer/agent-skills: `301b02b12bff98e4688e6984af6556802322bbde` (`301b02b`)
- refer subject: `Merge #736: validate review findings against code and baseline`
- refer date: `2026-11-01`
- ys-powers 同期 commit: `63c7db4` (`Merge pull request #88 from carl10086/chore/remove-show-me`)
- 上次 refer 基线: `98967c4` (`Merge pull request #396 from nucliweb/docs/adoption-guide`)
- 本次窗口: `98967c4..301b02b`，460 commits，218 files，`+10378/-1302`

## §2 已吸收度索引

| 上游能力 | ys-powers 状态 | 本次决策 |
|---|---|---|
| `source-driven-development` | 已存在，缺 retrieval safety | 已同步适配 |
| `security-and-hardening` | 已存在，缺 derived path、shared store、privacy lifecycle | 已同步适配 |
| `context-engineering` | 已存在，缺 restartable session boundaries | 已同步适配 |
| `performance-optimization` | 已存在，缺 keep/revert 与实验记录 | 已同步适配 |
| `api-and-interface-design` | 已存在，缺 `Idempotency-Key` 规则 | 暂不同步，待业务场景 |
| `observability-and-instrumentation` | 当前无同名本地 skill | 待定 |
| `constraint-driven-development` | 当前不存在 | 暂不同步，避免引入第二套 `CONSTRAINTS.md` 规则来源 |

## 更新历史

### 2026-11-13: 98967c4..301b02b

**摘要**：首次完成上游窗口分析，并将四项 Claude Code 相关方法论更新适配到 ys-powers 的本地目录和工作流约定。

**上下游**：
- 起点: `98967c4` (`Merge pull request #396 from nucliweb/docs/adoption-guide`)
- 终点: `301b02b` (`Merge #736: validate review findings against code and baseline`)
- 期间提交数: 460
- ys-powers 同期 commit: `63c7db4`

#### 4 维度变更

**1. 方法论修订**
- `source-driven-development`: 新增 retrieval safety，将抓取文档视为 untrusted input，并禁止未经披露硬编码 outbound endpoint。
- `security-and-hardening`: 新增 derived path 授权检查、多实例 shared-store rate limiting、personal data lifecycle。
- `context-engineering`: 新增 restartable session boundaries 和持久化交接要求。
- `performance-optimization`: 将验证明确为 keep or revert，要求同条件测量和记录 reverted attempts。

**2. 新增**
- 上游新增 `constraint-driven-development`、`skills/*/references/` 和质量门脚本；本次仅记录，未直接复制。
- 上游 `.gemini/` 新增或修改内容与本次 Claude Code 同步无关，不展开。

**3. 删除/合并**
- 上游 `hooks/hooks.json` 被删除；hooks 不属于本次目标，未同步。
- 上游 skill-local reference 文件未原样复制，相关内容改写到 ys-powers 已有中央 `references/` 目录。

**4. 编排层变化**
- 上游新增 `/constraints` 相关 command 编排；由于 ys-powers 尚未采用 `CONSTRAINTS.md` 作为项目契约，本次暂不同步。
- `.gemini/` command 编排变化标记为不相关，不展开。

#### 同步决策

- **要同步**：
  - 将 retrieval safety 适配到 `skills/source-driven-development/SKILL.md`。
  - 将三项安全缺口适配到 `skills/security-and-hardening/SKILL.md` 和 `references/security-checklist.md`。
  - 将 restartable session boundaries 适配到 `skills/context-engineering/SKILL.md`。
  - 将 keep/revert 验证规则适配到 `skills/performance-optimization/SKILL.md` 和 `references/performance-checklist.md`。
- **暂不同步**：
  - hooks、`.gemini/`、evals 和测试夹具不属于本次核心 skill 同步范围。
  - `constraint-driven-development` 会引入新的规则来源和质量门体系，当前工作流尚未采用。
- **已确认同步**：
  - 本次四项适配保留 ys-powers 的中文工作流、中央 references 结构和 `docs/ys-powers/` 路径约定。
- **待定**：
  - `api-and-interface-design` 的 `Idempotency-Key`：待出现支付、下单、扣库存或其他可重试副作用接口时同步。
  - `observability-and-instrumentation`：待本仓库明确多入口生产系统和本地 runbook 目录约定后决定。

#### TODO

- [ ] Review 本次四项 skill 适配内容。
- [ ] 合并 PR 后，以 `301b02b` 作为下一次同步基线。

## §4 Update Entry 模板

### YYYY-MM-DD: <prev-short>..<new-short>

**摘要**：一行总结本次更新的性质。

**上下游**：
- 起点: <prev-short> (<prev-subject>)
- 终点: <new-short> (<new-subject>)
- 期间提交数: N
- ys-powers 同期 commit: <short>

#### 4 维度变更

**1. 方法论修订**
- `<skill-name>`: 一行说明

**2. 新增**
- `<path>`: 一行说明

**3. 删除/合并**
- `<path>`: 一行说明

**4. 编排层变化**
- 一行说明

#### 同步决策

- **要同步**：
  - <动作> → 影响 ys-powers 路径 `<path>`
- **暂不同步**：
  - <理由>
- **已确认同步**：
  - <说明>
- **待定**：
  - <未决问题>

#### TODO

- [ ] <动作 1>
- [ ] <动作 2>
