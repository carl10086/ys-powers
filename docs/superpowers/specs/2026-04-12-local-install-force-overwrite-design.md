# local-install.py 全量覆盖设计

## 概述
修改 `local-install.py` 脚本，将复制策略从**增量复制**改为**全量覆盖**模式。

## 设计决策

### 变更原因
- Skills 内容应完全由源目录控制
- 不需要保留用户历史修改
- 简化逻辑，避免残留旧文件

### 技术方案

**原方案（增量）：**
```python
shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
```

**新方案（全量覆盖）：**
```python
if target_dir.exists():
    shutil.rmtree(target_dir)
shutil.copytree(source_dir, target_dir)
```

### 行为变更

| 场景 | 旧行为 | 新行为 |
|------|--------|--------|
| 目标已存在 | 保留旧文件 | 删除后全新复制 |
| 用户添加的文件 | 保留 | 删除 |
| 同名文件 | 覆盖 | 覆盖（因目录已清空） |

## 用户确认

用户选择 **A 方案（总是强制覆盖）**，确认符合预期。

## 实现

单次文件修改，无需复杂计划。
