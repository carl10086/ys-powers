---
name: eli
description: 用图解释代码、文档或架构。仅手动调用：/eli [topic]。
argument-hint: "[topic]"
disable-model-invocation: true
---

# eli

用单个自包含 HTML 解释当前主题，面向完全不了解当前项目、代码或架构的人。使用大图、少量文字和中文伪代码，不使用比喻。

HTML 写入系统临时目录下的 `.eli/` 子目录（macOS/Linux 使用 `$TMPDIR/.eli/`，未设置时使用 `/tmp/.eli/`），回复真实文件路径；不要只写入 `out://` artifact。

架构：面向第一次接触当前项目架构的人，先说明系统解决什么问题，再用系统边界图、模块关系图、调用时序图或数据流图解释真实结构。

代码：面向从未看过当前项目代码的人，用调用流、控制流、状态变化图和中文伪代码解释逻辑与执行顺序。

文档：面向不熟悉当前项目文档的人，用图解释核心概念、逻辑、决策和约束。

Topic: $ARGUMENTS
