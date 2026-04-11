# local-install.py 设计方案

## 概述
实现一个 Python 安装脚本，用于将 ys-powers 项目的 skills 目录安装到当前工作目录的 `.claude/skills` 中。

## 功能需求

1. **定位项目目录**
   - 通过脚本自身的路径，自动确定 ys-powers 项目的根目录（L_DIR）
   - 支持脚本从任意位置运行

2. **创建目标目录**
   - 在当前工作目录（用户运行脚本的目录）创建 `./.claude/skills`
   - 如果目录已存在，不进行任何操作

3. **复制 Skills**
   - 递归复制 `L_DIR/skills` 下的所有内容到 `./.claude/skills`
   - 采用增量复制策略：保留目标目录已有文件，仅覆盖同名文件
   - 保留原有文件权限和目录结构

## 技术方案

### 核心技术
- 使用 Python 标准库 `pathlib` 处理路径操作
- 使用 `shutil.copytree` 实现递归复制
- 通过 `__file__` 属性确定脚本位置，进而定位项目根目录

### 关键实现逻辑

```python
# 1. 获取项目根目录
script_dir = Path(__file__).resolve().parent  # install/
project_root = script_dir.parent  # ys-powers/
source_skills = project_root / "skills"

# 2. 确定目标目录
target_dir = Path.cwd() / ".claude" / "skills"

# 3. 执行复制
shutil.copytree(source_skills, target_dir, dirs_exist_ok=True)
```

## 错误处理

1. **源目录不存在**：检查 `L_DIR/skills` 是否存在，不存在则报错退出
2. **权限错误**：捕获 PermissionError，提示用户检查目录权限
3. **非目录文件冲突**：如果目标路径存在但不是目录，提示用户手动清理

## 使用示例

```bash
# 在项目根目录运行
python install/local-install.py

# 在任意目录运行（通过完整路径）
python /path/to/ys-powers/install/local-install.py
```

## 注意事项

- 脚本依赖于自身的文件路径来定位项目目录，不要移动或重命名脚本所在位置
- 使用 `dirs_exist_ok=True` 参数确保幂等性（Python 3.8+）
- 复制过程会覆盖目标目录中同名的旧文件，但不会删除用户自己添加的其他文件
