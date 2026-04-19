# QMD 记忆系统设计方案

## 目标

为 Claude Code 构建一个基于 qmd 的记忆能力：
- 每次解决问题后，提取关键信息生成 SOP 记忆
- 下次遇到类似问题时，AI 自动检索历史记忆供参考

---

## 核心流程

### 1. 写入记忆

```
用户: /remember "解决了 XX 项目的登录认证问题"

AI 自动:
  1. 从 session 历史提取关键信息
  2. 生成 SOP 记忆文件
  3. 写入 .memory/sop-YYYYMMDD-xxx.md
  4. 确认已保存
```

### 2. 查询记忆

```
用户: "我的登录功能有 bug"

AI 自动:
  1. 搜 .memory/ 有无相关记忆
  2. 呈现找到的相关记忆给用户确认
  3. 用户确认后，AI 参考记忆开始解决
```

### 3. CLAUDE.md 配置

在项目的 CLAUDE.md 中添加规则：

```markdown
## 记忆系统

开始新任务前，先搜索 `.memory/` 目录：
- 使用 qmd query 或 search 检索相关记忆
- 找到相关内容时，提示用户是否参考

如需保存当前任务的解决方案：
- 使用 /remember "<一句话描述解决的问题>"
```

---

## SOP 记忆文件格式

每个记忆文件放在项目根目录的 `.memory/` 下：

```
.my-project/
├── .memory/
│   ├── sop-20260417-001-auth-bugfix.md
│   ├── sop-20260418-002-database-migration.md
│   └── sop-20260419-003-api-integration.md
```

### YAML Frontmatter 结构

```yaml
---
title: "SOP: 修复登录认证 bug"
created: 2026-04-17
tags:
  - auth
  - login
  - bug-fix
  - session
project: my-project
summary: "解决了 JWT token 过期后无法自动刷新的问题"
related:
  - "参考: api-integration 项目的 token 处理逻辑"
---

## 背景

用户反馈登录后一段时间无操作会掉线，需要重新登录。

## 解决方案

1. 在前端添加 token 自动刷新机制
2. 刷新失败时优雅降级到登录页
3. 关键文件: `src/auth/session.ts`

## 关键命令

```bash
# 测试 token 刷新
npm test auth/session
```

## 关键决策

- 采用双 token 方案：access token + refresh token
- refresh token 存 httpOnly cookie
```

---

## QMD 配置方案

### Collection 管理

所有项目的 `.memory/` 统一索引：

```bash
# 添加所有项目的记忆文件夹
qmd collection add ~/.memory/projects/project-a/.memory --name memory
qmd collection add ~/.memory/projects/project-b/.memory --name memory

# 全局上下文
qmd context add qmd://memory "Carl 的项目经验记忆库"
qmd context add qmd://memory/project-a "Project A 的记忆"
```

### 简化方案（推荐）

如果所有 `.memory/` 在统一父目录下，可以只添加父目录：

```bash
qmd collection add ~/.memory --name memory
qmd context add qmd://memory "Carl 的项目 SOP 记忆库"
```

### Context 树结构

```
qmd://memory                          # 全局根
├── project-a                         # 项目级
│   ├── auth                          # 分类级
│   └── database
└── project-b
```

---

## 搜索策略

### AI 自动生成 Query

当用户描述问题时，AI 自动生成查询词：

```
用户: "我的登录功能有 bug"

AI 生成的 query:
- "login auth session token bug"
- "认证 登录 token 会话"
```

### qmd 搜索命令

```bash
# 混合搜索（推荐）
qmd query "login auth bug"

# 关键词搜索
qmd search "auth login"

# 语义搜索
qmd vsearch "session timeout"
```

### 搜索结果处理

AI 收到结果后：

```markdown
找到 2 条相关记忆：

1. **[Project A] SOP: 修复登录认证 bug** (2026-04-17)
   - 路径: project-a/.memory/sop-20260417-001.md
   - 摘要: JWT token 过期后无法自动刷新的问题
   - 相关度: 85%

2. **[Project B] SOP: 解决 API token 刷新问题** (2026-04-15)
   - 路径: project-b/.memory/sop-20260415-003.md
   - 摘要: refresh token 处理逻辑
   - 相关度: 72%

是否参考以上记忆？[Y/n]
```

---

## 实现步骤

### Phase 1: 基础配置（手动）

1. 在各项目创建 `.memory/` 目录
2. 配置 qmd collection
3. 在项目 CLAUDE.md 添加记忆规则

### Phase 2: Skill 开发

1. 开发 `/remember` skill
   - 从 session 历史提取关键信息
   - 生成 SOP 文件
   - 写入 `.memory/`

### Phase 3: 可选增强

- PreToolUse Hook 自动查询
- 自动判断是否需要查记忆

---

## 注意事项

1. **不要自动索引**：qmd 的 collection add/embed 不会自动运行
2. **手动更新**：`qmd update` 增量更新索引
3. **隐私**：记忆内容是纯文本，存放在本地 .memory/
4. **版本控制**：建议 .memory/ 加入 .gitignore，除非你想把 SOP 也提交到 git
