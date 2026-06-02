---
name: org-bookmarks
description: Use when the user asks to organize, clean up, or restructure Chrome bookmarks, mentions duplicate bookmarks, mixed-up categories, or too many bookmarks without clear classification. Reorganizes by reading the Chrome Bookmarks JSON, reporting the current state and sync risk, clarifying the target structure through multi-turn dialogue, and generating a Netscape Bookmark HTML import file on the Desktop. Avoids editing the Bookmarks JSON directly because Chrome sync overwrites local changes.
---

# Organizing Chrome Bookmarks

## Core principle

**Read the JSON to understand. Never write the JSON to fix.** Generate an HTML import file and let the user do the actual import. This bypasses Chrome's sync and memory-state overwrite behavior, which silently destroys direct Bookmarks JSON edits.

## When to use

- 用户说"整理书签"、"书签分类乱了"、"书签太多"、"重复书签"
- 用户描述 Chrome 书签的某个具体问题(错位、重复、命名)
- 用户登录了 Google 账号(Chrome 同步会覆盖本地 Bookmarks JSON,这点**必须**先报告)

## When NOT to use

- 其他浏览器(Edge/Safari/Firefox)— 路径和同步行为不同
- Chrome 密码、历史、扩展、cookie
- 跨设备同步策略本身(关/开同步)
- 用户的 Bookmarks 文件不存在(可能是新装 Chrome)— 建议先积累一些书签再整理

## Hard rule (违反就重做)

**不要直接修改 `Bookmarks` JSON 来落地方案。** Chrome 启动时会用内存中的书签状态覆盖文件,登录 Google 账号时还会从云端拉数据覆盖本地。任何对 JSON 的写操作,只要 Chrome 还活着,都是无效的。

**唯一可靠的落地方式:** 生成 Netscape Bookmark HTML 文件,用户从 Chrome 的 `chrome://bookmarks` 手动导入。

## Workflow (5 步,严格顺序)

### Step 1: 探测(报告给用户看)

```bash
# Chrome 是否在跑
pgrep -f "Google Chrome.app"
# → 若在,警告用户 Cmd+Q 退出,**不**自动 kill

# Bookmarks 路径(默认)
~/Library/Application Support/Google/Chrome/Default/Bookmarks
# → 若不存在,扫描 ~/Library/Application Support/Google/Chrome/ 找其他 profile

# 同步状态(读 Preferences 找账号)
python3 -c "
import json
p = '$HOME/Library/Application Support/Google/Chrome/Default/Preferences'
with open(p) as f: d = json.load(f)
ai = d.get('account_info', [])
sp = d.get('signin', {}).get('sync_paused_start_time')
print('账号:', [a.get('email') for a in ai] if ai else '无')
print('同步暂停:', bool(sp))
"
```

**这一步必须报告**:
- Chrome 进程是否在跑(若是,**不能**改文件)
- 同步状态(账号 + 是否暂停)
- Bookmarks 文件大小

### Step 2: 报告现状(必做,不跳)

用脚本枚举所有 URL + 文件夹,生成报告:

```python
import json
from urllib.parse import urlparse
from collections import defaultdict, Counter

with open(".../Bookmarks") as f: data = json.load(f)

def walk(node, path):
    if node.get("type") == "url":
        yield node["name"], node["url"], path
    for c in node.get("children", []):
        yield from walk(c, path + " / " + c.get("name","?"))

all_items = []
for rk in ("bookmark_bar","other","synced"):
    root = data["roots"].get(rk)
    if root:
        for n in walk(root, root.get("name",rk)):
            all_items.append(n)

# 重复 URL(规范化:host + path,忽略 query)
def norm(u): 
    p = urlparse(u); return f"{p.netloc.lower().replace('www.','')}{p.path.rstrip('/')}"

dup = Counter(norm(u) for _, u, _ in all_items)
dups = [k for k, c in dup.items() if c > 1]
```

