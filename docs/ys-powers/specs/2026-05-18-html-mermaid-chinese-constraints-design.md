# html command Mermaid 与中文约束设计文档

date: 2026-05-18

## 1. 目标 (Objective)

为 `commands/html.md` 和 `skills/html-anything/SKILL.md` 增加两项约束：
1. **Mermaid 图表支持**：在输入包含流程、架构、代码时，生成可渲染 mermaid 图表的 HTML
2. **中文内容**：生成的 HTML 默认使用中文展示，技术术语保留英文

## 2. 修改范围

### 2.1 `commands/html.md`

在现有 command 中增加以下约束：

- **Mermaid 渲染**：
  - 检测输入中的 ````mermaid` 代码块并渲染
  - 当输入包含代码文件时，自动分析并生成补充流程图（调用关系、模块依赖）
  - 使用 mermaid.js CDN（唯一允许的外部 JS 依赖例外）
  - mermaid 主题必须与 Clockless 设计系统协调

- **中文内容**：
  - 所有用户可见文本使用中文
  - 技术术语保留英文：style 名称、`data-ha-style`、`prefers-reduced-motion`、代码标识符、文件路径

### 2.2 `skills/html-anything/SKILL.md`

在 Design Requirements 章节增加：

#### Mermaid 图表支持

当输入内容包含以下情况时，生成的 HTML 应嵌入 mermaid.js 并渲染图表：
- 输入中存在 ````mermaid` 代码块
- 输入是代码文件，且可以提取出流程、架构、调用关系
- 输入是 markdown/文本，内容涉及流程、状态机、架构描述

实现要求：
- 引入 mermaid.js CDN（这是唯一允许的外部 JS 依赖之一）
- 使用 Clockless token 系统自定义 mermaid 主题（颜色、字体、圆角与页面一致）
- 图表必须响应式，在移动端可滚动查看
- 若 mermaid 渲染失败，提供纯文本 fallback

#### 内容语言规范

默认生成中文内容，除非用户明确要求英文。
- 所有用户可见的标题、描述、按钮文本、标签使用中文
- 技术术语保留英文：style 名称、HTML/CSS/JS 术语、代码标识符、文件路径
- 数据标签、图表坐标轴、图例使用中文
- 避免机器翻译腔，使用自然的中文表达

#### 外部依赖规则调整

当前规则："No external JS/CDN dependencies unless the user explicitly allows them"
修改为："No external JS/CDN dependencies unless the user explicitly allows them. **Exception: mermaid.js is permitted for diagram rendering when the source contains diagram-worthy content.**"

## 3. 测试策略

1. 生成测试 markdown 文档，包含：
   - mermaid 流程图代码块
   - 代码片段
   - 架构描述
2. 使用修改后的 `/html` 命令执行
3. 验证：
   - mermaid 图表是否正确渲染
   - 主题是否与 Clockless 协调
   - 内容是否为中文
   - 技术术语是否保留英文

## 4. 边界

- 不修改除 `commands/html.md` 和 `skills/html-anything/SKILL.md` 之外的其他文件
- 不删除现有功能，只增加约束
- mermaid.js 仅在需要时引入，不强制每个 HTML 都加载
