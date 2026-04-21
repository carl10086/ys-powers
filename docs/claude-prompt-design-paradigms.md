# Claude 源码提示词设计范式

> 从 Claude 泄露源码中提炼的提示词工程规范。源码中 60% 为提示词，40% 为代码，这套规范每天经过几十万工程师验证。

---

## 一、指令优先级体系（五级禁令）

所有约束按严重程度分级，避免"所有禁令都是 NEVER"导致的狼来了效应。

| 级别 | 语义 | 适用场景 | 示例 |
|------|------|----------|------|
| **CRITICAL** | 绝对不可违反 | 不可逆损失（删数据、泄露密钥、覆盖生产环境） | `CRITICAL: Do NOT execute DELETE on production DB` |
| **NEVER** | 禁止，功能级错误 | 会导致功能错误或逻辑混乱的行为 | `NEVER: Call tools in compact mode` |
| **IMPORTANT** | 质量项，容易遗忘 | 代码风格、边界检查、安全习惯 | `IMPORTANT: Validate all user inputs` |
| **Do NOT** | 一般禁止 | 常规不应做，但后果可控 | `Do NOT: Hardcode paths` |
| **Avoid** | 偏好，有例外 | 通常不推荐，但特定场景可破例 | `Avoid: Deep nesting unless necessary` |

**效果**：AI 对 CRITICAL 约束的遵循率显著提升，因为优先级是区分的，不是平铺的。

---

## 二、Prompt 结构工程

### 2.1 稳定规则前置，易变信息后置

源码使用 `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 显式标记分界线：

- **分界线之前**：稳定规则（角色定义、核心禁令、工具规范）→ **全局缓存**
- **分界线之后**：动态信息（用户问题、上下文、临时状态）→ **每次重算**

> 顺序错误 = 每次调用都在浪费 cache。

### 2.2 关键约束首尾夹逼

长 prompt 中间内容容易被注意力稀释。同一关键约束在头部和尾部各写一次：

```markdown
[头部] CRITICAL: Do NOT call any tools in this mode.
...
[长内容：上下文、分析、推理]
...
[尾部] REMINDER: Do NOT call any tools in this mode.
```

### 2.3 显式标记优于隐式假设

不要在 prompt 中依赖"AI 应该懂"的隐含知识。所有行为假设必须显式声明。

---

## 三、教学范式：示范 > 描述

### 3.1 正反例对照（Anti-pattern + Pattern）

复杂指令不写说明书，直接给：

1. **错误写法**（标注 `Anti-pattern`）
2. **正确写法**（精确到文件路径、行号、参数）

```markdown
## Anti-pattern
```python
# 模糊，AI 容易猜错
fix_the_bug()
```

## Correct
```python
# File: src/auth/login.py:142
# Function: validate_token()
# Change: Add expiry check before signature verification
```
```

### 3.2 精确坐标原则

所有引用必须精确到：
- 文件路径
- 行号或函数名
- 参数名或配置键

禁止模糊引用如"那个文件"、"相关函数"。

---

## 四、上下文管理

### 4.1 缓存感知设计

- 静态内容（角色定义、工具 schema、核心规则）放在 prompt 前部，利用 KV cache
- 动态内容（用户输入、对话历史、检索结果）放在后部
- 避免在动态区重复静态规则

### 4.2 注意力窗口优化

- 关键信息放在 prompt 前 1/3 或后 1/3（注意力两端更强）
- 中间区域放辅助性、可丢失的上下文
- 超长上下文时，关键约束必须重复出现

---

## 五、工具与行为控制

### 5.1 工具使用显式门控

不要给 AI 工具然后期望它"聪明地"决定用不用。而是：

```markdown
Before calling any tool, you MUST check:
1. Is this mode allowed to use tools? (see CRITICAL section)
2. Is the user request impossible without a tool?
3. Have you already tried reasoning?
```

### 5.2 输出格式预制

不要只要求"好的输出"，要给出输出模板：

```markdown
Your response MUST follow this structure:

## Analysis
[your reasoning]

## Decision
[your choice]

## Action
[specific next step]
```

---

## 六、质量与验证

### 6.1 自检清单（Self-Review）

在 prompt 末尾加入结构化自检：

```markdown
Before responding, verify:
- [ ] No CRITICAL constraints violated
- [ ] All user questions answered
- [ ] No speculative information presented as fact
- [ ] Output format matches requested template
```

### 6.2 不确定性显式声明

要求 AI 在不确定时显式标注，而不是猜测：

```markdown
If you are uncertain about any fact, you MUST:
1. State the uncertainty explicitly
2. Distinguish between "known" and "inferred"
3. Do NOT present inference as certainty
```

---

## 七、风格与一致性

### 7.1 指令风格统一

- 使用祈使句（Do / Do NOT / MUST / MUST NOT）
- 避免模糊修饰词（尽量、可能、一般来说）
- 同一概念使用同一术语

### 7.2 层级化组织

使用 Markdown 层级（# / ## / ###）+ 编号体系，让 AI 能定位到具体规则。

---

## 八、实际应用：对照优化 CLAUDE.md

### 优化前（平铺禁令）
```markdown
Don't delete files. Never hardcode secrets. Don't ignore errors.
```

### 优化后（分级+结构化）
```markdown
## CRITICAL
- Do NOT execute destructive file operations without explicit user confirmation.
- Do NOT log or output secrets in plaintext.

## NEVER
- Ignore error return values from system calls.

## IMPORTANT
- Validate all file paths before access.
- Check permissions before write operations.

## Avoid
- Deeply nested callbacks; prefer flat async/await.
```

---

## 九、补充范式（待补充完整 21 条）

以下是基于源码风格和社区分析推断的其他常见模式，待你补充具体的条目后整合：

- **渐进披露**：不要一次性给 AI 全部工具，按场景解锁
- **状态机思维**：用显式状态（PLANNING / EXECUTING / REVIEW）控制行为
- **失败模式预设**：在 prompt 中定义"如果 X 失败，做 Y"
- **领域术语表**：专有名词在 prompt 开头定义
- **版本锁定**：引用外部文档时要求版本号

---

## 待办

- [ ] 补充剩余 17 条具体范式的完整列表
- [ ] 每条配上源码中的原始出处或等效示例
- [ ] 整理成可直接粘贴到 CLAUDE.md 的模板格式
- [ ] 制作"提示词优化前后对照表"快速参考版

---

> 核心洞察：AI 的遵循率提升，不是因为 AI 变聪明了，而是因为提示词的**信号强度**和**优先级区分**做对了。
