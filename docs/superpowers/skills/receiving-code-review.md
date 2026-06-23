# receiving-code-review

**定位**：收到代码审查反馈后，用技术严谨性而非社交表演来处理它。

**触发条件**：收到 review 反馈，准备按建议修改，尤其是反馈看起来不清楚或技术上可疑时。

---

## 响应模式

```
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
```

1. **READ**：完整读完反馈，先不反应。
2. **UNDERSTAND**：用自己的话重述需求，或提问澄清。
3. **VERIFY**：对照代码库现实检查。
4. **EVALUATE**：对这个代码库来说技术上是否正确？
5. **RESPOND**：技术确认或有理由的 push back。
6. **IMPLEMENT**：一次改一项，每项测试。

## 禁止的回应

- “You’re absolutely right!”
- “Great point!” / “Excellent feedback!”
- “Let me implement that now”（未验证前）

应替换为：

- 重述技术要求。
- 提出澄清问题。
- 用技术理由 push back。
- 直接开始改。

## 处理不清晰反馈

只要有任何一项不清楚，就停下来先问。部分理解 = 错误实现。

## 来源差异

- **来自 human partner**：可信，但范围不清时仍需确认。
- **来自外部 reviewer**：必须检查是否适合本代码库、是否破坏现有功能、是否理解完整上下文。

## YAGNI 检查

如果 reviewer 建议“实现得更专业”，先 grep 代码库确认该功能是否真被使用：

- 未被使用 → 建议删除。
- 被使用 → 再实现。

## 修改顺序

1. 阻塞性问题（破坏、安全）。
2. 简单修复（typo、import）。
3. 复杂修复（重构、逻辑）。
4. 每项单独测试。
5. 验证无回归。

## GitHub 评论回复

对 inline 评论使用 `gh api repos/.../pulls/.../comments/.../replies`，不要发成顶层 PR 评论。
