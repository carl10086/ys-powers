# get-shit-done 可借鉴点与实施建议

> 从 GSD 的 86+ 命令、34 个 Agent、多层质量门中，筛选出**适合 ys-powers 轻量定位**的借鉴点。
>
> 原则：**吸收思想，不复制复杂度**。保持 ys-powers「纯配置、无运行时、中文优先」的定位。

---

## 借鉴点优先级总览

| 优先级 | 借鉴点 | 实施成本 | 预期收益 |
|--------|--------|----------|----------|
| P0（高） | Namespace Meta-Skills 路由 | 低 | 显著降低技能列表 token 消耗 |
| P0（高） | TDD Gate / 测试强制检查 | 低 | 提升代码质量 |
| P1（中） | 模糊度评分机制 | 中 | 提升 spec 质量 |
| P1（中） | 更丰富的 Agent 角色 | 中 | 提升 /ship 和专项任务质量 |
| P1（中） | 文档模板系统 | 低 | 规范项目初始化 |
| P2（低） | Cross-AI Peer Review | 高 | 多视角质量保障 |
| P2（低） | Context Window 监控 | 中 | 缓解 context rot |
| 不借鉴 | .planning 状态系统 | — | 与轻量定位冲突 |
| 不借鉴 | SDK/CLI 运行时 | — | 与纯配置定位冲突 |
| 不借鉴 | 15 运行时兼容 | — | 与聚焦 Claude Code 冲突 |

---

## P0 高优先级

### 1. Namespace Meta-Skills 路由

**GSD 方案**：6 个命名空间路由器（workflow/project/quality/context/manage/ideate），降低 2,150 → 120 tokens

**ys-powers 适配方案**：

将现有 20 个命令按功能分组为 4-5 个命名空间命令：

```
/ys-workflow    → spec, plan, build, test, ship
/ys-code        → ys-review, code-simplify, refactor, html
/ys-info        → scout, doc-codebase, easy-analysis, teach-code
/ys-git         → gc, local-commit, s2m
/ys-manage      → alias, wskill, sop-add
```

**实施方式**：
- 在 `commands/` 下新增 5 个命名空间命令文件
- 每个文件作为「一级路由」，内容简短（列出子命令 + 描述）
- 原有命令保持不变，仍然可直接调用
- 安装时同时安装命名空间和原子命令

**收益**：
- 降低模型选择命令时的 token 消耗
- 保持现有命令的向后兼容
- 不改变任何现有行为

---

### 2. TDD Gate / 测试强制检查

**GSD 方案**：MVP+TDD Gate 强制要求行为添加任务先提交 failing test

**ys-powers 适配方案**：

在 `/build` 命令中增加可选的 `--tdd` 模式：

```markdown
## TDD Mode（可选）

当用户运行 `/build --tdd` 时：

1. 读取当前任务的 acceptance criteria
2. 先写 failing test（RED）
3. 确认 test 失败后，才继续实现（GREEN）
4. 提交时必须包含 test 文件

如果跳过 failing test 步骤，中断并提示用户。
```

**实施方式**：
- 修改 `commands/build.md`
- 增加 `--tdd` flag 处理逻辑
- 在 incremental-implementation skill 中增加 TDD 分支

**收益**：
- 不强制所有人使用 TDD（默认关闭）
- 需要时提供结构化引导
- 与现有 workflow 无缝集成

---

## P1 中优先级

### 3. 模糊度评分机制（Ambiguity Scoring）

**GSD 方案**：spec-phase 在 Socratic 问答后，对 4 个维度进行 0-1 评分，≤0.20 才能写 SPEC.md

**ys-powers 适配方案**：

在 `/spec` 命令的 Phase 1（Explore and Clarify）中，增加可选的模糊度自检：

```markdown
## 模糊度自检（可选）

在生成 spec 前，评估以下维度：

| 维度 | 评分（0-1，越低越好） | 说明 |
|------|----------------------|------|
| 目标清晰度 | 0.15 | 用户想要什么很明确 |
| 范围边界 | 0.30 | 边界有些模糊，需要澄清 |
| 验收标准 | 0.10 | 成功标准已明确 |
| 技术约束 | 0.25 | 部分约束待确认 |

**综合模糊度：0.20**

如果综合模糊度 > 0.30，建议继续澄清后再写 spec。
```

**实施方式**：
- 修改 `commands/spec.md`
- 在 Phase 1 末尾增加自检步骤
- 不自检也可以继续（保持轻量）

**收益**：
- 提升 spec 质量，减少返工
- 不增加用户负担（可选步骤）

---

### 4. 更丰富的 Agent 角色

**GSD 方案**：34 个专门化 Agent，覆盖规划、执行、验证、研究、UI、文档等

**ys-powers 适配方案**：

在现有 3 个 Agent（code-reviewer, security-auditor, test-engineer）基础上，新增 3-5 个轻量 Agent：

| Agent | 用途 | 触发场景 |
|-------|------|----------|
| `plan-checker` | 验证 plan 的可执行性 | `/plan` 完成后自动执行 |
| `spec-reviewer` | 评审 spec 的完整性 | `/spec` 完成后可选执行 |
| `debugger` | 系统化的调试流程 | `/build` 失败时自动触发 |
| `context-engineer` | 优化上下文加载 | 大项目操作时建议 |

