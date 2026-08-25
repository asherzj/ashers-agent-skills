---
name: install-skills
description: 统一安装或升级本仓库的全部中文研发 Skill，包括封装流程和自由组合模块，使它们在当前 Coding Agent 的所有项目中可用。首次安装或升级时运行。
disable-model-invocation: true
---

# 安装或升级整套研发 Skill

把 `https://github.com/asherzj/agent-engineering-skills` 中的全部 Skill 安装到当前 Coding Agent 的用户级 Skill 目录。重复运行即为升级。

## 1. 定位用户级 Skill 目录

安装目录因 Agent 而异，例如 Claude Code 使用 `~/.claude/skills`，Codex 通常使用 `~/.codex/skills`。优先读取当前 Agent 的配置约定；仍无法确定时询问用户，不能猜测路径后直接写入。

## 2. 获取仓库源码

- 优先使用：`git clone --depth 1 https://github.com/asherzj/agent-engineering-skills.git /tmp/agent-engineering-skills`
- 如果克隆因网络问题失败，改用：`curl -sL --retry 3 -o /tmp/agent-engineering-skills.tar.gz https://codeload.github.com/asherzj/agent-engineering-skills/tar.gz/refs/heads/main`

只在明确、独立的临时目录中操作，不能把用户的工作目录当作安装暂存区。

## 3. 安装范围

扫描 `engineering-skills/` 的一级子目录，只安装其中直接包含 `SKILL.md` 的目录。这里应当得到 25 个 Skill：5 个封装流程、18 个工程模块、`grilling` 访谈原语和 `install-skills` 安装入口。

`engineering-skills/` 自身是集合根目录，不作为 Skill 安装；说明性 `README.md` 同样不安装。不要递归猜测更深层级，因为本仓库约定每个 Skill 都必须直接位于这一层。

关键依赖关系：

- `flow-feature` → `grill-with-docs`、`prototype`、`to-spec`、`to-tickets`、`implement`
- `flow-small-change` → `grill-with-docs`、`implement`
- `flow-incoming-issue` → `triage`、`implement`
- `flow-hard-bug` → `diagnosing-bugs`、`implement`、`code-review`
- `flow-large-effort` → `wayfinder`、`to-spec`、`to-tickets`、`implement`
- `grill-with-docs` → `grilling`、`domain-modeling`
- `improve-codebase-architecture` → `codebase-design`、`domain-modeling`、`grilling`
- `wayfinder` → `domain-modeling`、`grilling`、`prototype`、`research`
- `setup-engineering-skills` 提供 `triage`、`wayfinder`、`to-spec`、`to-tickets` 使用的仓库级配置

逐个 Skill 进行范围明确的覆盖安装。覆盖前确认目标是解析后的用户级 Skill 目录下的单个 Skill 文件夹，不能对用户主目录、Skill 根目录或未解析变量执行递归删除。保留与本仓库无关的其他 Skill。

## 4. 验证

- 对比目标目录和上述 25 个 Skill，确认没有遗漏；
- 检查每个 `SKILL.md` 的 frontmatter，确认 `name` 非空且与目录名一致；
- 检查 `agents/openai.yaml` 的界面信息保持中文；
- 检查引用到的 Skill 依赖都已安装；
- 确认模板、参考文件和脚本随各自 Skill 一并复制；
- 确认安装清单中不存在已经废弃的入口目录或重复别名。

## 5. 清理与汇报

只清理本次安装创建的临时目录和下载文件。最终汇报安装清单、验证结果、生效条件，以及首次在具体仓库使用前运行 `setup-engineering-skills` 的提示。
