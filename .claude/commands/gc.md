---
description: 智能 Git 工作流：分支创建、提交、推送、PR 一步完成
---

<CRITICAL>
- 永远不 force push 到 main/master
- 永远不提交包含密钥/token/credentials 的变更
</CRITICAL>

<NEVER>
- 不要跳过 Git 冲突解决直接提交
- 不要在未确定分支前缀正确前执行 push
</NEVER>

<IMPORTANT>
- commit message 用 commitizen 格式：type(scope): 描述
- 描述 ≤50 字，动词开头
- 分支名格式：{前缀}{简短描述-月日}
</IMPORTANT>

<Do NOT>
- 不要 hardcode 路径
- 不要自动合并冲突（除非用户明确授权）
</Do NOT>

---

## 流程

```
分析变更 → 确定分支 → 执行推送 → 打开 PR
```

### 1. 分析 → 确定分支前缀

根据变更类型选择前缀：

| 变更类型 | 分支前缀 | 示例 |
|---------|---------|------|
| 新功能 | feature/ | feature/user-auth-0414 |
| Bug 修复 | fix/ | fix/login-crash-0414 |
| 重构 | refactor/ | refactor/api-cleanup-0414 |
| 文档 | docs/ | docs/readme-0414 |
| 格式调整 | style/ | style/formatting-0414 |
| 测试 | test/ | test/add-tests-0414 |
| 构建/工具 | chore/ | chore/deps-upgrade-0414 |

### 2. 执行 Git 操作

```bash
# 创建并切换分支
git checkout -b {前缀}{简短描述-月日}

# 暂存所有变更
git add .

# 提交（commitizen 格式）
git commit -m "type(scope): 简短描述"
```

**Commit 格式：**
- `type`: feat | fix | refactor | docs | style | test | chore
- `scope`: 模块/功能名（可选）
- `描述`: ≤50字，动词开头

**示例：**
```
feat(auth): 添加 JWT 登录
fix(order): 修复订单页面白屏问题
```

### 3. 推送 → 打开 PR

```bash
# 推送分支
git push -u origin HEAD
```

**自动打开 PR：**
推送成功后，使用 chrome devtools 打开 PR 页面：

```javascript
mcp__chrome-devtools__new_page("https://github.com/carl10086/{repo}/pull/new/{branch}")
```

## 执行后自检

- [ ] 分支名符合 {前缀}{描述-月日} 规范
- [ ] commit message 格式正确
- [ ] 没有 secrets/keys/tokens 泄露
- [ ] push 到远程成功

## 特殊情况

| 情况 | 处理 |
|------|------|
| 分支已存在 | `git checkout {分支名}` 切换 |
| 推送失败 | 重试一次，仍失败提示用户 |
| 无变更 | 提示"无变更可提交" |
| 冲突 | 提示用户解决后继续 |

---

REMINDER: 检查分支名是否符合规范，确保没有 secrets 泄露。
