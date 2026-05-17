# html-anything Skill 步骤说明

date: 2025-05-17

## 1. 目标 (Objective)

html-anything 是一个 Claude Code skill，用于将**想法、文件、文件夹、URL、导出数据集或富交付物请求**转换为可打开、分享或发布的精美单一 HTML 页面。

核心能力：把原本会输出成长篇 Markdown 的内容，转化为可视化、可交互、可分享的 HTML 产物。

---

## 2. 核心原则 (Core Principles)

### 2.1 两大不可妥协的约束

1. **Style Fidelity（风格保真度）**: 若某个 style 基于参考设计，必须复现该参考的布局系统、首屏结构、组件词汇、排版角色、颜色/表面语言和动效语法，而非仅借用"氛围"。
2. **Final HTML Compliance（最终 HTML 合规性）**: 交付的 HTML 必须在视觉上和结构上遵循所选 style，而非一个换了颜色的通用报告。

### 2.2 默认行为

- 当最终答案是**长内容、视觉化、结构化、对比性、教育性、报告性或可分享**时，优先创建 HTML 产物而非 Markdown。
- 不询问用户选择 style，默认使用 `auto` 自动路由。

---

## 3. 输入模式 (Inputs)

| 输入模式 | 处理方式 |
|---|---|
| **Idea / brief** | 将 brief 扩展为具体内容计划，选择 auto style，创建 HTML，必要时生成资源。 |
| **Local file** | 检查文件，若较大则采样，识别 source 类型，创建页面。 |
| **Folder** | 检查结构和代表性文件，创建 atlas / audit / browser 页面。 |
| **URL** | 获取/检查 URL 内容，基于页面/仓库/文章内容创建页面。 |
| **Export request** | 若用户提到平台/source 但没有文件，读取对应的 source prompt 导出指南，先指导用户导出。 |

---

## 4. 用例分类 (Use-Case Taxonomy)

所有请求先经过四大用例之一，再选择 style system：

| 用例 | 用户意图 | 可能使用的 styles |
|---|---|---|
| **Teaching Studios** | 将想法、文章、课程、长文本转换为交互式或引导式学习界面 | `teaching`, `architectural-spread`, `kami-reading` |
| **Files & Work Data** | 转换文件和工作产物：CSV、PDF、DOCX、Markdown、日志、CI 输出、邮件、财务、日历等 | `dashboard`, `soft-saas`, `document`, `kami-reading`, `architectural-spread`, `digital-eguide`, `editorial-carousel`, `developer`, `terminal-cli` |
| **Conversation Analysis** | 分析私人聊天、关系导出、团队频道或消息存档 | `love-romance-3d`, `kinetic-scoreboard`, `network-map` |
| **Personal Data & Places** | 从个人导出创建回顾/时间线/故事/地图：订单、健康、浏览记录、媒体、支付、笔记等 | `timeline-story`, `global-travel`, `living-essay`, `network-map`, `map-atlas` |

---

## 5. Style 自动选择 (Auto Style Selection)

### 5.1 Style 不是皮肤，是页面形状

- Style 改变的是**首屏结构、布局脚手架、组件词汇、交互模型、信息密度、图表语法和语气**，而非仅 CSS 换色。
- 先选系统，再在其中设计页面。

### 5.2 17 种 Auto Styles

