# 领域建模：CONTEXT.md + ADR

本文档总结 `refer/skills/skills/engineering/domain-modeling/` 的核心做法。它不是要新增一个 skill，而是说明如何用一个**持续维护的领域知识库**支撑其他所有 skill。

> `refer/` 下文件**只读**。若要在 ys-powers 中实践，请在主项目目录下重写。

---

## ADR 是什么

**ADR = Architecture Decision Record（架构决策记录）**

用来记录那些**难以撤销、没有上下文会令人惊讶、来自真实权衡**的决策。它不是技术文档，也不是会议纪要，而是给未来维护者的一颗“后悔药”：当有人看到一段奇怪的代码或设计时，ADR 告诉他“这是当时 deliberate 的选择，不是 bug”。

只满足以下三条时才写 ADR：

1. **难以撤销** — 改主意成本很高
2. **令人惊讶** — 没有上下文会纳闷“为什么这样设计”
3. **真实权衡** — 当时有可行替代方案，因为具体原因选了这一个

---

## 核心文件结构

### 单上下文项目（大多数情况）

```
/
├── CONTEXT.md                 # 领域术语表
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

### 多上下文项目

```
/
├── CONTEXT-MAP.md             # 上下文地图：有哪些 bounded context，它们在哪、如何交互
├── docs/
│   └── adr/                   # 全局级 ADR
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md         # ordering 上下文的术语表
│   │   └── docs/adr/          # ordering 上下文专属的 ADR
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

**创建原则是 lazy**：不要一次性把文件都建出来。第一次有术语确定时写 `CONTEXT.md`；第一次有值得记录的决策时建 `docs/adr/`。

---

## CONTEXT.md 是什么

`CONTEXT.md` 是这个项目的**通用语言词典**。里面只放领域术语，不放实现细节、spec、临时笔记。

### 格式

```md
# Ordering

接收并追踪客户订单的上下文。

## Language

**Order**:
客户购买商品的一次请求。可能包含多个 LineItem。
_Avoid_: Purchase, transaction

**LineItem**:
Order 中的一行，表示一种商品及其数量。
_Avoid_: OrderItem, cart line

**Customer**:
在系统中下单的个人或组织。
_Avoid_: Client, buyer, account
```

### 规则

- **有主见**：同一个概念多个词时，选一个 canonical，其他列到 `_Avoid_`
- **简短**：每个定义最多一两句话，定义“它是什么”，不是“它做什么”
- **只放项目特有概念**：timeout、error type、util pattern 这类通用编程概念不要放
- **自然分组**：术语多了再用子标题归类，不要为了分类而分类

---

## ADR 长什么样

### 极简版（最常见）

```md
# 使用 Postgres 作为写模型存储

我们决定把写模型持久化到 Postgres，而不是继续用内存事件流。原因是团队对 Postgres 的运维工具最熟悉，且当前写入量远未达到需要专用事件存储的规模。这个决定预计在 6–12 个月内需要重新评估。
```

### 完整版（必要时）

```md
# Event Sourced Orders

状态：accepted
替代方案：传统 CRUD、CQRS 事件溯源

我们决定把 Order 状态管理改为事件溯源。订单状态变更频繁，业务上需要完整审计轨迹，且未来可能支持按时间回放。CRUD 方案虽然简单，但会在数据库层面留下大量变更历史表，查询和回滚都更复杂。事件溯源的写入复杂度可被现有基础设施吸收。

## 后果

- 订单查询需要额外投影到读模型
- 新成员需要理解领域事件概念
- 回滚/重放能力为后续客服场景铺路
```

### 编号规则

- 顺序编号：`0001-slug.md`、`0002-slug.md`
- 找当前最大编号 +1
- 文件名用短横线连接的小写 slug

---

## 工作方式：不是写一次，而是持续维护

`domain-modeling` 的关键不是“创建文件”，而是**在每次会话中主动维护它**。

### 会话中的行为

1. **挑战冲突术语**
   - 用户说“取消订单”，但 `CONTEXT.md` 里 cancellation 指“退款” → 立即指出并澄清

2. **把模糊词磨尖**
   - 用户说“account”，问清楚是指 `Customer` 还是 `User`

3. **用具体场景 stress-test 边界**
   - “如果订单部分发货，客户取消未发货部分，状态怎么变？”

4. **交叉验证代码**
   - 用户说支持 partial cancellation，但代码只能取消整个 order → 抛出矛盾

5. **术语一确定就更新 `CONTEXT.md`**
   - 不要攒到会话结束，实时写

6. **谨慎提供 ADR**
   - 只有同时满足“难撤销、令人惊讶、真实权衡”时才提议写 ADR

---

## 与其他 skill 的关系

`CONTEXT.md` + ADR 是**底层知识库**，其他 skill 依赖它们：

| 其他 skill | 怎么依赖 CONTEXT.md + ADR |
|---|---|
| `grill-with-docs` | 用已有术语和 ADR 加速需求澄清，避免重复发明词汇 |
| `prototype` | 原型里的概念必须与 `CONTEXT.md` 一致 |
| `to-prd` | 写 PRD 时必须用项目 domain glossary，尊重相关 ADR |
| `implement` | 实现时引用 `CONTEXT.md` 命名，遵循 ADR 约束 |
| `codebase-design` | 设计模块时参考术语边界，找到合适的 seams |
| `improve-codebase-architecture` | 分析现有代码与 `CONTEXT.md` 的偏离，找出架构腐化点 |
| `tdd` | 测试命名和断言应使用通用语言 |

换句话说：**CONTEXT.md 是项目的“事实之源”之一，ADR 是“决策之源”**。所有下游 skill 读它，而不是在每次对话里重新猜测。

