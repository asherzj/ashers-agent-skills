---
name: install-skills
description: 按用户选择安装或升级本仓库 coding、career、writing 分类中的中文 Skill，使它们在当前 Coding Agent 的所有项目中可用。首次安装、按分类增量安装或升级时运行。
disable-model-invocation: true
---

# 选择并安装 Skill

把 `https://github.com/asherzj/ashers-agent-skills` 中用户选择的分类安装到当前 Coding Agent 的用户级 Skill 目录。重复选择同一分类即为升级。

根目录下的 `install-skills` 是仓库唯一的安装入口，不属于任何内容分类。每次运行都同步安装或升级它自身，方便用户以后再次选择分类；分类内容只按用户本次选择处理。

## 1. 让用户选择分类

可选分类：

- `coding`：27 个编码与软件研发 Skill；
- `career`：1 个求职准备 Skill：`write-resume`；
- `writing`：当前 0 个 Skill，选择后只报告暂无可安装内容；
- `all`：选择全部三个分类。

支持多选，例如 `coding + career`。如果用户在调用时已经明确给出分类，直接采用该选择；否则先展示上述清单并询问：

```text
请选择要安装或升级的分类：coding、career、writing，或 all。可以多选；安装器 install-skills 自身会一并更新。
```

这是安装范围的 human-in-the-loop 门禁。在用户明确选择前可以做只读检查，但不得向用户级 Skill 目录写入内容。用户选择后，Agent 全权完成源码获取、扫描、冲突检查、复制、验证、清理和汇报，不再要求用户逐个确认 Skill。

本次未选择的分类不得安装、升级或删除；目标目录中原有的其他 Skill 也必须保留。

## 2. 定位用户级 Skill 目录

安装目录因 Agent 而异，例如 Claude Code 使用 `~/.claude/skills`，Codex 通常使用 `~/.codex/skills`。优先读取当前 Agent 的配置约定；仍无法确定时询问用户，不能猜测路径后直接写入。

如果必须询问安装目录，可以和分类选择合并为一次提问。写入前向用户明确展示解析后的目标目录和所选分类；用户先前已经明确指定二者时不重复确认。

## 3. 获取仓库源码

- 优先使用：`git clone --depth 1 https://github.com/asherzj/ashers-agent-skills.git /tmp/ashers-agent-skills`
- 如果克隆因网络问题失败，改用：`curl -sL --retry 3 -o /tmp/ashers-agent-skills.tar.gz https://codeload.github.com/asherzj/ashers-agent-skills/tar.gz/refs/heads/main`

如果当前工作目录已经是该仓库的有效检出，可以直接使用；否则只在明确、独立的临时目录中获取源码，不能把用户的工作目录当作安装暂存区。

## 4. 解析安装范围

始终把根目录下直接包含 `SKILL.md` 的 `install-skills/` 加入安装清单。然后只扫描用户选择的分类目录，并只安装其中直接包含 `SKILL.md` 的一级子目录。

当前预期数量为：根级 `install-skills` 1 个；`coding` 27 个，包括 6 个封装流程、20 个工程模块和 `grilling` 访谈原语；`career` 1 个；`writing` 0 个。选择 `all` 时合计安装 29 个 Skill。分类目录和说明性 `README.md` 不作为 Skill 安装，也不要递归猜测更深层级。

安装前检查所选分类之间以及与根级安装器之间是否存在重复 Skill 名称。发现重名时停止写入并报告冲突，不能按扫描顺序静默覆盖。

关键依赖关系：

- `flow-feature` → `from-transcript`（按需）、`grill-with-docs`、`prototype`、`to-spec`、`to-tickets`、`implement`
- `flow-small-change` → `from-transcript`（按需）、`grill-with-docs`、`implement`
- `flow-incoming-issue` → `triage`、`implement`
- `flow-hard-bug` → `diagnosing-bugs`、`implement`、`code-review`
- `flow-large-effort` → `from-transcript`（按需）、`wayfinder`、`to-spec`、`to-tickets`、`implement`
- `flow-architecture-maintenance` → `improve-codebase-architecture`、`to-spec`、`to-tickets`、`implement`、`context-gc`
- `from-transcript` → `grilling`、`domain-modeling`
- `context-gc` → `grilling`、`domain-modeling`
- `grill-with-docs` → `grilling`、`domain-modeling`
- `improve-codebase-architecture` → `codebase-design`、`domain-modeling`、`grilling`
- `wayfinder` → `domain-modeling`、`grilling`、`prototype`、`research`
- `setup-engineering-skills` 提供 `triage`、`wayfinder`、`to-spec`、`to-tickets` 使用的仓库级配置

这些依赖当前都在 `coding` 内；选择完整分类即可保持其内部依赖完整。

## 5. 安装

先同步根级 `install-skills`，再逐个安装所选分类中的 Skill。升级时只覆盖安装清单内解析后的单个 Skill 文件夹；不能对用户主目录、Skill 根目录、整个分类或未解析变量执行递归删除。不得改动未选分类和与本仓库无关的 Skill。

## 6. 验证

- 对比实际安装清单与“根级安装器 + 所选分类”，确认没有遗漏或越界；
- 检查每个 `SKILL.md` 的 frontmatter，确认 `name` 非空且与目录名一致；
- 检查 `agents/openai.yaml` 的界面信息保持中文；
- 如果选择了 `coding`，检查上述内部 Skill 依赖都已安装；
- 确认模板、参考文件和脚本随各自 Skill 一并复制；
- 确认安装清单中不存在已经废弃的入口目录或重复别名。

## 7. 清理与汇报

只清理本次安装创建的临时目录和下载文件。最终按分类汇报用户选择、实际安装或升级的 Skill、跳过的分类、验证结果和生效条件。只有安装了 `coding` 时，才提示首次在具体仓库使用前运行 `setup-engineering-skills`。
