# Spec: 在 refer/ 中增加 html-anything 并更新 CLAUDE.md

## Objective

在 `CLAUDE.md` 的 `refer/ 第三方参考项目` 章节中，补充 `html-anything` 的简短说明，使其与现有三个参考项目（agent-skills、superpowers、get-shit-done）的文档风格保持一致。

## Commands

无新增命令。本次变更仅涉及文档。

## Project Structure

无需创建新的目录或文件。变更范围仅限：

```
CLAUDE.md          ← 在 refer/ 章节下新增 html-anything 说明段落
```

不创建 `docs/html-anything/` 对照笔记（本次范围内不实施）。

## Code Style

- 保持与现有 `CLAUDE.md` 中其他 refer 项目一致的格式：三级标题 `### <project-name>/`，一段简短描述，一段 `**适用查阅**：...`
- 技术术语、项目名称保留英文
- 描述控制在 2-3 句话以内

## Testing Strategy

- 人工 review：确认描述准确反映 html-anything 的定位（agent skill，将各类输入转为美观 HTML 页面）
- 人工 review：确认格式与现有三个项目严格一致

## Boundaries

| 类型 | 内容 |
|------|------|
| **Always** | 只读参考；如有借鉴需求，应在 `skills/` 或 `commands/` 下重写，不得直接搬运 |
| **Ask first** | 若后续计划创建 `docs/html-anything/` 或搬运其中 prompts/styles |
| **Never** | 修改 `refer/html-anything/` 内任何文件；扩大本次变更范围至其他章节 |
