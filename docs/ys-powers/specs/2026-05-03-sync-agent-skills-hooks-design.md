# Spec: 同步 agent-skills hooks/session-start.sh JSON 转义修复

## 1. Objective（目标）

将 refer/agent-skills 在 commit `f504276` 中对 `hooks/session-start.sh` 的 JSON 转义修复同步到 ys-powers，消除 issue #89 风险：当 `SKILL.md` 内容包含引号、反斜杠等特殊字符时，手写 heredoc 构造的 JSON 可能输出无效格式，导致 Claude Code hook 解析失败。

## 2. Commands（涉及的命令/文件）

- **修改**：`.claude/hooks/session-start.sh`
- **参考**：`refer/agent-skills/hooks/session-start.sh`（commit `f504276`）
- **验证**：运行 hook 脚本，确认输出为合法 JSON

## 3. Project Structure（项目结构影响）

仅修改 1 个文件，无新增/删除：

```
.claude/hooks/
  └── session-start.sh   ← 修改
```

## 4. Code Style（编码规范）

- bash，匹配 refer 修复风格
- 使用 `jq` 命令构造 JSON，替代手写 heredoc
- 新增 `jq` 缺失时的优雅回退（`exit 0` + INFO 提示）
- 保持现有变量名和逻辑结构不变

## 5. Testing Strategy（测试策略）

- **步骤 1**：运行修复后的 hook：`bash .claude/hooks/session-start.sh`
- **步骤 2**：验证输出为合法 JSON（可用 `jq empty` 或目测）
- **步骤 3**：模拟 `jq` 缺失场景（临时重命名 `jq`），验证回退行为

## 6. Boundaries（边界）

- **Always**：
  - 保持 hook 的原有功能（注入 using-agent-skills meta-skill）不变
  - 仅修复 JSON 构造方式，不修改 message 内容或 priority
- **Ask First**：
  - 如果 ys-powers 的 `using-agent-skills` skill 内容与 refer 版本差异很大，是否需要同步 skill 内容本身
- **Never**：
  - 不碰 `.gemini/` 目录（Gemini CLI 不相关）
  - 不修改其他 hooks（`sdd-cache-*.sh`、`simplify-ignore*.sh` 不在本次范围）
  - 不修改 `skills/` 或 `commands/` 内容
