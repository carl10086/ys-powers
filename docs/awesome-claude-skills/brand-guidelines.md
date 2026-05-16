# brand-guidelines

## 定位

将 Anthropic 官方品牌色与字体应用到任意需要统一视觉风格的 Artifact 中，确保输出符合 Anthropic 的品牌识别标准。

## 触发时机

- 需要保持与 Anthropic 品牌一致的视觉风格时
- 创建对外展示的公司级文档、幻灯片或报告时
- 用户明确要求使用 Anthropic 品牌色或字体时
- **不适用**：纯内部草稿、无品牌要求的个人项目

## 核心能力

1. **品牌色自动应用**：主色（Dark `#141413`、Light `#faf9f5`）、强调色（Orange `#d97757`、Blue `#6a9bcc`、Green `#788c5d`）自动适配背景
2. **字体智能切换**：标题使用 Poppins（回退 Arial），正文使用 Lora（回退 Georgia），自动处理字体缺失情况
3. **图形着色**：非文本形状循环使用橙、蓝、绿三色作为点缀
4. **文本层级保持**：在应用品牌样式的同时保留原有文本结构和格式

## 指令流程概览

1. 识别 artifact 中需要应用品牌的元素（文本、形状、背景）
2. 根据背景明暗自动选择主色或反色
3. 标题（24pt+）应用 Poppins 字体，正文应用 Lora 字体
4. 非文本图形元素依次分配橙、蓝、绿强调色
5. 输出符合 Anthropic 品牌规范的格式化结果

## 技术细节

- 颜色通过 RGB 值精确匹配，使用 `python-pptx` 的 `RGBColor` 类实现
- 字体依赖系统预装，无字体时自动回退到 Arial / Georgia
- 无需额外安装字体即可工作，但预装 Poppins 和 Lora 可获得最佳效果

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 中暂无专门的品牌/视觉规范 skill，`brand-guidelines` 可作为前端/UI 相关输出的样式基准
- **借鉴价值**：其「主色 + 强调色循环」的配色模式可借鉴到 `html-anything` 等生成 HTML 的 skill 中
- **搬运建议**：价值中等，若 ys-powers 经常需要输出带品牌一致性要求的文档，可搬运

## 元信息

- 来源：`refer/awesome-claude-skills/brand-guidelines/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
