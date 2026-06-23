# 领域驱动上下文（Domain Modeling）学习笔记

> 本文档完全参考 `refer/skills/skills/engineering/domain-modeling/`。
> 第一版目标：**尽量模仿 + 原模板原样保留 + 直接可用**。
> 重点放在“写”——什么时候写 `CONTEXT.md`、什么时候写 ADR、怎么写、怎么避免写坏。
> `refer/` 下文件**只读**。要把这套机制用到自己项目，请在自己的项目里重写对应文件。

---

## 一、这是什么

**领域建模** = 在每次会话中**主动维护**项目的领域模型。它是一套“**主动纪律**”：在术语被混淆时挑战它，在模糊词出现时磨尖它，在场景被讨论时用具体边界场景压力测试它，并**在概念清晰的那一刻**就把它们写进 `CONTEXT.md` 和 ADR。

> 仅仅“读 `CONTEXT.md` 取词”不算这个 skill 做的事——这是任何 skill 都能做的一行习惯。这个 skill 管的是**变更模型**，而不只是消费模型。

它的核心产物是两个文件：

| 文件 | 作用 | 存放位置 |
|---|---|---|
| `CONTEXT.md` | 项目的通用语言词典（glossary） | 仓库根目录（或各上下文目录下） |
| `docs/adr/NNNN-slug.md` | 架构决策记录（Architecture Decision Record） | 仓库根目录的 `docs/adr/`（或各上下文目录下） |

---

## 二、文件结构

### 2.1 单上下文项目（大多数情况）

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

### 2.2 多上下文项目

如果存在 `CONTEXT-MAP.md`，说明仓库有多个 bounded context：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← 系统级决策
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← ordering 上下文专属决策
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

### 2.3 懒创建原则（Lazy Creation）

- **不要预先建文件**。`CONTEXT.md` 在“第一个术语确定”时创建。`docs/adr/` 在“第一个 ADR 需要时”创建。
- 没有 `CONTEXT-MAP.md` 时，仓库默认是**单上下文**结构。
- 如果存在多个上下文，必须先看 `CONTEXT-MAP.md` 找出所有上下文，然后推断当前话题属于哪一个；推断不出时**主动问**。

---

## 三、`CONTEXT.md` 怎么写

> 原模板见 `refer/skills/skills/engineering/domain-modeling/CONTEXT-FORMAT.md`。

### 3.1 结构

```md
# {Context Name}

{一到两句：描述这个上下文是什么、为什么存在。}

## Language

**Order**:
{一到两句描述}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

### 3.2 规则

- **Be opinionated（有主见）**：多个词描述同一概念时，**选一个 canonical**，其他列到 `_Avoid_`。
- **Keep definitions tight（定义要紧凑）**：每个术语最多一两句话。定义“它是什么”，不要定义“它做什么”。
- **Only project-specific terms（只放项目特有概念）**：通用编程概念（timeout、error type、util pattern）**不属于 `CONTEXT.md`**，哪怕项目里大量使用。判断标准：“这个概念**专属于这个上下文**吗？是 → 收录；否 → 不收录。”
- **Group when natural（自然分组）**：术语多了用子标题归类；术语少且属于同一领域时，平面列表即可。

### 3.3 硬性边界

> **`CONTEXT.md` 必须完全不含实现细节。** 它不是 spec，不是草稿本，也不是实现决策的存放地。**它就是一份词典，仅此而已。**

错误做法示例：

```md
# ❌ 不应出现
**Order**:
Stored in `orders` table. Created via POST /api/orders. Validates against `users.user_id`.
```

正确做法示例：

```md
# ✅ 只描述概念
**Order**:
A customer's request to purchase one or more items.
_Avoid_: Purchase, transaction
```

### 3.4 单 vs 多上下文判断逻辑

```
if exists(CONTEXT-MAP.md):
    读取它找到所有上下文
elif exists(CONTEXT.md):
    单上下文
else:
    都不存在 → 第一次有术语确定时创建根目录 CONTEXT.md