**报告必须包含**:
1. 唯一 URL 数 / 重复 URL 数(列具体)
2. 顶级文件夹列表 + 每个 URL 数
3. **错位检测**:games 里有视频站?tools 里有学习资料?(关键词扫描)
4. **空文件夹**(可能是 dead state)
5. **同步警告**(若检测到 Google 账号,放在报告最前面)

**报告格式**:
```
【同步状态】
⚠️ 检测到 Google 账号 (xxx@gmail.com),同步暂停中
   即使文件改了,Chrome 启动时可能从云端覆盖
   → 方案:不直接改 Bookmarks JSON,改用 HTML 导入

【概况】
- 唯一 URL: 88
- 重复 URL: 1(列具体)
- 空文件夹: 1(移动设备书签)

【当前结构】
📁 书签栏
  📁 github (7)
  📁 tools (41) ← 偏多
  📁 books (7)
  📁 ai (3)
  📁 games (23)
📁 其他书签 (7)
📁 移动设备书签 (空)

【错位】
- games 里混了视频站:低端影视、7xi 影院(2 项)
```

**报告完,等用户看完再继续。**

### Step 3: 多轮澄清(纪律:不替用户决定)

**最少 3 轮,必问内容**:

| 轮 | 问题 | 选项 |
|----|------|------|
| 1 | 目标形态 | 按使用场景 / 按主题 / 按访问频率 / 混合(场景+主题) |
| 2 | 颗粒度(顶级数 + 上限) | 3 类 / 4 类 / 5+ 类 |
| 3 | 删除项(列出 16+ 待删,让用户挑) | 文字列表 + 自由回答 |

**可加轮次**(用户主动展开时):
- 命名(emoji 标题?中文/英文?)
- 娱乐是否独立顶级
- 工具下子分类怎么切

**绝对禁止**:
- ❌ 替用户决定哪个 URL 留哪个删
- ❌ "我猜你想要" → 然后默默替用户分类
- ❌ 跳过 Step 2(报告)直接出方案
- ❌ 跳过 Step 3(澄清)直接写 HTML

### Step 4: 写 HTML(不要改 Bookmarks JSON)

**输出路径**:`~/Desktop/chrome-bookmarks-import-YYYYMMDD.html`

**Netscape Bookmark File Format v1**:

```html
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
  <DT><H3>顶级文件夹名</H3>
  <DL><p>
    <DT><A HREF="https://...">URL 名称</A>
    <DT><H3>子文件夹名</H3>
    <DL><p>
      <DT><A HREF="https://...">子项</A>
    </DL><p>
  </DL><p>
</DL><p>
```

**字符转义**(必做):
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`

**生成后自查**:
```bash
# 文件存在
ls -la ~/Desktop/chrome-bookmarks-import-*.html
# URL 数对得上
grep -c '<DT><A' ~/Desktop/chrome-bookmarks-import-*.html
# DOCTYPE 正确
head -1 ~/Desktop/chrome-bookmarks-import-*.html
```

### Step 5: 给用户操作步骤

```
✅ HTML 导入文件已生成

【文件位置】
~/Desktop/chrome-bookmarks-import-YYYYMMDD.html
XX URL,YY 文件夹

【操作步骤】
1. 退出 Chrome(Cmd+Q)
2. 打开 Chrome → 地址栏 chrome://bookmarks
3. 右上角"整理" → "从 HTML 文件导入书签"
4. 选桌面文件

【记得先清空】
在 chrome://bookmarks 里 Cmd+A 全选 + Delete,再导入。
否则会和旧书签混一起。

