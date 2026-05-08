# ys-powers

`ys-powers` 是一套用于增强 Claude Code 工作流的本地能力集，包含 **skills**（场景化行为技能）、**commands**（显式调用命令）、**agents**（专用子智能体）、**rules**（编码规范）四类配置。

## 快速开始

```bash
# 进入目标项目并安装
cd /path/to/your-project
python /path/to/ys-powers/install/local-install.py

# 验证
ls -la .claude/
```

安装策略：`skills/` 文件夹级全量覆盖；`rules/`、`commands/` 文件级同名覆盖，保留目标独有文件。

## 按场景速查

不知道自己该用什么？按当前场景选择：

| 我在做什么 | 推荐入手 |
|-----------|---------|
| 有一个模糊想法，想梳理成需求 | `/spec` → 自动触发 `idea-refine`、`spec-driven-development` |
| 需求已明确，要拆任务 | `/plan` |
| 写代码/改逻辑 | `/build`（增量实现）或 `/refactor`（重构） |
| 写 UI/前端 | `frontend-ui-engineering` [skill] 自动触发 |
| 修 bug | `/test`（先写重现测试）→ `/build` |
| 代码写完了，要审查 | `/review` |
| 准备发版 | `/ship` |
| 提交代码 | `/gc`（完整 Git 流程）或 `/local-commit`（极简本地提交） |
| 看不懂某段代码 | `/teach-code` |
| 项目结构混乱，想理清楚 | `/doc-codebase` |

## 典型工作流

开发新功能的完整路径：

```
/spec  →  /plan  →  /build  →  /test  →  /review  →  /ship
 构思      规划      构建       验证       审查       交付
```

横向贯穿的能力（自动触发或按需调用）：

- `debugging-and-error-recovery` [skill] — 测试失败或行为异常时系统调试
- `context-engineering` [skill] — 会话质量下降或切换任务时优化上下文
- `source-driven-development` [skill] — 基于官方文档实现，避免过时模式
- `/gc` [command] — 随时提交代码
- `/sop-add` [command] — 任务完成后记录经验

## 能力分类速览

### 显式命令（`/command`）

直接输入使用：

- `/spec` — 启动 spec 驱动开发
- `/plan` — 拆分任务与验收标准
- `/build` — 增量实现、测试、提交
- `/test` — TDD 流程或 bug 重现
- `/review` — 五轴代码审查
- `/ship` — 上线前检查清单
- `/refactor` — 识别 code smells 并重构
- `/code-simplify` — 简化代码复杂度
- `/gc` — 智能 Git 工作流（分支、提交、推送、PR）
- `/local-commit` — 极简本地提交
- `/sop-add` — 生成结构化 SOP
- `/s2m` — 退出 worktree 返回 main
- `/doc-codebase` — 生成 ARCHITECTURE.md
- `/teach-code` — 源码讲解
- `/wskill` — 创建新 skill
- `/easy-analysis` — 简易分析

### 行为技能（自动触发）

在对应场景自动应用：

**构思与规划** — `idea-refine` · `explore-then-ask` · `spec-driven-development` · `planning-and-task-breakdown` · `brainstorming`

**构建** — `incremental-implementation` · `frontend-ui-engineering` · `api-and-interface-design`

**验证** — `test-driven-development` · `browser-testing-with-devtools`

**审查** — `code-review-and-quality` · `security-and-hardening` · `performance-optimization`

**交付** — `shipping-and-launch` · `ci-cd-and-automation` · `git-workflow-and-versioning`

**维护** — `code-simplification` · `debugging-and-error-recovery` · `documentation-and-adrs` · `deprecation-and-migration`

**支撑** — `using-agent-skills`（元技能）· `context-engineering` · `source-driven-development` · `sop-search` · `writing-skills`

### 子智能体（Agent）

- `code-reviewer` — 五维度审查（正确性、可读性、架构、安全、性能）
- `security-auditor` — 漏洞检测与加固
- `test-engineer` — 测试策略与覆盖率

### 编码规范

- `code.md` — 先思考再编码、简化优先、精准修改、不随意重构

## 目录结构

```
ys-powers/
├── skills/      # 28 个场景化行为技能
├── commands/    # 16 个显式调用命令
├── agents/      # 3 个专用子智能体
├── rules/       # 编码规范与行为约束
├── install/     # 安装到任意项目 .claude/ 的脚本
└── docs/        # 项目内部文档与架构说明
```

## 使用示例

开发新功能时，通常按此顺序调用：

```bash
# 1. 先写 spec
/spec

# 2. 拆任务
/plan

# 3. 逐个实现
/build

# 4. 补测试
/test

# 5. 审查
/review

# 6. 提交
/gc

# 7. 上线检查
/ship
```