| Style ID | 使用场景 | 页面形状 (Page Shape) |
|---|---|---|
| `default` | 未知、混合或弱分类的 brief/source | **Insight Brief**: 回答头、主洞察面板、证据栈、本地钻取 |
| `teaching` | 教程、课程、"教我"、交互式讲解器 | **Lesson Lab**: 视觉舞台、步骤轨道、试控、概念卡片、自检、回顾 |
| `love-romance-3d` | 1:1 聊天、情侣/朋友/家人聊天、关系导出 | **Keepsake 3D Rhythm**: 柔和 3D 封面、脉冲板、对比车道、隐私优先证据 |
| `living-essay` | Kindle 高亮、反思性文章、概念密集型阅读存档 | **Mycelium Writing Environment**: 纸质手稿、垂直边距问题、内联孢子词、活 SVG 线、安静附录 |
| `dashboard` | 财务/管理数据、日志、运营数据、问题跟踪器 | **Ops Console**: 命令栏、KPI 轨道、工作面、标记队列、可搜索数据网格 |
| `soft-saas` | 支持邮箱、邮件活动、入职程序、客户成功队列 | **Soft SaaS Console**: 淡色应用画布、个人资料/source 卡片、中央指标绽放、活动面板 |
| `kinetic-scoreboard` | 多参与者活动流、团队聊天、按贡献排名的贡献者 | **Kinetic Championship**: 全视口车道、实时排名、大计数器、动态活动体、遥测页脚 |
| `timeline-story` | 个人历史 — 时间顺序和主题 | **Timeline Story**: 时间镜头、时间线脊柱、章节面板、节奏条、记忆抽屉 |
| `global-travel` | 旅行历史、Uber/Lyft 行程导出、机场模式 | **Global Travel Map**: 居中标题、source 选择器、点状世界地图、温暖图钉、指标跑道、行程浏览器 |
| `map-atlas` | 保存的地点、路线、位置历史、地理标记照片元数据 | **Map Atlas**: 空间舞台、地点抽屉、时期/地点过滤器、航点浏览器 |
| `network-map` | 联系人、LinkedIn、Venmo/PayPal、人员/组织图 | **Network Map**: 图形画布、实体检查器、集群控件、中心卡片、链接记录 |
| `document` | 文章、阅读列表、书签、研究集合、PDF、DOCX、法律/医疗记录 | **Document Review**: 封面、阅读轨道、正文页、证据边距、钻取。语气在叙事 ↔ 正式之间转换 |
| `kami-reading` | 长散文、DOCX 备忘录、文章、手稿，用于持续阅读 | **Kami Longform Reader**: 温暖羊皮纸文档、衬线封面、内联目录、可打印章节、source 附录 |
| `architectural-spread` | 长格式视觉讲解器、对象聚焦文章、宣言 | **Architectural Editorial Spread**: 左侧视觉隔间、右侧奶油色内容面板、衬线斜体强调、角锚、分页点 |
| `digital-eguide` | 电子指南、PDF 指南、创作者指南、剧本、铅磁铁 | **Digital E-Guide Spread**: 温暖桌面上的两张纸页、封面+目录、内课、引用、步骤、练习条 |
| `editorial-carousel` | 品牌策略文章、创始人信件、文章要点、轻量报告 | **Editorial Carousel**: 期刊封面、展开轨道、4-8 论点展开、证据抽屉、复制动作 |
| `developer` | Diff、PR 补丁、CI 日志、堆栈跟踪、仓库 | **Terminal Evidence Workbench**: 提示行、热点、风险检查清单、原始产物导航器、可复制交接 |
| `terminal-cli` | 终端、CLI、shell、大型机、黑客、服务器控制台 | **Terminal CLI**: shell 提示、状态轨道、终端窗格网格、命令控件、原始控制台、扫描线覆盖 |

### 5.3 自然语言路由规则

- "make it a tutorial" / "teach me" → `teaching`
- "make it more app-like" / "interactive studio" → `teaching` + object/model 作为主舞台
- "make it a carousel" / "magazine feel" → `editorial-carousel`
- "make it an e-guide" / "PDF guide" / "playbook" → `digital-eguide`
- "make it like a SaaS panel" / "support console" → `soft-saas`
- "more dashboard-like" → 增加密度、过滤器、图表
- "make it a map" / "spatial" → `map-atlas`
- "travel history" / "Uber history" → `global-travel`
- "show relationships/network" → `network-map`
- "make it terminal/CLI/mainframe" → `terminal-cli`
- 若都不匹配 → `default`

---

## 6. 标准工作流 (Standard Workflow)

### Step 1: Understand the request
决定用户提供的输入类型：idea、file、folder、URL 还是 export request。

### Step 2: Onboard exports when needed
若用户提到 source 但没有文件：
- 读取 `prompts/sources/<source>.md` 中的导出步骤
- 给出简明的导出指导
- **停止**，除非文件已可用

### Step 3: Inspect the source or brief
- **Files/Folders**: 读取代表性样本，收集统计信息
- **URLs**: 获取/检查足够内容以理解形状
- **Ideas/Briefs**: 自行创建结构化内容计划。对当前或高风险事实使用 web verification。

### Step 4: Load guidance
读取以下文件：
1. `prompts/styles/_design.md` — Clockless 设计系统 token
2. `prompts/styles/catalog.json` — style 元数据和路由信息
3. 最接近的 source prompt (`prompts/sources/<source>.md`)
4. 若适用，读取共享 family prompts (`_chat`, `_finance`, `_developer`, `_geo` 等)
5. 使用 catalog entry 作为紧凑的 preflight checklist
6. 读取并遵循 `prompts/styles/<style>.md`
7. 若 catalog entry 有 `referenceHtml`，读取该文件作为视觉目标

