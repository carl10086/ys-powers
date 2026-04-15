# ys-powers

`ys-powers` 是一套用于增强 Claude Code 工作流的本地能力集，包含 skills、rules、commands 三类配置。

## 目录说明

- `skills/` — Claude Code 技能定义
- `rules/` — 项目级或通用编码规范
- `commands/` — 特定工作流的操作指南/命令手册
- `install/local-install.py` — 安装脚本，用于将这些能力安装到任意项目的 `.claude/` 目录下

## 安装

```bash
python /path/to/ys-powers/install/local-install.py
```

运行后会在当前工作目录创建 `.claude/skills`、`.claude/rules`、`.claude/commands`，并按预设策略复制文件：

- `skills/`：文件夹级全量覆盖（同名文件夹整体替换）
- `rules/`、`commands/`：文件级同名覆盖（同名文件替换，保留目标独有的文件）

## 使用示例

```bash
# 进入你的目标项目
cd /path/to/your-project

# 执行安装
python /path/to/ys-powers/install/local-install.py

# 验证
ls -la .claude/
```
