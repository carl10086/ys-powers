# Plan: Optimize Install Output

## 依赖关系

```
install/lib/fs.py
├── collect_changes()          [新增，纯函数，无依赖]
│   ├── filecmp.cmp()          [shallow=True，文件级比较]
│   └── filecmp.dircmp()       [目录级比较，惰性递归]
│
install/lib/fs.py
├── install_directory()        [修改，集成 collect_changes]
│   ├── cleanup_stale_files()  [file 策略，时序：先 cleanup]
│   ├── collect_changes()      [时序：cleanup 之后，install 之前]
│   ├── install_folder_level() [folder 策略，逻辑不变]
│   ├── install_file_level()   [file 策略，逻辑不变]
│   └── 输出追加变更列表      [时序：install 成功之后]
│
install/install.py             [无需修改]
```

## 任务切片（垂直切分，每任务一条完整路径）

### 任务 1：实现 `collect_changes()` 函数

- **目标**：在 `install/lib/fs.py` 中新增变更检测函数，支持一级子项的 `A`/`M` 判断。
- **文件**：`install/lib/fs.py`
- **关键实现点**：
  1. 遍历 `source_dir.iterdir()`，跳过安全名单（`.` 开头、含路径分隔符）
  2. 目标不存在 → `A`
  3. 文件 vs 文件：`filecmp.cmp(shallow=True)` 比较
  4. 目录 vs 目录：`filecmp.dircmp()` 比较 `diff_files`/`left_only`/`right_only`/`funny_files`
  5. 类型不匹配 → `M`
  6. `PermissionError`/`OSError` → 保守标记 `M`
- **验收标准**：
  - 目标不存在时，所有子项返回 `A`
  - 文件内容相同（stat 一致）时，不返回
  - 文件内容不同或目录有差异时，返回 `M`
  - 类型不匹配时，返回 `M`
  - 权限异常时，返回 `M` 且不抛异常
- **验证**：直接审查代码逻辑，或写临时脚本对 `skills/` 与 `~/.claude/skills/` 做一次对比测试

### 任务 2：集成变更检测到 `install_directory()` 输出

- **目标**：调整 `install_directory()` 的时序和输出，安装成功后显示一级子项变更。
- **文件**：`install/lib/fs.py`
- **关键实现点**：
  1. **时序调整**：`cleanup_stale_files()` → `collect_changes()` → 安装逻辑 → 输出结果
  2. **输出格式**：在现有成功行（`✓ Xxx 安装成功` + 源目录/目标目录）之后，追加变更列表
     ```
     ✓ Skills 安装成功（文件夹级全量覆盖）
       源目录: /Users/.../ys-powers/skills
       目标目录: /Users/.../.claude/skills
       M html-anything
       A new-skill
     ```
  3. **无变更时**：不追加任何内容，保持现有简洁输出
  4. **失败时**：不输出变更列表（沿用现有失败分支）
- **验收标准**：
  - 安装成功且有变更时，成功行下方出现 `M`/`A` 列表
  - 安装成功但无变更时，输出与修改前完全一致
  - 安装失败时，输出与修改前完全一致
- **验证**：运行 `python3 install/install.py install global` 观察输出

### 任务 3：端到端验证与回归检查

- **目标**：确保输出格式正确，安装逻辑无回归。
- **文件**：无代码修改，纯验证
- **验证步骤**：
  1. 运行 `make global-install`，截图/记录输出，确认：
     - 有变更的目录块下出现 `M`/`A`
     - 无变更的目录块下无额外内容
     - 源目录/目标目录行仍然保留
  2. 连续运行两次 `make global-install`，确认第二次的输出中，未手动修改的项不显示 `M`/`A`（验证 `shallow=True` 和 `copy2` 时间戳复制正常工作）
  3. 检查 `~/.claude/` 下文件内容，确认与修改前完全一致（回归检查）
- **验收标准**：
  - 输出符合 spec 中的示例格式
  - 安装后 `.claude/` 内容无差异（可用 `diff -r` 或备份对比）

## 检查点

| 检查点 | 位置 | 检查内容 |
|--------|------|----------|
| CP1 | 任务 1 完成后 | `collect_changes()` 是否完整处理了类型检查、权限异常、空目标目录？ |
| CP2 | 任务 2 完成后 | 安装脚本是否能跑通？失败分支是否未受影响？ |
| CP3 | 任务 3 完成后 | 输出格式是否正确？连续安装是否不重复标记？安装内容是否无回归？ |

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| `filecmp.dircmp` 对大目录有意外递归 | 检测变慢 | 只访问 `diff_files`/`left_only`/`right_only`/`funny_files`，不访问 `subdirs`，避免深层递归 |
| 目标目录权限不足导致检测中断 | 安装失败 | `try/except (PermissionError, OSError)` 捕获，保守标记 `M` |
| 输出格式与现有解析脚本冲突 | 下游工具报错 | 只追加内容，不删除现有行；缩进用两个空格保持一致 |
