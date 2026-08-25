---
name: flow-incoming-issue
description: 把外部提交的 Issue 或 PR 先送入分诊，再只在其达到 ready-for-agent 后进入实现。适用于原始 Bug 报告和外部功能请求；不适用于 to-tickets 生成的工单。
disable-model-invocation: true
---

# 外部 Issue 处理流程

用明确的状态门禁组合 `triage` 和 `implement`。开始前读取仓库配置、工单系统说明、分诊标签映射、相关领域术语和 ADR。

## 边界

本流程只处理团队没有通过 `to-tickets` 创建的外部工作。拆票生成的工单天然可由代理执行，应直接进入 `implement`。

## 流程

1. 对指定 Issue 或外部 PR 调用 `triage`。由它负责收集上下文、验证事实、维护者检查点、AI 声明、代理简报、标签和拒绝事项的关闭动作。
2. 检查产生的规范状态：
   - `needs-triage` 或 `needs-info`：停止实现，说明还需要什么信息或维护者决策。
   - `ready-for-human`：停止，并把简报留给人类。
   - `wontfix`：停止；事项已经终结。
   - `ready-for-agent`：状态允许代理实现，但仍要服从用户本次请求的范围。
3. 只有事项为 `ready-for-agent`，且用户要求本流程继续完成交付时，才调用 `implement`。如果用户只要求分诊，即使事项已就绪也应停在分诊结果。

如果事项一开始就是 `ready-for-agent`，先确认它只有一个状态标签并包含耐久的代理简报，然后跳过重复分诊，直接进入实现。一张 Issue 始终是一份实现单元。

## 完成条件

分别汇报分诊结果和实现结果。只有实际完成验证、评审、提交、推送和工单收尾后，才能称为已交付；仅完成分诊不能称为交付。
