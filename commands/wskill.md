---
description: Use when creating or materially editing a skill with a predictable trigger, scope, and information hierarchy
argument-hint: [skill-name-or-idea]
disable-model-invocation: true
---

# /wskill

写 skill。目标不是把内容写长，而是让 future agent **稳定触发、稳定执行、稳定停在正确完成点**。

## Flow

1. 先判断是否真的需要 skill：跨项目复用、需要 agent 判断、无法用脚本/规则机械约束时才写；项目惯例放 `CLAUDE.md`。
2. 读取 `writing-great-skills`，用它决定 invocation、description、information hierarchy、split、prune。
3. 查已有 `skills/*/SKILL.md`：有重叠就扩展或替换，不新增第二套 convention。
4. 只在需求会影响 trigger / scope / public behavior 且 repo 无法回答时，按 `explore-then-ask` 一次问一个问题；否则直接写。
5. 保存到 `skills/<kebab-case-name>/SKILL.md`；supporting files 只放 heavy reference、工具、模板。
6. Verify：frontmatter 合法；body 中文；technical identifiers 保持英文；description 只写 trigger；无重复 reference；无 no-op 句子；路径存在。

## High-risk exception

如果 skill 是 discipline-enforcing（例如禁止某类捷径、要求某种流程），补 1-2 个 pressure scenarios 验证 agent 不会绕过。普通 reference / workflow skill 不走重型 RED-GREEN-REFACTOR。
