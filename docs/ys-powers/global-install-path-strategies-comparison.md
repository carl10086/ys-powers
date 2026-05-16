# Global Install 路径处理策略对比分析

**分析日期**: 2026-05-14
**分析目标**: 对比 `refer/` 下参考项目的 global install 路径处理方案，为 ys-powers 选择最合适的策略

---

## 一、参考项目策略总览

| 项目 | 核心策略 | 机制 | 复杂度 |
|------|---------|------|--------|
| **superpowers** | **$0 自定位** | `SCRIPT_DIR="$(dirname "$0")"` → `PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"`，然后读取 `${PLUGIN_ROOT}/skills/...` | 低 |
| **agent-skills** | **环境变量** | Hooks 中使用 `${CLAUDE_PLUGIN_ROOT}`（Claude Code 自动设置）；Skills 之间通过 `skill` 工具按名称调用 | 低 |
| **get-shit-done** | **安装时替换** | 安装脚本将 `~/.claude/`、`./.claude/` 替换为目标运行时路径，安装后还有泄漏检测扫描 | 高 |
| **html-anything**（原项目） | **__dirname 运行时解析** | 源代码用 `import.meta.url` 计算绝对路径；SKILL.md 中使用 `./prompts/styles/...` 相对路径 | 低 |

---

## 二、各策略详细分析

### 1. superpowers — $0 自定位

**实现方式**:
```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
using_superpowers_content=$(cat "${PLUGIN_ROOT}/skills/using-superpowers/SKILL.md")
```

**优点**:
- 完全自包含，不依赖任何外部变量
- 无论安装到 `~/.claude/` 还是 `./.claude/` 还是任意位置，都能正确工作
- 不需要安装时修改文件内容

**缺点**:
- 仅适用于可执行脚本（shell、Node.js、Python）
- 不适用于静态 markdown 文件（skill/agent instructions）
- 如果脚本被 symlink，需要额外处理

**适用场景**:
- Hooks（shell 脚本）
- 辅助脚本（如 brainstorming server）

---

### 2. agent-skills — 环境变量

**实现方式**:

Hooks 中使用 `${CLAUDE_PLUGIN_ROOT}`:
```json
{"command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"}
```

Skills 之间不引用文件路径，而是通过 `skill` 工具按名称调用:
```
skill: spec-driven-development
```

**优点**:
- 完全解耦：skills 之间不依赖文件系统结构
- 由 Claude Code 引擎负责解析 `skill` 名称到实际文件
- 静态 markdown 文件无需关心路径问题

**缺点**:
- 依赖 Claude Code 的运行时环境变量（`${CLAUDE_PLUGIN_ROOT}` 只在 hooks 中保证可用）
- 如果 skill 需要引用其他文件（如 prompts、模板），仍需额外机制
- 需要 Claude Code 支持 `skill` 名称解析机制

**适用场景**:
- Hooks 配置
- Skill 间调用（如果 Claude Code 支持）

---

### 3. get-shit-done — 安装时替换

**实现方式**:

安装脚本在复制文件时进行文本替换:
```javascript
// 伪代码
content = content.replace(/~\/\.claude\//g, targetPath);
content = content.replace(/\$HOME\/\.claude\//g, targetPath);
content = content.replace(/\.\.\/\.claude\//g, localTargetPath);
```

安装后扫描泄漏:
```javascript
scanForLeakedPaths(installedFiles, ["~/.claude", "$HOME/.claude"]);
```

**优点**:
- 最全面：支持多运行时（Claude、Cursor、Copilot 等 14+ 平台）
- 安装后验证，有泄漏检测兜底
- 可以处理任何文本内容中的路径

**缺点**:
- 复杂度最高：需要维护替换规则、扫描逻辑、多平台适配
- 安装时修改文件内容，增加了不确定性
- 如果文件内容包含不应被替换的路径（如文档示例），可能误替换
- 对于我们的项目来说"杀鸡用牛刀"

**适用场景**:
- 跨平台、跨运行时的通用工具
- 商业级产品（get-shit-done 是一个 npm 包）

---

### 4. html-anything — __dirname 运行时解析

**实现方式**:

源代码（TypeScript）:
```typescript
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROMPTS_DIR = path.resolve(__dirname, "..", "prompts");
// 使用时: path.join(PROMPTS_DIR, "styles", "catalog.json")
```

SKILL.md 中的相对路径:
```markdown
Read [`prompts/styles/_design.md`](./prompts/styles/_design.md)
```

**优点**:
- 代码层面完全自包含，运行时计算绝对路径
- SKILL.md 中的相对路径与 skill 文件一起打包，保持目录结构

**缺点**:
- 仅适用于可执行代码（TypeScript/Node.js）
- SKILL.md 中的相对路径依赖 Claude Code 的解析行为（是否从 skill 目录解析？）

