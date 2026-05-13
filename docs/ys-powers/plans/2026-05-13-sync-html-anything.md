# Plan: 集成 html-anything 到 ys-powers（最小搬运）

## 依赖图

```
┌─────────────────────────────────────────────────────────────┐
│  refer/html-anything/ (上游源，只读)                         │
│  ├── SKILL.md                                               │
│  └── prompts/                                               │
│       ├── sources/                                          │
│       └── styles/                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ 读取
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Task 1: scripts/sync_html_anything.py (同步脚本)            │
│  └── 标准库 only，支持 --dry-run                            │
└──────────────────────┬──────────────────────────────────────┘
                       │ 触发
           ┌───────────┴───────────┐
           ▼                       ▼
┌─────────────────────┐   ┌─────────────────────┐
│  Task 2: Makefile   │   │  Task 3: 首次同步    │
│  └── `make sync-html`│   │  └── skills/html-anything/ │
└─────────────────────┘   └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │  Task 4: 验证        │
                          │  └── 幂等性 + 完整性 │
                          └─────────────────────┘
```

**关键依赖说明：**
- Task 1 是前置任务，所有其他任务都依赖它
- Task 2 和 Task 3 可并行（Task 2 只需脚本存在即可编写 Makefile；Task 3 需要脚本正确运行）
- Task 4 必须在 Task 3 完成后执行

---

## 任务分解（垂直切片）

### Task 1: 编写同步脚本 `scripts/sync_html_anything.py`

**目标**: 实现一个零外部依赖的 Python 脚本，能够将 `refer/html-anything/` 中的 skill 核心资产搬运到 `skills/html-anything/`。

**实现范围**:
- 搬运 `SKILL.md` → `skills/html-anything/SKILL.md`
- 搬运 `prompts/sources/` → `skills/html-anything/prompts/sources/`
- 搬运 `prompts/styles/` → `skills/html-anything/prompts/styles/`
- 明确排除：`src/`、`scripts/`、`package.json`、`tsconfig.json`、`docs/`、`test-results/`、`.git/`、`examples/` 等

**脚本能力**:
- 使用 `pathlib` + `shutil` 处理文件操作
- 支持 `--dry-run` 参数：预览将要复制的文件列表，不实际写入
- 输出同步日志：已复制文件数、跳过文件数、源目录总计
- 幂等执行：多次运行结果一致（覆盖同名文件）

**验收标准**:
1. `python scripts/sync_html_anything.py --dry-run` 能正确列出所有应复制的文件（SKILL.md + prompts/ 下的 .md 和 .json 文件）
2. 脚本不引入任何 pip 依赖
3. 脚本在 macOS 和 Linux 上均可运行（pathlib 保证跨平台）

**验证步骤**:
```bash
# 验证 dry-run 输出
python scripts/sync_html_anything.py --dry-run
# 预期：列出 SKILL.md + prompts/sources/*.md + prompts/styles/*，不创建 skills/html-anything/

# 验证帮助信息
python scripts/sync_html_anything.py --help
# 预期：显示 --dry-run 等参数说明
```

---

### Task 2: 创建 Makefile，封装 `sync-html` target

**目标**: 提供一键命令 `make sync-html`，降低使用门槛。

**实现范围**:
- 新建项目根目录 `Makefile`
- 定义 `.PHONY: sync-html`
- `sync-html` target 调用 `python scripts/sync_html_anything.py`

**验收标准**:
1. `make sync-html` 成功触发同步脚本
2. `make sync-html` 不依赖当前目录（通过 `$(MAKEFILE_LIST)` 或绝对路径保证）
3. Makefile 语法简洁，无冗余

**验证步骤**:
```bash
# 验证 target 存在
make -n sync-html
# 预期：打印将要执行的命令（python scripts/sync_html_anything.py）

# 验证实际执行
make sync-html
# 预期：脚本执行成功，skills/html-anything/ 生成
```

---

### Task 3: 首次运行同步，生成 `skills/html-anything/`

