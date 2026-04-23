---
name: doc-codebase
description: 分析项目代码库架构并生成 ARCHITECTURE.md 到 docs/codebase/，用于项目 onboarding、重构前了解现状、或更新过期架构文档
---

# 代码库架构映射

分析当前项目代码库，生成结构化的架构文档到 `docs/codebase/ARCHITECTURE.md`。

## 使用时机

- 新项目 onboarding 时理解代码库结构
- 重大重构或添加功能前了解当前状态
- 架构文档过期或缺失时更新

## 约束

<CRITICAL>
- 生成的文档必须写入 `docs/codebase/ARCHITECTURE.md`
- 如果 `docs/codebase/` 目录不存在，先创建它
- 绝不读取 `.env`、密钥文件等敏感内容
</CRITICAL>

<NEVER>
- 不要输出到 `.planning/codebase/`（这是 gsd 的路径）
- 不要使用描述性语言（"项目使用 X"），必须使用规定性语言（"Use X pattern"）
- 不要自己发明文档结构，必须遵循标准模板
</NEVER>

<IMPORTANT>
- 必须阅读关键文件的内容，不能只做 `ls` 和 `find`
- 每个架构描述必须包含具体的文件路径（用反引号包裹）
- 至少阅读 3-5 个关键文件的完整内容
</IMPORTANT>

## 流程

```
检查现有文档 → 探索代码库 → 生成 ARCHITECTURE.md → 确认输出
```

### 1. 检查现有文档

检查 `docs/codebase/ARCHITECTURE.md` 是否已存在：

```bash
ls -la docs/codebase/ARCHITECTURE.md 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

- 如果存在：告知用户当前文档的行数和最后修改时间，询问是否覆盖
- 如果不存在：创建 `docs/codebase/` 目录

### 2. 探索代码库

阅读以下关键文件（根据项目类型选择）：

**依赖文件：**
```bash
ls package.json Cargo.toml go.mod requirements.txt pyproject.toml pom.xml build.gradle 2>/dev/null
```

**入口文件：**
```bash
ls src/index.* src/main.* src/app.* app/page.* 2>/dev/null
```

**配置文件：**
```bash
ls tsconfig.json vite.config.* .eslintrc.* 2>/dev/null
```

**核心模块：**
- 选择 3-5 个关键业务逻辑文件，阅读其完整内容
- 判断标准：如果删除它项目就无法运行，它就是关键文件

### 3. 生成 ARCHITECTURE.md

写入 `docs/codebase/ARCHITECTURE.md`，必须包含以下章节：

| 章节 | 内容要求 |
|------|---------|
| **Pattern Overview** | 架构模式名称（如 MVC、微服务、分层架构等），3-5 个关键特征 |
| **Layers** | 每层职责、位置、包含内容、依赖关系、使用方 |
| **Data Flow** | 请求/数据如何流经各层，状态管理方式 |
| **Key Abstractions** | 核心接口/类/模块的用途、示例文件、使用的模式 |
| **Entry Points** | 程序启动位置、触发方式、职责 |
| **Error Handling** | 错误处理策略和具体模式 |
| **Cross-Cutting Concerns** | 日志、验证、认证等横切关注点的实现方式 |
| **Where to Add New Code** | 新功能、新模块、新测试的放置位置指南 |

**写作要求：**
- 使用规定性语言："Use X pattern"、"Place Y in Z"、"Follow W convention"
- 每个描述包含 `具体文件路径`（反引号包裹）
- 只描述当前状态，不用过去时或将来时
- 包含代码示例展示实际模式

### 4. 安全扫描

生成完成后，扫描文档是否意外包含敏感信息：

```bash
grep -E '(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36}|-----BEGIN.*PRIVATE KEY|eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.)' docs/codebase/ARCHITECTURE.md 2>/dev/null && echo "SECRETS_FOUND" || echo "CLEAN"
```

如果发现敏感信息，必须删除后重新生成。

### 5. 确认输出

返回生成结果：

```
代码库架构映射完成。

文件：docs/codebase/ARCHITECTURE.md
行数：[N] 行

包含章节：
- Pattern Overview（架构模式）
- Layers（分层及职责）
- Data Flow（数据流）
- Key Abstractions（关键抽象）
- Entry Points（入口点）
- Error Handling（错误处理）
- Cross-Cutting Concerns（横切关注点）
- Where to Add New Code（新代码放置指南）

关键发现：
- [发现 1]
- [发现 2]
- [发现 3]
```

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 只扫描目录不读代码 | 阅读关键文件的实现逻辑 |
| "项目使用 camelCase" | "Use camelCase for functions" |
| "UserService 处理用户逻辑" | "`src/services/user.ts` 中的 UserService 处理用户逻辑" |
| 遗漏 "Where to Add New Code" | 必须包含新代码放置指南 |
| 读取 .env 内容 | 只记录存在性："`.env` 存在 — 包含环境配置" |

## 理性化借口

当想偷懒时，这些想法会出现：

| 借口 | 现实 |
|------|------|
| "目录结构已经说明一切" | 目录结构只看表面，代码逻辑才能说明架构 |
| "描述性语言更安全，不会错" | 描述性语言对未来开发者没有指导作用 |
| "文件路径太长影响阅读" | 没有文件路径的文档无法导航到具体代码 |
| "模板太死板，我想灵活处理" | 标准模板确保所有关键信息都被覆盖，不遗漏 |
| "我已经看了足够多的文件" | 关键文件必须读到，不能凭感觉判断 |
| "这个项目太简单不需要深入" | 简单项目的架构文档可以更短，但关键文件仍要读 |
| "我先写个初稿，后续再补充" | 初稿如果没有文件路径和规定性语言，后续也不会补充 |

## 红旗检查清单

生成完成后自检，出现以下任何一条 = 文档不合格，必须重写：

- [ ] 文档中没有反引号包裹的文件路径
- [ ] 章节标题与标准模板不符（缺少 Pattern Overview / Layers / Data Flow / Key Abstractions / Entry Points / Error Handling / Cross-Cutting Concerns / Where to Add New Code 中任意一个）
- [ ] 只有 "项目使用 X" 而没有 "Use X"
- [ ] 读取了 `.env` 或其他敏感文件内容
- [ ] 只探索了目录结构，没有阅读任何代码文件内容
