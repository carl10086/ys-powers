---
name: code-walk
description: Use when manually invoked after AI-written code is done, to prepare a hands-on debugging session in a JetBrains IDE for understanding that code. Trigger: /code-walk.
argument-hint: "[topic-or-path]"
disable-model-invocation: true
---

# code-walk

AI 写完代码后，你亲手在 JetBrains IDE（IntelliJ / GoLand / PyCharm）里 debug 来理解代码。本 skill 负责搭好**舞台**（可运行、已实测、IDE 一键启动）并产出**地图**（HTML：关键路径 + 断点 + 预期值），之后你独立 debug，AI 不参与。

修 bug 不用本 skill，用 `debugging-and-error-recovery`。

参数：`$ARGUMENTS`。给出 topic 或路径时以此为准；留空则默认本会话刚写的代码。

<rules>
- 预期值必须来自无头实测，禁止静态猜测。
- 舞台与运行配置纯本地：写入前检查 `.gitignore`，缺条目先补；不修改项目已有的共享配置。
- HTML 一律调用 `answer-me-with-html` 渲染：不手写 HTML / CSS，不复制它的规则。
- 交付即结束：Step 4 回复发出后本 skill 终止，不追问 debug 结果。
</rules>

## 流程

严格按 1 → 2 → 3 → 4 执行，不跳步。

### Step 1 圈定范围

- 产出一条关键路径（入口 → 核心分支 → 出口）和 3–8 个断点。
- 每个断点绑定一个**理解问题**——"走到这里能回答什么"，例如"缓存何时失效"、"什么输入会进这个分支"。

完成判据：断点清单每条都写有（位置，理解问题）；写不出理解问题的断点删掉。

### Step 2 搭舞台

子顺序固定 2.1 → 2.4。

**2.1 造入口**：一个能走到关键路径的入口 + realistic 示例数据。优先复用或扩展项目已有的测试 / fixtures；没有才新建最小示例。

**2.2 无头跑通**：按构建工具选命令。

| 信号文件 | 命令 |
|---|---|
| `pom.xml` / `build.gradle(.kts)` | `./mvnw test` / `./gradlew test`（或对应 run 任务） |
| `go.mod` | `go run ./cmd/<x>` / `go test ./...` |
| `pyproject.toml` | `pytest` / `python <entry>.py` |

**2.3 插桩采值**：在每个断点位置临时打印关键变量 → 再跑一次 → 把真实输出记为该断点的预期值 → 移除所有的桩。

**2.4 写运行配置**：生成 `.run/code-walk-<topic>.run.xml`（模板见 [`references/run-config.md`](references/run-config.md)）。已有等价配置则复用、不写新文件。然后检查 `.gitignore` 覆盖所选位置（如 `.run/`），缺条目则补上。

完成判据：CLI 跑通；每个断点的预期值都有实测来源；IDE 能直接选到该配置；`git status` 里不出现应被 ignore 的文件。

### Step 3 生成地图

调用 `answer-me-with-html` 渲染页面，页面固定三块：

1. 关键路径图（`flow` 组件）。
2. 断点清单表：`| 断点 | 位置 file:line | 预期观察值 | 理解问题 |`。
3. IDE 操作提示：运行配置名、建议的调试动作（在哪 step into / step over）。

底稿写 `docs/debug/<topic>.md`，渲染时用 `-o` 输出到同目录 `docs/debug/<topic>.html`。

完成判据：`am` 输出 `✓`；页面包含全部断点及其预期值。

### Step 4 交付

回复只含：页面链接 + 一行操作提示（"打开 IDE，选 `code-walk-<topic>` 配置，按页面清单下断点"）。

完成判据：回复已发出；没有任何后续追问。

## Red flags

- 断点不命中 → 示例数据没走到关键路径，回 2.1 修数据；不许改断点迁就数据。
- IDE 识别不了配置 → 查 `.run.xml` 的 `type` 与 `module` 名，见 `references/run-config.md`。
- 预期值写成"应该是…" → 违反 `<rules>` 第一条，回 2.3 实测。
