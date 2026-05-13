# Spec: build-doc Command

## Objective

为文档工作流（spec → plan → build-doc）设计 `build-doc` command，替代 `build` 在文档场景中的角色。

`build` 的核心是 TDD + 编译验证（写失败测试 → 实现代码 → 运行测试 → 运行构建 → 提交），这些步骤对文档工作不适用。文档需要的是**增量写作 → 审校 → 格式验证 → 保存**。

`build-doc` 的使命：按照 plan 中拆分的文档任务，逐条完成写作，并通过自检清单确保输出符合中文技术文档规范。

## Tech Stack

- Markdown（文档载体）
- `markdownlint-cli`（可选格式检查）
- `vale`（可选写作风格检查）

## Commands

```bash
# 文档格式检查（可选）
npx markdownlint-cli "docs/**/*.md"

# 写作风格检查（可选）
vale docs/

# 生成/更新文档（build-doc 的核心，无需外部命令）
```

## Project Structure

```
commands/
  build-doc.md          # command 定义（本 spec 的目标产物）

docs/ys-powers/guidelines/
  chinese-tech-writing-guide.md   # 中文技术文档写作规范（审校依据）
```

## Code Style

command 文件遵循 Anthropic Skill Authoring Best Practices：

- **简洁**：body 控制在 500 行以内，多余内容拆分到引用文件
- **第三人称 description**："Implements..." 而非 "I can help you..."
- **渐进式披露**：核心流程在 command 中，详细规范引用 guidelines 文件
- **Checklist 模式**：复杂流程提供可勾选的进度清单
- **自由度适中**：提供标准模板，但允许根据文档类型适配

## Testing Strategy

1. **Self-test**：build-doc command 写完后，用它自身来生成/审校一篇示例文档
2. **writing-skills skill 调试**：将 build-doc 作为 skill 加载，测试 Claude 是否能正确触发、读取相关文件、执行流程
3. **验收标准**：
   - build-doc 能正确读取 plan 中的 pending 任务
   - 能按 checklist 完成自检
   - 能引用 chinese-tech-writing-guide.md 中的规范
   - 输出文档符合技术文档格式要求

## Boundaries

- **Always**：
  - 读取 plan 中的验收标准，确保文档内容覆盖所有要点
  - 执行审校 checklist 后再保存
  - 引用 chinese-tech-writing-guide.md 作为规范依据

- **Ask first**：
  - 修改已有文档结构（如增删章节）
  - 使用自动化工具（markdownlint、vale）需要项目已配置
  - 涉及外部发布（如同步到文档站点）

- **Never**：
  - 执行代码测试或编译（这是 build 的职责）
  - 修改代码逻辑或配置文件
  - 跳过审校直接保存
  - 生成超出 plan 范围的文档内容

## Success Criteria

- [ ] build-doc.md 文件创建成功，body 不超过 500 行
- [ ] description 使用第三人称，包含触发条件和用途
- [ ] 核心流程使用 checklist 模式，便于跟踪进度
- [ ] 能引用 chinese-tech-writing-guide.md 进行审校
- [ ] 与现有 spec、plan command 风格一致
- [ ] 通过 writing-skills skill 调试，Claude 能正确触发和执行

## Open Questions

- 是否需要为不同文档类型（安装指南、API 文档、故障排查）提供差异化流程？
- 是否需要集成自动化工具（markdownlint、vale）的调用？