**适用场景**:
- 带有可执行组件的 skill（如 html-anything 的 HTML 生成器）
- prompts、模板等附属文件随 skill 一起分发

---

## 三、方案对比矩阵

| 维度 | $0 自定位 | 环境变量 | 安装时替换 | __dirname 运行时解析 |
|------|----------|---------|-----------|-------------------|
| **实现复杂度** | 低 | 低 | 高 | 低 |
| **维护成本** | 低 | 低 | 高 | 低 |
| **跨平台支持** | 中（shell 脚本） | 中（依赖 Claude Code） | 高（14+ 平台） | 高（Node.js/Python） |
| **静态文件支持** | ❌ | ✅（不引用路径） | ✅ | ⚠️（依赖解析行为） |
| **可执行脚本支持** | ✅ | ✅ | ✅ | ✅ |
| **安装时修改文件** | ❌ | ❌ | ✅ | ❌ |
| **运行时依赖** | 无 | `${CLAUDE_PLUGIN_ROOT}` | 无 | 无 |

---

## 四、对 ys-powers 的建议

### 当前状况

ys-powers 包含以下类型的能力：
- **Skills**: 纯 markdown instructions（大部分）+ 少量脚本
- **Agents**: 纯 markdown persona 定义
- **Commands**: 纯 markdown 命令手册
- **Hooks**: shell 脚本 + JSON 配置
- **Rules/References**: 纯 markdown

### 推荐的混合策略

基于参考项目的最佳实践，建议采用**分层策略**：

#### 层 1: Hooks — $0 自定位（已正确实现 ✅）

`hooks/session-start.sh` 已经使用 `$0` + `dirname` 模式，与 `superpowers` 一致。这是最优解。

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")/skills"
```

#### 层 2: 可执行脚本 — $0 自定位或 __dirname

如 `skills/brainstorming/scripts/server.cjs` 已使用 `__dirname`，正确。
`skills/brainstorming/scripts/start-server.sh` 已使用 `cd "$SCRIPT_DIR"`，正确。

#### 层 3: Skill/Agent 间引用 — 需要决策

**问题**: `agents/html-generator.md` 引用 `skills/html-anything/SKILL.md`，`skills/html-anything/SKILL.md` 引用 `./prompts/styles/...`。

**方案 A（推荐）: 假设 Claude Code 从 skill/agent 目录解析**
- 与 `html-anything` 原项目保持一致
- global install 后整个目录结构被复制，相对路径保持有效
- **前提**: 需要验证 Claude Code 确实从文件所在目录解析相对路径

**方案 B: 将引用改为 skill 名称调用**
- 学习 `agent-skills`，不引用文件路径，而是通过 Claude Code 的 skill 机制调用
- 但不确定 Claude Code 的 agent 是否能以这种方式调用 skill

**方案 C: 安装时替换**
- 学习 `get-shit-done`，但只针对最简单的场景（如 `~/.claude/` 替换）
- 复杂度较高，收益有限

#### 层 4: 明确 Bug — 立即修复

`skills/idea-refine/SKILL.md:22` 的 `/mnt/skills/user/...` 是容器残留路径，无论什么策略都应修复。

---

## 五、推荐优先级

| 优先级 | 事项 | 策略 |
|--------|------|------|
| P0 | 修复 `/mnt/skills/user/...` | 改为 `./scripts/idea-refine.sh` 或移除 |
| P1 | 验证 Claude Code 路径解析行为 | 在 global install 后，测试 `/html` 命令是否能加载 `prompts/styles/_design.md` |
| P2 | 如果验证失败，采用安装时简单替换 | 仅替换 `skills/html-anything/` 和 `agents/html-generator.md` 中的关键路径 |
| P3 | 长期：考虑 skill 间调用机制 | 参考 `agent-skills`，避免 agent 直接引用 skill 文件路径 |

---

## 六、修正后的验证方案

原方案："在非 ys-powers 项目中运行 `make global-install`" —— **错误**，因为 `make global-install` 需要在 ys-powers 仓库中执行。

**正确验证步骤**:

```bash
# Step 1: 在 ys-powers 仓库执行 global install
cd ~/soft/projects/ys-powers
make global-install

# Step 2: 确认 prompts 目录已被复制到 ~/.claude/
ls ~/.claude/skills/html-anything/prompts/styles/_design.md
ls ~/.claude/skills/idea-refine/scripts/idea-refine.sh

# Step 3: 切换到任意非 ys-powers 项目
cd /tmp/test-project

# Step 4: 在该项目下启动 Claude Code，尝试：
# - 运行 "/html test" 命令，观察是否能正确加载 prompts
# - 触发 idea-refine skill，观察是否能找到 scripts/idea-refine.sh
```

如果 Step 2 确认文件已复制，但 Step 4 中 Claude Code 报错 "file not found"，则说明 Claude Code 从用户 CWD 解析相对路径，需要修改。