---

## 为什么说它不是新增一个 skill，而是底层基础设施

`domain-modeling` 在 `refer/skills` 里确实是一个 skill，但它的价值**不在于被调用一次**，而在于它维护出来的 `CONTEXT.md` 和 `docs/adr/` 成为其他 skill 的**共享上下文层**。

### 普通 skill  vs. 知识库层

| 普通 skill | 知识库层（CONTEXT.md + ADR） |
|---|---|
| 被调用时执行一组步骤 | 一直放在那里，被读取和更新 |
| 解决“这次任务怎么做” | 回答“这个项目的事实和决策是什么” |
| 生命周期 = 一次会话 | 生命周期 = 项目全程 |
| 输出是动作或产物 | 输出是可被验证的文本 |
| 例如：`explore-then-ask` 这次把想法聊清楚 | 例如：`CONTEXT.md` 把聊清楚的术语固定下来 |

### 它支撑其他 skill 的方式

1. **减少每次启动时的重复澄清**

   没有知识库时，每次开新会话 agent 都要重新问：“你说的‘Order’是指购买订单还是服务订单？”

   有了 `CONTEXT.md`，agent 先读它，直接沿用项目已确认的术语。

2. **让多个 skill 对同一概念保持一致**

   - `to-prd` 写 PRD 时用 `CONTEXT.md` 里的术语
   - `implement` 写代码时用同样的术语命名变量、函数、模块
   - `codebase-design` 讨论模块边界时参考 `CONTEXT.md` 里的概念边界

   它们不需要互相知道对方存在，但都读同一份事实之源。

3. **把隐式决策变成显式约束**

   很多项目里的“规矩”其实只存在于某个工程师的脑子里：

   - “我们不用 GraphQL，因为上次踩过坑”
   - “这个字段叫 `status`，不是 `state`”
   - “订单和支付不要直接耦合，通过事件通信”

   ADR 把这些决策写下来，下游 skill 在实施时就不会无意中违反。

4. **让 subagent / 多会话协作有共同 ground**

   当 agent 派子 agent 去实现任务时，子 agent 只需要读两个文件就能快速进入状态：

   - `CONTEXT.md` → 知道这个世界里有什么概念
   - 相关 ADR → 知道这个世界有什么规矩

   不需要把完整对话历史都塞给子 agent。

5. **成为验证依据**

   其他 skill 可以检查自己的输出是否违背了 `CONTEXT.md` 或 ADR：

   - “你建议新增一个叫 `Purchase` 的模块，但 `CONTEXT.md` 里 `_Avoid_` 了 Purchase，应该用 `Order`。”
   - “这个实现直接调用了 Payment 服务，但 ADR-0003 规定两者必须通过事件通信。”

### 和 spec / plan 的区别

- **spec**：回答“这次任务要做什么”，任务完成后就定格了
- **plan**：回答“这次任务怎么做”，执行完可能过期
- **CONTEXT.md**：回答“这个项目里这些词是什么意思”，持续有效，随时更新
- **ADR**：回答“这个项目为什么做成这样”，永久有效，除非被新的 ADR 取代

也就是说，spec 和 plan 是**任务级**的，CONTEXT 和 ADR 是**项目级**的。

### 它为什么“不是加法”

如果只是新增一个 `domain-modeling` skill，那只是多了一个可以调用的工具。但真正的变化是：

> 让所有 skill 在执行时，把 `CONTEXT.md` 和 ADR 当作**前置读取和后置校验**的依据。

这会影响现有 skill 的行为方式，而不只是多一个文件。例如：

- `spec` 在写 spec 之前先读 `CONTEXT.md`，确保用词一致
- `plan` 在拆任务时检查相关 ADR，避免违反已有架构决策
- `build` 在实现新模块时同步更新 `CONTEXT.md`
- `review` 在审代码时检查是否引入了与 `CONTEXT.md` 冲突的术语

所以它不是一个独立功能，而是**工作流的底层基础设施**。

---

## 对 ys-powers 的启示

1. **我们自己的项目可以有一个 `CONTEXT.md`**
   - 定义 `skill`、`command`、`rule`、`sop`、`docs`、`refer` 这些词在我们仓库里的精确含义
   - 例如：skill 和 command 的边界是什么？rule 和 sop 的区别是什么？

2. **ADR 可以记录那些“现在 obvious，未来会困惑”的决策**
   - 为什么 `commands/` 和 `skills/` 分开？
   - 为什么 `refer/` 只读、不能直接搬运？
   - 为什么安装脚本用“文件级同名覆盖”而不是 merge？

3. **不需要新增 skill 也能先实践**
   - 先在仓库里创建 `CONTEXT.md` 和 `docs/adr/`
   - 然后在现有 `spec` / `plan` / `build` 流程中养成“先读/更新 CONTEXT.md 和 ADR”的习惯
   - 如果验证有效，再考虑把它固化成 skill 或 command 的前置步骤

---

## 什么时候不要做

- 不要为每个小决定都写 ADR → 会变成没人看的文档垃圾
- 不要把实现细节塞进 `CONTEXT.md` → 它不是 spec
- 不要一次性把术语表写满 → lazy creation，确定一个写一个
- 不要把它当成一次性的 → 不维护的知识库比没有更危险（会让人误以为它是对的）

---

## 参考

- `refer/skills/skills/engineering/domain-modeling/SKILL.md`
- `refer/skills/skills/engineering/domain-modeling/CONTEXT-FORMAT.md`
- `refer/skills/skills/engineering/domain-modeling/ADR-FORMAT.md`
