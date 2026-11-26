# Matt Pocock skills

除 `/teach` ownership cutover 外，本目录保持 Matt Pocock skills 的原始分包、Prompt、frontmatter、调用策略和 `agents/openai.yaml`；本地安装器只负责把 skill 扁平安装到 runtime 目录。

- Upstream: `https://github.com/mattpocock/skills.git`
- Pinned commit: [`abeeaf95660ba9e8b7c753eb38f441ca707a8823`](https://github.com/mattpocock/skills/commit/abeeaf95660ba9e8b7c753eb38f441ca707a8823)
- Relevant upstream paths: `skills/engineering/`、`skills/productivity/`
- Local reference: `refer/mattpocock-skills/`
- License: MIT

Active source 排除 Matt `productivity/teach/`，并删除 `ask-matt` 中对应的旧路由；`/teach` 由 `skills/pstack/teach/` 提供。Matt 原版保留在 `refer/mattpocock-skills/`。

同步上游时，必须在同一个 PR 中更新 skill 文件与 pinned commit。不要在本目录混入 local 或其他上游来源的 skill。
