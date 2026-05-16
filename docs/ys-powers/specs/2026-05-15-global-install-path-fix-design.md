# Spec: Global Install 路径兼容性修复

## Objective

修复 ys-powers 在 `make global-install`（安装到 `~/.claude/`）后的路径失效问题，确保所有能力（skills、agents、hooks、commands）在任意用户项目下都能正确加载和运行。

### 背景

Global install 将 ys-powers 内容复制到 `~/.claude/` 下，但 Claude Code 运行时的当前工作目录（CWD）是用户的项目目录，而非 `~/.claude/`。因此：

- 硬编码的容器路径（如 `/mnt/skills/user/...`）必定失效
- 不恰当的占位符（如 `${CLAUDE_PLUGIN_ROOT}`）在 non-plugin 模式下造成混淆
- Agent 直接引用 skill 文件路径，global install 后可能无法解析

### Acceptance Criteria

- [ ] Global install 后，hooks 在任何机器上都能正确执行，不依赖绝对用户名
- [ ] Global install 后，`/ideate` 命令不再报错 "file not found"
- [ ] Global install 后，`/html` 命令能正确加载 html-anything skill 及其 prompts
- [ ] Local install 行为保持不变，不受本次改动影响
- [ ] 安装脚本不修改 skill/agent markdown 文件内容（不做内容替换）

---

## Tech Stack

- Python 3（安装脚本）
- Bash（hooks、辅助脚本）
- Markdown（skill / agent / command 定义）

---

## Commands

```bash
# 验证安装脚本语法
python3 -m py_compile install/lib/hooks.py

# 本地验证 global install（在 ys-powers 仓库执行）
make global-install

# 验证 local install
make local-install project-dir=/tmp/test-project

# 验证卸载
make uninstall-global
make uninstall-local project-dir=/tmp/test-project
```

---

## Project Structure

```
ys-powers/
├── hooks/
│   ├── hooks.json              # 重写：直接使用 $HOME 和 CLAUDE_PROJECT_DIR
│   └── session-start.sh        # 不变：已使用 $0 自定位
├── install/
│   ├── install.py              # 不变：入口逻辑
│   └── lib/
│       └── hooks.py            # 简化：移除 ${CLAUDE_PLUGIN_ROOT} 替换逻辑
├── skills/
│   ├── idea-refine/
│   │   └── SKILL.md            # 修复：/mnt/... → ./scripts/...
│   └── html-anything/
│       └── SKILL.md            # 不变：保持 ./prompts/... 相对路径
├── agents/
│   └── html-generator.md       # 修复：Load skills/... → skill: html-anything
└── docs/ys-powers/specs/
    └── 2026-05-15-global-install-path-fix-design.md  # 本文档
```

---

## Code Style

### Hooks 路径规范

Hooks 配置中**不使用占位符**，直接写运行时解析路径：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash $HOME/.claude/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```

Global 场景用 `$HOME/.claude/...`，Local 场景用 `${CLAUDE_PROJECT_DIR}/.claude/...`。

### Skill 间调用规范

Agent 不直接引用 skill 文件路径，使用 Claude Code 的 `skill` 工具：

```markdown
<!-- 错误 -->
Load `skills/html-anything/SKILL.md`

<!-- 正确 -->
Invoke `skill: html-anything`
```

### Skill 内部资源引用

使用相对路径，假设 Claude Code 从 skill 文件所在目录解析：

```markdown
Read [`prompts/styles/_design.md`](./prompts/styles/_design.md)
```

---

## Testing Strategy

### 手动验证清单

| 步骤 | 命令 / 操作 | 预期结果 |
|------|-----------|---------|
| 1 | `cd ~/soft/projects/ys-powers && make global-install` | 安装成功，无报错 |
| 2 | `ls ~/.claude/hooks/session-start.sh` | 文件存在 |
| 3 | `cat ~/.claude/settings.json \| grep "SessionStart" -A 5` | command 为 `bash $HOME/.claude/hooks/session-start.sh` |
| 4 | `cd /tmp && mkdir test-project && cd test-project && claude` | 启动 Claude Code |
| 5 | 在新项目中运行 `/ideate` | 不报错，能正常触发 idea-refine skill |
| 6 | 在新项目中运行 `/html test` | 能正确加载 html-anything skill 和 prompts |
| 7 | `make local-install project-dir=/tmp/test-project` | 安装成功 |
| 8 | `cat /tmp/test-project/.claude/settings.local.json \| grep "SessionStart" -A 5` | command 为 `bash ${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh` |

### 边界情况

- 卸载后重新安装：settings.json 中不出现重复 hooks
- 已存在其他 hooks：正确合并，不覆盖用户自定义 hooks

---

## Boundaries

### Always
- 修改后必须验证 global install 和 local install 两种模式
- 保持 hooks 的 `$0` 自定位脚本逻辑不变
- 任何路径变更都要在 audit 文档中记录

### Ask First
- 如果要修改 `install.py` 的目录复制逻辑（非 hooks 注入部分）
- 如果要引入新的环境变量（超出 `$HOME` 和 `CLAUDE_PROJECT_DIR`）
- 如果验证发现 Claude Code 不从 skill 目录解析相对路径，需要内联 prompts 内容

### Never
- 不在安装时修改 skill / agent / command 的 markdown 文件内容
- 不引入 gsd 式的全局内容替换机制
- 不删除或重命名已存在的 skill/agent 目录结构
- 不将 `${CLAUDE_PLUGIN_ROOT}` 保留在最终 settings.json 中（它不是标准插件）

---

## Success Criteria

1. **Hooks 可移植**：global install 后的 `settings.json` 中出现 `$HOME/.claude/hooks/session-start.sh`，不含绝对用户名
2. **容器路径修复**：`skills/idea-refine/SKILL.md` 中不再出现 `/mnt/skills/user/...`
3. **Agent 解耦**：`agents/html-generator.md` 通过 `skill: html-anything` 调用，不直接引用文件路径
4. **验证通过**：在非 ys-powers 项目运行 `/ideate` 和 `/html` 均成功
5. **Local 不受影响**：local install 后的路径保持 `${CLAUDE_PROJECT_DIR}/.claude/...`

---

## Open Questions

1. Claude Code 是否从 skill 文件所在目录解析 `./prompts/...` 相对路径？—— 需验证，如验证失败则 prompts 内容需内联
2. `agents/html-generator.md` 改为 `skill: html-anything` 调用后，是否仍需要显式读取 prompts？—— 测试确认 skill 加载后是否自动处理
