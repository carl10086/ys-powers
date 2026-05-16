# document-skills

## 定位

一套专业的办公文档处理技能集，覆盖 Word（docx）、PDF、PowerPoint（pptx）、Excel（xlsx）四类核心格式的创建、编辑、分析和转换。

## 触发时机

- 需要创建或修改 `.docx`、`.pdf`、`.pptx`、`.xlsx` 文件时
- 需要从现有文档中提取文本、表格或元数据时
- 需要合并、拆分或转换文档格式时
- 需要处理文档中的修订痕迹（tracked changes）或批注时
- **不适用**：仅需阅读文档内容且已有其他工具（如 pandoc）可用时

## 核心能力

### DOCX（Word 文档）

1. **创建新文档**：使用 python-docx 从头生成带格式的 Word 文档
2. **基本 OOXML 编辑**：对自有文档进行简单修改
3. **修订模式（Redlining）**：对他人文档进行带修订痕迹的编辑，适用于法律、学术、商业文档
4. **文本提取**：使用 pandoc 将 docx 转为 Markdown，支持 `--track-changes=all` 查看修订

### PDF

1. **文本提取**：使用 `pypdf` 提取页面文本内容
2. **合并与拆分**：使用 `PdfWriter` / `PdfReader` 合并多个 PDF 或提取指定页面
3. **表单处理**：读取 `forms.md` 获取填表专用流程
4. **创建新 PDF**：使用 Python 库生成新文档

### PPTX（PowerPoint）

1. **读取幻灯片**：提取幻灯片文本、布局、模板信息
2. **生成演示文稿**：创建新幻灯片，调整布局和设计
3. **模板应用**：基于现有模板批量生成演示内容

### XLSX（Excel）

1. **公式与计算**：处理 Excel 公式、数据转换
2. **图表生成**：创建和修改图表
3. **数据操作**：读写单元格、批量处理数据

## 各子 Skill 的工作流决策树

| 任务 | DOCX 推荐工作流 | PDF 推荐工作流 |
|------|----------------|----------------|
| 仅读取内容 | `pandoc docx → markdown` | `pypdf.extract_text()` |
| 创建新文档 | python-docx / OOXML | Python 库（reportlab 等） |
| 编辑自有文档 | 基本 OOXML 编辑 | 合并/拆分/重组 |
| 编辑他人文档 | **Redlining 修订模式** | — |
| 法律/学术/政府文档 | **Redlining 模式（强制）** | — |

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 的 `html-anything` 擅长生成 HTML 页面，而 `document-skills` 专注于传统办公文档。两者互补：HTML 适合 Web 展示，Office 文档适合正式交付
- **借鉴价值**：DOCX 的「修订模式（Redlining）」工作流对任何需要「安全编辑他人文档」的场景都有参考价值；PDF 的表单处理流程可作为标准化操作模板
- **搬运建议**：中等价值。若 ys-powers 的使用者经常需要处理 Office 文档，值得搬运。注意部分子 skill 使用 Proprietary 许可证

## 元信息

- 来源：`refer/awesome-claude-skills/document-skills/{docx,pdf,pptx,xlsx}/SKILL.md`
- 维护者：Composio / 社区
- 许可证：docx 和 pdf 为 Proprietary（详见各子目录 `LICENSE.txt`），其余以目录内标注为准