```

当存在多上下文时：

- 推断当前话题属于哪个上下文。
- 推断不出 → **问**。

多上下文示例（`CONTEXT-MAP.md`）：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

---

## 四、ADR 怎么写

> 原模板见 `refer/skills/skills/engineering/domain-modeling/ADR-FORMAT.md`。

### 4.1 模板（极简版，最常用）

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

**这就是全部内容。** 一个 ADR 可以只是一段话。它的价值在于记录“**有一个决策被做了 + 为什么**”，而不是填满章节。

### 4.2 可选章节

只在能增加真实价值时再加，大多数 ADR 不需要：

- **Status**（frontmatter）：`proposed | accepted | deprecated | superseded by ADR-NNNN` — 在决策被重新审视时有用。
- **Considered Options** — 只在“被拒绝的替代方案值得记”时用。
- **Consequences** — 只在“需要点名非显而易见的下游影响”时用。

### 4.3 编号

- 顺序编号：`0001-slug.md`、`0002-slug.md`
- 查 `docs/adr/` 中最大编号 +1
- 文件名用小写 + 短横线 slug

### 4.4 何时提供 ADR

**必须同时满足三条**：

1. **Hard to reverse（难撤销）** — 改主意成本很高
2. **Surprising without context（没有上下文会令人惊讶）** — 未来读者会纳闷“为什么这么做”
3. **Real trade-off（真实权衡）** — 当时有可行替代方案，因为具体原因选了某一种

缺任何一条 → **不写**：

- 易撤销 → 直接撤销
- 不令人惊讶 → 没人会问
- 没真实权衡 → 记录“我们做了显然的事”没意义

### 4.5 什么算 ADR-worthy

- **架构形态**。“我们用 monorepo。” “写模型事件溯源，读模型投影到 Postgres。”
- **上下文之间的集成模式**。“Ordering 和 Billing 通过领域事件通信，不是同步 HTTP。”
- **带锁定效应的技术选型**。数据库、消息总线、认证提供商、部署目标。不是每个库都算——是要花一个季度才能换的那种。
- **边界与归属决策**。“Customer 数据归 Customer 上下文，其他上下文只引用 ID。” **明确的否定**和肯定一样重要。
- **故意的偏离常规**。“我们用裸 SQL 不用 ORM，因为 X。” 这种记录能阻止下个工程师“修好”它。
- **代码里看不到的约束**。“合规要求不能用 AWS。” “合作方 API 契约要求响应 < 200ms。”
- **非显而易见的拒绝**。如果当时考虑过 GraphQL，但选了 REST 且理由微妙——记下，否则六个月后会有人再提 GraphQL。

---

## 五、会话中怎么“写”

### 5.1 主动维护的五种动作

| 触发情境 | 怎么应对 |
|---|---|
| 用户用了与 `CONTEXT.md` 冲突的术语 | 立即指出：*“你的词典里 `cancellation` 是 X，但你这里像在说 Y，到底是哪个？”* |
| 用户用了模糊或过载的词 | 提议一个精确的 canonical 词：*“你说的 `account` 指的是 Customer 还是 User？这是两个不同的东西。”* |
| 讨论领域关系 | 用具体场景压力测试：*“如果订单部分发货后客户取消未发货部分，状态怎么变？”* |
| 用户说代码怎么工作 | 交叉验证代码与陈述：*“代码取消整个 Order，但你刚才说支持部分取消，到底哪个对？”* |
| 术语一确定 | **立刻**更新 `CONTEXT.md`，不要攒到最后 |

### 5.2 谨慎提供 ADR

只在 §4.4 的三条同时满足时**才提议**写一个 ADR。写之前先在心里核对：

- 难撤销？✓
- 没有上下文会令人惊讶？✓
- 真实权衡？✓

任何一条不满足，**别提 ADR**，让用户继续往下走。

---

## 六、与其他 skill 的关系

`CONTEXT.md` + ADR 不是孤立产物，它构成**被所有 skill 共享和治理的底层知识基板**。

### 6.1 读写分离的治理模型

- **唯一写入者**：`domain-modeling` 自己。其他 skill 不应该直接写 `CONTEXT.md` / ADR。
- **所有读取者**：其他 skill 都可以（也应该）读 `CONTEXT.md` / ADR 作为项目事实和决策的来源。
- 理由：避免多作者冲突词汇表。

### 6.2 它如何支撑其他 skill

| Skill | 怎么依赖 CONTEXT.md + ADR |
|---|---|
| `grill-with-docs` | 用已有术语和 ADR 加速需求澄清，避免重复发明词汇 |
| `to-prd` | 写 PRD 时必须用项目 domain glossary，尊重相关 ADR |
| `to-issues` | 拆 issue 时按领域边界切片 |
| `implement` | 实现时用 `CONTEXT.md` 命名变量/函数/模块，遵循 ADR 约束 |
| `tdd` | 测试名、断言、边界值取自 `CONTEXT.md` 的定义 |
| `codebase-design` | 用通用架构词汇（seam/adapter/depth）+ `CONTEXT.md` 找模块边界 |
| `improve-codebase-architecture` | 分析代码与 `CONTEXT.md` / ADR 的偏离 |
| `triage` | 写 agent brief 时引用 `CONTEXT.md` 帮子 agent 快速进入上下文 |
| `resolving-merge-conflicts` | 冲突涉及领域术语时以 `CONTEXT.md` 为准 |

### 6.3 显式冲突处理

当某个 skill 的输出与现有 ADR 冲突时，**必须显式标注**，而不是静默覆盖：

> *“Contradicts ADR-0007 (event-sourced orders) — but worth reopening because …”*

---

## 七、典型工作流

### 7.1 从想法到实现

```
grill-with-docs
  ├─ 读 CONTEXT.md + ADR
  ├─ 追问中调用 domain-modeling（更新 CONTEXT / ADR）
  └─ 输出 spec

