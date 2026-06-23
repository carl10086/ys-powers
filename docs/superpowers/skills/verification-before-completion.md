# verification-before-completion

**定位**：在声称任何工作完成、修复或通过之前，强制出示刚跑过的验证证据。

**触发条件**：准备说“完成了”“修好了”“测试通过了”“可以合并了”等任何积极状态声明之前。

---

## Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

如果本消息里还没跑过验证命令，就不能声称它通过。

## Gate Function

```
IDENTIFY → RUN → READ → VERIFY → CLAIM
```

1. **IDENTIFY**：什么命令能证明这个 claim？
2. **RUN**：完整执行该命令（freshly，不是之前的结果）。
3. **READ**：完整读输出、检查退出码、统计失败数。
4. **VERIFY**：输出是否确认 claim？
5. **CLAIM**：只有第 4 步为 yes 时才能声明。

跳过任何一步 = 撒谎，不是验证。

## 常见失败

| Claim | 需要 | 不足够 |
|---|---|---|
| 测试通过 | 测试命令输出：0 failures | 上次跑过、“应该会过” |
| Linter 干净 | Linter 输出：0 errors | 部分检查、推断 |
| 构建成功 | 构建命令 exit 0 | Linter 通过、日志看起来正常 |
| Bug 修复 | 复现原症状测试通过 | 代码改了、想当然 |
| 回归测试有效 | 红-绿循环验证 | 测试只跑过一次 |
| 需求满足 | 逐条 checklist 验证 | 测试通过 |

## 红旗信号

- 使用 should / probably / seems。
- 在验证前表达满意（“Great!”“Done!”“Perfect!”）。
- 未验证就提交 / PR。
- 相信 agent 的“成功”报告。
- 依赖部分验证。
- “就这一次”。

## 回归测试红-绿

1. 写能复现 bug 的测试，运行，确认失败。
2. 应用修复，运行，确认通过。
3. 回滚修复，运行，确认失败。
4. 恢复修复，运行，确认通过。

只有这样才能证明测试真正抓住了 bug。

## 适用范围

- 任何成功/完成/正确性的表达。
- 同义词、暗示、转述都包括在内。
- 提交、PR、任务完成、委派 agent 之前。

> **Run the command. Read the output. THEN claim the result.**
