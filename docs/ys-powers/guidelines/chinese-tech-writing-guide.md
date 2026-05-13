# 中文技术文档写作规范

> 适用范围：Markdown 格式的技术文档，包括 API 文档、安装指南、快速入门、故障排查等。
> 目标读者：开发者、运维人员、技术决策者。

---

## 1. 核心原则

技术文档的首要目标是**让读者能正确、高效地完成操作**。所有规范都服务于这一目的。

- **可执行**：命令行可直接复制粘贴运行，代码示例可直接编译执行
- **可搜索**：错误消息、日志关键词用代码格式包裹，便于检索
- **精确**：没有模糊的描述，数值、版本、路径都是准确的
- **分层**：不同水平的读者可以快速定位到需要的信息

---

## 2. 排版规范

### 2.1 空格规则

| 场景 | 规范 | 正例 | 反例 |
|:---|:---|:---|:---|
| 中文 + 英文 | **必须加空格** | `使用 Python 调用 API` | `使用Python调用API` |
| 中文 + 数字 | **必须加空格** | `设置超时为 30 秒` | `设置超时为30秒` |
| 数字 + 单位 | **不加空格** | `10GB`、`50%` | `10 GB` |
| 全角标点 + 任何字符 | **不加空格** | `你好，世界。` | `你好 ，世界 。` |
| 英文内部 | 正常空格 | `Hello world` | — |

### 2.2 标点符号

- 中文内容使用**全角标点**：`，。：；「」`
- 英文整句使用**半角标点**：`Hello, world.`
- 省略号用 `……`，不用 `......`
- 破折号用 `——`，占两个汉字位置
- **禁用重复标点**：`！！`、`？？`

### 2.3 句子与段落

- **单句不超过 40 字**，推荐 20 字以内
- 一个段落**只讲一个主题**，中心句放在段首
- 段落长度**不超过 7 行**（手机一屏）
- 段落间用**一个空行**分隔，不缩进

---

## 3. 代码与命令行规范

代码示例是技术文档的核心内容，必须保证精确和可执行。

### 3.1 代码块

**必须指定语言标识**，以便语法高亮：

```python
# 正例
 def greet(name: str) -> str:
     return f"Hello, {name}"
```

    ```
    # 反例：不指定语言
    def greet(name):
        return f"Hello, {name}"
    ```

**代码块前后必须有空行**，与正文分隔：

```markdown
安装完成后，验证版本：

```bash
python --version
```

如果输出 `Python 3.9.0` 或更高版本，说明安装成功。
```

**代码示例必须可运行**。如果片段不可运行，需要明确说明：

```python
# 以下为简化示例，省略了错误处理逻辑
def connect():
    pass
```

### 3.2 命令行

**区分输入和输出**。输入行前加 `$`，输出内容不加：

```bash
$ pip install requests

Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Successfully installed requests-2.31.0
```

**多行命令使用行尾反斜杠**，并在注释中说明每行的作用：

```bash
$ docker run \
    --name myapp \          # 容器名称
    -p 8080:8080 \         # 端口映射
    -v /data:/app/data \   # 数据卷挂载
    myimage:latest
```

**需要用户替换的内容用尖括号 `<>` 包裹**，并在前后说明：

```bash
$ curl -H "Authorization: Bearer <YOUR_API_TOKEN>" \
    https://api.example.com/v1/users
```

> 将 `<YOUR_API_TOKEN>` 替换为你的实际 API Token。

**禁止在命令中使用 `~/` 等依赖 shell 扩展的路径**（不同 shell 行为不一致）：

```bash
# 正例
$ docker run -v "$(pwd)/data:/app/data" myimage

# 反例（某些 shell 不展开 ~）
$ docker run -v ~/data:/app/data myimage
```

### 3.3 配置文件

配置文件示例必须包含**关键注释**，说明每个配置项的用途：

```yaml
# config.yaml
server:
  host: "0.0.0.0"      # 监听地址，0.0.0.0 表示所有接口
  port: 8080           # 服务端口
  timeout: 30          # 请求超时时间，单位秒

database:
  url: "postgresql://user:pass@localhost/db"  # 数据库连接字符串
  pool_size: 10        # 连接池大小，建议设置为 CPU 核心数的 2-4 倍
```

