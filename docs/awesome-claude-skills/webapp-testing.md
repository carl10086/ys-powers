# webapp-testing

## 定位

使用 Python Playwright 测试本地 Web 应用，支持验证前端功能、调试 UI 行为、捕获浏览器截图和查看控制台日志。

## 触发时机

- 需要自动化测试本地运行的 Web 应用时
- 需要捕获页面截图用于 UI 审查或回归测试时
- 需要检查浏览器控制台错误或网络请求时
- 需要与动态页面交互并验证行为时
- **不适用**：纯静态 HTML 页面（可直接读取文件分析）

## 核心能力

1. **服务器生命周期管理**：`scripts/with_server.py` 自动启动/停止后端和前端服务器
2. **动态页面侦查**：先导航并等待 `networkidle`，再截图或检查 DOM，最后基于渲染状态识别选择器
3. **Playwright 脚本**：原生 Python Playwright 自动化
4. **截图与日志**：捕获全页截图和控制台日志

## 决策树

```
用户任务
  ├── 静态 HTML?
  │     ├── 是 → 直接读取文件识别选择器 → 编写 Playwright 脚本
  │     └── 否（动态应用）
  │           ├── 服务器已运行?
  │           │     ├── 否 → 使用 with_server.py 启动 + 编写脚本
  │           │     └── 是 → 侦查-行动模式
  │           │                 1. 导航并等待 networkidle
  │           │                 2. 截图或检查 DOM
  │           │                 3. 从渲染状态识别选择器
  │           │                 4. 使用发现的选择器执行操作
```

## 关键要点

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| 动态应用 | 先 `wait_for_load_state('networkidle')` 再检查 DOM | 未等待直接检查选择器 |
| 脚本使用 | 先 `--help` 查看用法，作为黑盒直接调用 | 直接阅读大脚本源码 |
| 多服务器 | 使用 `with_server.py` 同时管理多个服务 | 手动分别启动 |

## 多服务器示例

```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

## 与 ys-powers 的关联

- **与 artifacts-builder 的关系**：`artifacts-builder` 构建前端 artifact，`webapp-testing` 测试 Web 应用。两者互补
- **借鉴价值**：其「侦查-行动（Reconnaissance-Then-Action）」模式是处理动态 Web 内容的通用最佳实践；其「服务器生命周期管理」封装解决了本地测试的常见痛点
- **搬运建议**：高价值。前端测试是开发工作流中的刚需，且 Playwright 是当前主流的浏览器自动化方案。`with_server.py` 的黑盒化设计尤其值得借鉴

## 元信息

- 来源：`refer/awesome-claude-skills/webapp-testing/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
