---
name: code-walk
description: Use when manually invoked after AI-written code is done, to prepare a hands-on debugging session in a JetBrains IDE for understanding that code. Trigger: /code-walk.
argument-hint: "[topic-or-path]"
disable-model-invocation: true
---

# code-walk

AI 写完代码后，你亲手在 JetBrains IDE（IntelliJ / GoLand / PyCharm）里 debug 来理解代码。本 skill 负责搭好**舞台**（可运行、已实测、IDE 一键启动）并产出**地图**（单文件 HTML：关键路径 + 断点 + 预期值），之后你独立 debug，AI 不参与。

修 bug 不用本 skill，用 `debugging-and-error-recovery`。

参数：`$ARGUMENTS`。给出 topic 或路径时以此为准；留空则默认本会话刚写的代码。

<rules>
- 地图的读者是**完全没见过这段代码的人**。先讲意图和人话，再给代码；每个图节点、每个断点都必须有人话解释，禁止只写函数名和行号。
- 被理解的源代码**一行不改**（AI 写的、人写的都一样）：伪代码和注释只存在于地图页面；插桩必须清理复原。
- 预期值必须来自无头实测，禁止静态猜测。
- 舞台与运行配置纯本地：写任何文件前先检查 `.gitignore`，缺条目先补；不修改项目已有的共享配置。
- 地图是**单文件 HTML**：以 [`references/page-template.html`](references/page-template.html) 为骨架，只填内容、不改结构、不加外链资源（无 CDN、无远程字体、无外部图片）；离线双击可看。
- 交付即结束：Step 4 回复发出后本 skill 终止，不追问 debug 结果。
</rules>

## 流程

严格按 1 → 2 → 3 → 4 执行，不跳步。

### Step 1 圈定范围

- 先用一句人话写下**这段代码解决什么问题**，再产出一条关键路径（入口 → 核心分支 → 出口）和 3–8 个断点。
- 每个断点绑定一个**理解问题**——"走到这里能回答什么"，例如"缓存何时失效"、"什么输入会进这个分支"。

完成判据：意图一句话写得出；断点清单每条都写有（位置，理解问题）；写不出理解问题的断点删掉。

### Step 2 搭舞台

子顺序固定 2.1 → 2.4。

**2.1 造入口**：一个能走到关键路径的入口 + realistic 示例数据。优先复用或扩展项目已有的测试 / fixtures；没有才新建最小示例。

**2.2 无头跑通**：按构建工具选命令。

| 信号文件 | 命令 |
|---|---|
| `pom.xml` / `build.gradle(.kts)` | `./mvnw test` / `./gradlew test`（或对应 run 任务） |
| `go.mod` | `go run ./cmd/<x>` / `go test ./...` |
| `pyproject.toml` | `pytest` / `python <entry>.py` |
| 以上都没有（单文件 / 脚本项目） | Java：`java <Main>.java`（单文件源码模式）；Python：`python3 <entry>.py` |

**2.3 插桩采值**：在每个断点位置临时打印关键变量 → 再跑一次 → 把真实输出记为该断点的预期值 → 移除所有的桩 → 复跑一次确认输出与插桩前一致。约定：

- 断点清单里的行号一律以**清理后**的代码为准；优先用同行临时打印，避免行号漂移。
- 每条预期值注明**暂停时**（停在断点行、该行尚未执行）还是**步过后**；赋值语句的右侧值只有步过后才可见。
- 并发 / 异步程序：只把稳定量（最终状态、次数、退避序列）写为预期值；调度到达顺序标注"顺序可变"，不许把一次运行的顺序当预期。

**2.4 写运行配置**：先确认 `.gitignore` 覆盖 `.run/`（缺条目先补），再生成 `.run/code-walk-<topic>.run.xml`（模板见 [`references/run-config.md`](references/run-config.md)）。已有等价配置则复用、不写新文件。

完成判据：CLI 跑通；每个断点的预期值都有实测来源；`.run.xml` 通过 XML 校验且 `module` 名按 run-config.md 的规则推导；目标是 git 仓库时 `git status` 不出现应被 ignore 的文件（非 git 项目跳过此项）。IDE 是否实际识别配置无法无头验证，不假装验证过——在 IDE 操作提示里写明"首次打开若配置不识别，在 Run Configuration 里重选模块"。

### Step 3 生成地图

以 [`references/page-template.html`](references/page-template.html) 为骨架生成**单文件 HTML 地图**，写到 `docs/debug/<topic>.html`。模板已内置样式，**只替换 `{{占位符}}`、复制需要的节点/小节块、删掉用不上的块**；不写新的 CSS、不改标签结构、不引外部资源。