### Step 5: Choose auto style
内部选择页面 style。**不要**询问用户选择，除非他们明确要求 style 选项。

### Step 6: Extract the style contract
在编写 HTML 之前，识别所选 style 的 5-8 个核心不变量：
1. 首屏几何结构 (first viewport geometry)
2. 布局脚手架 (layout scaffold)
3. 排版角色 (typography roles)
4. 颜色/表面语言 (color/surface language)
5. 组件词汇 (component vocabulary)
6. 主要交互 (primary interaction)
7. 动效语法 (motion grammar)
8. 必须 absent 的元素

从 `catalog.json` 提取 required primitives 和 avoid rules，从 style prompt 和 reference HTML 提取视觉细节。

### Step 7: Build the page
直接创建 HTML/CSS/JS：
- 保持页面有用、可交互、移动响应式、内容特定
- 在需要时包含搜索/过滤/复制功能
- 在根 `<html>` 元素上放置 `data-ha-style="<selected-style>"`
- 使用 style 的类/组件词汇

### Step 8: Generate assets when they improve the artifact
- 在生成新资源之前，检查是否有匹配的 `referenceAssets` 或官方示例资源文件夹
- 在许可和上下文允许时重用适当文件
- 使用 `imagegen` skill/tool 生成 raster 资源（对象模型、封面艺术、精灵图、纹理、预览图）
- 将项目绑定资源保存到输出文件夹
- 不要将引用资源仅留在 `$CODEX_HOME/generated_images`

### Step 9: Verify in a browser
通过本地文件或本地 HTTP 打开 HTML，检查：
- [ ] 页面非空白
- [ ] 桌面和移动视口渲染干净
- [ ] 无明显水平溢出
- [ ] 对比度可读，焦点状态可见
- [ ] 核心交互存在键盘和触摸路径
- [ ] 主要交互正常工作
- [ ] 生成的资源加载成功
- [ ] **Style Fidelity**: 首屏与所选 style 的 required scaffold 匹配
- [ ] source-required modules 被转换为 style 的原生组件词汇
- [ ] 页面未回退到通用的 hero/KPI/card/table 模式（除非该 style 本应如此）

若任一项失败，在交接前修订 HTML。

### Step 10: Handoff
- 给用户本地路径或实时链接
- 提及重要的生成资源（如有）
- 提及浏览器验证
- 保持解释简短
- **不要**解释内部 pipeline，除非用户询问

---

## 7. Style Fidelity Gate（交接前检查清单）

最终 HTML 必须通过以下内部检查清单：

- [ ] 根 `<html>` 声明了 `data-ha-style`
- [ ] 首屏由所选 style 的 scaffold 构建
- [ ] 若 style 有 catalog `referenceHtml`，生成的首屏在视觉上与参考的 scaffold、token 系统、表面语言和交互语法匹配
- [ ] HTML 中至少出现四个 style-specific 的类名/组件
- [ ] 主要交互是 style 原生的，且与本地数据工作
- [ ] Required source modules 存在，但以 style 的词汇塑造
- [ ] 文本对比度、焦点状态、键盘访问和触摸目标满足 UI 质量门
- [ ] 图表和密集视觉有可见值或列表/表格回退，不单独依赖颜色
- [ ] 无意外的 body 级水平溢出；有意水平舞台有明确控件
- [ ] 动效遵循 style 的 motion grammar 并尊重 `prefers-reduced-motion`
- [ ] 页面完整、可离线使用，不只是重新着色的默认报告

---

## 8. 设计系统 (Design System)

### 8.1 Clockless Tokens

默认使用 `prompts/styles/_design.md` 中的 Clockless 设计系统：
- **Brand**: `--primary: #a03b00`, `--secondary: #d5baff`, `--tertiary: #4d44e3`
- **Surface**: `--bg: #fff8f6`, 多层次 surface container
- **Text**: `--fg-1: #1e1b19`, `--fg-2: #594138`, `--fg-muted: #8d7166`
- **Font**: `Space Grotesk` (headline), `Plus Jakarta Sans` (body), `SF Mono` (mono)
- **Dark mode**: `prefers-color-scheme: dark` 自动切换

### 8.2 通用设计要求