**敏感信息用占位符**：

```yaml
database:
  password: "<DB_PASSWORD>"  # 生产环境建议使用环境变量注入
```

### 3.4 文件路径

- 使用正斜杠 `/`，即使在 Windows 文档中也统一使用（反斜杠需要转义）
- 相对路径以项目根目录为基准
- 路径中的变量用 `<>` 包裹

```markdown
配置文件位于 `config/settings.yaml`。
日志目录为 `<PROJECT_ROOT>/logs/`。
```

---

## 4. API 文档规范

### 4.1 接口说明格式

每个 API 接口必须包含以下要素：

```markdown
### POST /api/v1/users

创建新用户。

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| username | string | 是 | 用户名，长度 3-20 个字符 |
| email | string | 是 | 邮箱地址 |
| role | string | 否 | 用户角色，默认为 `user`，可选值：`user`、`admin` |

#### 请求示例

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "role": "admin"
}
```

#### 响应示例

**成功（201 Created）**

```json
{
  "id": "usr_1234567890",
  "username": "alice",
  "email": "alice@example.com",
  "role": "admin",
  "created_at": "2024-01-15T08:30:00Z"
}
```

**失败（400 Bad Request）**

```json
{
  "error": {
    "code": "INVALID_EMAIL",
    "message": "邮箱格式不正确"
  }
}
```

#### 错误码

| 错误码 | HTTP 状态 | 说明 |
|:---|:---|:---|
| INVALID_EMAIL | 400 | 邮箱格式不正确 |
| USERNAME_EXISTS | 409 | 用户名已存在 |
```

### 4.2 参数说明规范

- **必填参数**标注为「是」，可选标注为「否」并给出默认值
- **枚举值**用代码格式列出所有可选值
- **数值范围**明确给出边界值（如 `长度 3-20 个字符`，而非 `长度适中`）
- **嵌套对象**用缩进表格或子章节说明

### 4.3 版本兼容性

涉及 API 版本变更时，必须明确标注：

```markdown
> **版本变更**
> - v1.2.0 新增 `role` 参数
> - v1.1.0 废弃 `nickname` 字段，将在 v2.0.0 中移除
> - v1.0.0 初始版本
```

---

## 5. 术语与英文处理

### 5.1 专有名词

严格遵循官方大小写，禁止随意改写：

| 正确 | 错误 |
|:---|:---|
| GitHub、JavaScript、iPhone | github、javascript、iphone |
| macOS、iOS、MySQL | MacOS、IOS、Mysql |
| VS Code、Node.js | Vscode、Nodejs |

### 5.2 首次出现标注

技术术语**首次出现**时给出中英文对照，后续直接使用中文或英文（全文统一）：

```markdown
本系统采用 OAuth 2.0（Open Authorization，开放授权）协议进行身份验证。
配置 OAuth 2.0 客户端时，需要提供 client_id 和 client_secret。
```

**禁止在首次出现时使用「以下简称」等冗长表述**：

```markdown
# 反例
本系统采用 Open Authorization（以下简称 OAuth）协议...

# 正例
本系统采用 OAuth（Open Authorization，开放授权）协议...
```

### 5.3 版本号格式

- 遵循 SemVer：`主版本号.次版本号.修订号`（如 `v2.1.3`）
- 版本号前加 `v` 保持统一
- 版本范围用 `>=`、`<` 等数学符号表示

```markdown
支持 Python >= 3.8，< 4.0。
要求 Node.js v18.0.0 或更高版本。
```

---

## 6. 文档类型模板

### 6.1 安装指南

```markdown
# 安装指南

## 环境要求

- OS: Ubuntu 20.04+ / macOS 12+ / Windows 10+
- Python >= 3.9
- Docker >= 20.10（可选）

## 快速安装

### 方式一：pip 安装（推荐）

```bash
$ pip install mypackage
```

### 方式二：源码安装

```bash
$ git clone https://github.com/example/mypackage.git
$ cd mypackage
$ pip install -e ".[dev]"
```

## 验证安装

```bash
$ mypackage --version
mypackage 1.2.3
```

## 常见问题