地图是**导游，不是索引**：读者不看 IDE、不读源码，只读这页就该知道代码在干什么、debug 时每站要干什么。固定叙事六段，顺序不可换：

1. **这段代码是什么**（`{{TITLE}}` / `{{INTENT}}` / `{{EXAMPLE}}`）：一句话人话意图 + 一个具体例子（用 2.1 的真实示例数据，写清输入 → 输出）。
2. **主流程**（复制 `<li>` 节点块，每站一个）：入口 → 关键分支 → 出口。`{{NODE_LABEL}}` 写**人话动作**（"算会员折扣"），`{{NODE_META}}` 写函数名 + `file:line`，`{{NODE_BRANCH}}` 写分支条件（人话："是 GOLD 会员？"）。该站没有分支就删掉整个 `node-branch` div。
3. **逐站讲解**（复制 `<article class="station">` 块，每站一个）：`{{STATION_TITLE}}` = 节点人话动作；`{{STATION_TALK}}` = 这里做什么、为什么这么做（两句人话）；`{{CODE_HEAD}}` = `file:行号范围 · 注释版`；`{{CODE}}` = **带行间人话注释的代码块**——每 1–3 行真实代码上方写一行注释（用该语言注释符），人话里直接给关键常量值和实测值（如 `GOLD_RATE=0.15`、企业采购 `afterMember=889.95`）。**只选本站相关的行**，其他站的代码不许混入；调用点与函数体可分段。代码里的 `<`、`>`、`&` 写成 HTML 实体（`&lt;` `&gt;` `&amp;`），其余逐字照抄。
   - 保真规则：代码行与源文件**逐字一致**（注释行除外），写完用脚本剥离注释后逐行比对，全部 MATCH 才定稿。注释版已含原文，不再另附代码块。
4. **断点任务卡**（复制 `<tr>`，每断点一行）：`{{BP_NAME}}` = 断点名；`{{BP_LOCATION}}` = **函数名 + `file:line`**；`{{BP_RAW}}` = 该行代码原文（一行）；`{{BP_EXPECTED}}` = 实测预期值（按 2.3 的暂停时 / 步过后约定）；`{{BP_QUESTION}}` = 理解问题。位置必须能让人在 IDE 里逐字核对"就是这一行"。
5. **补充图**（可选段）：多对象 / 多服务交互才补一张时序图，有数据模型才补一张实体关系图，用纯文本图（等宽字符画）放进 `{{EXTRA_DIAGRAM}}`。**不需要就整段删掉**（连同 `<!-- OPTIONAL:START -->` / `<!-- OPTIONAL:END -->` 标记一并删）。<rules>不为了"全面"凑图。</rules>
6. **IDE 操作提示**：运行配置名、每个断点建议 step into 还是 step over、首次配置不识别的处理（见 Step 2 判据）。

地图写入 `docs/debug/<topic>.html`，**在项目根目录**落盘。

完成判据：文件已写入且**离线可看**（`grep -oE 'src="http|href="http' docs/debug/<topic>.html` 无命中）；所有 `{{占位符}}` 已被替换（`grep -o '{{[A-Z_]*}}' docs/debug/<topic>.html` 无命中）；零背景的读者读完第 1 段能说出代码是干什么的；每个图节点、每个断点都有人话；每个断点位置含该行代码原文；逐站代码块只含本站行，剥离注释后与源文件逐字比对全部 MATCH。

### Step 4 交付

回复只含：地图文件路径 + 一行操作提示（"浏览器打开 `docs/debug/<topic>.html`，然后选 IDE 里的 `code-walk-<topic>` 配置，按地图任务卡逐站下断点"）。

完成判据：回复已发出；没有任何后续追问。

## Red flags

- 读者要问"这段代码是干嘛的" → 第 1 段缺意图或例子，回 Step 3 补。
- 图节点 / 断点只有函数名和行号 → 违反 `<rules>` 第一条，回 Step 3 补人话。
- 断点不命中 → 示例数据没走到关键路径，回 2.1 修数据；不许改断点迁就数据。
- IDE 识别不了配置 → 查 `.run.xml` 的 `type` 与 `module` 名，见 `references/run-config.md`。
- 预期值写成"应该是…" → 违反实测规则，回 2.3。
- 注释版代码与源文件不一致 → 违反保真规则，修到脚本全部 MATCH 再定稿。
- 页面还残留 `{{占位符}}` 或引了外部资源 → 回 Step 3 补齐占位符、去掉外链。
