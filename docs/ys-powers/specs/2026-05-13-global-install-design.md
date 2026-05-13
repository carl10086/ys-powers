# Spec: 全局安装与本地卸载能力

## Objective

为 `ys-powers` 增加**全局安装**和**本地卸载**两个能力，解决当前仅支持项目级本地安装（`./.claude/`）的局限。

**用户故事**：
- 作为用户，我希望在任意项目都能使用 ys-powers，而不必在每个项目都运行一次 `local-install.py`
- 作为用户，我希望从本地安装切换到全局安装时，能干净地清理当前项目的本地文件，避免冲突

**验收标准**：
1. 运行 `install/global-install.py` 后，`~/.claude/` 下出现与本地安装一致的目录结构
2. 运行 `install/remove-local` 后，当前项目的 `./.claude/` 下不再包含 ys-powers 安装的文件
3. `local-install.py` 行为保持不变，现有用户不受影响
4. 两个新脚本完全独立，不提取共享模块（方案 A）

## Tech Stack

- Python 3（复用现有 `local-install.py` 的 `pathlib`、`shutil`、`json` 模式）
- 不引入外部依赖

## Commands

```bash
# 全局安装（安装到 ~/.claude/）
python /path/to/ys-powers/install/global-install.py

# 本地卸载（清理当前项目的 ./.claude/）
python /path/to/ys-powers/install/remove-local

# 本地安装（现有，行为不变）
python /path/to/ys-powers/install/local-install.py
```

## Project Structure

```
ys-powers/
├── install/
│   ├── local-install.py       # 现有，保持不变
│   ├── global-install.py      # 新增：全局安装脚本
│   ├── remove-local           # 新增：本地卸载脚本
│   └── renames.json           # 现有，继续使用
├── docs/ys-powers/specs/
│   └── 2026-05-13-global-install-design.md  # 本 spec
```

## Code Style

复用 `local-install.py` 的编码风格：

- 使用 `pathlib.Path` 处理路径，不使用 `os.path`
- 函数返回 `bool` 表示成功/失败，错误打印到 `sys.stderr`
- 使用 `print(f"✓ {name} 操作成功")` 风格的状态输出
- 路径遍历防护：跳过包含 `/`、 `\\` 或以 `.` 开头的名称
- 保持与现有脚本一致的注释风格和错误处理模式

示例（global-install.py 的目标目录获取）：

```python
def get_global_claude_dir() -> Path:
    """获取全局 Claude 配置目录 ~/.claude/"""
    return Path.home() / ".claude"
```

## Testing Strategy

- **无自动化测试**：安装脚本属于运维工具，验证以手动执行 + 目录结构检查为主
- **验证清单**：
  1. 运行 `global-install.py` 后，检查 `~/.claude/` 下是否存在 `skills/`、`commands/`、`agents/`、`rules/`、`hooks/`、`references/`
  2. 运行 `remove-local` 后，检查 `./.claude/` 下上述目录是否已删除，用户自定义的 `settings.json`、`memory/` 等是否保留
  3. 验证 `local-install.py` 仍能正常运行，安装策略不变

## Boundaries

- **Always**：
  - 全局安装和本地卸载的目录策略必须与 `local-install.py` 完全一致
  - `remove-local` 只删除 ys-powers 相关内容，绝不删除用户自己的配置
  - 两个新脚本都必须处理 `renames.json` 的 stale 文件清理
- **Ask first**：
  - 修改 `local-install.py` 的行为
  - 提取共享模块（本 spec 明确选择方案 A：完全独立）
- **Never**：
  - 在 `global-install.py` 中自动修改 `~/.claude/settings.json`（当前版本只打印提示，见下方 Hooks TODO）
  - 删除整个 `./.claude/` 目录（remove-local 只清理 ys-powers 子目录）

## Success Criteria

1. `global-install.py` 执行成功，将 `skills/`、`commands/`、`agents/`（folder 策略）和 `rules/`、`hooks/`、`references/`（file 策略）安装到 `~/.claude/`
2. `global-install.py` 执行 `cleanup_stale_files()`，根据 `renames.json` 清理 `~/.claude/` 中的旧名文件
3. `remove-local` 执行成功，删除当前项目 `./.claude/` 下的 `skills/`、`commands/`、`agents/`、`rules/`、`hooks/`、`references/`
4. `remove-local` 根据 `renames.json` 清理 file 策略目录中的旧名文件
5. `remove-local` 尝试从 `./.claude/settings.local.json` 中移除 ys-powers 注册的 hooks
6. `local-install.py` 行为与修改前完全一致

## Hooks 处理策略（关键决策）

### global-install.py

**当前版本暂不自动注册 hooks 到 `~/.claude/settings.json`。**

原因：全局 `settings.json` 的 hooks merge 涉及复杂逻辑（备份、去重、路径变量解析、跨平台绝对路径处理）。

替代方案：
1. 读取 `hooks/hooks.json`
2. 将 `${CLAUDE_PLUGIN_ROOT}` 替换为 `~/.claude` 的绝对路径（`Path.home() / ".claude"`）
3. **打印转换后的 JSON 片段**，提示用户手动复制到 `~/.claude/settings.json`
4. 脚本末尾打印 TODO：`[TODO] hooks 全局自动注册待实现`

### remove-local

**简化处理**：
- 读取 `hooks/hooks.json`，执行同样的路径转换（`${CLAUDE_PLUGIN_ROOT}` → `${CLAUDE_PROJECT_DIR}/.claude`）
- 在 `./.claude/settings.local.json` 中精确匹配这些 hooks 并移除
- 如果匹配逻辑过于复杂或 hooks.json 已变更，降级为打印警告，提示用户手动检查

## Open Questions

1. `remove-local` 的 hooks 反注册是否也需要降级为"仅打印提示"，与 `global-install.py` 保持一致？
- 仅仅打印提示
2. 全局安装后，Claude Code 是否支持 `~/.claude/settings.json` 中的绝对路径 hooks？需要实际验证。
- 暂时不用
