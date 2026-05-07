---
navigation_title: Best practices
description: Opinionated guidance for building scannable, performant Kibana dashboards, covering grid layout, panel sizing, information hierarchy, titling, and layout patterns.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
---

# Best practices for creating dashboards [dashboards-best-practices]

A well-designed dashboard answers a question at a glance and lets the reader drill in for detail. Use the recommendations on this page as defaults when building dashboards in {{product.kibana}}, whether through the UI, the [Dashboards API](create-dashboards-programmatically.md), or [{{agent-builder}}](create-dashboards-using-ai.md). Adapt them to your data and audience.

For the steps to build a dashboard, refer to [Create a dashboard](create-dashboard.md). For panel-arrangement mechanics, refer to [Organize dashboard panels](arrange-panels.md).

## Plan before you place panels [plan-before-place]

Before adding panels, decide who the dashboard is for and what it must answer. A few minutes of planning saves significant time later, when reorganizing a populated dashboard is harder than starting from a sketch.

Answer three questions:

* **Who is the audience?** Operators monitor for status changes, analysts explore comparisons, executives want summaries. Each scans the dashboard differently.
* **What is the primary question?** A current state, a trend over time, a comparison between groups, or a mix.
* **What decisions or actions does the dashboard support?** Alerting, investigation, reporting, or planning.

Then sketch the layout, on paper, a whiteboard, or a wireframe tool. Identify chart types for each data point, prioritize what goes where, and group related charts side by side. Leave room for the dashboard to grow as you add supporting panels.

## Build a clear information hierarchy [information-hierarchy]

Place the most important information at the top of the dashboard, where viewers look first.

* **Primary KPIs and key metrics** at the top.
* **Primary charts and trends** in the middle.
* **Detail tables and supporting panels** at the bottom for users who want to dig deeper.
* **Make the primary insight visually dominant.** A large, central panel anchors the dashboard and tells viewers where to look first. Wide rectangles like full-width timelines work especially well as focal points.
* **Place related panels next to each other.** When two related charts sit far apart, readers pay a cognitive tax to connect them. Group panels that share a data source or that explain the same trend.

The following sketch shows a standard hierarchy:

```text
┌─────────────────────────────────────────────────────┐
│  KPIs / Summary metrics (top row)                   │
├────────────────────────┬────────────────────────────┤
│  Primary chart         │  Secondary chart           │
│  (main insight)        │  (supporting data)         │
├────────────────────────┴────────────────────────────┤
│  Timeline / Trend chart (full width)                │
├────────────────────────┬────────────────────────────┤
│  Detail chart 1        │  Detail chart 2            │
└────────────────────────┴────────────────────────────┘
```

Aim to keep the most important content visible without scrolling. On a 1080p (16:9) screen, that's roughly the first 24 rows of the dashboard grid. On a 1440p screen, it's roughly 38 to 40 rows. Operational dashboards in particular benefit from showing 8 to 12 panels above the fold.

## Use the dashboard grid [dashboard-grid]

{{product.kibana}} dashboards use a 48-column grid with rows of fixed height. When you move or resize a panel, it snaps to column and row boundaries on this grid. New panels are created at half width (24 columns) by default.

Use these reference widths to keep panels aligned across a row:

| Panel width | Columns |
| ----------- | ------- |
| Full        | 48      |
| Half        | 24      |
| Third       | 16      |
| Quarter     | 12      |
| Sixth       | 8       |

Dashboards read better when there are no empty pockets between panels:

* **Remove dead vertical space.** Make each panel's top edge meet the bottom edge of the panel that sits directly over it. Gaps push supporting content further down the dashboard.
* **Align heights within a row.** When several panels sit side by side, give them the same height. Mismatched heights leave awkward gaps and make the row harder to scan. If panel heights must differ, fill the empty space with another panel before starting a new full-width row.

The {{product.kibana}} dashboard editor packs the grid for you when you drag and resize panels in the UI. When you author dashboards through the [Dashboards API](create-dashboards-programmatically.md), you set `x`, `y`, `w`, and `h` numerically, so apply the same packing rules in your JSON definitions.

## Size panels for what they show [size-panels]

