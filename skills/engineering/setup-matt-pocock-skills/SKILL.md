---
name: setup-matt-pocock-skills
description: 为本仓库配置工程技能：设置其工单系统（issue tracker）、分诊（triage）标签词汇表和领域文档布局。在其他工程技能首次使用之前运行一次。
disable-model-invocation: true
---

# 设置 Matt Pocock 的技能

搭建工程技能所依赖的仓库级配置：

- **工单系统（issue tracker）**：issue 的存放位置（默认 GitHub；本地 markdown 也开箱即用）
- **分诊标签**：五个规范分诊角色所使用的字符串
- **领域文档**：`CONTEXT.md` 和 ADR（架构决策记录）的存放位置，以及读取它们的消费规则

这是一个提示驱动的技能，不是确定性脚本。先探索、展示你的发现、与用户确认，然后再写入。

## 流程

### 1. 探索

查看当前仓库，了解其初始状态。已有的东西都要读一读，不要凭空假设：

- `git remote -v` 和 `.git/config`：这是一个 GitHub 仓库吗？是哪一个？
- 仓库根目录的 `AGENTS.md` 和 `CLAUDE.md`：是否存在其中之一？其中是否已有 `## Agent skills` 小节？
- 仓库根目录的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 以及任何 `src/*/docs/adr/` 目录
- `docs/agents/`：本技能此前是否已生成过输出？
- `.scratch/`：本地 markdown 工单系统约定已在使用的标志
- 是否安装了 `triage` 技能？（与本技能同级的 `triage` 技能文件夹，或你可用技能列表中的 `triage`。）这决定 B 节是否运行。
- Monorepo 信号：`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或有自己 `src/` 的 `packages/*`。这些只存在于真正大型的多包仓库中；缺失即意味着单上下文（single-context），而几乎所有仓库都是单上下文。

### 2. 展示发现并提问

总结哪些已存在、哪些缺失。然后按顺序处理各节。一节一个问题，得到回答后再进入下一节。

每节都以推荐答案开头，让用户一个词就能接受。只有当选择确实存在分叉时才给出一行说明；当探索已经敲定答案时整节跳过（未安装 `triage` 时跳过 B 节，没有 monorepo 时跳过 C 节）。

**A 节：工单系统。**

> 说明：「工单系统」是本仓库 issue 的存放处。`to-tickets`、`triage`、`to-spec` 等技能会对它读写。它们需要知道是调用 `gh issue create`、在 `.scratch/` 下写 markdown 文件，还是遵循你描述的其他工作流。请选择你实际为本仓库跟踪工作的位置。

默认姿态：这些技能为 GitHub 而设计。如果某个 `git remote` 指向 GitHub，就提议 GitHub。如果某个 `git remote` 指向 GitLab（`gitlab.com` 或自建主机），就提议 GitLab。否则（或用户另有偏好时），提供以下选项：

- **GitHub**：issue 存放在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**：issue 存放在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 markdown**：issue 以文件形式存放在本仓库的 `.scratch/<feature>/` 下（适合单人项目或没有远端的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述工作流；技能会将其记录为自由格式的文字

把选择记录到 `docs/agents/issue-tracker.md`。GitHub 和 GitLab 模板带有一个「PR 作为请求面」的开关，默认**关闭**。保持关闭，也不要主动提起：想把外部 PR 纳入分诊队列的用户，之后可以自己在文件里打开这个开关。

**B 节：分诊标签词汇表。**如果未安装 `triage` 技能（探索阶段已经告诉你了），整节跳过，因为未安装的技能不需要标签。

如果已安装，只问一个问题：

> 是否保留默认的分诊标签？（推荐：**是**）

默认值是五个规范角色，每个标签字符串与角色名相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。回答**是**时按原样写入。只有当用户说否时——通常是因为其工单系统已在使用其他名称（例如用 `bug:triage` 代替 `needs-triage`）——才收集覆盖值，让 `triage` 沿用现有标签而不是创建重复标签。

**C 节：领域文档。**默认为**单上下文（single-context）**（仓库根目录一个 `CONTEXT.md` + `docs/adr/`）。这适合几乎所有仓库；无需询问直接写入。

只有当探索发现 monorepo 信号时，才提供**多上下文（multi-context）**（根目录 `CONTEXT-MAP.md` 指向各上下文各自的 `CONTEXT.md` 文件）选项。此时需确认用户想要哪种布局。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要加入正在编辑的 `CLAUDE.md` / `AGENTS.md` 的 `## Agent skills` 块（选择规则见第 4 步）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一个仅在安装了 `triage` 时）

写入之前让用户先编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则，如果 `AGENTS.md` 存在，编辑它。
- 如果两者都不存在，询问用户要创建哪一个；不要替用户决定。

`CLAUDE.md` 已存在时绝不创建 `AGENTS.md`（反之亦然）；始终编辑已有的那一个。

如果所选文件中已有 `## Agent skills` 块，就地更新其内容，而不是追加一个重复块。不要覆盖用户对周围小节的修改。

该块的内容：

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

只有当已安装 `triage` 且 B 节已运行时，才包含 `### Triage labels` 子块并写入 `docs/agents/triage-labels.md`。否则两者都省略。

然后以本技能文件夹中的种子模板为起点写入各文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub 工单系统
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab 工单系统
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 markdown 工单系统
- [triage-labels.md](./triage-labels.md)：标签映射（仅在安装了 `triage` 时）
- [domain.md](./domain.md)：领域文档消费规则 + 布局

对于「其他」工单系统，根据用户的描述从头编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户设置已完成，以及哪些工程技能从现在起会读取这些文件。提醒他们之后可以直接编辑 `docs/agents/*.md`；只有想更换工单系统或从头重来时，才需要重新运行本技能。
