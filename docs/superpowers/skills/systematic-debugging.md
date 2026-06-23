# systematic-debugging

**定位**：遇到任何 bug、测试失败、意外行为时，先找到根因再修复。

**触发条件**：任何技术问题——测试失败、生产 bug、性能问题、构建失败、集成问题。

---

## Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

未完成 Phase 1，就不能提出修复方案。

## 四阶段

### Phase 1: Root Cause Investigation

修复前必须完成：

1. **仔细阅读错误信息**：不跳过错误/警告；完整读 stack trace；记录行号、文件、错误码。
2. **稳定复现**：能否可靠触发？exact steps？每次都发生？
3. **检查最近变更**：git diff、最近提交、新依赖、配置变更、环境差异。
4. **多组件系统加诊断**：在每个组件边界记录输入/输出、环境/配置传播、每层状态。
5. **追踪数据流**：坏值从哪来？谁用坏值调用了它？向上追溯直到源头。

### Phase 2: Pattern Analysis

- 找代码库中类似但正常的代码。
- 如果有参考实现，**完整读完**，不要 skim。
- 对比“工作 vs 损坏”的每个差异。
- 理解依赖、配置、环境、假设。

### Phase 3: Hypothesis and Testing

- 形成单一假设：“根因是 X，因为 Y”。
- 做最小改动验证假设，一次只变一个变量。
- 验证成功 → Phase 4；失败 → 形成新假设。
- 不懂就说不懂，问人。

### Phase 4: Implementation

1. **创建失败测试**：最简单复现，自动化测试优先。
2. **单一修复**：只修根因，不做“顺便”重构。
3. **验证修复**：测试通过，没破坏其他测试，问题真的解决。
4. **3 次修复仍失败 → 质疑架构**：如果每次修复都暴露新的耦合/共享状态，说明架构有问题，先和 human partner 讨论，不要继续修第 4 次。

## Red Flags

- “先 quick fix，以后再调查”。
- “改多个地方试试”。
- “跳过测试，我手动验证”。
- “可能就是 X，我先修一下”。
- 已经试了 2+ 次修复还没好，还想再试一次。

## 与 TDD 的衔接

Phase 4 第一步写失败测试时，使用 `superpowers:test-driven-development`；修复后使用 `superpowers:verification-before-completion` 验证。

## 真实效果

- 系统化：15–30 分钟修复。
- 随机修：2–3 小时折腾，常引入新 bug。
