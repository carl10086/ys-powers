# 🐛 Find Bugs - TypeScript + Bun 系统化调试技能

## 核心工作流

```
1. 复现问题 ─────┐
   ↓            │
2. 定位根因 ─────┼──→ 用脚本验证假设
   ↓            │    (bun -e / bun run scripts/tmp_*.ts)
3. 伪代码沟通 ───┘
   ↓
4. 修复确认 ←── 用户批准
   ↓
5. 清理临时文件
```

## 约束（必须遵守！）

| 步骤 | 约束 | 原因 |
|------|------|------|
| **分析阶段** | 不准先写修复代码 | 避免过早锚定，误判根因 |
| **沟通阶段** | 用伪代码说明问题和方案 | 降低理解成本，快速对齐 |
| **验证阶段** | 临时脚本命名 `scripts/tmp_*.ts` | 区分验证脚本和永久脚本 |
| **修复后** | 删除所有 `scripts/tmp_*.ts` | 保持项目清洁 |

---

## TypeScript + Bun 调试工具箱

### 1. 快速代码执行 (`bun -e`)

```bash
# 单行验证
bun -e "console.log(JSON.stringify(process.env))"

# 多行验证（用于复杂逻辑）
cat << 'EOF' | bun -e "$(cat)"
const data = { a: 1, b: 2 };
console.log(Object.keys(data));
EOF

# 结合管道
bun -e "console.log('test')" 2>&1 | grep "error"
```

### 2. 类型检查定位 (`bun tsc`)

```bash
# 快速类型检查
bun tsc --noEmit 2>&1 | head -30

# 只看特定文件的错误
bun tsc --noEmit 2>&1 | grep "src/auth.ts"

# 生成详细错误报告
bun tsc --noEmit --pretty 2>&1 | tee /tmp/type_errors.txt
```

### 3. 测试调试 (`bun test`)

```bash
# 运行特定测试
bun test --filter="auth.*expired"

# 详细输出
bun test --reporter=verbose 2>&1

# 带覆盖率
bun test --coverage 2>&1

# 调试单个测试文件
bun test src/auth.test.ts --reporter=verbose
```

### 4. 运行时调试 (`bun --inspect`)

```bash
# 启动调试模式
bun --inspect=0.0.0.0:9229 run src/index.ts

# 带 break on start
bun --inspect-brk run src/index.ts
```

### 5. 包依赖检查

```bash
# 检查重复依赖
bun pm ls --all 2>&1 | grep "duplicate"

# 验证依赖版本
bun pm ls | grep "typescript"
```

---

## 输出格式模板

```markdown
## 🐛 Bug 分析

### 现象
[客观描述看到的问题，引用具体错误信息]
- 错误类型: TypeError / SyntaxError / TestFailure / LogicError
- 错误信息: `具体报错文本`
- 触发位置: `文件:行号`

### 复现步骤
```bash
# 复现命令
bun test --filter="test_name"
# 或
bun run src/problematic.ts
```

### 根因分析（伪代码）
```typescript
// 预期行为
function expected() {
  if (conditionA) {
    return resultX;  // ← 应该返回这个
  }
}

// 实际行为 ← BUG 在这里  
function actual() {
  if (conditionA) {
    return resultY;  // ← 实际返回这个（不一致！）
  }
}
```

### 定位依据
- **文件**: `src/module.ts:42`
- **代码片段**:
  ```typescript
  // 相关代码
  ```

### 验证方案
```bash
# 创建临时验证脚本
# scripts/tmp_verify_bug.ts
```
**脚本内容**:
```typescript
// 最小复现代码
```

**运行**:
```bash
bun run scripts/tmp_verify_bug.ts
```

### 修复建议（伪代码）
```typescript
// 修复思路
function fix() {
  if (修正后的条件) {
    return resultX;  // 和预期一致
  }
}
```

### 待确认
1. [ ] 根因分析是否正确？
2. [ ] 修复方案是否合理？
3. [ ] 是否有其他类似问题？
```

---

## 分析技巧

### 1. 独立复现

**不要**相信用户的描述，**自己跑一遍**:

```bash
# 运行测试
bun test 2>&1

# 运行具体文件
bun run src/index.ts 2>&1

# 检查类型错误
bun tsc --noEmit 2>&1

# 快速验证某个假设
bun -e "console.log(typeof someVariable)"
```

### 2. 二分定位

从错误信息出发，向上追溯:

```
错误位置 → 调用链向上追溯 → 找到数据来源 → 检查数据是否符合预期
```

