# Spec: Optimize Install Output

## Objective

优化 `make global-install` / `make local-install` 的输出，让用户能看到本次安装具体修改了哪些 commands、skills、rules 等一级子项，而不是只看到目录级的成功/失败提示。

**用户故事：**
- 作为 ys-powers 维护者，当我更新了一个 skill 或 command 后运行安装，我想一眼确认只有预期的文件发生了变化，而不是对整个目录做盲目覆盖。

## Tech Stack

- Python 3.11+
- 标准库 `filecmp`（用于变更检测）
- 标准库 `pathlib`（路径操作）

## Commands

```bash
# 安装到全局
make global-install
# 等价于：python3 install/install.py install global

# 安装到本地项目
make local-install
# 等价于：python3 install/install.py install local
```

## Project Structure

```
install/
├── install.py          # 主入口，无需修改核心逻辑，仅配合输出格式调整
├── lib/
│   ├── config.py       # DIRECTORIES 配置，无需修改
│   ├── fs.py           # 核心：新增 collect_changes() 函数，调整 install_directory() 输出
│   └── hooks.py        # hooks 注册，无需修改
└── renames.json        # stale 文件重命名映射，无需修改
```

## Code Style

```python
import filecmp
from pathlib import Path


def collect_changes(source_dir: Path, target_dir: Path) -> list[tuple[str, str]]:
    """收集源目录相对于目标目录的一级子项变更。

    Args:
        source_dir: 源目录路径（如 .../ys-powers/skills）
        target_dir: 目标目录路径（如 ~/.claude/skills）

    Returns:
        [(mark, name), ...]，mark 为 'A'（新增）或 'M'（修改）
    """
    changes: list[tuple[str, str]] = []

    for item in source_dir.iterdir():
        if item.name.startswith(".") or "/" in item.name or "\\" in item.name:
            continue

        target_item = target_dir / item.name
        if not target_item.exists():
            changes.append(("A", item.name))
            continue

        try:
            if item.is_file() and target_item.is_file():
                if not filecmp.cmp(item, target_item, shallow=True):
                    changes.append(("M", item.name))
            elif item.is_dir() and target_item.is_dir():
                dc = filecmp.dircmp(str(item), str(target_item))
                if dc.diff_files or dc.left_only or dc.right_only or dc.funny_files:
                    changes.append(("M", item.name))
            else:
                # 类型不同（文件 vs 目录）→ 视为修改
                changes.append(("M", item.name))
        except (PermissionError, OSError):
            # 无法读取目标项时保守标记为修改
            changes.append(("M", item.name))

    return changes
```

关键约定：
- 函数名用 `snake_case`
- 类型注解使用 `list[tuple[str, str]]`（Python 3.9+ 语法）
- 路径操作统一用 `pathlib.Path`
- 输出缩进用两个空格，与现有输出风格一致
- 文件系统遍历跳过 `.` 开头和含路径分隔符的名称（沿用现有安全策略）

## Testing Strategy

- **手动验证**：运行 `make global-install`，确认输出包含 `M`/`A` 标记
- **边界检查**：
  - 目标目录不存在时，所有源子项应标记为 `A`
  - 内容未变的子项不应出现在输出中
  - 无变更的目录块下不显示任何内容
  - 源子项与目标同名项类型不同时（文件 vs 目录），应标记为 `M`
  - 目标项无权限读取时，应保守标记为 `M`（不中断安装）
- **回归检查**：安装后 `.claude/` 下的文件内容与修改前完全一致

## Boundaries

- **Always:**
  - 安装核心逻辑保持现有 `folder`/`file` 策略完全不变
  - 变更检测只在安装前执行一次，不重复扫描
  - 只对比到一级子项，不递归到内部文件
  - `cleanup_stale_files()` 必须在 `collect_changes()` 之前执行（file 策略下）
- **Ask first:**
  - 如果需要在 `install.py` 中添加 CLI flag（如 `--verbose`）
  - 如果要改变 `folder` 策略的"先删后复制"行为
- **Never:**
  - 删除现有输出中的成功/失败状态行
  - 引入外部依赖（只用 Python 标准库）
  - 递归到二级及以下文件级别
  - 显示删除标记 `D`

## Success Criteria

- [ ] 运行 `make global-install` 时，每个有变更的目录块下显示 `M`/`A` 标记的一级子项列表
- [ ] 内容未变的子项不显示
- [ ] 无变更的目录块下不显示额外内容
- [ ] 安装逻辑行为与修改前完全一致（回归测试通过）
- [ ] `filecmp` 使用 `shallow=True` 优化对比性能，避免对大文件做无意义的内容读取

## Open Questions

- [x] 是否同步修改 `make local-install`？是，同一脚本共用同一输出逻辑。