### 安装时报错 `No module named 'setuptools'`

升级 setuptools：

```bash
$ pip install --upgrade setuptools
```
```

### 6.2 快速入门

```markdown
# 快速入门

## 目标

完成本教程后，你将能够：
- 发起第一个 API 请求
- 解析响应结果
- 处理常见错误

## 前提条件

- 已安装 SDK（参见[安装指南](install.md)）
- 已获取 API Key

## 步骤 1：配置客户端

```python
from mysdk import Client

client = Client(api_key="<YOUR_API_KEY>")
```

## 步骤 2：发起请求

```python
user = client.users.create(username="alice")
print(user.id)
```

## 下一步

- 阅读 [API 完整文档](api.md)
- 了解 [错误处理](error-handling.md)
```

### 6.3 故障排查

```markdown
# 故障排查

## 连接超时

### 现象

```
ConnectionError: HTTPConnectionPool timeout
```

### 原因

网络不可达或目标服务未启动。

### 解决方案

1. 检查网络连通性：
   ```bash
   $ curl -I https://api.example.com/health
   ```

2. 确认服务状态：
   ```bash
   $ docker ps | grep myservice
   ```

3. 调整超时配置：
   ```python
   client = Client(timeout=60)  # 默认 30 秒
   ```

## 认证失败

### 现象

```
HTTP 401: Unauthorized
```

### 原因

API Key 无效或已过期。

### 解决方案

1. 检查 API Key 是否正确设置
2. 在控制台确认 Key 未过期
3. 重新生成 Key 并更新配置
```

---

## 7. 错误消息与日志引用

引用错误消息或日志时，必须**完整保留原文**，便于读者搜索：

```markdown
如果看到以下错误：

```
ERROR: Could not find a version that satisfies the requirement numpy==99.0
```

说明指定的版本不存在，请检查版本号是否正确。
```

**禁止只描述大意而不给出原文**：

```markdown
# 反例
如果看到 numpy 版本不存在的错误...

# 正例
如果看到 `ERROR: Could not find a version...` 错误...
```

---

## 8. 链接与图片

### 8.1 内部链接

- 使用相对路径，确保在任意环境下可用
- 链接文本描述目标内容，不用「点击这里」

```markdown
# 正例
参见 [安装指南](./install.md)。

# 反例
点击[这里](./install.md)查看安装方法。
```

### 8.2 外部链接

- 技术参考优先链接到官方文档
- 链接后标注访问日期（官方文档除外）

```markdown
关于 OAuth 2.0 的详细说明，参见 [RFC 6749](https://tools.ietf.org/html/rfc6749)。
```

### 8.3 图片

- 所有图片必须提供有意义的 alt 文本
- 截图包含关键标注（红框、箭头）
- 使用相对路径存放于 `assets/` 目录

```markdown
![架构图：服务调用链路示意](../assets/architecture.png)
```

---

## 9. 审校清单

发布前逐项检查：

### 格式
- [ ] 标题层级连续，一篇文档只有一个 H1
- [ ] 中英文之间有空格，全角标点与其他字符间无空格
- [ ] 代码块指定了语言标识
- [ ] 命令行前 `$` 和输出内容区分正确
- [ ] 用户需要替换的内容用 `<>` 包裹并说明

### 内容
- [ ] 所有代码示例经过实际运行验证
- [ ] 命令行可直接复制粘贴执行（无行号、无多余 `$`）
- [ ] 专有名词大小写正确（GitHub、JavaScript、macOS）
- [ ] 技术术语首次出现有中英文对照
- [ ] 版本号格式统一（`v1.2.3`）
- [ ] 错误消息引用完整原文，非大意描述
- [ ] 数值和范围精确（如 `超时 30 秒`，而非 `超时时间适中`）

### 链接
- [ ] 内部链接使用相对路径，且目标文件存在
- [ ] 外部链接可访问
- [ ] 图片有 alt 文本且路径正确

---

## 参考来源

- [中文技术文档的写作规范 - 阮一峰](https://www.ruanyifeng.com/blog/2016/10/document_style_guide.html)
- [中文文案排版指北 - sparanoid](https://github.com/sparanoid/chinese-copywriting-guidelines)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
