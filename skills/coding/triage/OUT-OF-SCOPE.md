# 超出范围知识库

仓库中的 `.out-of-scope/` 目录存放被否决功能请求的持久记录。它有两个用途：

1. **组织记忆**：记录功能为何被否决，这样推理过程不会因 issue 关闭而丢失
2. **去重**：当新 issue 与先前的否决相匹配时，skill 可以呈现之前的决策，而不必重新争论一遍

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个文件对应一个**概念**，而不是一个 issue。请求同一件事的多个 issue 归入同一个文件。

## 文件格式

文件应以轻松、易读的风格撰写，更像一篇短小的设计文档，而不是一条数据库记录。使用段落、代码示例和例子，让推理过程对初次接触的人清晰而有用。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
```

### 文件命名

为概念取一个简短、有描述性的 kebab-case 名称：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。名称应足够易于辨认，让浏览目录的人不打开文件就能明白什么被否决了。

### 撰写理由

理由应当有实质内容：不是「我们不想要这个」，而是为什么。好的理由会提及：

- 项目范围或理念（「本项目专注于 X；主题化是下游使用者关心的事」）
- 技术约束（「支持它需要 Y，而这与我们的 Z 架构冲突」）
- 战略决策（「我们选择用 A 而不是 B，因为……」）

理由应当经久耐用。避免引用临时状况（「我们现在太忙了」）；那不是真正的否决，而是搁置。

## 何时检查 `.out-of-scope/`

在分诊（triage）期间（第 1 步：收集上下文），阅读 `.out-of-scope/` 中的所有文件。评估新 issue 时：

- 检查请求是否匹配某个已存在的超出范围概念
- 匹配依据概念相似度，而非关键词："night theme" 与 `dark-mode.md` 相匹配
- 如果匹配，把它呈现给维护者：「这与 `.out-of-scope/dark-mode.md` 类似。我们之前否决过它，原因是 [reason]。你现在还是同样的看法吗？」

维护者可以：

- **确认**：新 issue 被加入现有文件的 "Prior requests" 列表，然后关闭
- **重新考虑**：该超出范围文件被删除或更新，issue 走正常分诊流程
- **不认同**：这些 issue 相关但不同，继续正常分诊

## 何时写入 `.out-of-scope/`

只有当 **enhancement**（而非 bug）被*否决*为 `wontfix` 时才写入这里。这对 enhancement PR 与对 issue 完全一样：被否决的 PR 也记录在这里，以免同样的请求以新代码的形式卷土重来。

当某项因**已实现**而被关闭为 `wontfix` 时，**不要**写到这里。那是已构建的功能，不是被否决的功能；记录它会用虚假的否决污染去重检查。正确的做法是，在关闭评论中指出该功能已经存在的位置。

流程：

1. 维护者判定某个功能请求超出范围
2. 检查是否已存在匹配的 `.out-of-scope/` 文件
3. 如果有：把新 issue 追加到 "Prior requests" 列表
4. 如果没有：以概念名创建新文件，写明决策、理由和第一条先前的请求
5. 在 issue 上发布评论，解释决策并提到该 `.out-of-scope/` 文件
6. 以 `wontfix` 标签关闭该 issue

## 更新或删除超出范围文件

如果维护者对先前否决的概念改变了主意：

- 删除该 `.out-of-scope/` 文件
- skill 不需要重新打开旧 issue；它们是历史记录
- 触发重新考虑的新 issue 走正常分诊流程
