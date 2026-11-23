# Domain Docs

Engineering skills 探索代码库时，按以下规则消费 domain documentation。

## Before exploring, read these

- 根目录的 `GLOSSARY.md`；或
- 若存在根目录 `GLOSSARY-MAP.md`，读取与当前主题相关的每个 context 的 `GLOSSARY.md`；
- 读取涉及当前工作区域的 `docs/adr/` 中的 ADR。

文件不存在时静默继续，不要主动建议预先创建。`domain-modeling` skill 会在术语或决策真正确定时按需创建这些文件。

## File structure

本仓库使用 single-context：

```text
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

## Use the glossary's vocabulary

在 issue title、refactor proposal、hypothesis、test name 等输出中命名 domain concept 时，使用 `GLOSSARY.md` 定义的术语。若 glossary 明确避免某个 synonym，不要使用它。

若所需 concept 尚未记录，说明可能正在发明项目未使用的语言，或存在 glossary gap；交由 `domain-modeling` 处理。

## Flag ADR conflicts

若输出与现有 ADR 冲突，必须明确指出，而不是静默覆盖。

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_
