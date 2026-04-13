# Commands 目录设计

## 背景

用户希望将 `commands` 目录纳入 `local-install.py` 安装脚本，与 `skills` 和 `rules` 并列，支持本地安装到 `.claude/` 目录。

## 设计决策

### 安装策略：文件级同名覆盖

与 `rules` 目录相同策略：
- 同名文件会被覆盖
- 目标目录独有的文件会被保留
- 源目录新增的文件会被复制

### 配置变更

`install/local-install.py` 中的 `DIRECTORIES` 字典新增：

```python
"commands": ("commands", "file")
```

### 目录用途

`commands/` 包含 AI 执行特定工作流时的操作指南/命令手册，供 Claude 在执行特定操作时参考。

## 实现

- 修改 `install/local-install.py`，在 `DIRECTORIES` 中添加 `commands` 条目
- 安装命令时输出与 `rules` 一致的格式

## 验证

安装后验证：
```bash
python install/local-install.py
ls -la .claude/commands/
```