**示例**:
```bash
# 1. 先看错误堆栈
bun test 2>&1 | grep -A 5 "at "

# 2. 定位到具体函数
# 3. 查看该函数的调用者
# 4. 检查传入的参数
# 5. 找到参数异常的源头
```

### 3. 对比法

找不同：对比正常分支和异常分支

```typescript
// 正常路径
if (user.isActive) {
  // 这里工作正常 ← 对比这个
  processUser(user);
} else {
  // 这里出问题 ← 和上面的差异在哪？
  throw new Error("Inactive user");
}
```

### 4. 假设验证

创建临时脚本验证假设:

```typescript
// scripts/tmp_check_null.ts
import { parseToken } from "./src/auth";

// 验证假设：token 解析会返回 null
const result = parseToken("invalid-token");
console.log("Result:", result);
console.log("Is null:", result === null);
console.log("Type:", typeof result);
```

```bash
bun run scripts/tmp_check_null.ts
```

### 5. 类型驱动调试

利用 TypeScript 类型系统定位问题:

```bash
# 启用严格类型检查
bun tsc --noEmit --strict 2>&1

# 查找隐式 any
bun tsc --noEmit --noImplicitAny 2>&1 | grep "implicitly has an 'any'"

# 检查未使用变量（可能是逻辑错误）
bun tsc --noEmit --noUnusedLocals 2>&1
```

---

## 伪代码规范

**用伪代码而不是真实代码沟通**，因为：

1. **避免语法细节干扰** - 伪代码只关注逻辑
2. **快速表达** - 不必顾虑 TypeScript 类型细节
3. **易于理解** - 用户能立即看懂意图

### 伪代码格式

```typescript
// TypeScript-like 伪代码
function processUser(user: User) {
  if (user.age >= 18) {
    return grantAccess();  // ← 预期
  } else {
    return denyAccess();   // ← BUG: 没有检查用户是否已验证
  }
}

// 或流程图风格
condition: user.age >= 18?
├── true → checkVerification()?
│   ├── true → grantAccess()
│   └── false → denyAccess()  ← BUG: 应该检查这里
└── false → denyAccess()
```

### 伪代码 vs 真实代码

| 场景 | 用伪代码 | 用真实代码 |
|------|:--------:|:----------:|
| 解释 bug 根因 | ✅ | ❌ |
| 沟通修复思路 | ✅ | ❌ |
| 写验证脚本 | ❌ | ✅ |
| 最终修复代码 | ❌ | ✅ |

---

## 临时脚本管理

### 创建

```typescript
// scripts/tmp_reproduce_bug.ts
// scripts/tmp_check_state.ts
// scripts/tmp_verify_fix.ts
```

### 命名规范

- 必须以 `tmp_` 开头
- 描述清楚用途：`tmp_verify_null_handling.ts`
- 一个脚本只做一件事

### 清理

```bash
# 修复完成后删除
rm scripts/tmp_*.ts

# 或保留最近的一个（用于回归测试）
ls -t scripts/tmp_*.ts | tail -n +2 | xargs rm
```

### 禁止

- ❌ 不要把临时脚本提交到代码库
- ❌ 不要在临时脚本里写复杂逻辑
- ❌ 不要保留过期的验证脚本

---

## 修复后检查清单

- [ ] 重新运行验证脚本（应该通过）
- [ ] 运行 `bun test`（相关测试通过）
- [ ] 运行 `bun tsc --noEmit`（无类型错误）
- [ ] 删除 `scripts/tmp_*.ts` 文件
- [ ] 检查没有引入新问题（运行全量测试）

---

## 特殊场景

### 场景 1: 类型错误 (Type Error)

```bash
# 1. 查看完整类型错误
bun tsc --noEmit 2>&1 | head -50

# 2. 找到第一个错误位置
# 3. 分析类型不匹配的根因
# 4. 追溯数据来源的类型定义
```

**常见类型错误模式**:
- `Property 'x' does not exist` → 拼写错误或类型定义缺失
- `Type 'A' is not assignable to type 'B'` → 接口不匹配
- `Cannot find module` → 导入路径错误或模块未安装
- `Implicitly has 'any' type` → 缺少类型注解

### 场景 2: 测试失败 (Test Failure)

```bash
# 1. 运行单个失败的测试
bun test --filter="test_name" --reporter=verbose 2>&1

# 2. 查看 expected vs actual
# 3. 定位到具体 assertion
# 4. 分析为什么结果不一致
```

