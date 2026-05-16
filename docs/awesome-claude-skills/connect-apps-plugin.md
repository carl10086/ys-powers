# connect-apps-plugin

## 定位

`connect-apps` 的物理插件载体，通过 `claude --plugin-dir` 安装到 Claude Code 中，为 Claude 提供 500+ 应用的自动化执行能力。

## 触发时机

- 需要通过 `claude --plugin-dir` 方式安装 Composio 插件时
- 已安装并运行 `/connect-apps:setup` 进行初始化配置时
- **不适用**：使用 Python/TypeScript SDK 直接集成的场景（此时用 `connect`）

## 核心能力

1. **插件化部署**：将 Composio 能力打包为 Claude Code 可识别的插件格式
2. **自动认证管理**：内置 OAuth 流程处理，用户只需粘贴 API Key
3. **500+ 应用覆盖**：安装后 Claude 可发送邮件、创建 Issue、发布消息、更新文档等

## 安装流程

```bash
# 1. 安装插件
claude --plugin-dir ./connect-apps-plugin

# 2. 在 Claude Code 中运行配置
/connect-apps:setup

# 3. 粘贴从 platform.composio.dev 获取的免费 API Key

# 4. 重启 Claude Code
```

## 与 ys-powers 的关联

- **与 connect-apps 的关系**：`connect-apps-plugin` 是「插件代码目录」，`connect-apps` 是「面向用户的使用说明」。两者配套使用
- **借鉴价值**：其插件结构（commands 目录 + README.md）可作为 ys-powers 开发 Claude Code 插件时的参考模板
- **搬运建议**：价值较低。这是 Composio 的专有插件实现，ys-powers 若需类似能力可直接使用 Composio SDK，无需搬运插件代码

## 元信息

- 来源：`refer/awesome-claude-skills/connect-apps-plugin/README.md`
- 维护者：Composio
- 许可证：Apache 2.0
