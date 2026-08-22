# 领域文档

工程技能在探索代码库时应如何使用本仓库的领域文档。

## 探索之前，先阅读这些

- 仓库根目录的 **`CONTEXT.md`**，或
- 仓库根目录的 **`CONTEXT-MAP.md`**（如果存在）：它指向每个上下文各一个 `CONTEXT.md`。阅读与主题相关的每一个。
- **`docs/adr/`**：阅读与你即将工作区域相关的 ADR（架构决策记录）。在多上下文仓库中，还要检查 `src/<context>/docs/adr/` 中上下文范围的决策。

如果这些文件不存在，**静默继续**。不要指出其缺失；也不要建议预先创建。`/domain-modeling` 技能（经由 `/grill-with-docs` 和 `/improve-codebase-architecture` 到达）会在术语或决策真正敲定时按需创建它们。

## 文件结构

单上下文（single-context）仓库（大多数仓库）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文（multi-context）仓库（根目录存在 `CONTEXT-MAP.md`）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用词汇表中的词汇

当你的输出提到某个领域概念时（issue 标题、重构提案、假设、测试名中），使用 `CONTEXT.md` 中定义的术语。不要漂移到词汇表明确回避的同义词。

如果你需要的概念还不在词汇表中，那是一个信号：要么你在发明项目并不使用的语言（请重新考虑），要么存在真实缺口（记下来交给 `/domain-modeling`）。

## 标记 ADR 冲突

如果你的输出与现有 ADR 相矛盾，请明确指出，而不是默默覆盖：

> _与 ADR-0007（event-sourced orders）相矛盾，但值得重新审议，因为……_
