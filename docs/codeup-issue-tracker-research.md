# 云效 Codeup 作为 issue tracker 的可行性调研

访问日期：2026-11-25

## 结论

1. **可以支持云效，但不能把 Codeup 本身直接等同于 issue tracker。** Codeup 的官方边界是代码托管、评审、检测和搜索；需求、缺陷、任务等工作项属于云效项目协作 Projex。要满足本仓库 tracker contract，应以 **Projex work item 作为 ticket**，以 **Codeup change request 作为 MR**。[Codeup 产品说明](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-code-management)；[Projex 产品说明](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-project-collaboration-1)
2. **云效整体上能覆盖当前 contract。** create/view/list/edit/comment、assignee、父子关系和依赖关系都有原生 work item 模型及 OpenAPI；close 需要映射到项目自定义 workflow 的终态；frontier 需要客户端组合查询后计算，官方文档没有一条直接返回“未认领且无开放 blocker”的接口。[工作项 API 目录](https://help.aliyun.com/zh/yunxiao/developer-reference/work-items/)；[工作项关系说明](https://help.aliyun.com/zh/yunxiao/user-guide/work-item-relationship-customization-settings)
3. **没有找到一个与 `gh` / `glab` 同类的、独立通用的 Codeup 专用官方 CLI。** 最接近的官方自动化入口是通用 Alibaba Cloud CLI 的 `aliyun devops` 插件，它覆盖 `codeup-*` 和 `projex-*` 命令；官方同名 `Codeup-CLI` 是批量迁移工具，不是日常 work item/MR 客户端。[云效 CLI 指南](https://help.aliyun.com/zh/yunxiao/developer-reference/how-to-install-initialize-and-use-the-apsara-devops-cli)；[Codeup-CLI 安装与迁移范围](https://help.aliyun.com/zh/yunxiao/user-guide/install-the-local-migration-tool)
4. **当前即可通过 `setup-matt-pocock-skills` 的 `Other` / custom tracker 接入，不建议立即新增内置 template。** 先用一个薄 wrapper 固化部署类型、项目、work item 类型、终态和 ID 解析；完成真实组织验证后，再考虑新增 Yunxiao template。

## 调研范围与判断口径

### 本仓库 tracker contract

本仓库 setup skill 目前内置 GitHub、GitLab 和 local Markdown，其他 tracker 以 freeform prose 写入 `docs/agents/issue-tracker.md`；GitHub/GitLab 依赖各自官方 CLI，local tracker 依赖文件约定。[setup skill](../skills/matt/engineering/setup-matt-pocock-skills/SKILL.md)；[GitHub template](../skills/matt/engineering/setup-matt-pocock-skills/issue-tracker-github.md)；[GitLab template](../skills/matt/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md)；[local template](../skills/matt/engineering/setup-matt-pocock-skills/issue-tracker-local.md)

从三个 template 与本仓库当前配置中提取出的最小 contract 为：

- ticket 的 create、view/read、list/filter、edit、comment、close；关闭前先写解释；
- labels/tags 与 assignee；
- PR/MR 的 create/view/list/comment/label/close，以及可选的“PR/MR as a triage surface”；
- wayfinding 的 map、parent-child、blocking dependency、claim、resolve、frontier；
- frontier 的语义是：map 下仍开放、无开放 blocker、无 assignee 的 child ticket，按 map 顺序取第一个；
- 命令输出应可机器解析，并能从本地 clone 或显式配置稳定确定目标仓库/项目。

本仓库当前 `docs/agents/issue-tracker.md` 只配置了 GitHub 的 create/read/list/comment/label/close 基线；完整 wayfinding contract 来自 seed templates。[当前 tracker 配置](agents/issue-tracker.md)

### 状态标记

- **native**：云效有明确的一等模型，并有当前官方 OpenAPI；`aliyun devops` 可作为该 OpenAPI 的官方 CLI 前端。
- **API-only**：能用官方 OpenAPI/通用 CLI 组合实现，但没有与 contract 同语义的一步操作，wrapper 必须补齐映射或计算。
- **fallback**：不依赖原生能力、退回 description/comment 中的文本约定。
- **unsupported/unclear**：当前官方资料未证明可满足，或行为依赖组织配置且缺少足够说明。

这里的 **API-only** 不表示“只能手写 `curl`”：官方明确说明 `aliyun devops` 用于调用云效 OpenAPI，并提供 `codeup-*`、`projex-*` 命令族及 JSON/JMESPath 输出。[云效 CLI 指南](https://help.aliyun.com/zh/yunxiao/developer-reference/how-to-install-initialize-and-use-the-apsara-devops-cli)

## 产品边界：Codeup 与 Projex

### Codeup

Codeup 的官方定义是代码管理服务，核心能力为代码托管、评审、检测和搜索；其功能表把合并请求、OpenAPI、Webhook、Git 身份认证列为 Codeup 能力，但没有把需求、缺陷或任务作为 Codeup repository 内的 issue 对象。[Codeup 产品说明](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-code-management)

因此，若用户只有 Codeup repository、没有可用的 Projex project，则**不能仅靠 Codeup 满足本仓库 issue tracker contract**。Git CLI 也只负责 clone/add/commit/push/pull、branch 和 remote 等 Git 数据操作，不管理 work item 或 MR 元数据。[Codeup Git 指南](https://help.aliyun.com/zh/yunxiao/user-guide/quick-to-get-started)

### Projex

Projex 明确提供项目、需求、缺陷、任务、迭代规划和自定义流程，才是 issue/work item 所属产品面。[Projex 产品说明](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-project-collaboration-1)

两者不是割裂的：

- 创建 Codeup MR 时可传 `workItemIds` 关联 Projex work items。[CreateChangeRequest](https://help.aliyun.com/zh/yunxiao/developer-reference/createchangerequest-create-merge-request)
- Projex 可用 `codeupMergeRequest`、`codeupBranch`、`codeupCommit` external relation 回链 Codeup 资源。[CreateWorkitemExtRelationRecord](https://help.aliyun.com/zh/yunxiao/developer-reference/new-work-item-associates-external-resources)

推荐的数据模型是：

```text
Projex project
└── work item（ticket / spec / map / child）
    ├── status / assignee / labels / comments
    ├── PARENT / SUB
    ├── DEPEND_ON / DEPENDED_BY
    └── external relation → Codeup MR / branch / commit

Codeup repository
└── change request（MR）
    └── workItemIds → Projex work items
```

## 兼容性矩阵

| Contract 项 | 兼容性 | 官方能力与限制 | 对 setup 的含义 |
| --- | --- | --- | --- |
| create | **native** | `CreateWorkitem` 可创建需求、缺陷、任务、风险、主题等，支持 Markdown description、`assignedTo`、`labels`、`parentId`；但必须预先知道 `spaceId`、`workitemTypeId` 和 assignee user ID。[CreateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitem) | wrapper 需把默认 ticket type、project 和 assignee 解析为 ID。 |
| view/read | **native** | `GetWorkitem` 返回 title、description、status、assignee、labels、`parentId`、`idPath` 等。[GetWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/getworkitem) | 另调 comments 与 relations，才能得到与 `gh issue view --json ...comments` 相近的完整视图。 |
| list/filter | **native** | `SearchWorkitems` 支持按 status、assignee、creator、tag、日期等条件搜索和分页；一次仅搜索一个 project 或 program，且 `page * perPage <= 10000`。[SearchWorkitems](https://help.aliyun.com/zh/yunxiao/developer-reference/searchworkitems) | 单项目 tracker 足够；跨项目必须逐项目调用并合并。 |
| edit | **native** | `UpdateWorkitem` 可改 title、description/format、status、assignee、priority，并允许按 field ID 更新配置字段。[UpdateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/updateworkitem) | wrapper 需从 field config 解析组织自定义字段，而不能硬编码所有 ID。 |
| close | **API-only** | 当前 work item API 目录没有 `CloseWorkitem`；状态由项目 workflow 配置，先读取状态列表，再用 `UpdateWorkitem` 写入目标 `statusId`。删除是另一个操作，不能代替关闭。[工作项 API 目录](https://help.aliyun.com/zh/yunxiao/developer-reference/work-items/)；[GetWorkitemWorkflow](https://help.aliyun.com/zh/yunxiao/developer-reference/getworkitemworkflow-get-a-list-of-the-status-of-the-work-item)；[UpdateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/updateworkitem) | 配置必须显式记录 terminal status ID/name；按 contract 先 comment，再转终态。不能把 `DeleteWorkitem` 当 close。 |
| comment | **native** | 可创建和列出 work item comments，支持 Markdown/Rich Text、父评论、作者和时间。[CreateWorkitemComment](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitemcomment)；[ListWorkitemComments](https://help.aliyun.com/zh/yunxiao/developer-reference/listworkitemcomments) | 可直接实现发布进展、关闭说明和 resolve answer。 |
| labels/tags | **native + unclear** | project 可 create/list labels；work item 创建可传 label ID，读取与搜索可返回/过滤 labels。当前 `UpdateWorkitem` 文档没有明确给出既有 work item 增删 label 的完整示例，仅说明按 field ID 更新，因此该部分需在真实 project 的 field config 上验证。[CreateLabel](https://help.aliyun.com/zh/yunxiao/developer-reference/createlabel)；[ListLabels](https://help.aliyun.com/zh/yunxiao/developer-reference/listlabels)；[CreateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitem)；[UpdateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/updateworkitem) | 创建时可原生打标签；既有 ticket 的 add/remove label 在纳入 template 前应做集成验证。必要时可 **fallback** 到自定义 `Status` 字段或 description 约定。 |
| assignee / claim | **native** | create/update/get/search 都支持 `assignedTo`；值是 user ID，而非 `@me` 字符串。[CreateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitem)；[UpdateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/updateworkitem)；[SearchWorkitems](https://help.aliyun.com/zh/yunxiao/developer-reference/searchworkitems) | wrapper 需要获取当前用户 ID，并把 claim 实现为第一次写入 assignee。 |
| parent-child | **native** | create 支持 `parentId`；relation records 支持 `PARENT` / `SUB`；Projex 官方模型是一父多子，但组织可启停/自定义类型间关系。[CreateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitem)；[CreateWorkitemRelationRecord](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitemrelationrecord)；[关系自定义说明](https://help.aliyun.com/zh/yunxiao/user-guide/work-item-relationship-customization-settings) | map 可做父 work item，ticket 做 child；setup 时要验证目标 work item types 之间已启用父子关系。不可用时 **fallback** 为 child description 顶部 `Part of <serialNumber>`。 |
| blocking dependencies | **native** | relation records 支持 `DEPEND_ON`（依赖项）和 `DEPENDED_BY`（支撑项），可 create/list/delete；Projex 把依赖定义为有向多对多，依赖方需等待被依赖方完成。[CreateWorkitemRelationRecord](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitemrelationrecord)；[ListWorkitemRelationRecords](https://help.aliyun.com/zh/yunxiao/developer-reference/listworkitemrelationrecords)；[关系自定义说明](https://help.aliyun.com/zh/yunxiao/user-guide/work-item-relationship-customization-settings) | 将 “child blocked by blocker” 映射为 child `DEPEND_ON` blocker。类型关系未启用时 **fallback** 为 `Blocked by: <serialNumber>`。 |
| frontier | **API-only** | 依赖边与 work item 状态均可查询，但当前工作项 API 目录没有 first-class frontier/ready endpoint；relation list 也不直接返回相关 work item 的完整状态。[ListWorkitemRelationRecords](https://help.aliyun.com/zh/yunxiao/developer-reference/listworkitemrelationrecords)；[GetWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/getworkitem)；[工作项 API 目录](https://help.aliyun.com/zh/yunxiao/developer-reference/work-items/) | wrapper 必须：列 map children → 去掉终态 → 逐项查 `DEPEND_ON` → 查 blocker 状态 → 去掉已有 assignee。官方 API 未说明稳定的 map-child 手工排序字段，故“first in map order”应由自定义 order field 或 map description 顺序提供；否则为 **unclear**。 |
| MR create/view/list/edit/close/comment/merge | **native（Codeup）** | 当前 MR API 目录包含 create/get/list/update/close/reopen/comment/review/merge/diff/patch sets/CI checks/labels；list 支持 repository、state、author、reviewer 等过滤。[MR API 目录](https://help.aliyun.com/zh/yunxiao/developer-reference/merge-request-1/)；[ListChangeRequests](https://help.aliyun.com/zh/yunxiao/developer-reference/listchangerequests-query-the-list-of-merge-requests) | MR 操作走 `codeup-*`，ticket 操作走 `projex-*`；不要混成一个 Codeup issue API。 |
| work item ↔ MR | **native** | MR 创建可带 `workItemIds`；work item 可创建 `codeupMergeRequest` external relation。[CreateChangeRequest](https://help.aliyun.com/zh/yunxiao/developer-reference/createchangerequest-create-merge-request)；[CreateWorkitemExtRelationRecord](https://help.aliyun.com/zh/yunxiao/developer-reference/new-work-item-associates-external-resources) | wrapper 应同时建立或核对双向关联，至少保证从 ticket 能定位 MR。 |
| external MR triage surface | **unsupported/unclear** | Codeup 可列 MR、读取 author 和 reviewer，但当前 list 文档未给出类似 GitHub `author_association` 的“外部贡献者/组织成员”分类语义。[ListChangeRequests](https://help.aliyun.com/zh/yunxiao/developer-reference/listchangerequests-query-the-list-of-merge-requests) | 保持 `MRs as a request surface: no`。若未来开启，需额外查询组织/项目成员并定义“external”。 |

## 官方工具与 CLI 结论

### `aliyun devops`：可自动化，但不是独立 Codeup CLI

官方现在推荐安装通用 Alibaba Cloud CLI，再安装 `aliyun-cli-devops` 插件：

```bash
aliyun plugin install --names aliyun-cli-devops
aliyun devops version
aliyun devops --help
```

其命令按产品分为 `codeup-*`、`projex-*` 等，输出为 JSON，并可用 `--cli-query` 做 JMESPath 过滤；官方示例包括 `aliyun devops projex-search-workitems` 与 `codeup-list-repositories`。[云效 CLI 指南](https://help.aliyun.com/zh/yunxiao/developer-reference/how-to-install-initialize-and-use-the-apsara-devops-cli)

这使它足以作为 wrapper 的底层 transport，但体验上不同于 `gh issue ...` / `glab issue ...`：

- 它是通用 `aliyun` CLI 的插件，不是 repository-aware 的独立 Codeup 客户端；
- 命令按 OpenAPI operation 展开，ticket 跨 `projex-*`，MR 跨 `codeup-*`；
- 通常需要显式的 organization/project/repository/work item type/status/user IDs；
- 不会自动提供本仓库 contract 中的“comment then close”“claim”“frontier”等高层语义。

官方 `aliyun` GitHub 组织的 command catalog 也把 Alibaba Cloud CLI command set 与 MCP toolset 分开，并记录 `codeup-*`、`projex-*` 两组命令及 `aliyun devops --help` 的发现方式。[官方 command catalog](https://github.com/aliyun/alibabacloud-aiops-skills/blob/master/skills/developertools/rdc/alibabacloud-devops/references/tool-catalog.md)

### `Codeup-CLI`：名字相似，但只是迁移工具

官方 `Codeup-CLI` 文档限定的对象是：自建 GitLab 的 Git 数据、权限、Webhooks、保护分支和开启的 MR，以及 GitHub/Gitee/Coding 或本地 repository 的 Git 数据迁入 Codeup；它不是 create/view/comment/close work item 或日常 MR 管理工具。[Codeup-CLI 安装与迁移范围](https://help.aliyun.com/zh/yunxiao/user-guide/install-the-local-migration-tool)

因此不能因为存在名为 `Codeup-CLI` 的二进制，就把它写进 tracker template 充当 `gh` / `glab` 替代品。

### OpenAPI、Git CLI、MCP 与第三方工具

- **OpenAPI / `curl` / SDK**：是完整且可追溯的底层接口；当前文档给出中心版与 Region 版 URL、PAT header、权限和请求体。`aliyun devops` 是更适合 shell automation 的官方前端。[云效 API reference](https://help.aliyun.com/zh/yunxiao/developer-reference/api-reference-standard-proprietary/)
- **Git CLI**：只管理 Git repository 内容与 refs，不替代 Projex work item 或 Codeup MR API。[Codeup Git 指南](https://help.aliyun.com/zh/yunxiao/user-guide/quick-to-get-started)
- **官方 MCP Server**：官方开源项目可让 AI client 读取 work item、评论并提交 MR，是额外的自动化入口，但不是人类 shell 中与 `gh` / `glab` 同类的 CLI。[云效 MCP 文档](https://help.aliyun.com/zh/yunxiao/developer-reference/cloud-effect-mcp-tool-instructions)；[官方源码仓库](https://github.com/aliyun/alibabacloud-devops-mcp-server)
- **第三方 wrapper**：本调研不把社区工具作为能力证据，也不能称为官方 CLI。

### “没有找到”的检索边界

截至 2026-11-25，检索范围包括：

- 阿里云帮助中心的云效产品文档、当前与旧版 Codeup/Projex API 目录；
- Alibaba Cloud CLI 官方文档及 `aliyun devops` 插件说明；
- `aliyun` GitHub organization 中的 Alibaba Cloud CLI、云效 MCP Server 和官方 command catalog；
- 官方 Git/Codeup-CLI 迁移文档。

在该范围内，**没有找到独立、通用、官方支持且定位类似 `gh` / `glab` 的 Codeup CLI**。这是截至访问日期的“未发现”，不是对所有时间、所有阿里内部或未公开工具作绝对不存在声明。已发现的两个官方命令行路径分别是通用 `aliyun devops` 插件和迁移专用 `Codeup-CLI`。

## 对 `setup-matt-pocock-skills` 的实施建议

### 现在能否支持

**能，但应选择 `Other` / custom tracker，并把名称写成“Yunxiao Projex + Codeup”，而不是“Codeup Issues”。** setup skill 已允许其他 tracker 使用 freeform prose，因此无需先修改 skill 即可记录工作流。[setup skill](../skills/matt/engineering/setup-matt-pocock-skills/SKILL.md)

建议当前接入分两层：

1. `docs/agents/issue-tracker.md` 记录稳定 contract 与 wrapper 命令；
2. wrapper 调用 `aliyun devops`，在底层命令不足或参数不稳定时直接调用同一套官方 OpenAPI。

### 是否新增 template

**暂不新增内置 template。** 先在真实中心版或 Region 版组织验证以下仍不完全由文档消除的不确定性：

- 既有 work item 的 label add/remove 如何通过当前 field config 稳定表达；
- 目标 work item types 是否启用 `PARENT/SUB` 与 dependency 关系；
- 哪个 project-specific status 是 terminal/closed；
- map children 的稳定顺序字段；
- `aliyun devops` 实际发布版本中的对应命令名与参数。

验证后若流程稳定，再新增一份单一 Yunxiao template；不要分别维护“Codeup issue”与“Projex issue”两套模板，因为 ticket/MR 的跨产品边界是同一个 tracker contract。

### 推荐 wrapper contract

建议提供一个很薄的本地命令，例如 `yunxiao-tracker`，只标准化本仓库需要的操作：

```text
yunxiao-tracker issue create|view|list|edit|comment|close
yunxiao-tracker issue label-add|label-remove|assign
yunxiao-tracker relation parent|block|unblock
yunxiao-tracker frontier <map-id>
yunxiao-tracker mr create|view|list|comment|close
```

wrapper 不应复制完整 OpenAPI；它只负责：

- 从配置解析 organization/project/repository/type/status/label/user IDs；
- 对 `view` 聚合 work item、comments 和 relations；
- 对 `close` 强制先 comment 再写 terminal status；
- 对 `frontier` 计算 open + unblocked + unassigned；
- 输出稳定 JSON，错误时非零退出；
- 对中心版/Region 版选择正确 endpoint；
- 在 MR 创建时带 `workItemIds`，并按需建立 external relation。

### Auth 与必要配置

官方 CLI 不使用常规 AK/SK profile；云效数据面使用 PAT。推荐通过环境变量注入，不在命令行或仓库内明文保存：[云效 CLI 指南](https://help.aliyun.com/zh/yunxiao/developer-reference/how-to-install-initialize-and-use-the-apsara-devops-cli)；[PAT 安全说明](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)

```text
ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN
ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID   # 中心版必需
ALIBABA_CLOUD_YUNXIAO_API_BASE_URL      # Region 版必需
```

中心版默认 endpoint 为 `openapi-rdc.aliyuncs.com`；Region 版使用实例访问域名。[服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)

本地非敏感配置还需记录：

```text
organization type: central | region
organization ID or API base URL
Projex project/space ID
work item type ID/category
terminal status ID
map/ticket label IDs
Codeup repository ID or full path
current/default assignee user ID resolution rule
```

PAT 按最小权限授权。只做 ticket 时至少需要项目协作的 work item、comment、label、relation 读写；启用 MR 操作时再加代码管理 MR 读写。官方说明 PAT 同时受申请人资源权限与 token API scope 限制，并建议环境变量、短有效期与定期轮换。[PAT 安全说明](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)

## 尚未由官方文档完全确认的事项

- 当前 API 能创建带 labels 的 work item，但文档没有明确演示对既有 work item 做 label add/remove；需在 field config 上验证。
- work item 没有全局固定的 closed 状态；终态与允许的 transition 取决于 project workflow。
- dependency 是原生模型，但是否允许特定 work item type 之间建立关系取决于组织关系配置。
- 没有发现 first-class frontier endpoint，也没有确认原生 child order 足以表达 template 所需的“first in map order”。
- Codeup MR list 没有文档化的外部贡献者分类，不能直接复刻 GitHub external PR triage query。
- 官方 CLI 文档说明命令覆盖 OpenAPI，但 template 落地前仍应以安装版本的 `aliyun devops --help` 核对 operation 名称和参数；不要在文档中臆造命令。

## Primary sources

以下来源均于 **2026-11-25** 访问：

### 阿里云 / 云效官方文档

- [Codeup：什么是代码管理](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-code-management)
- [Projex：什么是项目协作](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-project-collaboration-1)
- [当前工作项 API 目录](https://help.aliyun.com/zh/yunxiao/developer-reference/work-items/)
- [CreateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitem)
- [GetWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/getworkitem)
- [SearchWorkitems](https://help.aliyun.com/zh/yunxiao/developer-reference/searchworkitems)
- [UpdateWorkitem](https://help.aliyun.com/zh/yunxiao/developer-reference/updateworkitem)
- [CreateWorkitemComment](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitemcomment)
- [ListWorkitemComments](https://help.aliyun.com/zh/yunxiao/developer-reference/listworkitemcomments)
- [CreateLabel](https://help.aliyun.com/zh/yunxiao/developer-reference/createlabel)
- [ListLabels](https://help.aliyun.com/zh/yunxiao/developer-reference/listlabels)
- [CreateWorkitemRelationRecord](https://help.aliyun.com/zh/yunxiao/developer-reference/createworkitemrelationrecord)
- [ListWorkitemRelationRecords](https://help.aliyun.com/zh/yunxiao/developer-reference/listworkitemrelationrecords)
- [工作项关系自定义设置](https://help.aliyun.com/zh/yunxiao/user-guide/work-item-relationship-customization-settings)
- [GetWorkitemWorkflow](https://help.aliyun.com/zh/yunxiao/developer-reference/getworkitemworkflow-get-a-list-of-the-status-of-the-work-item)
- [CreateWorkitemExtRelationRecord](https://help.aliyun.com/zh/yunxiao/developer-reference/new-work-item-associates-external-resources)
- [当前合并请求 API 目录](https://help.aliyun.com/zh/yunxiao/developer-reference/merge-request-1/)
- [CreateChangeRequest](https://help.aliyun.com/zh/yunxiao/developer-reference/createchangerequest-create-merge-request)
- [ListChangeRequests](https://help.aliyun.com/zh/yunxiao/developer-reference/listchangerequests-query-the-list-of-merge-requests)
- [如何安装、初始化配置和使用云效 CLI](https://help.aliyun.com/zh/yunxiao/developer-reference/how-to-install-initialize-and-use-the-apsara-devops-cli)
- [Codeup-CLI：安装迁移工具](https://help.aliyun.com/zh/yunxiao/user-guide/install-the-local-migration-tool)
- [Codeup Git 指南](https://help.aliyun.com/zh/yunxiao/user-guide/quick-to-get-started)
- [服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)
- [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)
- [云效 MCP Server 使用说明](https://help.aliyun.com/zh/yunxiao/developer-reference/cloud-effect-mcp-tool-instructions)
- [Alibaba Cloud CLI 概览](https://help.aliyun.com/zh/cli/what-is-alibaba-cloud-cli)

### 阿里云官方源码仓库

- [`aliyun/alibabacloud-aiops-skills` 云效 command catalog](https://github.com/aliyun/alibabacloud-aiops-skills/blob/master/skills/developertools/rdc/alibabacloud-devops/references/tool-catalog.md)
- [`aliyun/alibabacloud-devops-mcp-server`](https://github.com/aliyun/alibabacloud-devops-mcp-server)
- [`aliyun/aliyun-cli`](https://github.com/aliyun/aliyun-cli)