- Mobile-first 响应式布局
- WCAG AA 对比度，有意义的文本、可见焦点状态、标记控件、44px 主要触摸目标
- 报告/数据产物支持 light + dark mode；app-like 示例可仅 polished light-mode
- 内联 CSS 和 JS，无外部 JS/CDN 依赖（除非用户明确允许）
- 唯一默认外部字体调用是 `_design.md` 的 Google Fonts
- 需要丰富视觉主题时生成 bitmap 资源；确定性图表和 UI 使用 SVG/CSS/canvas
- 不构建通用 landing page，用户要工具就建工具，要 dashboard 就建 dashboard

---

## 9. 数据与隐私默认 (Data & Privacy Defaults)

- **默认敏感**: 将生成的 HTML 视为与 source 数据同等敏感，因为它可能在客户端嵌入 source 记录
- **亲密聊天**: 默认不包含 raw-message 附录，使用聚合图表和小的匿名化证据片段
- **高风险 sources**（医疗、法律、税务、会计、移民、保险、投资相关）: 保持观察性，包含免责声明，不提供专业建议
- **标识符遮蔽**: 对联系人、支付、聊天和个人导出，遮蔽或省略敏感标识符，除非用户要求显示
- **照片元数据优先**: 对 Google Photos 风格 sources，优先仅元数据分析，除非用户明确要求检查实际媒体

---

## 10. 采样指导 (Sampling Guidance)

读取足够内容以理解 source 形状，但避免将巨大私人导出不必要地加载到模型中：

| Source 类型 | 采样内容 |
|---|---|
| **Tabular data** | 表头、前/后几行、列统计、日期范围、类别、数值摘要 |
| **Chat** | 首/末消息、发送者列表、时间跨度、日/月计数、媒体/删除/转账计数 |
| **Long text** | 标题、首节、字数、章节大纲 |
| **Email** | 线程数、发送者数、首/末消息、未闭合循环 |
| **Transcript** | 说话者统计、首/末提示、最长提示、决策和行动项线索 |
| **Event/log stream** | 推断 schema、严重度/类别计数、时间桶直方图、代表性错误/异常 |
| **Finance/admin** | 收入/支出/净值或状态总计、类别、周期性项目、重复/异常 |
| **Geo/routes** | bbox、距离、点数、海拔/配速（如有）、航点列表 |
| **Folder/repo** | 树、README/索引文件、代表性关键文件 |

---

## 11. Source Prompts 目录结构

```
prompts/
├── sources/           # Source-specific 导出步骤和内容分析指导
│   ├── _sensitive.md  # 共享隐私/敏感数据处理规则
│   ├── _developer.md  # 开发者相关 sources 共享规则
│   ├── _document.md   # 文档相关 sources 共享规则
│   ├── _planning.md   # 规划相关 sources 共享规则
│   ├── default.md     # 通用回退
│   ├── csv.md
│   ├── json.md
│   ├── wechat.md
│   ├── whatsapp.md
│   ├── slack.md
│   ├── email.md
│   ├── bank-transactions.md
│   ├── amazon-orders.md
│   ├── github-repo.md
│   └── ... (50+ sources)
└── styles/            # Reusable page systems
    ├── _design.md     # Clockless token system
    ├── _system.md     # 共享系统规则
    ├── catalog.json   # Style 元数据、路由、质量门单一真相源
    ├── README.md      # Styles 目录说明
    ├── default.md     # 默认 Insight Brief
    ├── teaching.md    # Lesson Lab
    ├── dashboard.md   # Ops Console
    ├── love-romance-3d.md
    ├── timeline-story.md
    ├── global-travel.md
    ├── map-atlas.md
    ├── network-map.md
    ├── document.md
    ├── kami-reading.md
    ├── architectural-spread.md
    ├── digital-eguide.md
    ├── editorial-carousel.md
    ├── developer.md
    ├── terminal-cli.md
    └── references/    # 参考 HTML 和资产
        ├── teaching/
        │   ├── object-lab.html
        │   └── assets/
        └── ...
```

---

## 12. 输出规范 (Outputs)

### 12.1 默认输出
- `output.html`，位于 source 旁边，或从 brief 开始时放在清晰的项目/示例文件夹中
- 若用户给 `foo.csv`，`foo.html` 也可接受（若对本地工作流更自然）

### 12.2 资源输出
- 若生成的图片、精灵图、缩略图或其他本地媒体能让页面实质更好，在 HTML 旁边创建 `assets/` 文件夹
- 若用户要求 "single-file"，将 CSS、JS、数据和资产内联到一个 HTML 文件中（在可行情况下）

### 12.3 最终响应
- 给出 HTML 的路径/链接
- 提及重要的生成资源（如有）
- 提及浏览器验证
- **不要**解释内部 pipeline，除非用户询问
