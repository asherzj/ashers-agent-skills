# 封装流程

这里存放面向用户的端到端研发流程。流程 Skill 只负责编排阶段、门禁和上下文交接；具体做法仍由 `skills/engineering/` 与 `skills/productivity/` 中的自由组合模块负责。

| Skill | 适用场景 | 编排路径 |
|---|---|---|
| `flow-feature` | 范围可澄清、但需要规格和多张工单的新需求 | `grill-with-docs → [prototype] → to-spec → to-tickets → implement × N` |
| `flow-small-change` | 一次上下文能完成的小改动 | `grill-with-docs → implement` |
| `flow-incoming-issue` | 外部提交的 Issue 或 PR | `triage → ready-for-agent 门禁 → implement` |
| `flow-hard-bug` | 难复现、间歇性或性能回归问题 | `diagnosing-bugs → implement 收尾` |
| `flow-large-effort` | 路线尚不清晰的超大型工作 | `wayfinder → to-spec → to-tickets → implement × N` |

不知道该选哪条流程时，调用 `ask-anything-about-engineering-skills`。