Match panel size and shape to the chart type. Use the following heights and widths as a starting point and adjust based on the density of your data and the dashboard's overall layout. Heights are expressed in dashboard grid rows.

| Chart type                          | Width                         | Height (rows) | Placement                |
| ----------------------------------- | ----------------------------- | ------------- | ------------------------ |
| KPI metric                          | Quarter (12)                  | 4 to 6        | Top row                  |
| Compact bar chart (≤ 7 items)       | Half (24)                     | 8 to 10       | Above the fold           |
| Standard bar chart (8 to 12 items)  | Half (24)                     | 12 to 13      | Mid-dashboard            |
| Tall bar chart (13+ items)          | Half (24) to full (48)        | 15 or more    | Mid-dashboard            |
| Time series (line, area, time bar)  | Full (48)                     | 12 to 15      | Own row                  |
| Pie or donut                        | Quarter (12) to half (24)     | 12 to 18      | Grouped with related     |
| Heat map                            | Full (48)                     | 15 to 25      | Own row                  |
| Table                               | Half (24) to full (48)        | 15 or more    | Bottom of the dashboard  |

A few principles behind these numbers:

* **Single-value metrics and KPIs** work in compact panels of any shape, since the rendered content is one number.
* **Time series, bar charts, and tables** need horizontal room so the time axis, bar labels, and column headers don't get cramped.
* **Pie and donut charts** read best in roughly square panels. Stretching either axis wastes space without showing more data.
* **Use width to signal importance.** Give primary charts more horizontal room, and group dense KPI metrics into narrower panels along a single row.

For per-chart configuration options, refer to the dedicated page for each chart type, listed under [Lens](../visualize/lens.md).

## Title and label panels [title-label-panels]

A descriptive panel title is the most important label in the visualization. It explains what the chart shows in one phrase, so the data underneath has a clear answer to point to.

* **Write titles that explain the insight, not the field.** "Requests by response code" reads better than "count by status".
* **Hide redundant axis titles.** Once the panel title makes the X and Y axes obvious, the axis titles repeat what the reader already knows. In the [Lens](../visualize/lens.md) editor, set **Axis title** to **None** for both axes when the panel title is self-explanatory.
* **Don't repeat the same word in every title.** When most panels start with the same prefix (such as "Usage" across eight panels), drop it from each title and put it in the dashboard title or a section header instead.
* **Trim numbers to what readers need.** A KPI tile reads better as `$3.4M` than `$3,364,726`. Round to the magnitude that conveys the change you're tracking, and reserve full precision for tables.
* **Don't use [text panels](../visualize/text-panels.md) as section headers.** They take vertical space without showing data. For section breaks, use [collapsible sections](arrange-panels.md#collapsible-sections) and descriptive panel titles.

## Use color deliberately [use-color]

Color is a strong signal. Use it to encode meaning, not for decoration.

* **Stick to {{product.kibana}}'s built-in palettes.** They're tuned for accessibility, including color-blind safety, and produce a consistent look across dashboards.
* **Reuse the same color for the same dimension across panels.** When a value (a service, a region, a status) appears in multiple panels, give it the same color in each so readers track it without re-orienting. Turn on the dashboard **Sync color palettes across panels** setting to enforce this automatically.
* **Match the palette to the data.** For sequential data (low to high, like usage or counts), use a single-hue gradient that gets darker as values grow. For divergent data (around a meaningful midpoint, like deviation from a target), use a two-color palette with the darkest tones at the extremes.
* **Don't use too many colors in a single panel.** Many distinct colors create noise and make patterns harder to spot. Group categories or use shape and weight to differentiate where you can.
* **For brand-customized dashboards, keep the palette small.** A few brand colors mixed with neutral grays read better, and more accessibly, than a full custom rainbow.

## Apply consistent dashboard settings [dashboard-settings]

A handful of dashboard-wide settings control how the whole dashboard reads. Set them deliberately when you create the dashboard so panels look like they belong together. Find them in the **Settings** menu in the application menu.