【为什么用 HTML 导入】
直接改 Bookmarks JSON 会被 Chrome 同步从云端覆盖,
HTML 导入是 Chrome 原生支持,绕开这个坑。
```

## Common mistakes

| 错误 | 后果 | 修正 |
|------|------|------|
| 直接改 `Bookmarks` JSON 落地方案 | Chrome 启动时覆盖,白做 | 用 HTML 导入 |
| 跳过 Step 2 报告 | 用户看不到现状,失去信任 | 必做报告 |
| 替用户决定"工作/学习/娱乐"分类 | 用户觉得越界,反复改 | 必问 AskUserQuestion |
| 在 Chrome 跑着时改文件 | 改完立刻被覆盖 | 警告用户 Cmd+Q |
| 用 `osascript` 或 pkill 强制关 Chrome | 可能误杀 mcp/其他进程 | 只警告,不自动关 |
| 用 DevTools Protocol / chrome-devtools-mcp 改书签 | 改的是 isolated profile,不影响主 profile | 不推荐 |
| 假设 macOS Chrome 远程调试端口可用 | macOS 沙箱限制,无法 HTTP 暴露 | 不用 port 方式 |
| 用 mcp 的 chrome.bookmarks API | mcp 在 isolated profile,操作不到主 profile | 不推荐 |
| 输出文件不在桌面 | 用户找不到 | 强制 `~/Desktop/` |
| 路径含中文/空格 | 写入失败 | 用 quote 转义 |

## Verification checklist(完成后自查)

- [ ] HTML 文件存在,文件大小合理
- [ ] URL 总数 = 用户确认的保留数(`grep -c '<DT><A'`)
- [ ] 顶级文件夹数 = 方案指定数
- [ ] 字符转义正确(中英文都能显示)
- [ ] DOCTYPE 是 `<!DOCTYPE NETSCAPE-Bookmark-file-1>`
- [ ] 报告给用户的步骤清晰(退出 → 导入 → 清空)

## Red flags(出现立即停下)

- "我直接改 Bookmarks JSON 吧,这样最快" → **停下来**,Chrome 同步会覆盖
- "我猜你想这样分" → **问用户**,别替决定
- "用户没说要删,我先替它删一些" → **列出待删,让用户挑**
- "Chrome 还在跑,但改个文件没事吧" → **警告用户退出**
- "我用 mcp 的 chrome.bookmarks API 改" → **无效**,mcp 是 isolated profile
- "我先改一个试试" → **别试**,先做完整报告

## Notes

- 用户的 Chrome 同步可能暂停(我已验证),但**不能**依赖此状态 — 仍按"会被覆盖"对待
- 跨用户时(其他人的 Chrome),路径都是 `~/Library/Application Support/Google/Chrome/Default/Bookmarks`,除非他们用 Brave/Edge(类似但路径不同)
- 用户导入 HTML 后,文件可以删除(已经持久化到 Chrome)
- 若用户想"先备份再尝试改 JSON",可以:`cp Bookmarks Bookmarks.bak.$(date +%Y%m%d)`,但要明确告知"改 JSON 大概率被覆盖"

## Edge cases(漏了会出问题的)

### 多 profile Chrome
如果 `Default/Bookmarks` 不存在,**先**扫描 `~/Library/Application Support/Google/Chrome/` 找所有 profile:
```bash
find ~/Library/Application\ Support/Google/Chrome/ -name "Bookmarks" -maxdepth 2
```
**不要自动选** — 列出路径让用户确认是哪个 profile。

### 文件名冲突
若 `~/Desktop/chrome-bookmarks-import-YYYYMMDD.html` 已存在(用户跑过多次),加后缀 `-2`、`-3` 等:
```python
out = f"~/Desktop/chrome-bookmarks-import-{date}.html"
if exists(out):
    i = 2
    while exists(out.replace('.html', f'-{i}.html')):
        i += 1
    out = out.replace('.html', f'-{i}.html')
```

### 大文件(1000+ URL)
读 + 报告可能慢,提示用户:
> "你的 Bookmarks 有 1500 个 URL,完整分析需要约 30 秒,稍等。"

如果用户在澄清 3 轮中途说"算了,先这样",**保存当前决定**(方案 + 已删项),不要强推完成。

### 字符没转义的隐蔽 bug
中文 URL 名 + `&` 或 `<`(少见但有)会导致导入失败。生成 HTML 后必须 `grep -c '&amp;\|&lt;\|&gt;'` 确认有转义。

