# Systematic Debugging SKILL 深度分析

---

## 分析概要

本文档是一个**强制性的调试流程规范**，核心主张是：**没有根本原因调查，就没有修复权**。

### 四阶段流程

| 阶段 | 核心任务 | 关键规则 |
|------|----------|----------|
| **Phase 1** | 根本原因调查 | 读错误、复现、git diff、分层诊断、反向追踪 |
| **Phase 2** | 模式分析 | 找正常工作的例子对比，禁止略读参考实现 |
| **Phase 3** | 假设与测试 | 单一假设、最小化测试、一次只变一个变量 |
| **Phase 4** | 实施修复 | 先写失败测试，再修复；3次失败必须质疑架构 |

### 最重要的三条铁律

1. **Phase 1 是门槛** — 没完成就不能提修复方案
2. **3次修复失败 = 架构问题** — 不是继续试，要停下来讨论
3. **在源头修复，不在症状处修复** — 治本 vs 治标

### 实际效果

- 系统化方法：**15-30分钟**修复，成功率 **95%**
- 随机修复：**2-3小时**乱试，成功率 **40%**，还经常引入新 bug

---

## 整体理解

这个 skill 本质上是一个**反人性的调试纪律**。

人性是急躁的：看到 bug 就想改，看到错误就想 "试试"。这个 skill 强制你压抑这种冲动，遵循一个四阶段的科学方法。

**核心洞察：** 大多数 "调试" 其实不是在解决问题，而是在缓解焦虑。"我在改代码" 给人一种 "我在做事" 的感觉，即使完全是乱试。

**这个 skill 的价值在于：**
- **强制减速** — 让你慢下来，避免 "脑热式修复"
- **结构化迷茫** — 当你不知道怎么办时，给你明确的下一步
- **防止沉没成本** — 3次失败强制升级，不让你陷入 "再试一次" 的死循环
- **建立专业标准** — 调试不是猜谜，是工程实践

**什么时候最容易违反？** 紧急情况、简单问题、"明显"的 bug。skill 明确指出：这些正是最需要遵守的时候。

---

## 段落 1: 元数据 (Frontmatter)

**原文:**
```yaml
---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---
```

**翻译:**
```yaml
---
名称: 系统化调试
描述: 在遇到任何 bug、测试失败或意外行为时使用，在提出修复方案之前
---
```

**要点:**
- 这是一个关于**系统化调试**的 skill
- 触发时机：**在提出任何修复方案之前**必须先使用
- 适用范围：bug、测试失败、意外行为

---

## 段落 2: Overview (概述)

**原文:**
> Random fixes waste time and create new bugs. Quick patches mask underlying issues.
>
> **Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.
>
> **Violating the letter of this process is violating the spirit of debugging.**

**翻译:**
> 随机修复会浪费时间并制造新 bug。快速补丁掩盖了根本问题。
>
> **核心原则：** 在尝试修复之前，**始终**找到根本原因。只修症状就是失败。
>
> **违反这个流程的字面规定，就是违反调试的精神。**

**要点:**
- **反对随机修复** → 浪费时间、引入新 bug
- **反对快速补丁** → 掩盖真正的问题
- **核心铁律** → 先找根本原因，再修复
- **只修症状 = 失败** → 这是对调试工作的定义

---

## 段落 3: The Iron Law (铁律)

