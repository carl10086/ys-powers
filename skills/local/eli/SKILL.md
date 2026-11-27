---
name: eli
description: Explain code, documentation, or architecture completely with multiple diagrams grounded in real structures. Do not use metaphors. Manual invocation only: /eli [topic].
argument-hint: "[topic]"
disable-model-invocation: true
---

# eli

用单个自包含 HTML 完整解释 `$ARGUMENTS` 指定的主题。

HTML 写入系统临时目录下的 `.eli/` 子目录（macOS/Linux 使用 `$TMPDIR/.eli/`，未设置时使用 `/tmp/.eli/`），回复真实文件路径；不要只写入 `out://` artifact。

不要使用比喻。使用多张图解释真实内容；根据主题自行判断图的数量和类型，不套固定模板，不用重复的图表达同一内容。

不要阉割内容。在用户指定的主题范围内，覆盖所有影响理解的结构、执行路径、条件、约束、错误处理和副作用。“完整”不等于扩展到无关内容，也不等于逐行复述代码。

解释架构时，检查真实系统结构，选择能完整呈现系统边界、模块关系、数据流、调用时序、运行结构或部署结构的图。解释代码时，检查真实实现，选择能完整呈现入口、调用链、控制流、状态变化、数据转换、错误路径和副作用的图。只呈现与指定主题实际相关的内容。

Topic: $ARGUMENTS
