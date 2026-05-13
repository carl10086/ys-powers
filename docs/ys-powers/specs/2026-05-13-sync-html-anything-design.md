# Spec: 集成 html-anything 到 ys-powers（最小搬运）

## Objective

将 `refer/html-anything/` 中的核心 skill 资产以最小化方式搬运到 `skills/html-anything/`，使 ys-powers 用户可直接使用该 skill 的方法论与 prompts。提供手动触发的同步机制（脚本 + Make），确保未来上游更新时可重复执行。

## Commands

| 命令 | 作用 |
|------|------|
| `make sync-html` | 触发同步脚本，一键完成搬运 |
| `python scripts/sync_html_anything.py` | 直接运行同步脚本 |

## Project Structure

新增/变更的文件和目录：

```
scripts/
  sync_html_anything.py          # 新增：同步脚本（Python，标准库 only）
skills/
  html-anything/                  # 新增：同步后的 skill 目录
    SKILL.md
    prompts/
      sources/                    # 60 个 source prompts
      styles/                     # 17 个 style prompts + catalog.json + _design.md + _system.md + references/
Makefile                          # 新增：提供 `sync-html` target
```

不搬运的内容（明确排除）：
- `src/` — Node.js CLI 源码，与 skill 体系无关
- `scripts/` — 上游示例生成脚本，非 skill 核心
- `package.json`、`tsconfig.json`、`package-lock.json` — Node.js 项目配置
- `docs/`、`test-results/` — 上游文档和测试产物
- `.git/`、`.gitignore`、`.clawhubignore` — 版本控制文件
- `examples/` — 本次范围外，如需搬运后续单独决策

## Code Style

- **Python 脚本**：
  - 仅用标准库（`pathlib`、`shutil`、`argparse`），零外部依赖
  - 使用 `pathlib.Path` 处理路径，跨平台兼容
  - 输出清晰的同步日志（复制了哪些文件、跳过了哪些、总计数量）
  - 支持 `--dry-run` 参数预览变更，不实际写入
  - 支持幂等执行：多次运行结果一致

- **Makefile**：
  - 简洁，仅定义 `sync-html` target
  - 调用 `python scripts/sync_html_anything.py`
  - 使用 `.PHONY` 标记

- **路径策略**：
  - 保持 `html-anything` 原有目录结构，不做路径改写
  - `SKILL.md` 中的相对路径（如 `prompts/styles/_design.md`）在搬运后仍然有效

## Testing Strategy

- **运行后验证**（脚本内置检查）：
  1. `skills/html-anything/SKILL.md` 存在且大小 > 0
  2. `skills/html-anything/prompts/sources/` 存在且包含至少 1 个 `.md` 文件
  3. `skills/html-anything/prompts/styles/` 存在且包含至少 1 个 `.md` 文件
  4. `skills/html-anything/prompts/styles/catalog.json` 存在

- **dry-run 测试**：运行 `python scripts/sync_html_anything.py --dry-run`，确认输出列表与预期一致

- **幂等测试**：连续运行两次脚本，第二次应报告"无变更"或相同文件覆盖（内容不变）

## Boundaries

| 类型 | 内容 |
|------|------|
| **Always** | 只搬运 `SKILL.md` + `prompts/`；保持路径原样；refer/ 下文件只读 |
| **Ask first** | 若需搬运 `examples/`、修改 `SKILL.md` frontmatter、增加路径适配逻辑、改为自动触发（git hook / CI） |
| **Never** | 修改 `refer/html-anything/` 中任何文件；搬运 `src/`/`scripts/`/`package.json` 等非 skill 资产；在同步脚本中引入外部依赖 |