**原文:**
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```
> If you haven't completed Phase 1, you cannot propose fixes.

**翻译:**
```
未完成根本原因调查之前，禁止修复
```
> 如果你还没有完成第一阶段，你就不能提出修复方案。

**要点:**
- 这是**绝对禁令**：没有调查就没有修复权
- Phase 1 (根本原因调查) 是**门槛条件**
- 未完成 Phase 1 → **无权提方案**

---

## 段落 4: When to Use (何时使用)

**原文:**
> Use for ANY technical issue:
> - Test failures
> - Bugs in production
> - Unexpected behavior
> - Performance problems
> - Build failures
> - Integration issues
>
> **Use this ESPECIALLY when:**
> - Under time pressure (emergencies make guessing tempting)
> - "Just one quick fix" seems obvious
> - You've already tried multiple fixes
> - Previous fix didn't work
> - You don't fully understand the issue
>
> **Don't skip when:**
> - Issue seems simple (simple bugs have root causes too)
> - You're in a hurry (rushing guarantees rework)
> - Manager wants it fixed NOW (systematic is faster than thrashing)

**翻译:**
> 适用于**任何**技术问题：
> - 测试失败
> - 生产环境 bug
> - 意外行为
> - 性能问题
> - 构建失败
> - 集成问题
>
> **特别要在以下情况使用：**
> - 时间压力下（紧急情况下更容易想猜）
> - "就改一行"看起来很明显
> - 你已经尝试了多种修复
> - 之前的修复没奏效
> - 你还没完全理解问题
>
> **以下情况也不要跳过：**
> - 问题看起来简单（简单 bug 也有根本原因）
> - 你在赶时间（匆忙保证会返工）
> - 经理要求立刻修复（系统化比乱试更快）

**要点:**
- **适用范围极广** → 任何技术问题
- **越是紧急情况越要用** → 反直觉但正确
- **"看起来简单"是陷阱** → 简单问题也需要调查
- **时间压力不是借口** → 系统化更快
- **已经试过多次修复？** → 停下来，回到 Phase 1

---

## 段落 5: The Four Phases (四阶段总览)

**原文:**
> You MUST complete each phase before proceeding to the next.

**翻译:**
> 你必须完成每个阶段，然后才能进入下一个阶段。

**要点:**
- **强制性顺序** → 不能跳过
- **阶段制流程** → 类似瀑布模型，但用于调试

---

## 段落 6: Phase 1 - Root Cause Investigation (根本原因调查)

**原文:**
> **BEFORE attempting ANY fix:**
>
> 1. **Read Error Messages Carefully**
>    - Don't skip past errors or warnings
>    - They often contain the exact solution
>    - Read stack traces completely
>    - Note line numbers, file paths, error codes
>
> 2. **Reproduce Consistently**
>    - Can you trigger it reliably?
>    - What are the exact steps?
>    - Does it happen every time?
>    - If not reproducible → gather more data, don't guess
>
> 3. **Check Recent Changes**
>    - What changed that could cause this?
>    - Git diff, recent commits
>    - New dependencies, config changes
>    - Environmental differences
>
> 4. **Gather Evidence in Multi-Component Systems**
>
>    **WHEN system has multiple components (CI → build → signing, API → service → database):**
>
>    **BEFORE proposing fixes, add diagnostic instrumentation:**
>    ```
>    For EACH component boundary:
>      - Log what data enters component
>      - Log what data exits component
>      - Verify environment/config propagation
>      - Check state at each layer
>
>    Run once to gather evidence showing WHERE it breaks
>    THEN analyze evidence to identify failing component
>    THEN investigate that specific component
>    ```
>
>    **Example (multi-layer system):**
>    ```bash
>    # Layer 1: Workflow
>    echo "=== Secrets available in workflow: ==="
>    echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"
>
>    # Layer 2: Build script
>    echo "=== Env vars in build script: ==="
>    env | grep IDENTITY || echo "IDENTITY not in environment"
>
>    # Layer 3: Signing script
>    echo "=== Keychain state: ==="
>    security list-keychains
>    security find-identity -v
>
>    # Layer 4: Actual signing
>    codesign --sign "$IDENTITY" --verbose=4 "$APP"
>    ```
>
>    **This reveals:** Which layer fails (secrets → workflow ✓, workflow → build ✗)
>
> 5. **Trace Data Flow**
>
>    **WHEN error is deep in call stack:**
>
>    See `root-cause-tracing.md` in this directory for the complete backward tracing technique.
>
>    **Quick version:**
>    - Where does bad value originate?
>    - What called this with bad value?
>    - Keep tracing up until you find the source
>    - Fix at source, not at symptom

**翻译:**
> **在尝试任何修复之前：**
>
> 1. **仔细阅读错误信息**
>    - 不要跳过错误或警告
>    - 它们通常包含确切的解决方案
>    - 完整阅读堆栈跟踪
>    - 记录行号、文件路径、错误代码
>
> 2. **稳定复现**
>    - 你能可靠地触发它吗？
>    - 确切的步骤是什么？
>    - 每次都发生吗？
>    - 如果无法复现 → 收集更多数据，不要猜
>
> 3. **检查近期变更**
>    - 什么变更可能导致这个问题？
>    - Git diff、最近的提交
>    - 新依赖、配置变更
>    - 环境差异
>
> 4. **在多组件系统中收集证据**
>
>    **当系统有多个组件时（CI → 构建 → 签名，API → 服务 → 数据库）：**
>
>    **在提出修复之前，添加诊断工具：**
>    ```
>    对于每个组件边界：
>      - 记录什么数据进入组件
>      - 记录什么数据离开组件
>      - 验证环境/配置的传递
>      - 检查每层的状态
>
>    运行一次以收集证据，显示在哪里中断
>    然后分析证据以确定失败的组件
>    然后调查该特定组件
>    ```
>
>    **示例（多层系统）：**
>    ```bash
>    # 第1层：工作流
>    echo "=== 工作流中可用的 Secrets: ==="
>    echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"
>
>    # 第2层：构建脚本
>    echo "=== 构建脚本中的环境变量: ==="
>    env | grep IDENTITY || echo "IDENTITY 不在环境中"
>
>    # 第3层：签名脚本
>    echo "=== 钥匙串状态: ==="
>    security list-keychains
>    security find-identity -v
>
>    # 第4层：实际签名
>    codesign --sign "$IDENTITY" --verbose=4 "$APP"
>    ```
>
>    **这揭示了：** 哪一层失败（secrets → 工作流 ✓, 工作流 → 构建 ✗）
>
> 5. **追踪数据流**
>
>    **当错误在调用栈深处时：**
>
>    查看本目录中的 `root-cause-tracing.md` 获取完整的反向追踪技术。
>
>    **快速版本：**
>    - 坏值从哪里开始？
>    - 谁用坏值调用了这个？
>    - 一直向上追踪直到找到源头
>    - 在源头修复，不在症状处修复

**要点:**
- **5 个步骤，顺序执行**
- **错误信息是金矿** → 不要跳过
- **无法复现 = 不能猜** → 必须收集数据
- **近期变更是头号嫌疑人** → git diff 是第一工具
- **多层系统必须分层诊断** → 定位哪一层失败
- **数据流追踪** → 从症状反向追溯到源头
- **在源头修复** → 不是哪里报错修哪里

---

## 段落 7: Phase 2 - Pattern Analysis (模式分析)

**原文:**
> **Find the pattern before fixing:**
>
> 1. **Find Working Examples**
>    - Locate similar working code in same codebase
>    - What works that's similar to what's broken?
>
> 2. **Compare Against References**
>    - If implementing pattern, read reference implementation COMPLETELY
>    - Don't skim - read every line
>    - Understand the pattern fully before applying
>
> 3. **Identify Differences**
>    - What's different between working and broken?
>    - List every difference, however small
>    - Don't assume "that can't matter"
>
> 4. **Understand Dependencies**
>    - What other components does this need?
>    - What settings, config, environment?
>    - What assumptions does it make?

**翻译:**
> **修复之前先找模式：**
>
> 1. **找到工作正常的例子**
>    - 在同一代码库中找到类似的工作正常代码
>    - 什么工作正常的东西和坏掉的东西相似？
>
> 2. **与参考实现对比**
>    - 如果在实现某个模式，**完整**阅读参考实现
>    - 不要略读 —— 逐行阅读
>    - 在应用之前完全理解该模式
>
> 3. **识别差异**
>    - 工作正常的和坏掉的之间有什么不同？
>    - 列出每个差异，无论多小
>    - 不要假设"那个不重要"
>
> 4. **理解依赖**
>    - 这需要什么其他组件？
>    - 什么设置、配置、环境？
>    - 它做了什么假设？

**要点:**
- **对比法** → 用工作正常的 vs 坏掉的
- **禁止略读** → 必须逐行读参考实现
- **微小差异也重要** → "那个不重要"是危险想法
- **理解依赖链** → 不是孤立看代码

---

## 段落 8: Phase 3 - Hypothesis and Testing (假设与测试)

**原文:**
> **Scientific method:**
>
> 1. **Form Single Hypothesis**
>    - State clearly: "I think X is the root cause because Y"
>    - Write it down
>    - Be specific, not vague
>
> 2. **Test Minimally**
>    - Make the SMALLEST possible change to test hypothesis
>    - One variable at a time
>    - Don't fix multiple things at once
>
> 3. **Verify Before Continuing**
>    - Did it work? Yes → Phase 4
>    - Didn't work? Form NEW hypothesis
>    - DON'T add more fixes on top
>
> 4. **When You Don't Know**
>    - Say "I don't understand X"
>    - Don't pretend to know
>    - Ask for help
>    - Research more

**翻译:**
> **科学方法：**
>
> 1. **形成单一假设**
>    - 清楚陈述："我认为 X 是根本原因，因为 Y"
>    - 写下来
>    - 具体，不要模糊
>
> 2. **最小化测试**
>    - 做**最小**的变更来测试假设
>    - 一次只变一个变量
>    - 不要同时修复多个东西
>
> 3. **继续之前验证**
>    - 奏效了吗？是的 → 进入 Phase 4
>    - 没奏效？形成**新**假设
>    - **不要**在上面叠加更多修复
>
> 4. **当你不知道时**
>    - 说"我不懂 X"
>    - 不要假装懂
>    - 求助
>    - 做更多研究

**要点:**
- **科学方法** → 假设→验证→结论
- **写下来** → 强制清晰思考
- **最小变更原则** → 一次只改一点
- **验证失败 = 新假设** → 不是叠加修复
- **承认不懂** → 比假装懂更好

---

## 段落 9: Phase 4 - Implementation (实施修复)

**原文:**
> **Fix the root cause, not the symptom:**
>
> 1. **Create Failing Test Case**
>    - Simplest possible reproduction
>    - Automated test if possible
>    - One-off test script if no framework
>    - MUST have before fixing
>    - Use the `superpowers:test-driven-development` skill for writing proper failing tests
>
> 2. **Implement Single Fix**
>    - Address the root cause identified
>    - ONE change at a time
>    - No "while I'm here" improvements
>    - No bundled refactoring
>
> 3. **Verify Fix**
>    - Test passes now?
>    - No other tests broken?
>    - Issue actually resolved?
>
> 4. **If Fix Doesn't Work**
>    - STOP
>    - Count: How many fixes have you tried?
>    - If < 3: Return to Phase 1, re-analyze with new information
>    - **If ≥ 3: STOP and question the architecture (step 5 below)**
>    - DON'T attempt Fix #4 without architectural discussion
>
> 5. **If 3+ Fixes Failed: Question Architecture**
>
>    **Pattern indicating architectural problem:**
>    - Each fix reveals new shared state/coupling/problem in different place
>    - Fixes require "massive refactoring" to implement
>    - Each fix creates new symptoms elsewhere
>
>    **STOP and question fundamentals:**
>    - Is this pattern fundamentally sound?
>    - Are we "sticking with it through sheer inertia"?
>    - Should we refactor architecture vs. continue fixing症状?
>
>    **Discuss with your human partner before attempting more fixes**
>
>    This is NOT a failed hypothesis - this is a wrong architecture.

**翻译:**
> **修复根本原因，不是症状：**
>
> 1. **创建失败的测试用例**
>    - 最简单的复现
>    - 如果可能，自动化测试
>    - 如果没有框架，用一次性测试脚本
>    - **修复前必须有**
>    - 使用 `superpowers:test-driven-development` skill 编写正确的失败测试
>
> 2. **实施单一修复**
>    - 针对已识别的根本原因
>    - 一次只做一个变更
>    - 不要"顺便"改进其他东西
>    - 不要打包重构
>
> 3. **验证修复**
>    - 测试现在通过了吗？
>    - 没有其他测试被破坏？
>    - 问题真的解决了吗？
>
> 4. **如果修复不奏效**
>    - **停下**
>    - 数一数：你尝试了多少次修复？
>    - 如果 < 3：回到 Phase 1，用新信息重新分析
>    - **如果 ≥ 3：停下并质疑架构（见下面的步骤 5）**
>    - **没有架构讨论不要尝试第 4 次修复**
>
> 5. **如果 3+ 次修复失败：质疑架构**
>
>    **指示架构问题的模式：**
>    - 每次修复都暴露不同地方的新共享状态/耦合/问题
>    - 修复需要"大规模重构"才能实现
>    - 每次修复都在别处制造新症状
>
>    **停下并质疑基本假设：**
>    - 这个模式从根本上合理吗？
>    - 我们是不是"纯粹因为惯性"在坚持它？
>    - 我们应该重构架构还是继续修症状？
>
>    **在尝试更多修复之前，与你的人类搭档讨论**
>
>    这不是失败的假设 —— 这是错误的架构。

**要点:**
- **测试先行** → 先写失败测试，再修复
- **单一修复** → 不"顺便"做其他事
- **修复计数器** → 追踪尝试次数
- **3 次失败 = 架构问题** → 不是假设错了，是根基错了
- **必须讨论** → 不能自己决定重构架构
- **这不是失败** → 是发现了架构缺陷

---

## 段落 10: Red Flags (危险信号)

**原文:**
> If you catch yourself thinking:
> - "Quick fix for now, investigate later"
> - "Just try changing X and see if it works"
> - "Add multiple changes, run tests"
> - "Skip the test, I'll manually verify"
> - "It's probably X, let me fix that"
> - "I don't fully understand but this might work"
> - "Pattern says X but I'll adapt it differently"
> - "Here are the main problems: [lists fixes without investigation]"
> - Proposing solutions before tracing data flow
> - **"One more fix attempt" (when already tried 2+)**
> - **Each fix reveals new problem in different place**
>
> **ALL of these mean: STOP. Return to Phase 1.**
>
> **If 3+ fixes failed:** Question the architecture (see Phase 4.5)

**翻译:**
> 如果你发现自己在想：
> - "先快速修一下，以后再调查"
> - "试试改改 X 看行不行"
> - "加几个改动，跑下测试"
> - "跳过测试，我手动验证"
> - "可能是 X，让我修一下"
> - "我不太懂但这可能有用"
> - "模式说 X 但我会不同地适配"
> - "主要问题是：[还没调查就列修复方案]"
> - 在追踪数据流之前就提出解决方案
> - **"再试一次修复"（已经试了 2+ 次）**
> - **每次修复都在不同地方暴露新问题**
>
> **所有这些意味着：停下。回到第一阶段。**
>
> **如果 3+ 次修复失败：** 质疑架构（见 Phase 4.5）

**要点:**
- **12 个危险想法** → 每一个都要 STOP
- **"先快速修"是头号敌人** → 现在不修，以后更惨
- **"可能"是禁词** → 不懂就不要动
- **"再试一次"是陷阱** → 3 次失败要升级
- **新问题在别处出现** → 指示架构问题

---

## 段落 11: Your Human Partner's Signals (人类的纠正信号)

**原文:**
> **Watch for these redirections:**
> - "Is that not happening?" - You assumed without verifying
> - "Will it show us...?" - You should have added evidence gathering
> - "Stop guessing" - You're proposing fixes without understanding
> - "Ultrathink this" - Question fundamentals, not just symptoms
> - "We're stuck?" (frustrated) - Your approach isn't working
>
> **When you see these:** STOP. Return to Phase 1.

**翻译:**
> **注意这些纠正：**
> - "那不是没发生吗？" - 你没验证就假设了
> - "那能给我们显示...吗？" - 你应该添加证据收集
> - "别猜了" - 你在没理解的情况下提修复方案
> - "深入想想这个" - 质疑基本原理，不只是症状
> - "我们卡住了？"（沮丧）- 你的方法不管用
>
> **看到这些时：** 停下。回到第一阶段。

**要点:**
- **5 个人类信号** → 每个都表示你偏离了流程
- **"假设"是敌人** → 验证一切
- **"猜"是敌人** → 理解先行
- **"卡住" = 方法错了** → 不是坚持，是重启

---

## 段落 12: Common Rationalizations (常见借口与真相)

**原文:**
| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

**翻译:**
| 借口 | 真相 |
|--------|---------|
| "问题很简单，不需要流程" | 简单问题也有根本原因。对简单 bug，流程也很快。 |
| "紧急情况，没时间走流程" | 系统化调试比猜测试错更快。 |
| "先试试这个，然后再调查" | 第一次修复设定了模式。从一开始就做好。 |
| "我确认修复有效后再写测试" | 没测试的修复不持久。先写测试才能证明。 |
| "同时修多个东西省时间" | 无法隔离哪个奏效。会引入新 bug。 |
| "参考太长，我会适配模式" | 部分理解保证会出 bug。完整阅读。 |
| "我看到问题了，让我修" | 看到症状 ≠ 理解根本原因。 |
| "再试一次修复"（2+ 失败后） | 3+ 失败 = 架构问题。质疑模式，不要继续修。 |

**要点:**
- **8 个常见借口** → 每个都有反驳
- **"简单"不是借口** → 流程对简单问题也很快
- **"紧急"不是借口** → 系统化更快
- **"先试试"是坏习惯** → 第一次就做对
- **"看到"不等于"理解"** → 关键区别

---

## 段落 13: Quick Reference (快速参考)

**原文:**
| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

**翻译:**
| 阶段 | 关键活动 | 成功标准 |
|-------|---------------|------------------|
| **1. 根本原因** | 读错误、复现、检查变更、收集证据 | 理解**什么**和**为什么** |
| **2. 模式** | 找到工作正常例子、对比 | 识别差异 |
| **3. 假设** | 形成理论、最小化测试 | 确认或新假设 |
| **4. 实施** | 创建测试、修复、验证 | Bug 解决，测试通过 |

**要点:**
- **四阶段速查表** → 随时对照
- **每个阶段有明确产出** → 不是模糊的进行式

---

## 段落 14: When Process Reveals "No Root Cause"

**原文:**
> If systematic investigation reveals issue is truly environmental, timing-dependent, or external:
>
> 1. You've completed the process
> 2. Document what you investigated
> 3. Implement appropriate handling (retry, timeout, error message)
> 4. Add monitoring/logging for future investigation
>
> **But:** 95% of "no root cause" cases are incomplete investigation.

**翻译:**
> 如果系统调查显示问题确实是环境性的、时间依赖的、或外部的：
>
> 1. 你已完成流程
> 2. 记录你调查了什么
> 3. 实施适当的处理（重试、超时、错误信息）
> 4. 添加监控/日志以供未来调查
>
> **但是：** 95% 的"无根本原因"案例都是调查不完整。

**要点:**
- **真无原因的情况存在** → 但很少
- **必须记录调查过程** → 证明你尽力了
- **95% 是借口** → "找不到"通常意味着"没找够"

---

## 段落 15: Supporting Techniques (支持技术)

**原文:**
> These techniques are part of systematic debugging and available in this directory:
>
> - **`root-cause-tracing.md`** - Trace bugs backward through call stack to find original trigger
> - **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
> - **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling
>
> **Related skills:**
> - **superpowers:test-driven-development** - For creating failing test case (Phase 4, Step 1)
> - **superpowers:verification-before-completion** - Verify fix worked before claiming success

**翻译:**
> 这些技术是系统化调试的一部分，在本目录中可用：
>
> - **`root-cause-tracing.md`** - 反向追踪调用栈找到原始触发点
> - **`defense-in-depth.md`** - 找到根本原因后在多层添加验证
> - **`condition-based-waiting.md`** - 用条件轮询替代任意超时
>
> **相关 skills：**
> - **superpowers:test-driven-development** - 用于创建失败测试用例（Phase 4，步骤 1）
> - **superpowers:verification-before-completion** - 在声称成功前验证修复有效

**要点:**
- **3 个支持文档** → 在同一目录下
- **2 个相关 skills** → TDD 和验证
- **需要时深入学习** → 不是每次都全用

---

## 段落 16: Real-World Impact (实际效果)

**原文:**
> From debugging sessions:
> - Systematic approach: 15-30 minutes to fix
> - Random fixes approach: 2-3 hours of thrashing
> - First-time fix rate: 95% vs 40%
> - New bugs introduced: Near zero vs common

**翻译:**
> 来自调试会话的数据：
> - 系统化方法：15-30 分钟修复
> - 随机修复方法：2-3 小时乱试
> - 首次修复成功率：95% vs 40%
> - 引入新 bug：接近零 vs 常见

**要点:**
- **量化收益** → 快 4-6 倍
- **成功率翻倍** → 95% vs 40%
- **几乎不引入新 bug** → vs 经常引入

---

## 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Root Cause (根本原因)** | 问题的源头，不是表面症状 |
| **Symptom Fix (症状修复)** | 只让表象消失，问题还在 |
| **Phase-Gate (阶段门槛)** | 必须完成当前阶段才能进入下一阶段 |
| **Hypothesis-Driven (假设驱动)** | 先假设再验证，不是试错 |
| **Architecture Problem (架构问题)** | 3+ 次修复失败指示模式缺陷 |

### 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: 根本原因调查                                        │
│  ├─ 读错误信息                                                │
│  ├─ 稳定复现                                                  │
│  ├─ 检查近期变更 (git diff)                                    │
│  ├─ 多层系统收集证据                                           │
│  └─ 追踪数据流 (反向追溯)                                       │
│                          ↓                                    │
│  Phase 2: 模式分析                                            │
│  ├─ 找到工作正常的例子                                         │
│  ├─ 完整阅读参考实现                                           │
│  ├─ 列出所有差异 (无论多小)                                     │
│  └─ 理解依赖关系                                               │
│                          ↓                                    │
│  Phase 3: 假设与测试                                           │
│  ├─ 形成单一假设 (写下来)                                       │
│  ├─ 最小化测试 (一次只变一个变量)                                │
│  ├─ 验证 → 成功? 进入 Phase 4                                   │
│  └─ 失败? 形成新假设 (不叠加修复)                                │
│                          ↓                                    │
│  Phase 4: 实施修复                                             │
│  ├─ 创建失败测试用例                                           │
│  ├─ 实施单一修复 (不"顺便"改进)                                 │
│  ├─ 验证修复                                                   │
│  └─ 失败 ≥3 次? 质疑架构 (必须讨论)                              │
└─────────────────────────────────────────────────────────────┘
```

### 关键文件

| 文件 | 作用 |
|------|------|
| `SKILL.md` (本文档) | 系统化调试总流程 |
| `root-cause-tracing.md` | 反向追踪技术 |
| `defense-in-depth.md` | 多层验证策略 |
| `condition-based-waiting.md` | 条件轮询替代超时 |
| `superpowers:test-driven-development` | 测试驱动开发 skill |
| `superpowers:verification-before-completion` | 完成前验证 skill |

### 如何复刻/应用

1. **遇到任何 bug 时** → 打开这个 skill
2. **严格遵守阶段顺序** → 不能跳过
3. **Phase 1 是门槛** → 没完成就不能提修复方案
4. **写下假设** → 强制清晰思考
5. **计数修复尝试** → 3 次失败要升级
6. **注意危险信号** → 看到 "快速修"、"试试"、"可能" 就 STOP
7. **使用相关 skills** → TDD、验证等配合使用

### 最重要的 3 条规则

1. **没有 Phase 1，就没有修复权** → 调查先行
2. **3 次失败 = 架构问题** → 不是继续试，是质疑根基
3. **在源头修复，不在症状处修复** → 治标 vs 治本
