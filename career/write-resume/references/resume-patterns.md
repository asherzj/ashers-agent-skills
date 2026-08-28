# Resume Patterns

The examples in this reference are fictional. Use their structure, never their facts or metrics, in a user's resume.

## Decision Point Checklist

A strong resume item usually has at least two of these:

- Role relevance: directly maps to the target job.
- Scarcity: few candidates can credibly claim it.
- Scale: users, revenue, traffic, data, team, geography, complexity.
- Impact: improved a business, product, system, team, or process.
- Recognition: awards, performance rating, promotion, adoption, public result.
- Defensibility: the candidate can explain their exact contribution.
- Personality evidence: ownership, quality bar, service mindset, learning ability, persistence, collaboration.

Delete or compress items that provide none of these.

## Bullet Formulas

Use one of these depending on the evidence:

```text
Built/led/owned X for Y users/teams/systems, improving Z by N%.
```

```text
Under constraint X, designed Y approach, reducing/increasing Z from A to B.
```

```text
Owned X module in Y project; delivered A/B/C, enabling measurable outcome Z.
```

```text
Diagnosed X bottleneck, introduced Y, and reduced latency/error/cost/time from A to B.
```

```text
Coordinated X stakeholders without formal authority, delivered Y by deadline, and created repeatable process Z.
```

```text
Maintained quality bar by doing X; kept Y metric at/above/below Z across N releases.
```

## Baseline Rule

所有变化型结果必须提供可比较的基线和终值。不要只写“提升至 B”“降低至 B”或“优化了 X%”；应写成“指标在同一统计口径下从 A 提升至 B”或“从 A 降低至 B”，并尽量补充统计周期、样本范围或比较对象，让面试官能判断变化的实际量级。

```text
转化率从18%提升至24%（提升6个百分点），覆盖当月12组A/B实验。
```

```text
核心链路P99延迟从800ms降至180ms，统计口径为生产环境连续30天请求。
```

百分比与百分点不得混用：从18%到24%是增加6个百分点，相对增幅约33.3%。只保留与用户原始数据及计算口径一致的表达。如果用户只提供终值或变化比例，先追问基线；无法确认时使用待确认占位符，或只陈述可以自证的终值和规模，不得声称未经证实的提升或降低。

## Section Templates

### Summary

Use 2-3 lines. The first line should be the strongest universal signal.

```text
Backend engineer with 5 years of high-traffic system experience; led order/payment services supporting 3M daily orders.
Quality-oriented owner: introduced CI quality gates and raised unit test coverage from 42% to 86% across 12 services.
Seeking to build reliable commerce infrastructure in a team that values engineering depth and product impact.
```

### Experience

```text
Company | Role | Dates
- Scope/result bullet.
- Technical or business challenge bullet.
- Ownership/collaboration bullet.
- Recognition/learning/quality bullet if strong.
```

### Project

```text
Project Name
Background: one short line on why the project mattered.
Scale: users, QPS, data volume, revenue, team size, duration, or operational scope.
Challenge: hardest technical/product/coordination constraint.
Ownership: what the candidate personally decided, built, led, or improved.
Result: measurable impact and current status.
```

## Weak To Strong Examples

Weak:

```text
参与用户增长项目，负责数据分析和活动策划。
```

Strong:

```text
负责新客转化实验分析，3周内完成12组A/B实验，推动注册转化率从18%提升至24%。
```

Weak:

```text
熟悉微服务架构，参与系统优化。
```

Strong:

```text
重构订单服务拆分边界，将核心链路P99延迟从800ms降至180ms，并支撑日均300万订单。
```

Weak:

```text
沟通能力强，具备团队协作精神。
```

Strong:

```text
作为技术接口人对接产品、运营、销售3类角色，将复杂风控规则拆解为可执行配置，使跨部门平均确认周期从5个工作日缩短至3个工作日。
```

Weak:

```text
爱好写作、跑步、足球。
```

Strong:

```text
技术写作博客坚持周更3年，单篇最高8万+阅读；每周3次5公里跑步，坚持7年。
```

## Quantification Prompts

If the user lacks numbers, ask about or suggest relevant categories:

- How many users, customers, merchants, requests, files, records, devices, regions, or teams?
- Before/after values under the same definition: latency, conversion, cost, failure rate, manual time, delivery cycle, coverage, accuracy. For every change claim, collect baseline A, outcome B, measurement period, and sample scope.
- Ranking/rarity: top X%, only N people, first project, largest account, highest priority.
- Time: built in N weeks, saved N hours/week, supported N releases, maintained for N months.
- Team: managed N people, coordinated N stakeholders, hired N people, mentored N promotions.

If exact numbers are unavailable, use ranges or scale language only when the user can substantiate them:

```text
千万级数据
百人级内部用户
多个核心业务方
从小时级缩短到分钟级
```

## Review Rubric

Score each resume from 1-5:

- Clarity: can a reader understand the strongest value in 30 seconds?
- Relevance: does the content match the target role/JD?
- Evidence: are claims backed by numbers, scope, or concrete examples?
- Baseline integrity: does every increase/decrease claim show comparable before-and-after values without confusing percentages and percentage points?
- Ownership: is the candidate's personal contribution clear?
- Differentiation: does it show why this candidate is not generic?
- Defensibility: can every strong bullet survive interview challenge?
- Brevity: is weak or repetitive content removed?
- Scanability: is it visually easy to read?

High-impact fixes usually follow this order:

1. Reorder sections so the strongest evidence appears first.
2. Rewrite summary into decision points.
3. Quantify top projects.
4. Clarify personal ownership.
5. Delete unsupported adjectives and filler skills.
6. Improve bullet length and formatting.

## ATS Compatibility

- Prefer a simple reading order, standard section names, selectable text, and conventional date formatting.
- Keep essential contact information and section content out of decorative images, headers, and footers that an ATS may ignore.
- Use JD terminology only when it accurately describes the candidate's experience; do not keyword-stuff or hide keywords.
- When producing PDF, confirm that copied text follows the intended reading order.

## Cautions

- Do not fabricate metrics, titles, awards, school quality, or ownership.
- Do not encourage discriminatory or legally risky personal disclosures. Treat age, marital status, fertility, health, ethnicity, and politics as sensitive; include only when the user explicitly requests and understands the tradeoff.
- Do not overfit ATS keywords at the cost of human credibility.
- Do not make every bullet sound like a world-changing achievement; believable precision is better than inflated grandeur.
