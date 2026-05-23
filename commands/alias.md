---
description: Manage zsh aliases with conflict checking and Markdown help docs
---

Help the user create or manage zsh aliases for a specific tool/topic.

## Output Structure

```
~/.config/zsh/
├── <topic>-aliases.zsh   # alias definitions
├── <topic>-help.md       # Markdown help (rendered with glow)
```

`~/.zshrc` must contain: `source ~/.config/zsh/<topic>-aliases.zsh`

## Workflow

Track progress with this checklist:

```
Alias Task Progress:
- [ ] Step 1: Check existing aliases for conflicts
- [ ] Step 2: Design alias names (consistent prefix)
- [ ] Step 3: Confirm with user before writing
- [ ] Step 4: Write aliases file
- [ ] Step 5: Write Markdown help doc
- [ ] Step 6: Source into ~/.zshrc
- [ ] Step 7: Verify with user
```

### Step 1: Check conflicts

Run these commands:

```bash
alias | grep '<prefix>'
grep -h "alias <prefix>" ~/.config/zsh/*-aliases.zsh 2>/dev/null
grep -h "alias " ~/.zshrc
```

If conflicts found, show the user and ask for alternative prefix.

### Step 2: Design aliases

Rules:
- Use a short prefix (2-4 chars) + hyphen: `gnx-`, `dk-`, `k8s-`
- Group by topic: `gnx-a` (analyze), `gnx-s` (status)
- Reserve `-h` suffix for help
- Keep commands short but readable

### Step 3: Confirm with user

Present designed aliases in a table and wait for approval:

```markdown
拟定的 alias：

| Alias | 命令 | 说明 |
|-------|------|------|
| `dk` | `docker` | 基础前缀 |
| `dk-ps` | `docker ps` | 查看运行容器 |

确认吗？（y/n/修改）
```

**Do not proceed until user explicitly confirms.**

### Step 4: Write aliases file

Create `~/.config/zsh/<topic>-aliases.zsh`:

```zsh
#!/bin/zsh
# <Topic> Aliases
# Help: <topic>-h

alias <prefix>='<base-command>'
alias <prefix>-a='<base-command> action'
alias <prefix>-h='glow ~/.config/zsh/<topic>-help.md 2>/dev/null || cat ~/.config/zsh/<topic>-help.md'
```

### Step 5: Write help doc

Create `~/.config/zsh/<topic>-help.md`:

```markdown
# <Topic> 命令速查

## 常用命令

| 命令 | 说明 |
|------|------|
| `<prefix>` | 基础前缀 |
| `<prefix>-a` | 描述 |

## 帮助

- `<prefix>-h` 打开此文档
```

### Step 6: Source into ~/.zshrc

Add if missing:

```bash
source ~/.config/zsh/<topic>-aliases.zsh
```

### Step 7: Verify

Ask user to run:

```bash
source ~/.zshrc && <prefix>-h
```

## Red Flags

- Never overwrite existing aliases without confirming
- Never use single-letter aliases for complex tools
- Always include a `-h` help alias
- Always check ~/.zshrc for duplicate source lines
