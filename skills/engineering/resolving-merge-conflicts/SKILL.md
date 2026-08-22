---
name: resolving-merge-conflicts
description: "在需要解决进行中的 git merge/rebase 冲突时使用。"
---

1. **查看 merge/rebase 的当前状态。** 检查 git 历史和冲突文件。

2. **为每个冲突找到一手来源。** 深入理解每处修改为何而来、原始意图是什么。读 commit message，查 PR，查原始的 issue/工单（ticket）。

3. **逐个解决差异块（hunk）。** 尽可能同时保留双方意图。二者不可兼得时，选择符合本次 merge 声明目标的一方，并记下权衡。**不要**发明新行为。始终解决，绝不 `--abort`。

4. 发现项目的**自动化检查**并运行它们，通常是先 typecheck，再测试，再格式化。修好 merge 弄坏的任何东西。

5. **完成 merge/rebase。** Stage 所有内容并 commit。如果是在 rebase，就继续 rebase 流程，直到所有 commit 都完成 rebase。
