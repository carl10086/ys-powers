# ys-powers

`ys-powers` 是一套用于增强 Claude Code 工作流的本地能力集，包含 **skills**（场景化行为技能）、**commands**（显式调用命令）、**agents**（专用子智能体）、**rules**（编码规范）四类配置。

## 安装

ys-powers 提供两种安装方式，分别适用于不同场景：

| 方式 | 命令 | 适用场景 |
|------|------|----------|
| **Global** | `make global-install` | 个人机器，所有项目共享同一套能力 |
| **Local** | `make local-install [project-dir=/path]` | 特定项目，或需要项目独立配置 |

### Global 安装（推荐）

```bash
cd /path/to/ys-powers
make global-install
```

将 skills/commands/agents/rules/hooks 复制到 `~/.claude/`，并自动注册 SessionStart hook 到 `~/.claude/settings.json`。安装后，**任何项目**启动 Claude Code 时都会自动加载 ys-powers 的能力。

### Local 安装

```bash
cd /path/to/ys-powers
make local-install                  # 安装到当前目录
make local-install project-dir=/path/to/project  # 安装到指定项目
```

将内容复制到 `<project>/.claude/`，并注册 hooks 到 `<project>/.claude/settings.local.json`。适用于：
- 需要在特定项目使用定制版本
- 团队共享同一套项目级配置
- 避免全局安装影响其他项目

### 安装策略

| 目录 | 策略 | 说明 |
|------|------|------|
| `skills/`、`agents/` | 文件夹级全量覆盖 | 删除旧版本，复制新版本 |
| `rules/`、`commands/`、`hooks/`、`references/` | 文件级同名覆盖 | 覆盖同名文件，保留目标独有文件 |
| `hooks` 注册 | 合并去重 | 向 settings.json 追加 hooks，不覆盖用户已有配置 |

### 路径兼容性

Global install 后的核心挑战：**Claude Code 运行时的 CWD 是用户项目目录，而非 `~/.claude/`**。因此：

- **Hooks** 使用 `$HOME/.claude/...`（global）或 `${CLAUDE_PROJECT_DIR}/.claude/...`（local），由 shell 在运行时解析
- **Skills** 内部使用 `./scripts/...` 相对路径，由 Claude Code 从 skill 文件所在目录解析
- **Agents** 通过 `skill: <name>` 工具调用，不直接引用 skill 文件路径

无需安装时修改任何文件内容，所有路径在运行时自解析。

## 按场景速查

不知道自己该用什么？按当前场景选择：

| 我在做什么 | 推荐入手 |
|-----------|---------|
| 有一个模糊想法，想梳理成需求 | `/spec` → `explore-then-ask`、`spec-driven-development` |
| 需求已明确，要拆任务 | `/plan` |
| 写代码/改逻辑 | `/build`（增量实现）或 `/refactor`（重构） |
| 写 UI/前端 | `frontend-ui-engineering` [skill] 自动触发 |
| 修 bug | `/test`（先写重现测试）→ `/build` |
| 代码写完了，要审查 | `/ys-review` |
| 准备发版 | `/ship` |
| 提交代码 | `/gc`（完整 Git 流程）或 `/local-commit`（极简本地提交） |
| 看不懂某段代码 | `/teach-code` |
| 项目结构混乱，想理清楚 | `/doc-codebase` |

## 典型工作流

开发新功能的完整路径：

```mermaid
flowchart LR
    A[/spec<br/>构思/] --> B[/plan<br/>规划/]
    B --> C[/build<br/>构建/]
    C --> D[/test<br/>验证/]
    D --> E[/ys-review<br/>审查/]
    E --> F[/ship<br/>交付/]

    C -.异常调试.-> G[debugging]
    C -.查文档实现.-> H[source-driven]
    C -.优化上下文.-> I[context-eng]
    E -.随时提交.-> J[/gc/]
    F -.记录经验.-> K[/sop-add/]
```

**主线**（实线）：构思 → 规划 → 构建 → 验证 → 审查 → 交付  
**支撑**（虚线）：构建、审查、交付阶段按需触发的横向能力，非强制步骤

## 简化依赖关系

README 只展示使用者需要的入口关系：command 是你输入的入口，skill 是背后执行的方法论。完整依赖说明见 [`docs/power-dependencies.md`](docs/power-dependencies.md)。

```mermaid
flowchart LR
    subgraph Commands["显式 commands"]
        spec["/spec"]
        plan["/plan"]
        build["/build"]
        test["/test"]
        review["/ys-review"]
        simplify["/code-simplify"]
        ship["/ship"]
        wskill["/wskill"]
        refactor["/refactor"]
        git["/gc · /local-commit · /s2m"]
        docs["/doc-codebase · /easy-analysis · /teach-code · /sop-add"]
    end

    subgraph Skills["核心 skills"]
        explore["explore-then-ask"]
        specdev["spec-driven-development"]
        planning["planning-and-task-breakdown"]
        incremental["incremental-implementation"]
        tdd["test-driven-development"]
        browser["browser-testing-with-devtools"]
        quality["code-review-and-quality"]
        codesimp["code-simplification"]
        shipping["shipping-and-launch"]
        writing["writing-skills"]
        brainstorm["brainstorming"]
        debug["debugging-and-error-recovery"]
    end

    spec --> explore
    spec --> specdev
    plan --> planning
    build --> incremental
    build --> tdd
    build -.失败时.-> debug
    test --> tdd
    test -.浏览器相关.-> browser
    review --> quality
    simplify --> codesimp
    ship --> shipping
    wskill --> explore
    wskill --> writing
    refactor --> brainstorm
    refactor --> tdd
```

自包含 commands（`/gc`、`/local-commit`、`/s2m`、`/doc-codebase`、`/easy-analysis`、`/teach-code`、`/sop-add`）主要把完整流程写在 command 内部，不显式委托某个 skill。

## 能力分类速览

| 类型 | 数量 | 调用方式 | 核心代表 |
|------|------|----------|----------|
| 显式命令 | 16 | 直接输入 `/command` | `/spec` `/plan` `/build` |
| 行为技能 | 25 | 场景自动触发 | `idea-refine` `test-driven-development` |
| 子智能体 | 3 | 自动指派 | `code-reviewer` |
| 编码规范 | 1 | 自动生效 | `code.md` |

### 显式命令（`/command`）

直接输入使用，按开发阶段分组：

| 阶段 | 命令 |
|------|------|
| 构思与规划 | `/spec` `/plan` |
| 构建与验证 | `/build` `/test` |
| 审查与优化 | `/ys-review` `/refactor` `/code-simplify` |
| 交付与提交 | `/ship` `/gc` `/local-commit` |
| 辅助 | `/sop-add` `/s2m` `/doc-codebase` `/teach-code` `/wskill` `/easy-analysis` |

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
├── skills/      # 25 个场景化行为技能
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
/ys-review

# 6. 提交
/gc

# 7. 上线检查
/ship
```
