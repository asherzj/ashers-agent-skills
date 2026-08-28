# 仓库维护说明

## 仓库定位

本仓库维护一套面向 Agent 的中文 Skill，按使用领域组织为编码、求职准备和写作三类。根目录 `README.md` 面向使用者；本文件约束维护本仓库的 Agent。

## 目录结构

- 除唯一的根级安装入口 `install-skills/` 外，所有可安装 Skill 必须位于 `<category>/<skill-name>/`。分类目录直接位于仓库根目录，当前固定为 `coding`、`career` 和 `writing`。
- 每个 Skill 必须直接位于所属分类目录下并包含 `SKILL.md`；不要在分类内重新引入 `engineering/`、`productivity/`、`flows/` 等中间层。
- 各分类目录只是分类入口，不作为 Skill 安装；允许用 `README.md` 说明分类边界和清单。
- `install-skills/` 负责选择分类、安装和升级，不归入任何分类，也不得在分类目录中保留别名或副本。
- Skill 文件夹名必须与 `SKILL.md` frontmatter 中的 `name` 完全一致，名称使用小写字母、数字和连字符。
- Skill 专属的 `agents/`、`scripts/`、`references/`、模板和说明文件放在该 Skill 目录内；不要创建没有实际用途的占位目录或文档。

## 内容与命名

- Skill 的 frontmatter `description`、正文、界面名称、简短说明和默认提示保持中文。
- Skill 标识符、路径、命令、代码、协议字段和稳定标签保留英文，不为追求中文化破坏互引用或自动触发。
- `coding` 中封装完整研发链路的 Skill 使用 `flow-*` 前缀；可自由组合的阶段能力保持独立，不增加分类目录。
- 流程 Skill 只负责阶段编排、门禁和上下文交接。具体阶段的详细规则留在对应模块 Skill 中，避免复制后产生两套规范。
- 除根 `README.md` 的来源说明和 `LICENSE` 中的版权声明外，不重新引入 Matt Pocock 个人品牌。

## 修改时保持同步

- 新增、移动、重命名或删除 Skill 时，同步更新根 `README.md`、对应分类的 `README.md` 以及相关 Skill 间的引用。
- 同步检查 `install-skills/SKILL.md` 中的分类选择、扫描规则、预期数量和安装说明。
- 新增或修改 Skill 时，同步维护 `agents/openai.yaml`；其中的显示名称、简短说明和默认提示必须与 `SKILL.md` 一致。
- 重命名时搜索旧名称和旧路径，确保正文、相对链接、安装说明和流程引用中没有残留。
- 修改流程编排时，同时检查 `ask-anything-about-engineering-skills` 的路由说明和各 `flow-*` Skill 的阶段边界。

## 验证

提交前至少完成以下检查：

- 三个分类目录和唯一的 `install-skills/` 入口直接位于仓库根目录；除安装入口外，每个 Skill 都直接位于某个分类目录下并包含 `SKILL.md`，不存在更深层的 Skill。
- 每个 Skill 的文件夹名与 frontmatter `name` 一致，YAML 可解析，必填字段完整。
- 新增或修改的说明和 UI 元数据保持中文，相关相对链接指向真实文件。
- 安装 Skill 中声明的预期数量与实际 Skill 数量一致。
- 新增或修改的脚本已按其真实使用方式运行验证。
- `git diff --check` 通过，并检查 `git status` 与最终差异中没有无关文件。

如果仓库后续增加统一验证脚本或 CI，应优先运行它们，并把命令补充到本节。