**实施方式**：
- 在 `.claude/agents/` 或 `skills/` 下新增 Agent 定义
- 保持轻量（单文件，无复杂 frontmatter）
- 由相关命令按需调用

**收益**：
- `/ship` 的 fan-out 可以更丰富
- 专项任务有专门支持
- 不增加日常使用复杂度

---

### 5. 文档模板系统

**GSD 方案**：templates/ 目录下有 PROJECT.md、REQUIREMENTS.md、ROADMAP.md 等模板

**ys-powers 适配方案**：

在 `commands/spec.md` 中增加「生成 CLAUDE.md 模板」的功能：

```markdown
## 生成项目模板（可选）

如果当前项目缺少 CLAUDE.md，在 spec 完成后询问用户：

> 需要基于本 spec 生成 CLAUDE.md 项目规范吗？

生成内容包含：
- 项目概述
- 目录结构
- 代码风格
- 测试策略
- 常用命令
```

**实施方式**：
- 修改 `commands/spec.md`
- 增加 CLAUDE.md 生成步骤
- 使用现有 spec 内容填充模板

**收益**：
- 降低新项目初始化成本
- 与现有 workflow 自然衔接
- 不引入新的状态系统

---

## P2 低优先级

### 6. Cross-AI Peer Review

**GSD 方案**：`/gsd-review --gemini --claude --codex` 调用外部 AI CLI 独立评审

**ys-powers 适配方案**：

新增 `/cross-review` 命令：

```markdown
## Cross-AI Review（实验性）

调用其他 AI 工具对当前 plan 或代码进行独立评审。

支持：
- Gemini CLI（如果已安装）
- Codex CLI（如果已安装）

输出：REVIEWS.md，可被 `/plan --reviews` 消费
```

**实施方式**：
- 新建 `commands/cross-review.md`
- 检测外部 CLI 可用性
- 生成标准化评审报告格式

**收益**：
- 多视角发现盲点
- **但**：需要用户安装多个 CLI，使用门槛高

---

### 7. Context Window 监控

**GSD 方案**：Context-Window-Aware Prompt Thinning、Utilization Guard

**ys-powers 适配方案**：

在 `rules/code.md` 或新增 skill 中增加上下文管理建议：

```markdown
## Context 管理自检

当会话超过 30 轮或检测到性能下降时：

1. 检查是否有无关的旧上下文
2. 建议用户 `/clear` 或开启新会话
3. 提示加载 plan 文件以恢复上下文
```

**实施方式**：
- 新增 `skills/context-management/SKILL.md`
- 或修改 `skills/context-engineering/SKILL.md`

**收益**：
- 缓解 context rot
- **但**：Claude Code 已有自动 compaction，收益有限

---

## 明确不借鉴的点

### 1. `.planning` 状态系统

**原因**：
- 与 ys-powers「无状态、纯配置」的定位根本冲突
- 引入 `.planning/` 意味着绑架项目结构
- 维护成本高（STATE.md 解析、 staleness 检测、workstream 管理）

**替代方案**：
- 继续使用 `docs/superpowers/specs/` 和 `docs/superpowers/plans/` 保存文档
- 状态由 git 提交历史和 GitHub Issues 管理
- 用户自行选择项目管理工具

---

### 2. SDK / CLI 运行时

**原因**：
- ys-powers 是纯 Markdown + Python 配置系统
- 引入 Node.js/TypeScript SDK 会大幅增加复杂度
- 需要处理安装、版本兼容、运行时错误等问题

**替代方案**：
- 继续使用 `install/local-install.py` 做文件级安装
- 命令和技能由 Claude Code 直接解析执行
- 无中间运行时层

---

### 3. 15 运行时兼容

**原因**：
- ys-powers 明确聚焦 Claude Code
- 多运行时兼容需要大量的格式转换和适配层
- 维护 15 个运行时的测试矩阵不现实

**替代方案**：
- 专注优化 Claude Code 体验
- 如果未来需要支持其他运行时，再考虑轻量适配

---

### 4. 86 个命令的完整覆盖

**原因**：
- 命令数量多 ≠ 好用
- ys-powers 的 20 个命令已经覆盖核心场景
- 增加过多命令会提高认知负担

**替代方案**：
- 通过 Namespace Meta-Skills 组织现有命令
- 只新增高 ROI 的命令（如 plan-checker、debugger Agent）
- 保持「每个命令都有明确价值」的门槛

---

## 实施路线图建议

### Phase 1（立即）
1. 实现 **Namespace Meta-Skills**（5 个命名空间命令）
2. 在 `/build` 中增加 **TDD Mode**（`--tdd` flag）

### Phase 2（近期）
3. 新增 **plan-checker** 和 **spec-reviewer** Agent
4. 在 `/spec` 中增加 **模糊度自检**（可选）
5. `/spec` 支持生成 **CLAUDE.md 模板**

### Phase 3（远期）
6. 实验性 **Cross-AI Review** 命令
7. **Context Management** skill

---

*整理时间：2026-06-01*
*分析原则：吸收思想，不复制复杂度；保持 ys-powers 轻量定位*
