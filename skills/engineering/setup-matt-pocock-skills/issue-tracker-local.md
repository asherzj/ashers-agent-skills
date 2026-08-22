# 工单系统（issue tracker）：本地 Markdown

本仓库的 issue 和 spec（规格说明）以 markdown 文件的形式存放在 `.scratch/` 中。

## 约定

- 每个功能一个目录：`.scratch/<feature-slug>/`
- spec 是 `.scratch/<feature-slug>/spec.md`
- 实现 issue 每个工单一个文件，位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 开始编号，绝不合并为单个工单文件
- 分诊（triage）状态记录为每个 issue 文件顶部附近的 `Status:` 行（角色字符串见 `triage-labels.md`）
- 评论和对话历史追加到文件底部 `## Comments` 标题之下

## 当技能说「发布到工单系统」时

在 `.scratch/<feature-slug>/` 下创建一个新文件（必要时创建目录）。

## 当技能说「获取相关工单」时

读取所引用路径下的文件。用户通常会直接给出路径或 issue 编号。

## 探路（wayfinding）操作

供 `/wayfinder` 使用。**地图**（map）是一个文件，每个工单（ticket）对应一个**子**（child）文件。

- **地图**：`.scratch/<effort>/map.md`（Notes / Decisions-so-far / Fog 正文）。
- **子工单**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 开始编号，正文中写问题。`Type:` 行记录工单类型（`research`/`prototype`/`grilling`/`task`）；`Status:` 行记录 `claimed`/`resolved`。
- **阻塞关系**：顶部附近的一行 `Blocked by: NN, NN`。当其列出的每个文件都是 `resolved` 时，工单即解除阻塞。
- **前沿（frontier）**：扫描 `.scratch/<effort>/issues/`，找出开放、未阻塞且未认领的文件；编号最小的胜出。
- **认领**：设置 `Status: claimed`，并在任何工作开始之前保存。
- **解决**：在 `## Answer` 标题下追加答案，设置 `Status: resolved`，然后向 `map.md` 中地图的 Decisions-so-far 追加一个上下文指针（gist + 链接）。
