# gstack 概览

> 来源：[garrytan/gstack](https://github.com/garrytan/gstack)（MIT 许可）
> 维护者：Garry Tan（Y Combinator 总裁兼 CEO）

---

## 项目定位

gstack 是一套将 Claude Code（及 9+ 其他 AI 编码智能体）转化为**虚拟工程团队**的开源技能框架。它把单个开发者的工作流扩展为包含 23+ 名"专家"的完整软件工厂，覆盖从需求思考到发布部署的全生命周期。

Garry Tan 在 2026 年前 4 个月的生产力（以逻辑代码变更衡量）是他 2013 年水平的 **240 倍**，核心差异不是个人能力，而是工具链。

---

## 核心哲学

| 原则 | 含义 |
|------|------|
| **Process over prompts** | gstack 是一个冲刺流程，不是提示词集合。技能之间环环相扣：`/office-hours` 产出设计文档 → `/plan-ceo-review` 审视 → `/plan-eng-review` 锁定架构 → `/qa` 执行测试。 |
| **Boil the Lake** | 在 AI 时代，完整性比捷径更便宜。每个技能都追求端到端的彻底实现，而非最小可行演示。 |
| **Real browser as first-class** | 浏览器不是事后补丁，而是整个体系的硬核心。持久化 Chromium 守护进程、亚秒级延迟、真实 Cookie 导入、反 bot  stealth。 |
| **Measurable claims** | 所有生产力声明都有方法论、复现脚本和可审计数据（见 `ON_THE_LOC_CONTROVERSY.md`）。 |
| **Safety by design** | 分层防御：ML 分类器 + canary token + 双监听器隧道 + 集成阻断规则。 |

---

## 架构概览

```
gstack
├── skills/                    # 50+ 个 slash-command 技能
│   ├── 规划类：office-hours, plan-ceo-review, autoplan...
│   ├── 实现类：review, investigate, design-shotgun...
│   ├── 发布类：ship, land-and-deploy, canary...
│   ├── 运营类：learn, retro, health, context-save...
│   └── 安全类：cso, careful, freeze, guard...
├── browse/                    #  headless Chromium 守护进程
│   ├── src/server.ts          # Bun HTTP 服务 (~142KB)
│   ├── src/browser-manager.ts # 浏览器生命周期管理 (~65KB)
│   └── src/security.ts        # 内容安全与反注入
├── extension/                 # Chrome 侧边栏扩展
│   ├── sidepanel.js           # 主面板 (44KB)
│   ├── background.js          # 后台服务 (21KB)
│   ├── content.js             # 页面注入 (12KB)
│   └── inspector.js           # CSS 审查器 (16KB)
├── bin/                       # 60+ 个 CLI 工具
│   ├── gstack-update-check    # 自动更新（每小时静默检查）
│   ├── gstack-ios-qa-daemon   # iOS 真机 QA 守护进程
│   └── gstack-brain-sync      # 跨机器记忆同步
├── hosts/                     # 多智能体适配层
│   ├── claude.ts, codex.ts, cursor.ts
│   ├── openclaw.ts, slate.ts, kiro.ts...
│   └── 新增适配：一个 TS 配置文件 + 重新导出
└── docs/designs/              # 18 份设计文档（架构决策记录）
```

---

## 生命周期流程

gstack 把一次交付定义为六阶段循环：

```
Think（思考）      → /office-hours, /plan-ceo-review
Plan（计划）       → /autoplan, /plan-eng-review, /plan-design-review
Build（构建）      → （Claude Code 常规编码）
Review（审查）     → /review, /codex, /design-review, /cso
Test（测试）       → /qa, /qa-only, /benchmark, /ios-qa
Ship（发布）       → /ship, /land-and-deploy, /canary
Reflect（复盘）    → /retro, /learn, /document-release
```

每个阶段都有对应的技能和质量门（quality gate），未通过则阻断到下一阶段。

---

## 与 ys-powers 的对比视角

| 维度 | gstack | ys-powers |
|------|--------|-----------|
| **生命周期覆盖** | 完整六阶段闭环（Think→Reflect） | 聚焦 Build/Test/Review/Ship，Planning 较薄 |
| **浏览器集成** | 自研 headless daemon + 真实 Chromium + iOS 真机 | 依赖 DevTools MCP（外部工具） |
| **设计工作流** | `/design-shotgun` → `/design-html` 完整管线 | 无 |
| **多智能体** | 10 个智能体自动适配 | 仅 Claude Code |
| **安全审计** | `/cso` 内置 OWASP + STRIDE + ML 注入检测 | `security-and-hardening` skill（通用） |
| **记忆系统** | `/learn`, gbrain 跨机器同步 | 无 |
| **iOS 支持** | USB 真机驱动 + Tailscale 远程 | 无 |
| **技能数量** | 50+ | 25 skills + 20 commands |
| **产出质量** | 追求可投产（shippable） | 追求工程正确性 |

**关键洞察**：gstack 的强项在**流程 orchestration** 和**真实环境交互**（浏览器、iOS）；ys-powers 的强项在**工程规范**（编码规范、SOP、安装脚本）和**轻量可组合性**。两者互补而非替代。

---

## 参考索引

- 完整技能清单 → [`skills-inventory.md`](skills-inventory.md)
- 可借鉴/集成分析 → [`integration-analysis.md`](integration-analysis.md)
- 原始项目：`refer/gstack/`（**只读**，如需修改请在 ys-powers 自有目录重写）
