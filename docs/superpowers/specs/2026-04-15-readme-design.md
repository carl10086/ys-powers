# README.md 设计

## 背景

当前 `ys-powers` 项目的 `README.md` 为空文件，新成员无法快速了解项目用途和使用方式。需要补充一份面向团队内部、以实用为主的 README。

## 目标读者

团队内部成员，重点是第一次接触此项目或需要在新项目中安装 ys-powers 的开发者。

## 设计决策

### 内容范围

采用"实用为主"策略，包含：
1. 项目一句话定位
2. 核心目录说明
3. 安装方式
4. 日常使用示例

不展开贡献指南、详细架构设计或变更日志。

### 语言

使用中文，与团队现有设计文档和代码注释保持一致。

### 结构

```markdown
# ys-powers

## 简介
...

## 目录说明
...

## 安装
...

## 使用示例
...
```

## 内容草稿

### 简介

`ys-powers` 是一套用于增强 Claude Code 工作流的本地能力集，包含 skills、rules、commands 三类配置。

### 目录说明

- `skills/` — Claude Code 技能定义
- `rules/` — 项目级或通用编码规范
- `commands/` — 特定工作流的操作指南/命令手册
- `install/local-install.py` — 安装脚本，用于将这些能力安装到任意项目的 `.claude/` 目录下

### 安装

```bash
python /path/to/ys-powers/install/local-install.py
```

运行后会在当前工作目录创建 `.claude/skills`、`.claude/rules`、`.claude/commands`，并按预设策略复制文件：

- `skills/`：文件夹级全量覆盖（同名文件夹整体替换）
- `rules/`、`commands/`：文件级同名覆盖（同名文件替换，保留目标独有的文件）

### 使用示例

```bash
# 进入你的目标项目
cd /path/to/your-project

# 执行安装
python /path/to/ys-powers/install/local-install.py

# 验证
ls -la .claude/
```

## 验证标准

- `README.md` 文件非空
- 包含简介、目录说明、安装、使用示例四个部分
- 安装命令可直接复制执行
