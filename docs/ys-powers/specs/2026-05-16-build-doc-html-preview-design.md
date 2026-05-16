# Spec: 为 build-doc 添加 HTML Preview 步骤

## Objective

为 `build-doc` command 在工作流尾部追加一个**强制**的 HTML 预览步骤。每次完成一个文档任务后，自动将刚保存的 Markdown 转为单文件 HTML 并在浏览器中打开，方便阅读、审阅与分享。

设计灵感来自此前 `commands/spec.md` 中的 Phase 4（commit `7560e6b` 引入，commit `<本次改动前>` 删除）。从删除后的实际使用感受出发，用户判断：

- spec 是工程产物，HTML 预览价值中等，删除可接受。
- 文档（build-doc 产物）天然以"被阅读"为目的，HTML 预览价值高，**应当强制存在**。

因此本次将 spec 已废弃的 Phase 4 模板搬迁并强化到 build-doc。

## Tech Stack

- 既有 `html-generator` subagent（位于本仓库 agents 配置）
- 既有 `skills/html-anything/SKILL.md`（Output Path Rule）
- Chrome DevTools MCP（`mcp__chrome-devtools__navigate_page`）

无新增依赖。

## Commands

无新增 CLI 命令。改动仅作用于 `/build-doc` 这个 Claude Code command 的工作流定义。

## Project Structure

```
commands/
  build-doc.md          # 本 spec 的目标改动文件
  spec.md               # 参考：曾经的 Phase 4 模板，已删除

skills/html-anything/
  SKILL.md              # 被引用，不修改
```

## Workflow Changes

`build-doc.md` 当前工作流为 7 步：

```
Step 1: Read plan task
Step 2: Load context
Step 3: Draft content
Step 4: Self-review
Step 5: Fix issues
Step 6: Save
Step 7: Mark complete
```

改动后变为 8 步，新插入的 Step 7 为 HTML 预览，原 Step 7 顺延为 Step 8：

```
Step 1: Read plan task
Step 2: Load context
Step 3: Draft content
Step 4: Self-review
Step 5: Fix issues
Step 6: Save
Step 7: Generate HTML preview and open in browser     ← 新增
Step 8: Mark task complete                            ← 原 Step 7
```

文件顶部的 `Doc Task Progress` checklist 同步增加一行。

## HTML Preview Step 规范

新 Step 7 的内部结构（与 spec.md 之前的 Phase 4 对齐）：

### 触发条件

Step 6 保存 Markdown 文件成功后立即执行。

### Subagent 调用

通过 Agent tool 启动 `html-generator` subagent：

```
Agent tool:
  subagent_type: "html-generator"
  description: "Convert doc to HTML preview"
  prompt: |
    Input: <doc-file-path>
    Input type: file
    Working directory: <current-directory>
    Generate HTML following skills/html-anything/SKILL.md.
    Apply the Output Path Rule and return the result in the specified output format.
```

等待 subagent 返回 HTML 文件路径。

### Browser Open

收到 subagent 返回的 HTML 路径后：

1. 将绝对路径拼成 `file://` URL
2. 调用 `mcp__chrome-devtools__navigate_page` 打开该 URL

### Response to User

在转入 Step 8 前，先以中文向用户报告：

```markdown
**文档已完成**

- 文档路径：`<doc-file-path>`
- HTML 预览：`<html-file-path>`

已在浏览器中打开 HTML 预览版。
如需调整文档内容，直接描述修改需求。
```

### Rules

1. **强制**：每次执行 build-doc 都必须执行 Step 7，**无跳过开关**。
2. HTML 生成必须委派给 `html-generator` subagent，不允许在 primary agent 中直接拼接 HTML。
3. 传给 subagent 的路径必须与 Step 6 实际保存路径完全一致，不做任何变形。
4. 若 Chrome DevTools MCP 不可用导致打开失败，仍应返回 HTML 路径让用户手动打开（fallback 行为）。

## Code Style

- 与现有 `build-doc.md` 保持一致：英文标题、英文工作流叙述、Markdown 代码块描述模板。
- "Response to User" 模板沿用中文（与 spec.md 之前的 Phase 4 完全一致）。
- 新 Step 在文件中的写法仿照 Step 1~6（`**Step 7: ...**` 粗体小标题 + 段落 + 子小节）。

## Testing Strategy

由于改动对象是 prompt 文件而非可运行代码，验证以人审 + 真实运行为主：

1. **静态对照**
   - 顶部 checklist 包含 Step 7 / Step 8 两行
   - 步骤编号 1~8 连续，无跳号
   - Step 7 与 spec.md 历史版本（`git show 7560e6b:commands/spec.md` 的尾部）对照，确认模板核心结构一致，仅文案做了 spec→doc 的替换。
   - Rules 部分**不含**"Skip HTML preview" 这一项

2. **真实运行验证**
   - 在本仓库或一个测试项目中用 `/build-doc` 跑一个真实文档任务
   - 确认：
     - Step 6 保存 md 后自动调用 html-generator
     - HTML 文件被生成且路径返回
     - Chrome 自动打开 file:// URL
     - 用户得到"文档已完成"格式的中文响应

3. **失败回退**
   - 若 Chrome DevTools MCP 调用失败，命令应仍把 HTML 路径返回给用户，而不是中断流程。

## Acceptance Criteria

- [ ] `commands/build-doc.md` 步骤从 7 步增加到 8 步
- [ ] 顶部 `Doc Task Progress` checklist 同步包含 Step 7、Step 8
- [ ] 新 Step 7 内容结构对齐 spec.md 历史 Phase 4，文案做了 spec→doc 替换
- [ ] Rules 不含跳过开关
- [ ] 真实运行 `/build-doc` 一次能看到 md 保存 → HTML 生成 → 浏览器打开的完整链路

## Boundaries

**Always do（一定做）：**

- 复用既有 `html-generator` subagent
- 复用既有 `skills/html-anything/SKILL.md` 的 Output Path Rule
- 文案、模板与 spec.md 之前的 Phase 4 保持高一致度

**Ask first（先确认再做）：**

- 是否同时把"强制 HTML 预览"语义反映到 `description:` frontmatter（默认不动 description，避免影响 skill 触发条件）
- 是否需要给生成的 HTML 路径附带任何元数据（默认不加）

**Never do（绝不做）：**

- 不在 primary agent 中直接生成 HTML
- 不修改 `skills/html-anything/SKILL.md`
- 不恢复 `commands/spec.md` 中已删除的 Phase 4（spec 与 doc 是两条独立判断）
- 不为新 Step 引入额外的 CLI 工具、外部服务或新 MCP

## Open Questions

无。Phase 1 探讨中三个关键问题已确认：

1. 触发时机：仅当前任务 md 保存后做单文件预览
2. 浏览器：自动打开（与历史 Phase 4 一致）
3. 强制程度：强制生成，无跳过开关