**调试步骤**:
1. 找到失败的 test 文件和行号
2. 查看 assertion 的 expected 和 actual 值
3. 追溯 actual 值的来源
4. 检查数据转换/处理逻辑

### 场景 3: 运行时错误 (Runtime Error)

```bash
# 1. 查看完整错误堆栈
bun run src/index.ts 2>&1

# 2. 找到 throw 的位置
# 3. 分析异常值
# 4. 追溯该值的来源
```

**常见运行时错误**:
- `Cannot read property 'x' of undefined` → 空值检查缺失
- `undefined is not a function` → 方法不存在或拼写错误
- `Maximum call stack exceeded` → 无限递归

### 场景 4: 逻辑错误（无报错但结果不对）

```bash
# 1. 添加日志输出中间状态
bun -e "
import { processData } from './src/utils';
const result = processData(testData);
console.log('中间状态:', JSON.stringify(result, null, 2));
"

# 2. 对比预期值和实际值
# 3. 定位第一个出现差异的位置
# 4. 修复源头而非症状
```

### 场景 5: 异步问题

```bash
# 1. 检查 Promise 处理
bun -e "
async function debug() {
  try {
    const result = await fetchData();
    console.log('Success:', result);
  } catch (e) {
    console.error('Error:', e);
  }
}
debug();
"

# 2. 使用 --inspect 调试
bun --inspect run src/async-code.ts
```

**常见异步问题**:
- 忘记 await
- Promise 未正确处理 rejection
- 竞态条件
- 超时设置不当

---

## 示例对话

**用户**: "`test_auth_token_expired` 测试失败了"

**助手** (触发 find-bugs 技能):

```markdown
## 🐛 Bug 分析

### 现象
测试 `test_auth_token_expired` assertion failed:
- Expected: `{ error: "TOKEN_EXPIRED" }`
- Actual: `{ success: true }` ← token 过期后没有返回错误

### 复现
```bash
bun test --filter="test_auth_token_expired" --reporter=verbose 2>&1
```

### 根因（伪代码）
```typescript
TokenValidator.validate(token):
  if (token.isExpired()):
    return { error: "TOKEN_EXPIRED" };  ← 预期走这里
  else:
    return { success: true };          ← 实际走这里

问题：isExpired() 返回 false，但 token 确实过期了
```

### 验证方案
```typescript
// scripts/tmp_check_expiry.ts
import { createExpiredToken } from "./test/helpers";
import { TokenValidator } from "./src/auth";

const token = createExpiredToken();
console.log("isExpired:", TokenValidator.isExpired(token));
console.log("current_time:", Date.now());
console.log("token_expires_at:", token.expiresAt);
```

**运行**:
```bash
bun run scripts/tmp_check_expiry.ts
```

### 修复建议（伪代码）
```typescript
// isExpired() 的实现问题：
// 当前：token.expiresAt > Date.now()
// 应该：Date.now() > token.expiresAt  ← 时间比较方向反了
```

### 待确认
1. 修复 `isExpired()` 的比较逻辑
2. 确认其他时间相关比较是否也有同样问题
```

**用户**: "对，就是这个问题"

**助手**: "好，我修复 `isExpired()` 并删除临时脚本"

```typescript
// src/auth.ts:45
function isExpired(token: Token): boolean {
-   return token.expiresAt > Date.now();
+   return Date.now() > token.expiresAt;
}
```

```bash
# 验证修复
bun test --filter="test_auth_token_expired" 2>&1

# 清理
rm scripts/tmp_check_expiry.ts
```

---

## 快速参考卡片

| 任务 | 命令 |
|------|------|
| 快速执行代码 | `bun -e "console.log(123)"` |
| 类型检查 | `bun tsc --noEmit` |
| 运行测试 | `bun test` |
| 运行特定测试 | `bun test --filter="pattern"` |
| 调试模式 | `bun --inspect run file.ts` |
| 包管理 | `bun pm ls` |
| 查看依赖树 | `bun pm ls --all` |

---

## 调试思维检查表

在开始调试前问自己：

- [ ] 我是否独立复现了问题？
- [ ] 我是否定位到了**根因**而不仅是症状？
- [ ] 我是否用伪代码向用户解释了问题？
- [ ] 我是否创建了临时脚本验证假设？
- [ ] 我是否在修复前获得了用户确认？

在修复后检查：

- [ ] 修复是否针对根因而非症状？
- [ ] 是否运行了相关测试验证？
- [ ] 是否删除了所有临时脚本？
- [ ] 是否检查了整个系统的回归？
