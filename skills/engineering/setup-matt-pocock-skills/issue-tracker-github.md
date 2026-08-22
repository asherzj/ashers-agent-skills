# 工单系统（issue tracker）：GitHub

本仓库的 issue 和 spec（规格说明）以 GitHub issue 的形式存放。所有操作使用 `gh` CLI。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取 issue**：`gh issue view <number> --comments`，用 `jq` 过滤评论，并一并获取标签。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 和 `--state` 过滤器。
- **评论 issue**：`gh issue comment <number> --body "..."`
- **添加 / 移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

通过 `git remote -v` 推断仓库；在克隆内运行时 `gh` 会自动完成。

## 将 PR 作为分诊（triage）面

**PR 作为请求面：no。** _（如果本仓库把外部 PR 视为功能请求，请设为 `yes`；`/triage` 会读取此标志。）_

设为 `yes` 时，PR 与 issue 走同一套标签和状态，使用 `gh pr` 的等价命令：

- **读取 PR**：`gh pr view <number> --comments`，并用 `gh pr diff <number>` 获取 diff。
- **列出待分诊的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，然后只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的（丢弃 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论 / 打标签 / 关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 issue 和 PR 共用一个编号空间，因此单独一个 `#42` 可能是两者之一：先用 `gh pr view 42` 判定，再回退到 `gh issue view 42`。

## 当技能说「发布到工单系统」时

创建一个 GitHub issue。

## 当技能说「获取相关工单」时

运行 `gh issue view <number> --comments`。

## 探路（wayfinding）操作

供 `/wayfinder` 使用。**地图**（map）是一个 issue，以**子**（child）issue 作为工单（ticket）。

- **地图**：一个带 `wayfinder:map` 标签的 issue，承载 Notes / Decisions-so-far / Fog 正文。`gh issue create --label wayfinder:map`。
- **子工单**：作为 GitHub sub-issue 关联到地图的 issue（对 sub-issues 端点调用 `gh api`）。在未启用 sub-issue 之处，把子项加进地图正文的任务列表，并在子工单正文顶部写 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。一旦被认领，工单即指派给负责推进的开发者。
- **阻塞关系**：GitHub 的**原生 issue 依赖**，是规范且在 UI 中可见的表示。用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加一条边，其中 `<blocker-db-id>` 是阻塞者的数字**数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，_不是_ `#number` 或 `node_id`）。GitHub 会报告 `issue_dependencies_summary.blocked_by`（仅统计开放的阻塞者，即实时闸门）。在依赖不可用之处，回退为在子工单正文顶部写一行 `Blocked by: #<n>, #<n>`。所有阻塞者都关闭后，工单即解除阻塞。
- **前沿（frontier）查询**：列出地图的开放子项（`gh issue list --state open`，范围限定到地图的 sub-issue / 任务列表），丢弃任何带开放阻塞者（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中存在开放 issue）或已有指派人的；按地图顺序排在最前的胜出。
- **认领**：`gh issue edit <n> --add-assignee @me`，这是本会话的第一次写入。
- **解决**：`gh issue comment <n> --body "<answer>"`，然后 `gh issue close <n>`，再向地图的 Decisions-so-far 追加一个上下文指针（gist + 链接）。
