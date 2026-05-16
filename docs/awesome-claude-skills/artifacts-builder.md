# artifacts-builder

## 定位

使用 React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui 构建复杂、多组件的 Claude.ai HTML Artifacts。适合需要状态管理、路由或 shadcn/ui 组件的交互式 artifact，不适用于简单的单文件 HTML。

## 触发时机

- 需要创建多组件、有状态管理的交互式 artifact 时
- 需要使用 shadcn/ui 的 40+ 预制组件时
- 需要将 React 应用打包为单文件 HTML 分享给用户时
- **不适用**：简单的单文件 HTML / JSX artifact（直接用 Claude 原生能力即可）

## 核心能力

1. **一键初始化**：通过 `scripts/init-artifact.sh` 创建预配置项目，含 React + TypeScript + Tailwind + shadcn/ui + 路径别名
2. **40+ 组件开箱即用**：shadcn/ui 组件及所有 Radix UI 依赖已预装
3. **自动打包**：通过 `scripts/bundle-artifact.sh` 使用 Parcel 将项目内联为单文件 `bundle.html`
4. **Node 18+ 兼容**：自动检测并固定 Vite 版本

## 指令流程概览

1. **初始化项目**：运行 `bash scripts/init-artifact.sh <project-name>`，生成完整项目结构
2. **开发 Artifact**：编辑生成的文件，参考 shadcn/ui 文档构建界面
3. **打包输出**：运行 `bash scripts/bundle-artifact.sh`，生成自包含的 `bundle.html`
4. **分享给用户**：将 `bundle.html` 作为 artifact 在对话中展示
5. **（可选）测试**：使用 Playwright / Puppeteer 验证，但建议先展示再按需测试

## 设计规范

Skill 明确强调避免 "AI slop"：
- 避免过度居中对齐
- 避免紫色渐变
- 避免统一的圆角
- 避免默认使用 Inter 字体

## 与 ys-powers 的关联

- **与 html-anything skill 的关系**：`artifacts-builder` 聚焦前端组件化 artifact 开发，`html-anything` 聚焦将任意输入转换为精美 HTML 页面。两者互补：前者是「开发工具」，后者是「输出格式化工具」
- **借鉴价值**：其「反 AI slop」设计指南可直接纳入 ys-powers 的 UI 相关 skill 中
- **搬运建议**：ys-powers 中暂无同类前端 artifact 构建 skill，若团队需要频繁构建复杂交互式 artifact，值得搬运

## 元信息

- 来源：`refer/awesome-claude-skills/artifacts-builder/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
