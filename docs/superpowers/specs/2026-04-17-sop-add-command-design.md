# SOP-ADD 命令设计方案

## 目标

实现 `/sop-add` 命令，从当前 session 历史自动提取关键信息，生成 SOP 文件供后续参考。

## 用户流程

```
用户: /sop-add
  ↓
AI 自动从 session 历史提取信息
  ↓
生成 SOP 预览，显示给用户
  ↓
用户确认 (y/n)
  ↓
保存到 ./sop/sop-YYYYMMDD-NNN.md
  ↓
显示保存路径
```

## 命令定义

**文件**: `commands/sop-add.md`

**调用方式**: `/sop-add`

**前置条件**: 有可提取的 session 历史

**交互模式**: 预览确认模式

## SOP 文件格式

**输出目录**: `./sop/`

**命名规则**: `sop-{日期}-{序号}.md`

示例: `sop-20260417-001.md`

### 文件内容模板

```yaml
---
title: "SOP: {标题}"
created: {日期 YYYY-MM-DD}
tags:
  - {标签1}
  - {标签2}
project: {项目名}
summary: "{一句话摘要}"
---

## 背景

{问题背景描述}

## 解决方案

1. {步骤1}
2. {步骤2}
3. {步骤3}

## 关键文件

- `{文件路径1}`
- `{文件路径2}`

## 关键命令

```bash
{命令1}
{命令2}
```

## 关键决策

- {决策点1}
- {决策点2}
```

## AI 提取策略

### 从 session 历史提取的内容

1. **标题**: 从对话中推断解决的问题类型
2. **标签**: 基于问题领域关键词 (auth, database, api, bug-fix, refactor 等)
3. **摘要**: 一句话描述解决方案
4. **背景**: 问题描述或用户反馈
5. **解决方案**: 具体的修复/实现步骤
6. **关键文件**: 涉及的文件路径
7. **关键命令**: 执行的测试/构建命令
8. **关键决策**: 技术选型或架构决策

### 提取优先级

| 优先级 | 内容 | 说明 |
|--------|------|------|
| P1 | 标题 + 摘要 | 必须提取 |
| P1 | 解决方案步骤 | 必须提取 |
| P2 | 背景 | 从对话中推断 |
| P2 | 关键文件 | 从 git diff 或对话中提取 |
| P3 | 关键命令 | 从对话中提取 |
| P3 | 关键决策 | 从对话中推断 |

### 自动标签规则

根据内容关键词自动打标签:

| 关键词 | 标签 |
|--------|------|
| login, auth, token, session, JWT | auth |
| database, db, migration, query | database |
| api, endpoint, REST, GraphQL | api |
| bug, fix, error, crash | bug-fix |
| refactor, restructure | refactor |
| test, unit, integration | testing |
| config, env, setting | config |
| deploy, build, ci | deploy |

## 交互细节

### 预览显示

```
已生成 SOP 预览:

---
title: "SOP: 修复登录认证 bug"
created: 2026-04-17
tags: [auth, bug-fix]
summary: "JWT token 过期后无法自动刷新的问题"
---

## 背景
...

## 解决方案
...

---
是否保存? (y/n)
```

### 序号生成规则

- 每日序号从 001 开始
- 检查 `./sop/` 目录下当日已有的文件，自动递增

### 目录不存在时

自动创建 `./sop/` 目录

## 实现步骤

1. 创建 `commands/sop-add.md` 命令文件
2. 实现 AI 提示词，指导如何从 session 提取信息
3. 定义 SOP 模板格式
4. 添加预览和确认交互
5. 实现文件保存逻辑

## 验收标准

- [ ] `/sop-add` 能正确从 session 历史提取信息
- [ ] 生成符合模板格式的 SOP 文件
- [ ] 预览内容正确显示
- [ ] 用户确认后保存到 `./sop/` 目录
- [ ] 序号自动递增
- [ ] 目录不存在时自动创建
