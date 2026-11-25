# gstack 上游参考源确认

> 查询日期：2026-11-25
> 数据来源：GitHub 官方仓库、README、LICENSE 与 GitHub API。

## 结论

用户所称的 “gstack 或 ystack” 指向：

- 官方仓库：[`garrytan/gstack`](https://github.com/garrytan/gstack)
- clone URL：`https://github.com/garrytan/gstack.git`
- 默认分支：`main`
- License：[`MIT`](https://github.com/garrytan/gstack/blob/main/LICENSE)
- GitHub stars：142,603（2026-11-25 查询）
- GitHub forks：21,040（2026-11-25 查询）

仓库地址、clone URL、默认分支、stars、forks 与 License 标识均来自
[GitHub repository API](https://api.github.com/repos/garrytan/gstack)。

## 判断依据

gstack 的
[官方 README](https://github.com/garrytan/gstack/blob/main/README.md)
将项目描述为面向 Claude Code 及其他 coding agents 的虚拟工程团队，提供 CEO、
engineering manager、designer、reviewer、QA、security 和 release 等角色化
skills，覆盖 Think、Plan、Build、Review、Test、Ship 和 Reflect 工作流。

“知名项目”的描述也与 gstack 的公开指标吻合。2026-11-25 的 GitHub API 数据显示其
有 142,603 stars；相比之下，同名或近似的 ystack 候选规模很小：

| 仓库 | Stars | 判断 |
|---|---:|---|
| [`garrytan/gstack`](https://github.com/garrytan/gstack) | 142,603 | **唯一推荐**；名称接近、项目内容吻合，且知名度指标明显成立。 |
| [`Go7hic/ystack`](https://github.com/Go7hic/ystack) | 16 | portable pstack adaptation，不是 Garry Tan 的 gstack。 |
| [`ychampion/ystack`](https://github.com/ychampion/ystack) | 8 | 独立的 mods、skills 与 setup tools 集合。 |
| [`yulonghe97/ystack`](https://github.com/yulonghe97/ystack) | 8 | doc-driven development agent harness。 |

候选数据分别来自：

- [`garrytan/gstack` GitHub API](https://api.github.com/repos/garrytan/gstack)
- [`Go7hic/ystack` GitHub API](https://api.github.com/repos/Go7hic/ystack)
- [`ychampion/ystack` GitHub API](https://api.github.com/repos/ychampion/ystack)
- [`yulonghe97/ystack` GitHub API](https://api.github.com/repos/yulonghe97/ystack)

因此，“ystack”更可能是名称记忆偏差，不能据此选择 stars 只有个位数或十余个的同名
项目。

## 许可证

gstack 使用 MIT License。官方
[`LICENSE`](https://github.com/garrytan/gstack/blob/main/LICENSE)
标明：

```text
MIT License
Copyright (c) 2026 Garry Tan
```

MIT 允许使用、复制、修改、合并、发布和分发，但复制或分发时必须保留原版权声明和许可
声明。

## `refer/gstack/` 用途

官方仓库以完整 upstream checkout 引入：

```bash
git clone https://github.com/garrytan/gstack.git refer/gstack
```

`refer/gstack/` 的定位仅为**只读上游参考快照**，用于：

- 查阅原始 skills、prompts、workflow 和实现结构；
- 记录上游 commit，支持后续差异分析；
- 为本仓库的中文解释和本地适配提供来源依据；
- 核对 LICENSE、文档与上游行为。

不得直接修改 `refer/gstack/`，也不应把它加入本仓库安装逻辑。需要吸收的能力应在本仓库
自有目录中重新设计或适配，并保留来源和许可证说明。
