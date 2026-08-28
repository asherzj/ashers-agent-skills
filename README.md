# Agent Skills

一套面向 Agent 的中文 Skill 集合，按编码、求职准备和写作三个领域组织。当前包含 28 个编码类 Skill 和 1 个求职准备类 Skill；编码类涵盖口述输入、需求澄清、原型、验收规格、工单拆分、TDD、代码评审、Issue 分诊、疑难问题诊断、大型工作寻路、架构维护和上下文垃圾回收。

> 本项目 fork 自 [mattpocock/skills](https://github.com/mattpocock/skills)，最初从其工程 Skill 的中文翻译起步。
> 目前已脱离上游同步节奏，围绕中文研发场景、端到端流程编排、仓库适配和 Coding Agent 协作方式独立演化。
> 原始作品及许可证归属见 [LICENSE](./LICENSE)；本项目后续修改继续遵循 MIT 许可证。

## Skill 分类

| 目录 | 中文领域 | 当前内容 |
|---|---|---|
| [`skills/coding/`](./skills/coding/) | 编码 | 现有 28 个研发流程与工程模块 |
| [`skills/career-prep/`](./skills/career-prep/) | 求职准备 | 现有 `write-resume` 简历写作 Skill |
| [`skills/writing/`](./skills/writing/) | 写作 | 为选题、起草、编辑和发布类 Skill 预留 |

分类总览见 [`skills/`](./skills/)。

## Coding Skill 的两种使用方式

用户可直接选择完整交付流程，也可以像积木一样自由组合小模块。不确定怎么选时，调用 `ask-anything-about-engineering-skills`。

### 1. 封装好的流程

这些流程负责阶段编排、门禁和上下文交接，适合直接从一个研发目标开始。

| Skill | 适用场景 | 主要路径 |
|---|---|---|
| `flow-feature` | 需要规格和多张工单的新需求 | `[from-transcript] → grill-with-docs → [prototype] → to-spec → to-tickets → implement × N` |
| `flow-small-change` | 一次上下文能完成的小改动 | `[from-transcript] → grill-with-docs → implement` |
| `flow-incoming-issue` | 外部提交的 Issue 或 PR | `triage → ready-for-agent 门禁 → implement` |
| `flow-hard-bug` | 疑难 Bug、间歇问题或性能回归 | `diagnosing-bugs → implement 收尾` |
| `flow-large-effort` | 路线尚不清晰的超大型工作 | `[from-transcript] → wayfinder → to-spec → to-tickets → implement × N` |
| `flow-architecture-maintenance` | 保持行为不变的独立架构优化 | `improve-codebase-architecture → to-spec → to-tickets → implement × N → context-gc` |

详细说明见 [`skills/coding/`](./skills/coding/)。

### 2. 自由组合的小模块

只需要某个阶段，或已有自己的流程时，可以直接调用这些模块。

#### 入口与仓库配置

| Skill | 说明 |
|---|---|
| `ask-anything-about-engineering-skills` | 在封装流程和自由组合模块之间选择正确入口 |
| `setup-engineering-skills` | 为具体仓库配置工单系统、分诊标签与领域文档布局 |
| `install-skills` | 把本仓库全部 Skill 安装或升级到用户级 Skill 目录 |

#### 澄清与规划

| Skill | 说明 |
|---|---|
| `grill-with-docs` | 逐轮澄清方案，同时维护 `CONTEXT.md` 与 ADR |
| `from-transcript` | 把口述和逐字稿整理成经人类确认的研发输入 |
| `prototype` | 用一次性逻辑或 UI 原型回答一个具体设计问题 |
| `to-spec` | 把当前上下文综合成规格并发布到工单系统 |
| `to-tickets` | 把规格拆成带阻塞边的纵向交付工单 |
| `wayfinder` | 把超大型模糊工作规划成共享决策地图 |

#### 实现与质量

| Skill | 说明 |
|---|---|
| `implement` | 按一张规格或工单完成实现、验证、评审、提交与推送 |
| `tdd` | 以红—绿纵向切片驱动行为实现 |
| `code-review` | 从代码规范与规格忠实度两个维度评审差异 |
| `diagnosing-bugs` | 先建立能捕获具体故障的反馈回路，再定位并修复 |
| `resolving-merge-conflicts` | 按双方变更意图逐块解决合并或变基冲突 |

#### 工单、知识与架构

| Skill | 说明 |
|---|---|
| `triage` | 按规范状态机分诊外部 Issue 和 PR |
| `research` | 针对高可信一手来源调研并沉淀带引用结论 |
| `domain-modeling` | 打磨领域术语并维护上下文文档与 ADR |
| `codebase-design` | 使用深模块、接口、接缝和局部性设计模块边界 |
| `improve-codebase-architecture` | 扫描代码库并发现值得深化的架构机会 |
| `context-gc` | 审计并清理过期、重复和矛盾的长期项目上下文 |
| `wizard` | 为只有人类能完成的第三方配置或切换步骤生成交互向导 |
| `grilling` | 单独使用逐轮访谈原语，不附带仓库文档包装 |

## 安装

方式一（推荐）：让 Agent 克隆仓库后调用 `install-skills`，由它探测当前 Agent 的用户级 Skill 目录并完成安装与验证。

```bash
git clone --depth 1 https://github.com/asherzj/ashers-agent-skills.git
```

方式二（手动）：扫描 `skills/<category>/` 下直接包含 `SKILL.md` 的 Skill 目录，并把每个 Skill 目录复制到当前 Agent 的用户级 Skill 目录。`skills/`、分类目录和其中的说明性 `README.md` 不安装；新开会话后生效。

## 为项目初始化工程 Skill

安装完成后，在每个具体项目里首次使用这套研发流程前，先进入目标仓库并调用：

```text
$setup-engineering-skills
```

`setup-engineering-skills` 会先探索仓库，再与用户确认以下配置：

- Issue 存放在 GitHub、GitLab、本地 Markdown，还是其他工单系统
- 是否采用默认的五个 Triage 标签
- 领域文档使用单上下文还是多上下文布局

确认后，它会更新仓库已有的 `AGENTS.md` 或 `CLAUDE.md`，并在 `docs/agents/` 下生成工单系统、Triage 标签和领域文档约定。`wayfinder`、`triage`、`to-spec` 和 `to-tickets` 等 Skill 会读取这些配置。

每个仓库通常只需运行一次。之后可以直接维护 `docs/agents/*.md`；只有更换工单系统或希望重新初始化配置时，才需要再次调用。

## 中文约定

- Skill 的说明、正文、界面名称与用户提示保持中文。
- 分类目录使用稳定的英文名称：`coding`、`career-prep`、`writing`。
- `name`、Skill 标识符、命令、文件名、路径和标签字符串保留稳定的英文形式，避免破坏互引用和自动触发。
- 必须保留的协议字段、代码、命令和模板键不做强行翻译。
- 新增或修改 Skill 时，同步更新 `agents/openai.yaml` 中的中文界面信息。

## 许可证与来源

[MIT](./LICENSE)。本仓库保留上游项目的版权与许可证声明；在此基础上的中文化、流程编排和后续功能由本仓库独立维护与演化。
