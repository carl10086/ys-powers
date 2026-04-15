---
name: refactoring
description: 代码重构专家。识别 code smells，应用标准重构手法，在保持行为不变的前提下改进代码结构。
---

# 重构

<HARD-GATE>
**不要直接开始改代码。**

使用本命令前，必须先调用 `brainstorming` skill 进行重构方案设计。本文档中所有内容（Code Smells 识别、重构手法、输出格式、风险评估框架）都是 `brainstorming` 阶段的输入和思考素材。

重构分成两个阶段：
1. **方案设计** — 通过 `brainstorming` 产出具体重构计划
2. **代码执行** — 严格遵循 TDD 流程逐步实施（项目有专门的 TDD skill）

在 `brainstorming` 完成并输出重构方案之前，禁止直接编辑文件。

类，函数，字段的注释非常重要，尤其是中文注释
</HARD-GATE>

## 重构黄金法则

- **重构时绝不改变行为** — 重构和功能变更必须分开提交
- **重构前必须有测试** — 没有测试就补测试
- **小步增量修改** — 每一步都能独立验证
- **保持代码随时可运行** — 每次改动后测试必须通过

---

## Code Smells 识别

### Bloaters（膨胀）

| Smell | 特征 | 典型阈值 |
|-------|------|---------|
| Long Method | 函数职责过多 | > 20 行 |
| Large Class | 类做了太多事 | > 200 行 |
| Primitive Obsession | 用原始类型代替小对象 | 多处重复出现相同字段组合 |
| Long Parameter List | 参数过多 | > 3 个 |
| Data Clumps | 同一组数据总是一起出现 | 多次重复出现的字段集合 |

### Object-Orientation Abusers（OO 滥用）

- **Switch Statements** — 可用 polymorphism 替代的类型判断
- **Parallel Inheritance Hierarchies** — 每增加一个子类就要在另一个继承体系中加对应子类
- **Refused Bequest** — 子类根本不使用父类的方法

### Change Preventers（变更阻止器）

- **Divergent Change** — 一个类因为多种不同原因被修改
- **Shotgun Surgery** — 做一次改动要改很多个类
- **Feature Envy** — 方法过度使用另一个类的数据

### Dispensables（可有可无）

- **Dead Code** — 未被使用的代码
- **Duplicate Code** — 重复逻辑
- **Speculative Generality** — 为"未来"设计的未使用抽象
- **Comments** — 用注释解释烂代码，而不是修复它

### Couplers（耦合过度）

- **Inappropriate Intimacy** — 类之间过度了解内部细节
- **Message Chains** — `a.b().c().d()`
- **Middle Man** — 类把所有事情都委托给别人

---

## 常见重构手法

### Extract Method

- **Before**: 一个长函数包含多个职责
- **After**: 多个命名清晰的聚焦函数

### Extract Class

- **Before**: 一个类做了太多事
- **After**: 多个高内聚、职责单一的类

### Replace Conditional with Polymorphism

- **Before**: switch / if 语句判断类型后执行不同逻辑
- **After**: 多态方法调用

### Introduce Parameter Object

- **Before**: 多个相关参数散落各处
- **After**: 用一个对象封装相关数据

---

## 安全重构流程（执行阶段）

方案确定后，进入代码执行阶段。具体 TDD 细节由项目专门的 TDD skill 负责，这里只保留核心安全原则：

```
1. 验证测试通过（绿）
2. 做一个小的改动（应用单一重构手法）
3. 运行测试（确认行为未变）
4. 提交（保存安全状态）
5. 重复（继续下一步）
```

**原则**：每一步只改一件事，改完立即验证。

---

## 向后兼容策略

当重构涉及 public API 时：

- 添加新方法，废弃旧方法
- 接口变更使用 Adapter Pattern
- 提供迁移路径文档
- 必要时对破坏性变更进行版本控制

---

## 输出格式（brainstorming 阶段使用）

在 `brainstorming` 阶段分析代码问题时，按以下格式输出重构方案：

```markdown
## 当前问题
[描述识别到的 code smell]

## 建议变更
[具体的重构手法]

## 分步计划
1. [第一步安全改动]
2. [第二步安全改动]
...

## 风险评估
[什么可能出错，以及如何验证没有出错]
```

---

## 优先级分类

| 优先级 | 行动 | 示例 |
|--------|------|------|
| Critical | 立即修复 | 变异体存活、知识重复、嵌套 > 3 层 |
| High | 本次会话 | 魔法数字、命名不清、函数 > 30 行 |
| Nice | 稍后 | 轻微命名、一次性辅助函数 |
| Skip | 不改 | 已经足够干净的代码 |

---

## DRY = 知识，而不是代码

**应该抽象时**：
- 相同的业务概念（语义意义）
- 如果需求变化会一起变化
- 分组原因显而易见

**应该保持分离时**：
- 看起来相似的不同概念（结构性）
- 会独立演化
- 耦合会造成困惑

---

## 何时不重構

- ❌ 代码工作正常，没有 bug 要修
- ❌ 没有测试要求这个改变（推测性重构）
- ❌ 会改变行为（那是功能，不是重构）
- ❌ 过早优化
- ❌ 代码对当前阶段来说"足够好"
- ❌ **纯粹为了可测试性而提取** — 如果移动代码到单独文件的唯一原因是"方便单元测试"，那就保持内联。提取应该是为了可读性、DRY 或关注点分离，不是为了可测试性本身。

---

## 提交规范

```
refactor: extract payment validation logic
refactor: replace switch with polymorphism
refactor: introduce parameter object for address
```

**格式**：`refactor: <做了什么>`

重构提交不应该与功能提交混在一起。
