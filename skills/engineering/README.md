# 自由组合的工程模块

本目录提供可以单独调用、也可以被 `skills/flows/` 编排的研发小模块。完整交付优先使用封装流程；只需要某个阶段时再直接调用这里的模块。

## 用户显式调用

这些模块默认需要用户明确点名调用。

- **[ask-anything-about-engineering-skills](./ask-anything-about-engineering-skills/SKILL.md)**：根据研发处境选择封装流程或自由组合模块。
- **[grill-with-docs](./grill-with-docs/SKILL.md)**：逐轮澄清方案并同步维护领域文档与 ADR。
- **[triage](./triage/SKILL.md)**：按规范角色状态机流转外部 Issue 和 PR。
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)**：扫描代码库中的架构深化机会并逐项澄清。
- **[setup-engineering-skills](./setup-engineering-skills/SKILL.md)**：为仓库配置工单系统、分诊标签和领域文档布局。
- **[to-spec](./to-spec/SKILL.md)**：把当前对话综合成规格并发布到工单系统。
- **[to-tickets](./to-tickets/SKILL.md)**：把计划或规格拆成带阻塞边的纵向交付工单。
- **[implement](./implement/SKILL.md)**：按一张规格或工单完成实现、验证、评审、提交与推送。
- **[wayfinder](./wayfinder/SKILL.md)**：用共享决策地图规划超出一次会话容量的大型工作。

## 模型按需调用

这些模块既可以由用户点名，也可以由模型根据明确场景自动选择。

- **[prototype](./prototype/SKILL.md)**：制作一次性逻辑或 UI 原型，回答一个具体设计问题。
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**：为疑难 Bug 与性能回归建立反馈回路，最小化、定位、修复并补回归覆盖。
- **[research](./research/SKILL.md)**：针对高可信一手来源调研，并在仓库中留下带引用结果。
- **[tdd](./tdd/SKILL.md)**：通过红—绿纵向切片实现或修复一个行为。
- **[domain-modeling](./domain-modeling/SKILL.md)**：打磨领域模型、`CONTEXT.md` 与 ADR。
- **[codebase-design](./codebase-design/SKILL.md)**：使用深模块、接口、接缝和局部性设计模块边界。
- **[code-review](./code-review/SKILL.md)**：从代码规范与规格忠实度两个维度评审指定差异。
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)**：依据双方变更意图逐块解决合并或变基冲突。
- **[wizard](./wizard/SKILL.md)**：为只有人类能完成的第三方配置或切换步骤生成交互向导。

访谈原语 `grilling` 位于 `skills/productivity/grilling/`，供多个工程模块复用。
