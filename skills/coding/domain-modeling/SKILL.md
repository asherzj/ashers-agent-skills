---
name: domain-modeling
description: 构建并打磨项目的领域模型。在讨论代码库术语、编写或编辑 CONTEXT.md，或记录/编辑 ADR 时使用。
---

# 领域建模

在设计的同时，主动构建并打磨项目的领域模型（domain model）。这是一项*主动*的纪律：挑战术语、发明边缘案例场景，并在术语敲定的那一刻把词汇表和决策写下来。（仅仅为了查词汇而*阅读* `CONTEXT.md` 不算本 skill：那是任何 skill 都能顺手做的一行习惯。本 skill 用于你要改变模型的时候，而不只是消费它。）

## 文件结构

大多数仓库只有单一上下文（context）：

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `CONTEXT-MAP.md`，仓库就有多个上下文。这份 map 指出每个上下文所在的位置：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

惰性创建文件：只在有内容可写时才创建。如果不存在 `CONTEXT.md`，在第一个术语敲定时创建它。如果不存在 `docs/adr/`，在需要第一个 ADR（架构决策记录）时创建它。

## 会话期间

### 对照词汇表发起挑战

当用户使用的术语与 `CONTEXT.md` 中的既有语言冲突时，立即指出。"你的词汇表把 'cancellation' 定义为 X，但你似乎指的是 Y。到底是哪个？"

### 打磨含糊的语言

当用户使用含糊或多义的术语时，提出一个精确的规范术语。"你在说 'account'：你指的是 Customer 还是 User？它们是不同的东西。"

### 讨论具体场景

在讨论领域关系时，用具体场景对它们做压力测试。发明能够探查边缘案例的场景，迫使用户精确说明概念之间的边界。

### 与代码交叉验证

当用户陈述某样东西如何工作时，检查代码是否同意。发现矛盾时，把它摆出来："你的代码取消的是整个 Order，但你刚才说部分取消是可能的。哪个是对的？"

### 就地更新 CONTEXT.md

术语一旦敲定，当场更新 `CONTEXT.md`。不要攒起来批量处理：随发生随记录。使用 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) 中的格式。

`CONTEXT.md` 应当完全不含实现细节。不要把 `CONTEXT.md` 当作 spec、草稿本或实现决策的存放处。它是词汇表，仅此而已。

### 谨慎提议 ADR

只在以下三条全部成立时，才提议创建 ADR：

1. **难以逆转**：之后再改变主意的代价是实质性的
2. **脱离上下文令人意外**：未来的读者会问"他们为什么这么做？"
3. **一次真实权衡的结果**：存在真正的备选方案，而你出于具体理由选了其中一个

三条中任何一条不满足，就跳过 ADR。使用 [ADR-FORMAT.md](./ADR-FORMAT.md) 中的格式。