to-prd
  ├─ 读 CONTEXT.md（用正确术语）
  ├─ 读 ADR（尊重已有决策）
  └─ 输出 PRD issue

to-issues
  └─ 把 PRD 拆成垂直切片 issue

implement
  ├─ 读 CONTEXT.md（命名、接口）
  ├─ 读 ADR（遵守约束）
  ├─ 调用 tdd
  └─ 实现 + review
```

### 7.2 代码库健康流程

```
improve-codebase-architecture
  ├─ 读 CONTEXT.md + ADR
  ├─ 调用 codebase-design 获得架构词汇
  ├─ 生成 HTML 报告（用领域词汇命名模块）
  └─ 用户选择候选后运行 grilling
       └─ 调用 domain-modeling 更新 CONTEXT.md/ADR
            ├─ 新模块命名 → 加到 CONTEXT.md
            ├─ 术语精确化 → 更新 CONTEXT.md
            └─ 拒绝理由有分量 → 创建 ADR
```

---

## 八、什么时候不要做

- **不要为每个小决定都写 ADR** → 会变成没人看的文档垃圾
- **不要把实现细节塞进 `CONTEXT.md`** → 它不是 spec
- **不要一次性把术语表写满** → lazy creation，确定一个写一个
- **不要把它当成一次性的工作** → 不维护的知识库比没有更危险（会让人误以为它是对的）

---

## 九、可直接复制的模板

### 9.1 `CONTEXT.md` 空白模板

```md
# {Context Name}

{One or two sentences describing what this context is and why it exists.}

## Language

**{Term}**:
{One or two sentences describing the term.}
_Avoid_: {Synonym1}, {Synonym2}
```

### 9.2 `CONTEXT-MAP.md` 空白模板

```md
# Context Map

## Contexts

- [{Context1}](./{path1}/CONTEXT.md) — {一句话说明}
- [{Context2}](./{path2}/CONTEXT.md) — {一句话说明}

## Relationships

- **{Context1} → {Context2}**: {集成方式}
```

### 9.3 ADR 空白模板

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

需要可选章节时加：

```md
# {Short title}

Status: proposed | accepted | deprecated | superseded by ADR-NNNN

{1-3 sentences: context, decision, why.}

## Considered Options

- **{Option A}**: pros/cons
- **{Option B}**: pros/cons

## Consequences

- {non-obvious downstream effect}
```

---

## 十、参考

- `refer/skills/skills/engineering/domain-modeling/SKILL.md`
- `refer/skills/skills/engineering/domain-modeling/CONTEXT-FORMAT.md`
- `refer/skills/skills/engineering/domain-modeling/ADR-FORMAT.md`
- `refer/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md`（如何在 repo 初始化时配套设置）