* **Use margins between panels.** Margins create visual breathing room and signal which panels belong to the same group. Keep them on for most dashboards.
* **Sync color palettes across panels.** Applies the same color to the same value across every panel. Refer to [](#use-color) for why this matters.
* **Sync cursor across panels** and **Sync tooltips across panels.** When a viewer hovers a time series chart or heatmap, the same point highlights and the same tooltip appears on every related chart. Useful when panels share the same time axis.

For the full list of dashboard settings and where to find them, refer to [Create a dashboard](create-dashboard.md).

## Choose the right panel for the job [choose-panel-type]

A dashboard isn't only charts. {{product.kibana}} offers several panel types. Use them deliberately:

* **Charts** ([Lens](../visualize/lens.md)) form the bulk of most dashboards.
* **[Tables](../visualize/charts/tables.md)** show row-level detail when comparison and lookup matter more than at-a-glance trends.
* **[Filter controls](add-controls.md)** let viewers narrow the dashboard to a subset of the data without editing.
* **[Collapsible sections](arrange-panels.md#collapsible-sections)** group supporting panels and detail tables under a header, so the primary view stays focused. Content inside a collapsed section is loaded on demand, which speeds up the dashboard.
* **[Text panels](../visualize/text-panels.md)** add context, instructions, links, or images. Use them for short paragraphs that explain the dashboard, not as visual section dividers.

## Layout patterns to start from [layout-patterns]

These templates are starting points. Adapt them to your data and your readers.

### Operational dashboard [operational-dashboard]

Best for: system health, real-time monitoring, alerts.

```text
┌──────────┬──────────┬──────────┬──────────┐
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4   │  Status at a glance
├──────────┴──────────┴──────────┴──────────┤
│         Main timeline (trends)            │  Primary metric over time
├───────────────────────┬───────────────────┤
│   Breakdown chart 1   │  Breakdown chart 2│  Drill down by dimension
├───────────────────────┴───────────────────┤
│         Secondary timeline                │  Supporting trends
└───────────────────────────────────────────┘
```

A row of compact KPIs at the top tells viewers whether anything needs attention. The main timeline gives shape to the trend, breakdowns explain it, and a secondary timeline anchors longer-running context.

### Analytical dashboard [analytical-dashboard]

Best for: data analysis, comparisons, deep dives.

```text
┌───────────────────────┬───────────────────┐
│                       │   Filter / summary│
│   Primary analysis    ├───────────────────┤
│   (large chart)       │   Top-N list      │
├───────────────────────┴───────────────────┤
│            Comparison chart               │
├───────────────────────┬───────────────────┤
│   Dimension A         │   Dimension B     │
└───────────────────────────────────────────┘
```

A large primary chart anchors the analysis, with focused summaries and a top-N list grouped alongside. The comparison chart and per-dimension breakdowns let analysts pivot without leaving the dashboard.

### Executive dashboard [executive-dashboard]

Best for: high-level summaries, stakeholder reports.

```text
┌──────────┬──────────┬──────────┬──────────┐
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4   │
├──────────┴──────────┼──────────┴──────────┤
│   Trend chart 1     │    Trend chart 2    │
├─────────────────────┴─────────────────────┤
│           Distribution / breakdown        │
└───────────────────────────────────────────┘
```

KPIs anchor the headline. Two trend charts show direction, and a single distribution panel summarizes the population. Detail belongs in a separate dashboard, accessed through a [drilldown](drilldowns.md).

## Tune dashboard performance [dashboard-performance]

A well-designed dashboard also loads quickly:

* **Restrict the time range.** Time series and aggregations scan more data over longer ranges. Set a default time range that matches the dashboard's primary question.
* **Defer the supporting view.** Place secondary panels and detail tables inside [collapsible sections](arrange-panels.md#collapsible-sections). Content inside a collapsed section is loaded on demand.
* **Split very large dashboards.** Many tens of panels on a single dashboard hurt both performance and scannability. Build focused dashboards and link them with [drilldowns](drilldowns.md).
* **Prefer summaries over raw row scans.** For high-cardinality data, build panels on aggregations or summarized [ES|QL](../query-filter/languages/esql-kibana.md) queries rather than scanning raw documents.

## Related [related]

* [Create a dashboard](create-dashboard.md)
* [Organize dashboard panels](arrange-panels.md)
* [Add filter controls](add-controls.md)
* [Drilldowns](drilldowns.md)
* [Create dashboards programmatically](create-dashboards-programmatically.md)
* [Create dashboards using AI](create-dashboards-using-ai.md)