**目标**: 执行脚本，完成首次搬运，产出可用的 skill 目录。

**实现范围**:
- 运行 `python scripts/sync_html_anything.py` 或 `make sync-html`
- 确认 `skills/html-anything/` 目录结构正确

**验收标准**:
1. `skills/html-anything/SKILL.md` 存在且文件大小 > 0
2. `skills/html-anything/prompts/sources/` 存在且包含 ≥1 个 `.md` 文件
3. `skills/html-anything/prompts/styles/` 存在且包含 ≥1 个 `.md` 文件
4. `skills/html-anything/prompts/styles/catalog.json` 存在
5. 无 `src/`、`scripts/`、`package.json` 等非 skill 资产被混入

**验证步骤**:
```bash
# 结构检查
ls -la skills/html-anything/
ls -la skills/html-anything/prompts/sources/ | head -5
ls -la skills/html-anything/prompts/styles/ | head -5

# 文件存在性检查
test -s skills/html-anything/SKILL.md && echo "SKILL.md OK"
test -f skills/html-anything/prompts/styles/catalog.json && echo "catalog.json OK"

# 排除项检查（应无输出）
ls skills/html-anything/src 2>/dev/null || echo "No src/ — correct"
ls skills/html-anything/package.json 2>/dev/null || echo "No package.json — correct"
```

---

### Task 4: 验证幂等性和完整性

**目标**: 确保脚本可重复运行，且产出完整、一致。

**实现范围**:
- 再次运行同步脚本
- 对比两次运行前后的文件差异
- 统计文件数量，与上游源核对

**验收标准**:
1. 第二次运行脚本不报错（幂等）
2. 第二次运行后，没有新增或丢失文件
3. 文件内容未被意外修改（仅覆盖，内容不变）
4. `skills/html-anything/` 中的 `.md` 文件总数与 `refer/html-anything/prompts/` 中的 `.md` 文件总数一致（加上 SKILL.md）

**验证步骤**:
```bash
# 记录首次同步后的文件清单
find skills/html-anything -type f | sort > /tmp/first-run.txt

# 再次运行
make sync-html

# 对比文件清单
find skills/html-anything -type f | sort > /tmp/second-run.txt
diff /tmp/first-run.txt /tmp/second-run.txt
# 预期：无差异

# 统计核对
find skills/html-anything -name "*.md" | wc -l
find refer/html-anything/prompts -name "*.md" | wc -l
# 预期：skills 下的 .md 数 = refer prompts 下的 .md 数 + 1（SKILL.md）
```

---

## 检查点（Checkpoints）

| 检查点 | 位置 | 决策项 |
|--------|------|--------|
| **CP1: 脚本开发完成** | Task 1 后 | dry-run 输出是否正确？文件过滤逻辑是否符合预期？ |
| **CP2: 首次同步完成** | Task 3 后 | `skills/html-anything/` 结构是否完整？有无非 skill 资产混入？ |
| **CP3: 最终验收** | Task 4 后 | 幂等性是否通过？是否可以提交？ |

---

## 风险与回退

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 上游 `refer/html-anything/` 目录结构变更 | 同步脚本失效 | 脚本使用相对路径遍历，结构小幅变更可自适应；大幅变更需人工更新脚本 |
| `skills/html-anything/` 已存在且包含本地修改 | 同步覆盖导致丢失 | 当前脚本直接覆盖；如需保护本地修改，未来可增加 `--backup` 或冲突检测 |
| prompts 文件数量庞大导致同步慢 | 体验下降 | 实测：60+17 个 prompt 文件总计 < 5MB，复制耗时 < 1s，无性能风险 |

---

## 任务执行顺序

```
Task 1 (脚本) → CP1 ─┬→ Task 2 (Makefile) 
                     └→ Task 3 (首次同步) → CP2 → Task 4 (验证) → CP3
```

Task 2 与 Task 3 可并行执行，但建议先完成 Task 3 再提交，以便在 CP2 统一检查产出。
