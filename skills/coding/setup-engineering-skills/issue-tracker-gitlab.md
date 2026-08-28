# 工单系统（issue tracker）：GitLab

本仓库的 issue 和 spec（规格说明）以 GitLab issue 的形式存放。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行描述使用 heredoc。传 `--description -` 可打开编辑器。
- **读取 issue**：`glab issue view <number> --comments`。需要机器可读输出时用 `-F json`。
- **列出 issue**：`glab issue list -F json`，配合适当的 `--label` 过滤器。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 把评论称为「note」。
- **添加 / 移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可以用逗号分隔，也可以重复该标志。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，因此先用 `glab issue note <number> --message "..."` 发布说明，再关闭。
- **合并请求**：GitLab 把 PR 称为「merge request」。使用 `glab mr create`、`glab mr view`、`glab mr note` 等，形式与 `gh pr ...` 相同，只是用 `mr` 代替 `pr`、`note`/`--message` 代替 `comment`/`--body`。

通过 `git remote -v` 推断仓库；在克隆内运行时 `glab` 会自动完成。

## 将 MR 作为分诊（triage）面

**MR 作为请求面：no。** _（如果本仓库把外部 merge request 视为功能请求，请设为 `yes`；`/triage` 会读取此标志。）_

设为 `yes` 时，MR 与 issue 走同一套标签和状态，使用 `glab mr` 的等价命令：

- **读取 MR**：`glab mr view <number> --comments`，并用 `glab mr diff <number>` 获取 diff。
- **列出待分诊的外部 MR**：`glab mr list -F json`，然后只保留作者不是项目成员/所有者的 MR（贡献者的 MR，而不是维护者进行中的工作）。
- **评论 / 打标签 / 关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 对 issue 和 MR 分别编号，因此只要知道维护者指的是哪个面，`#42` 就没有歧义。

## 当技能说「发布到工单系统」时

创建一个 GitLab issue。

## 当技能说「获取相关工单」时

运行 `glab issue view <number> --comments`。

## 探路（wayfinding）操作

供 `/wayfinder` 使用。**地图**（map）是一个 issue，以**子**（child）issue 作为工单（ticket）。

- **地图**：一个带 `wayfinder:map` 标签的 issue，承载 Notes / Decisions-so-far / Fog 正文。`glab issue create --label wayfinder:map`。（在提供原生 epic 的 GitLab 版本中，也可以改用 epic 承载地图；带标签的 issue 则在任何版本都可用。）
- **子工单**：描述顶部带 `Part of #<map>` 并带 `wayfinder:<type>` 标签（`research`/`prototype`/`grilling`/`task`）的 issue。一旦被认领，工单即指派给负责推进的开发者。
- **阻塞关系**：GitLab 的**原生阻塞链接**，是规范且在 UI 中可见的表示。用快捷操作 `/blocked_by #<n>` 添加，以 note 形式发布（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接是 Premium/Ultimate 功能；在免费版（或不可用之处）回退为在描述顶部写一行 `Blocked by: #<n>, #<n>`。所有阻塞者都关闭后，工单即解除阻塞。
- **前沿（frontier）查询**：`glab issue list -F json` 限定到地图的子项，丢弃任何带开放阻塞者的：指向开放 issue 的原生 `blocked_by` 链接（`glab api projects/:id/issues/:iid/links`）、`Blocked by` 行中的开放 issue，或已有指派人；按地图顺序排在最前的胜出。
- **认领**：`glab issue update <n> --assignee @me`，这是本会话的第一次写入。
- **解决**：`glab issue note <n> --message "<answer>"`，然后 `glab issue close <n>`，再向地图的 Decisions-so-far 追加一个上下文指针（gist + 链接）。
