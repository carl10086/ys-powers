# video-downloader

## 定位

从 YouTube 下载视频，支持自定义质量（1080p、720p 等）、格式（MP4、WebM、MKV）和音频提取（MP3）。基于 yt-dlp 实现，自动处理安装和流合并。

## 触发时机

- 需要离线观看 YouTube 视频时
- 需要下载视频用于编辑、存档或二次创作时
- 仅需提取视频音频（如播客、音乐）时
- **不适用**：版权受限内容、或平台明确禁止下载的视频

## 核心能力

1. **多质量选择**：best、1080p、720p、480p、360p、worst
2. **多格式支持**：MP4（默认）、WebM、MKV
3. **音频提取**：仅下载音频并转为 MP3
4. **自动依赖管理**：自动安装 yt-dlp（如未安装）
5. **自定义输出目录**：默认保存到 `/mnt/user-data/outputs/`

## 使用方式

```bash
# 默认下载（最佳质量 MP4）
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定质量
python scripts/download_video.py "URL" -q 720p

# 指定格式
python scripts/download_video.py "URL" -f webm

# 仅音频
python scripts/download_video.py "URL" -a

# 自定义输出目录
python scripts/download_video.py "URL" -o /path/to/directory
```

## 与 ys-powers 的关联

- **与 image-enhancer / canvas-design 的关系**：`video-downloader` 获取媒体素材，`image-enhancer` 优化图片，`canvas-design` 创作视觉内容。三者构成「获取 → 优化 → 创作」的媒体工作流
- **借鉴价值**：其「自动依赖安装 + 简洁 CLI 封装」的模式可作为任何基于外部工具的技能的设计参考
- **搬运建议**：低价值。功能单一，yt-dlp 本身已是成熟工具。但可作为「媒体处理工具集」的一部分保留

## 元信息

- 来源：`refer/awesome-claude-skills/video-downloader/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
