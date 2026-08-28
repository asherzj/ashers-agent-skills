# Coding Skills

本目录收纳编码与软件研发领域的 Skill，并采用平铺结构：除本说明文件外，每个一级子目录都是一个可独立安装的 Skill。分类内不再额外区分流程和模块；`flow-` 前缀负责聚类完整流程，下面的目录只负责说明它们在使用方式上的差异。

## 封装好的流程

适合从一个研发目标直接开始，由流程负责阶段门禁和上下文交接。

| Skill | 适用场景 | 编排路径 |
|---|---|---|
| [`flow-feature`](./flow-feature/SKILL.md) | 需要规格和多张工单的新需求 | `[from-transcript] → grill-with-docs → [prototype] → to-spec → to-tickets → implement × N` |
| [`flow-small-change`](./flow-small-change/SKILL.md) | 一次上下文能完成的小改动 | `[from-transcript] → grill-with-docs → implement` |
| [`flow-incoming-issue`](./flow-incoming-issue/SKILL.md) | 外部提交的 Issue 或 PR | `triage → ready-for-agent 门禁 → implement` |
| [`flow-hard-bug`](./flow-hard-bug/SKILL.md) | 疑难 Bug 或性能回归 | `diagnosing-bugs → implement 收尾` |
| [`flow-large-effort`](./flow-large-effort/SKILL.md) | 路线尚不清晰的超大型工作 | `[from-transcript] → wayfinder → to-spec → to-tickets → implement × N` |
| [`flow-architecture-maintenance`](./flow-architecture-maintenance/SKILL.md) | 保持行为不变的独立架构优化 | `improve-codebase-architecture → to-spec → to-tickets → implement × N → context-gc` |

## 自由组合的小模块

适合只需要某个阶段，或者已经有自己的流程时单独调用。

### 入口与仓库配置

- [`ask-anything-about-engineering-skills`](./ask-anything-about-engineering-skills/SKILL.md)：选择封装流程或自由组合模块。
- [`setup-engineering-skills`](./setup-engineering-skills/SKILL.md)：配置工单系统、分诊标签和领域文档布局。
- [`install-skills`](./install-skills/SKILL.md)：安装或升级本仓库全部分类中的 Skill。

### 澄清与规划

- [`from-transcript`](./from-transcript/SKILL.md)：把口述和逐字稿整理成经人类确认的研发输入。
- [`grill-with-docs`](./grill-with-docs/SKILL.md)：逐轮澄清方案并同步维护领域文档与 ADR。
- [`prototype`](./prototype/SKILL.md)：制作一次性逻辑或 UI 原型，回答具体设计问题。
- [`to-spec`](./to-spec/SKILL.md)：把当前对话综合成规格并发布到工单系统。
- [`to-tickets`](./to-tickets/SKILL.md)：把计划或规格拆成带阻塞边的纵向交付工单。
- [`wayfinder`](./wayfinder/SKILL.md)：用共享决策地图规划超出一次会话容量的大型工作。

### 实现与质量

- [`implement`](./implement/SKILL.md)：按一张规格或工单完成实现、验证、评审、提交与推送。
- [`tdd`](./tdd/SKILL.md)：通过红—绿纵向切片实现或修复一个行为。
- [`code-review`](./code-review/SKILL.md)：从代码规范与规格忠实度两个维度评审指定差异。
- [`diagnosing-bugs`](./diagnosing-bugs/SKILL.md)：为疑难 Bug 与性能回归建立反馈回路并完成诊断修复。
- [`resolving-merge-conflicts`](./resolving-merge-conflicts/SKILL.md)：依据双方变更意图逐块解决合并或变基冲突。

### 工单、知识与架构

- [`triage`](./triage/SKILL.md)：按规范角色状态机流转外部 Issue 和 PR。
- [`research`](./research/SKILL.md)：针对高可信一手来源调研并沉淀带引用结果。
- [`domain-modeling`](./domain-modeling/SKILL.md)：打磨领域模型、`CONTEXT.md` 与 ADR。
- [`codebase-design`](./codebase-design/SKILL.md)：使用深模块、接口、接缝和局部性设计模块边界。
- [`improve-codebase-architecture`](./improve-codebase-architecture/SKILL.md)：扫描代码库中的架构深化机会并逐项澄清。
- [`wizard`](./wizard/SKILL.md)：为只有人类能完成的第三方配置或切换步骤生成交互向导。
- [`grilling`](./grilling/SKILL.md)：单独使用逐轮访谈原语，不附带仓库文档包装。
