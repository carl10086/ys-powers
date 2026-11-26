# Cursor pstack skills

本目录收纳来源于 Cursor pstack、但在 ys-powers 中独立启用的 skills；它们不属于 Matt workflow 分包。

- Upstream: `https://github.com/cursor/plugins.git`
- Pinned commit: [`41e400932eca14f289e7db717a70455256b6d388`](https://github.com/cursor/plugins/commit/41e400932eca14f289e7db717a70455256b6d388)
- Relevant upstream path: `pstack/skills/`
- Local reference: `refer/cursor-plugins/pstack/`
- License: MIT

当前内容：

- `bro/`：基于 `pstack/skills/bro/`，保留本地 runtime metadata。
- `why/`：基于 `pstack/skills/why/` 的中文五步改编，保留上游 attribution。
- `how/`：原样保留 `pstack/skills/how/SKILL.md`，仅增加本地 runtime metadata。
- `teach/`：原样保留 `pstack/skills/teach/SKILL.md`；实验性组合 `how`、`why` 与 `unslop`，跨 skill 调用必须经过 runtime smoke test。
- `unslop/`：原样保留 `pstack/skills/unslop/SKILL.md`，既可独立调用，也是 `teach` 的显式依赖。

同步上游时，必须在同一个 PR 中更新 skill 文件与 pinned commit。不得把 pstack router 或整套 plugin 隐式引入本目录。
