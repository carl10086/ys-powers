# commands/spec.md 轻量改造设计

- 日期：2026-04-27
- 类型：配置微调
- 目标文件：`commands/spec.md`

## 背景

当前 `commands/spec.md` 存在两个问题：
1. 调用 `agent-skills:spec-driven-development skill`，但本地 `skills/spec-driven-development/` 已存在，命名空间前缀多余。
2. 要求保存到项目根的 `SPEC.md`，不符合 ys-powers 按日期归档的文档约定。

## 目标

1. 去掉 `agent-skills:` 命名空间前缀，直接调用本地 skill。
2. 将输出路径改为 `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md`。
3. 要求生成的 spec 内容为中文（技术名词保留英文）。

## 非目标

- 不改动 `skills/spec-driven-development/SKILL.md` 的任何内容。
- 不改 spec 的 6 区域内容结构（objective / commands / project structure / code style / testing strategy / boundaries）。
- 不改其他 command 文件。

## 方案

方案 A（轻量 Override）：只改 `commands/spec.md`，不改 skill。

## 改动点

### 1. 去掉命名空间前缀

```diff
- Invoke the agent-skills:spec-driven-development skill.
+ Invoke the spec-driven-development skill.
```

### 2. 追加输出路径与语言要求

在文件末尾、保存指令之前，加 `<IMPORTANT>` 块：

```markdown
<IMPORTANT>
- Write the spec content in Chinese. Keep technical terms, code identifiers, file paths, and command names in English.
- Save the spec to `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md` where `<feature-name>` is a kebab-case short name derived from the spec title.
- If the directory does not exist, create it first.
- Confirm the file path with the user before saving.
</IMPORTANT>
```

## 验收标准

- [ ] `commands/spec.md` 中不再有 `agent-skills:` 前缀。
- [ ] `commands/spec.md` 包含 `<IMPORTANT>` 块，明确要求中文输出和 `docs/ys-powers/specs/` 路径。
- [ ] `skills/spec-driven-development/SKILL.md` 未被修改。
