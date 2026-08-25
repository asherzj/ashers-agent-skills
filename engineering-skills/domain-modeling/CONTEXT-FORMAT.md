# CONTEXT.md 格式

## 结构

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## 规则

- **要有主见。** 当同一概念存在多个词时，选出最好的一个，把其余列在 `_Avoid_` 下。
- **定义保持紧凑。** 最多一到两句。定义它「是」什么，而不是它「做」什么。
- **只收录该上下文特有的术语。** 一般编程概念（超时、错误类型、工具模式）不属于这里，即使项目大量使用它们。添加术语前先问：这是该上下文独有的概念，还是一般编程概念？只有前者属于这里。
- **当自然分组出现时，把术语归到子标题下。** 如果所有术语都属于单一内聚领域，平铺列表即可。

## 单上下文与多上下文仓库

**单一上下文（大多数仓库）：** 仓库根目录放一个 `CONTEXT.md`。

**多个上下文：** 仓库根目录的 `CONTEXT-MAP.md` 列出各上下文、它们的位置以及相互关系：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md): receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

本 skill 会推断适用哪种结构：

- 如果存在 `CONTEXT-MAP.md`，读它来找到各上下文
- 如果只存在根 `CONTEXT.md`，则为单一上下文
- 如果两者都不存在，在第一个术语敲定时惰性创建根 `CONTEXT.md`

存在多个上下文时，推断当前话题与哪个上下文相关。如果不清楚，就问。
