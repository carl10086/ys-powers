# Spec: Python 版本检查与 uv 唯一支持

## Objective

解决 `make global-install` 在系统 Python 3.9 下因 `dict | None` 语法报错的问题。通过两项改动：

1. **install/install.py 增加版本检查**：脚本执行任何逻辑前检测 Python 版本，< 3.10 时输出清晰报错指引（推荐 uv / 其他方式），而非暴露晦涩的 `TypeError`
2. **Makefile 仅支持 uv**：所有 `python3` 调用替换为 `uv run --python 3.12 python`，统一用 uv 管理 Python 版本，消除版本碎片化

用户故事：
- 作为 ys-powers 用户，当我在 Python 3.9 的系统上运行 `make global-install` 时，我希望看到清晰的错误提示和安装指引，而不是 `TypeError`
- 作为 ys-powers 用户，我希望安装流程统一使用 uv，不需要关心系统 Python 版本

## Tech Stack

- Python 3.12（通过 uv 管理）
- Makefile（GNU make / BSD make 兼容）
- uv（https://docs.astral.sh/uv/）

## Commands

```bash
# 安装 uv（首次）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Python 3.12（首次）
uv python install 3.12

# 安装 ys-powers（global）
make global-install

# 安装 ys-powers（local）
make local-install
make local-install project-dir=/path/to/project

# 其他目标同理
make update-global
make update-local
make uninstall-global
make uninstall-local
```

## Project Structure

涉及的文件：

```
install/
├── install.py          # 增加 sys.version_info 检查（文件顶部）
└── lib/
    └── hooks.py        # 保持不变（已有 Python 3.10+ 语法）

Makefile                # python3 → uv run --python 3.12 python
README.md               # 安装节增加 uv 依赖说明
```

## Code Style

**版本检查代码（install/install.py 顶部）：**

```python
import sys

if sys.version_info < (3, 10):
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✗ 需要 Python 3.10+，当前: {py_ver}", file=sys.stderr)
    print("", file=sys.stderr)
    print("推荐方式（通过 uv）:", file=sys.stderr)
    print("  curl -LsSf https://astral.sh/uv/install.sh | sh", file=sys.stderr)
    print("  uv python install 3.12", file=sys.stderr)
    print("  uv run --python 3.12 python install/install.py <action> <scope>", file=sys.stderr)
    print("", file=sys.stderr)
    print("其他方式:", file=sys.stderr)
    print("  自行安装 Python 3.10+，然后重新运行安装命令", file=sys.stderr)
    sys.exit(1)
```

**Makefile 变量替换：**

```makefile
PYTHON := uv run --python 3.12 python

global-install:
	$(PYTHON) $(YS_POWERS_ROOT)/install/install.py install global
```

## Testing Strategy

- **手动验证**：
  1. 在 Python 3.9 环境下运行 `make global-install`，确认输出友好报错
  2. 在已安装 uv + Python 3.12 的环境下运行 `make global-install`，确认安装成功
  3. 验证所有 Makefile 目标（local-install, update-global, update-local, uninstall-global, uninstall-local）都能正常调用
- 无自动化测试（Makefile 和安装脚本通常不做单元测试）

## Boundaries

- **Always:**
  - install.py 脚本执行任何业务逻辑前先检查 Python 版本
  - Makefile 所有目标统一使用 `uv run --python 3.12 python`
  - 报错信息用中文，包含 uv 安装命令和通用替代方案

- **Ask first:**
  - 修改 install 目录下其他 Python 文件的语法兼容性
  - 在 README 中增加 uv 的详细安装教程（超出当前范围）

- **Never:**
  - 修改 `install/lib/hooks.py` 中的 `dict | None` 语法（保留现代写法）
  - 保留 `python3` 作为 fallback（统一 uv 路径）
  - 在本次改动中调整安装策略或目录结构

## Success Criteria

1. `python3 install/install.py install global`（系统 Python 3.9）输出清晰的中文报错，包含 uv 安装指引和替代方案
2. `make global-install`（有 uv 有 3.12）成功完成安装，行为和修改前一致
3. `make help` 帮助信息中的目标描述不需要修改（保持现有文案）
4. README.md 安装节增加了 uv 作为前置依赖的说明
5. 所有 Makefile 目标都通过 `uv run --python 3.12` 调用

## Open Questions

无。
