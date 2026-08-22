---
name: install-skills
description: 统一初始化入口。把本仓库（Matt Pocock skills 中文版）的全部 skills 安装或升级到当前 coding agent 的用户级（全局）skill 目录，使所有项目可用。首次使用或升级时运行。
disable-model-invocation: true
---

# 安装 / 升级本套 skills

把本仓库（https://github.com/asherzj/matt-pocock-skills-zh）中的全部 skill
安装到当前 coding agent 的**用户级（全局）skill 目录**。重复运行即为升级。

## 1. 定位用户级 skill 目录

安装目录因 agent 而异（如 Claude Code 为 `~/.claude/skills`，其他 agent 各有不同）。
若不确定自己平台的用户级 skill 目录位置，先探测或查阅本 agent 的配置约定，
仍无法确定时询问用户，**不要**猜一个路径就写入。

## 2. 获取仓库源码

- 优先：`git clone --depth 1 https://github.com/asherzj/matt-pocock-skills-zh.git /tmp/matt-pocock-skills-zh`
- 若克隆失败（网络中断、early EOF），降级为 tarball 下载并解压：
  `curl -sL --retry 3 -o /tmp/skills.tar.gz https://codeload.github.com/asherzj/matt-pocock-skills-zh/tar.gz/refs/heads/main`

## 3. 安装范围

本仓库 `skills/` 下的全部 skill 目录：

- `skills/engineering/` 下 18 个（ask-matt、code-review、codebase-design、diagnosing-bugs、
  domain-modeling、grill-with-docs、implement、improve-codebase-architecture、prototype、
  research、resolving-merge-conflicts、setup-matt-pocock-skills、tdd、to-spec、to-tickets、
  triage、wayfinder、wizard）
- `skills/productivity/grilling`（拷问核心，多个 engineering skill 的依赖）
- `skills/install-skills/`（本 skill 自身，一并安装以便日后升级）

内部依赖关系（安装时全量覆盖，无需单独处理）：

- grill-with-docs → grilling + domain-modeling
- improve-codebase-architecture → codebase-design + domain-modeling + grilling
- tdd → codebase-design
- triage → domain-modeling + grilling
- wayfinder → domain-modeling + grilling + prototype + research
- setup-matt-pocock-skills → triage（被 wayfinder/triage/to-spec/to-tickets 运行时引用）

逐个覆盖安装以保证升级干净：

```
rm -rf <用户级skill目录>/<name> && cp -r <src> <用户级skill目录>/<name>
```

已存在同名 skill 时直接覆盖（重新安装即升级）。

## 4. 验证

- 列出用户级 skill 目录内容，与上述清单比对，缺一不可
- 检查每个 `SKILL.md` 含合法 frontmatter（`name:` 字段非空）
- 统计各 skill 目录的文件数，确认附带文件（如 domain-modeling 的 CONTEXT-FORMAT.md、
  setup-matt-pocock-skills 的模板文件）一并复制

## 5. 清理与汇报

- 删除 /tmp 下所有临时文件
- 最终汇报：安装清单、生效条件（新开会话后生效）、
  以及使用提示：wayfinder/triage/to-spec/to-tickets 依赖仓库级配置，
  在具体项目里首次使用前先运行一次 setup-matt-pocock-skills
