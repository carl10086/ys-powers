# slack-gif-creator

## 定位

创建针对 Slack 优化的动画 GIF，提供符合 Slack 尺寸约束的验证器和可组合的动画原语（shake、bounce、move 等）。

## 触发时机

- 需要为 Slack 制作表情包（emoji）或消息动图时
- 用户描述类似 "make me a GIF for Slack of X doing Y" 的需求时
- 需要确保 GIF 符合 Slack 的严格大小限制时
- **不适用**：非 Slack 场景的通用 GIF 制作（虽然可用，但优化方向不同）

## 核心能力

1. **Slack 约束验证**：自动检查 GIF 是否符合 Slack 的消息或 emoji 尺寸限制
2. **动画原语**：提供可组合的动画基础模块：
   - **Shake**（抖动）
   - **Bounce**（弹跳）
   - **Move**（移动）
   - **Kaleidoscope**（万花筒）
3. **尺寸优化策略**：针对 Slack 的严格限制提供优化建议
4. **辅助工具**：文本渲染、颜色处理、特效叠加等可选工具

## Slack GIF 规格

| 类型 | 最大尺寸 | 推荐尺寸 | FPS | 颜色 | 时长 |
|------|---------|---------|-----|------|------|
| **消息 GIF** | ~2 MB | 480×480 | 15-20 | 128-256 | 2-5s |
| **Emoji GIF** | 64 KB | 128×128 | 10-12 | 32-48 | 1-2s |

## Emoji GIF 优化策略

- 限制总帧数 10-15 帧
- 使用 32-48 色
- 设计简洁，避免渐变
- 频繁验证文件大小

## 验证器使用

```python
from core.validators import validate_gif, is_slack_ready

# 完整验证
all_pass, results = validate_gif('emoji.gif', is_emoji=True)

# 快速检查
if is_slack_ready('emoji.gif', is_emoji=True):
    print("Ready to upload!")
```

## 与 ys-powers 的关联

- **与 canvas-design / image-enhancer 的关系**：`canvas-design` 创作静态视觉艺术，`image-enhancer` 优化现有图片，`slack-gif-creator` 创作 Slack 专用动画。三者覆盖「静→动→优化」的完整视觉生产链路
- **借鉴价值**：其「约束验证器 + 可组合原语」的设计模式可复用到任何需要「在严格约束下创作」的场景（如社交媒体内容、邮件签名、小程序素材）
- **搬运建议**：低价值。功能高度聚焦 Slack 生态，适用面较窄

## 元信息

- 来源：`refer/awesome-claude-skills/slack-gif-creator/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
