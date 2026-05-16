# image-enhancer

## 定位

提升图像和截图的质量，包括分辨率放大、锐度增强和清晰度优化，使图片更适合用于演示、文档和社交媒体。

## 触发时机

- 需要为博客或文档优化截图质量时
- 分享图片到社交媒体前需要提升视觉效果时
- 低分辨率图片需要放大使用（如投影展示）时
- 压缩导致的马赛克或模糊需要修复时
- **不适用**：原始图片质量极差（超出算法修复范围）或需要专业级照片后期处理时

## 核心能力

1. **质量分析**：检查分辨率、锐度和压缩损伤程度
2. **智能放大**：将图片 upscale 到更高分辨率（如 Retina 级别）
3. **锐化增强**：强化边缘和细节，提升文字可读性
4. **降噪修复**：清理压缩伪影和噪点
5. **场景优化**：根据用途（Web、印刷、社交媒体）调整输出参数

## 指令流程概览

1. 分析输入图片的当前规格（分辨率、格式、质量缺陷）
2. 根据用户需求确定增强方向（放大、锐化、降噪、综合优化）
3. 应用对应的图像处理算法
4. 输出优化后的图片，同时保留原始文件作为备份

## 输出示例

```
Analyzing screenshot-2024.png...

Current specs:
- Resolution: 1920x1080
- Format: PNG
- Quality: Good, slight blur

Enhancements applied:
✓ Upscaled to 2560x1440 (retina)
✓ Sharpened edges
✓ Enhanced text clarity
✓ Optimized file size

Saved as: screenshot-2024-enhanced.png
Original preserved as: screenshot-2024-original.png
```

## 常见场景

- **博客写作**：提升截图清晰度后再发布
- **技术文档**：让 UI 截图更易于阅读
- **社交媒体**：按平台尺寸优化图片
- **演示文稿**：放大图片适应大屏幕
- **印刷材料**：提升分辨率用于实体输出

## 与 ys-powers 的关联

- **与 canvas-design 的关系**：`canvas-design` 负责「创建视觉艺术」，`image-enhancer` 负责「优化现有图像」。两者互补
- **借鉴价值**：其「分析 → 增强 → 保留原图」的安全处理流程可作为任何媒体处理 skill 的模板
- **搬运建议**：中等价值。截图优化是常见需求，但图像处理依赖底层算法库，搬运时需确保环境中有对应的图像处理工具

## 元信息

- 来源：`refer/awesome-claude-skills/image-enhancer/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
