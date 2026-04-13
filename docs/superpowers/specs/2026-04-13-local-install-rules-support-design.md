# local-install.py 增加 rules 目录支持

## 概述

扩展 `local-install.py` 脚本，在安装 skills 的同时，也安装项目的 rules 目录到目标位置的 `.claude/rules`。

## 设计决策

### 功能范围

- **同时安装**：每次运行脚本时，同时复制 skills 和 rules（如果存在）
- **相同策略**：对 rules 使用与 skills 相同的**全量覆盖**策略
- **独立处理**：每个目录的复制独立执行，互不影响

### 技术方案

**目录映射**：
```python
DIRECTORIES = {
    "skills": "skills",  # 源目录名: 目标子目录名
    "rules": "rules"
}
```

**处理流程**：
1. 遍历 `DIRECTORIES` 中的每个条目
2. 检查源目录是否存在（不存在则跳过并提示）
3. 确定目标路径：`{cwd}/.claude/{target_subdir}`
4. 执行全量覆盖复制
5. 汇总输出结果

### 代码结构变更

**当前结构**：
```python
def install_skills():
    # 单一目录处理逻辑
    ...
```

**新结构**：
```python
def install_directory(source_name: str, target_name: str) -> bool:
    """安装单个目录，返回是否成功"""
    ...

def main():
    """主入口，批量处理所有目录"""
    directories = {"skills": "skills", "rules": "rules"}
    results = []
    for source_name, target_name in directories.items():
        success = install_directory(source_name, target_name)
        results.append((source_name, success))
    # 输出汇总结果
```

### 边界情况处理

| 场景 | 处理策略 |
|------|----------|
| 源目录不存在 | 跳过，输出警告信息，继续处理其他目录 |
| 目标目录已存在 | 删除后全新复制（全量覆盖） |
| 复制过程中出错 | 捕获异常，输出错误，返回失败状态 |
| 所有目录都失败 | 以非零状态码退出 |
| 部分成功 | 输出成功和失败列表，以零状态码退出 |

### 用户输出示例

**全部成功**：
```
✓ Skills 安装成功（全量覆盖）
  源目录: /path/to/ys-powers/skills
  目标目录: /path/to/project/.claude/skills
✓ Rules 安装成功（全量覆盖）
  源目录: /path/to/ys-powers/rules
  目标目录: /path/to/project/.claude/rules
```

**部分失败**：
```
✓ Skills 安装成功（全量覆盖）
  源目录: /path/to/ys-powers/skills
  目标目录: /path/to/project/.claude/skills
✗ Rules 安装失败
  错误: 权限不足，无法写入 /path/to/project/.claude/rules
```

## 实现说明

- 保持与现有代码风格一致
- 不引入外部依赖（仅使用标准库）
- 错误信息输出到 stderr
- 支持通过 exit code 判断整体成功/失败
