# theme-factory

## 定位

为幻灯片、文档、报告或 HTML 页面应用专业字体与配色主题的工具包。内置 10 套预设主题，每套包含协调的调色板和字体搭配。

## 触发时机

- 需要统一多份文档或幻灯片的视觉风格时
- 创建演示文稿希望快速应用专业配色时
- 需要为不同受众（商务、创意、学术）选择合适视觉风格时
- 现有主题都不满足需求，需要生成自定义主题时
- **不适用**：已有明确品牌规范且需严格遵守时（此时用 `brand-guidelines`）

## 核心能力

1. **10 套预设主题**：涵盖多种视觉风格：
   - Ocean Depths（海洋深蓝，专业冷静）
   - Sunset Boulevard（暖色活力，温暖鲜明）
   - Forest Canopy（自然大地色，沉稳 grounded）
   - Modern Minimalist（灰度极简，干净现代）
   - Golden Hour（秋意浓，丰富温暖）
   - Arctic Frost（冷色 crisp，冬感清爽）
   - Desert Rose（柔粉 dusty，精致优雅）
   - Tech Innovation（ bold 科技，现代 bold）
   - Botanical Garden（清新有机，花园色调）
   - Midnight Galaxy（深邃宇宙，戏剧感强）

2. **主题展示**：通过 `theme-showcase.pdf` 直观展示所有主题效果
3. **一键应用**：选中主题后自动将配色和字体应用到整个 artifact
4. **自定义主题**：基于用户描述生成新的配色和字体组合

## 指令流程概览

1. **展示主题库**：向用户展示 `theme-showcase.pdf`
2. **获取选择**：询问用户偏好哪个主题
3. **等待确认**：获得明确的主题选择
4. **应用主题**：读取对应主题文件并统一应用到 artifact

## 与 ys-powers 的关联

- **与 brand-guidelines 的关系**：`brand-guidelines` 强制执行特定品牌规范（Anthropic），`theme-factory` 提供灵活的视觉风格选择。前者是「约束」，后者是「选择」
- **与 canvas-design 的关系**：`canvas-design` 创作原创视觉艺术，`theme-factory` 应用标准化设计系统。两者互补
- **借鉴价值**：其「展示 → 选择 → 应用」的三步流程是任何「样式配置」功能的通用模式
- **搬运建议**：中等价值。适合需要频繁创建演示文稿或文档的团队。注意 theme 定义依赖 `themes/` 目录下的具体文件

## 元信息

- 来源：`refer/awesome-claude-skills/theme-factory/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
