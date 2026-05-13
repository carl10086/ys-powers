# Update Entry 模板

每次 `git pull` 后，在 `docs/agent-skills/refer-commit.md` 的「更新历史」顶部追加一条，按以下模板填写。

```markdown
### YYYY-MM-DD: <prev-short>..<new-short>

**摘要**：一行总结本次更新的性质。

**上下游**：
- 起点: <prev-short> (<prev-subject>)
- 终点: <new-short> (<new-subject>)
- 期间提交数: N
- ys-powers 同期 commit: <short>

#### 4 维度变更

**1. 方法论修订**
- `<skill-name>`: 一行说明

**2. 新增**
- `<path>`: 一行说明

**3. 删除/合并**
- `<path>`: 一行说明

**4. 编排层变化**
- 一行说明

#### 同步决策

- **要同步**：
  - <动作> → 影响 ys-powers 路径 `<path>`
- **暂不同步**：
  - <理由>
- **已确认同步**：
  - <说明>
- **待定**：
  - <未决问题>

#### TODO

- [ ] <动作 1>
- [ ] <动作 2>
```
