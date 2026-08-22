# Matt Pocock Engineering Skills 中文版

一套面向 coding agent 的研发流程 skills（拷问式规划、spec/工单拆分、TDD、代码评审、分诊等）的**中文翻译版本**。

> **本项目演化自 [mattpocock/skills](https://github.com/mattpocock/skills)**，由 Matt Pocock 创作（MIT 许可证）。
> 在原仓库 `skills/engineering/` 全部 18 个 skill 及其依赖 `skills/productivity/grilling` 的基础上翻译为中文，
> 并新增统一初始化入口 `install-skills`。翻译内容与原文如有出入，以[原仓库](https://github.com/mattpocock/skills)为准。

## Skills 一览（19 + 1）

### 用户调用（user-invoked）

| Skill | 说明 |
|---|---|
| `ask-matt` | 路由器：不知道该用哪个 skill 时问它 |
| `grill-with-docs` | 拷问式打磨方案，同时沉淀领域文档（ADR + 术语表） |
| `triage` | 按 分诊（triage）角色状态机流转 issue 和外部 PR |
| `improve-codebase-architecture` | 扫描代码库寻找「深化」机会，生成可视化 HTML 报告，逐项拷问 |
| `setup-matt-pocock-skills` | 仓库级一次性配置：工单系统（issue tracker）、分诊标签、领域文档布局 |
| `to-spec` | 把当前对话沉淀成 spec（规格说明）并发布到工单系统 |
| `to-tickets` | 把计划/spec 拆成带阻塞关系的 曳光弹（tracer-bullet）工单 |
| `implement` | 按 spec/工单实现：在预定 接缝（seam）处驱动 TDD，提交前跑 code-review |
| `wayfinder` | 把超大块工作规划成工单系统上的 共享地图（决策工单逐个击破） |

### 模型调用（model-invoked）

| Skill | 说明 |
|---|---|
| `prototype` | 造一个一次性原型回答设计问题（逻辑原型 / UI 变体） |
| `diagnosing-bugs` | 疑难 bug 与性能回归的 诊断循环（diagnosis loop） |
| `research` | 对高可信源做调研并沉淀为带引用的 Markdown |
| `tdd` | 测试驱动开发：红-绿-重构循环 |
| `domain-modeling` | 主动构建和打磨领域模型（CONTEXT.md / ADR） |
| `codebase-design` | 深模块（deep module）设计词汇与原则 |
| `code-review` | 双轴代码评审：Standards（规范）+ Spec（忠实实现） |
| `resolving-merge-conflicts` | 按意图逐 差异块（hunk）解决合并/变基冲突 |
| `wizard` | 生成引导人类执行手工步骤的 bash 向导 |
| `grilling` | 拷问核心：逐轮追问直到达成共识（多个 skill 的依赖） |

### 本仓库新增

| Skill | 说明 |
|---|---|
| `install-skills` | **统一初始化入口**：把本仓库全部 skills 安装/升级到当前 agent 的用户级 skill 目录 |

## 安装

方式一（推荐）：让 agent 克隆本仓库后调用 `install-skills` skill，它会探测当前 agent 的用户级
skill 目录并完成安装与验证：

```bash
git clone --depth 1 https://github.com/asherzj/matt-pocock-skills-zh.git
```

方式二（手动）：把 `skills/engineering/` 下各目录、`skills/productivity/grilling/`、
`skills/install-skills/` 复制到你所用 agent 的用户级 skill 目录（如 Claude Code 为
`~/.claude/skills`），新开会话后生效。

> 提示：`wayfinder` / `triage` / `to-spec` / `to-tickets` 依赖仓库级配置，
> 在具体项目里首次使用前先运行一次 `setup-matt-pocock-skills`。

## 翻译约定

- `name`、skill 名、命令、文件名（SKILL.md、CONTEXT.md、ADR 等）、路径、标签字符串
  （`needs-triage` 等）保留英文，保证互引用和触发词不被破坏
- 概念术语首次出现采用「中文（English）」形式，如 拷问（grilling）、接缝（seam）、
  曳光弹（tracer-bullet）、工单系统（issue tracker）
- frontmatter 中 `description` 译为中文，其余键值原样保留
- 代码块、ASCII 图、模板占位符整体不动

## 许可证

[MIT](./LICENSE)，版权归 Matt Pocock 所有。本仓库为翻译演化版本，遵循同一许可证。
