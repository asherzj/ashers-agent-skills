# HTML 报告格式

架构评审渲染为操作系统临时目录中的一个自包含 HTML 文件。Tailwind 和 Mermaid 都来自 CDN。Mermaid 可靠地处理图状结构；手工构建的 div 和内联 SVG 处理更具编辑感的视觉（体量图、剖面图）。两者混用：不要事事依赖 Mermaid，那会开始显得千篇一律。

## 脚手架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* 一个小型自定义层，处理 Tailwind 无法干净覆盖的东西：
         虚线接缝线、手绘感的箭头等 */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 页眉

仓库名、日期，以及一个紧凑的图例：实线框 = 模块，虚线 = 接缝（seam），红色箭头 = 泄漏，深色粗框 = 深模块（deep module）。不要简介段落。直接进入候选。

## 候选卡片

图承担主要分量。文字稀疏、平实，使用词汇表术语（来自 `/codebase-design` skill）时不加虚饰。

每个候选是一个 `<article>`：

- **标题**：简短，点出深化动作（例如「收拢 Order 接入管线」）。
- **徽章行**：推荐强度（`Strong` = 祖母绿，`Worth exploring` = 琥珀，`Speculative` = 石板灰），外加一个依赖类别的标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **文件**：等宽字体列表，`font-mono text-sm`。
- **前/后图**：核心所在。两栏并排。见下面的模式。
- **问题**：一句话。痛在哪里。
- **方案**：一句话。改变什么。
- **收益**：列表项，每条不超过 6 个词。例如「测试只命中一个接口」「定价逻辑不再泄漏」「删掉 4 个浅包装」。
- **ADR 提示**（如适用）：琥珀色底框里的一行字。

不要成段的解释。如果一张图需要一段文字才能被理解，就重画这张图。

## 图表模式

挑选适合候选的模式。混着用。不要让每张图看起来都一样。多样性本身就是意义的一部分。

### Mermaid 图（依赖/调用流的主力）

当重点是「X 调用 Y 调用 Z，看看这团乱麻」时，使用 Mermaid 的 `flowchart` 或 `graph`。把它包进一张 Tailwind 样式的卡片，免得显得像是空投进来的。用 classDef 把泄漏边标红、把深模块标暗。时序图很适合表达「前：6 次往返；后：1 次」。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手工方框与箭头（当 Mermaid 的布局跟你作对时）

模块用带边框和标签的 `<div>` 表示。箭头用内联 SVG 的 `<line>` 或 `<path>` 元素，在一个相对容器上绝对定位。当你希望「后」图呈现为一个粗边框、内部灰显的深模块时，就用这种画法，因为 Mermaid 渲染不出那种分量。

### 剖面图（适合分层式的浅薄）

堆叠水平条带（`h-12 border-l-4`）展示一次调用穿过的各层。前：6 个薄层，每层无所事事。后：1 个厚条带，标注合并后的职责。

### 体量图（适合「接口与实现一样宽」）

每个模块两个矩形：一个代表接口表面积，一个代表实现。前：接口矩形几乎与实现矩形一样高（浅）。后：接口矩形矮，实现矩形高（深）。

### 调用图折叠

前：函数调用树渲染为嵌套方框。后：同一棵树折叠成一个方框，如今变为内部的调用以褪色方式显示在其中。

## 样式指导

- 走精炼的编辑风，而不是企业仪表盘风。留白大方。标题可选衬线体（`font-serif` 与 stone/slate 搭配良好）。
- 节制用色：一个强调色（祖母绿或靛蓝），外加泄漏用红色、警告用琥珀色。
- 图保持约 320px 高，让前/后能舒适并排而无须滚动。
- 图内模块标签使用 `text-xs uppercase tracking-wider`，让它读起来像示意图，而不是 UI。
- 脚本只有 Tailwind CDN 和 Mermaid 的 ESM 导入。报告其余部分是静态的：没有应用代码，除 Mermaid 自身的渲染外没有任何交互。

## 首选推荐部分

一张更大的卡片。候选名称、一句说明原因的话、指向其卡片的锚点链接。就这些。

## 语气

语言平实、简洁，但架构名词和动词全部直接来自 `/codebase-design` skill。简洁不是术语漂移的借口。

**精确使用：**模块（module）、接口（interface）、实现（implementation）、深度（depth）、深（deep）、浅（shallow）、接缝（seam）、适配器（adapter）、杠杆（leverage）、局部性（locality）。

**绝不替换为：**component、service、unit（指 module 时）· API、signature（指 interface 时）· boundary（指 seam 时）· layer、wrapper（指 module 时，当你本意就是 module）。

**符合该风格的措辞：**

- 「Order 接入模块是浅的：接口几乎与实现相当。」
- 「定价跨接缝泄漏。」
- 「深化：一个接口，一处测试之地。」
- 「两个适配器证明这条接缝成立：生产用 HTTP，测试用内存实现。」

**收益列表项**要用词汇表术语点名收益：*「局部性：bug 集中到一个模块」*、*「杠杆：一个接口，N 个调用点」*、*「接口收缩；实现吸收包装层」*。不要写*「更易维护」*或*「更干净的代码」*，因为这些说法不在词汇表里，配不上它们占据的位置。

不含糊其辞，不清嗓子铺垫，不写「值得注意的是……」。如果一个句子能写成列表项，就写成列表项。如果一个列表项能删，就删掉。如果一个术语不在 `/codebase-design` 词汇表里，先找表里有的，再考虑发明新词。
