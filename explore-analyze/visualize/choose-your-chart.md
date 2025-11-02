---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/chart-types.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Choose your chart [choose-your-chart]

Use this guide to pick the most effective visualization. 

## How do I choose?
 
### OPTION A

**I want to visualize trend in time**

| My data | My goal | Best choice | Why | 
| --- | --- | --- | --- | 
| I have one data series  |  I want to track time-based changes to quickly spot issues rather than perform detailed analysis.  | Line chart, Bar chart | Ideal for spotting small changes day‑to‑day changes (or across any time period).  |
|                         |  I want to show overall intensity             | Heatmap           | Great for quickly assessing periods of high vs. low activity. |
| I have more data series |  I want to show differences among data series | Line chart, Grouped Bar chart, Heatmap        | Keeping lines close or bars grouped enables quick, across-series comparison. |
|                         |  I want to show the sum of the data series    | Stacked Bar chart, Area chart  | Ideal for aggregating values into a single total to see overall behavior. |

**I have one or more values to display**

| My data | My goal | Best choice | Why |
| ----------------------- | ----------------------------------------------| ----------------- | --- | 
| I have one value        |  I want to display a single value             | Metric chart, Bullet      |  Ideal for showing a single value, for example a KPI. To compare against targets, consider a Gauge in bullet style.  |
| I have more values      |  I want to display the sum of the values as part of something     | Bar chart        | Great for fast comparison and clear ranking across series |
|                         |  I want to show their cumulative value        | Treemap chart, Pie chart, Single Stacked bar chart      | Also called “part‑to‑whole” charts, they show how an item compares to, and contributes to, the whole.

### OPTION B

| **Chart type** | **Use when you want to...** |
| --- | --- |
| Line chart | Show how a metric changes over time or another continuous dimension. |
| Area chart | Show change over time while emphasizing cumulative magnitude or part-to-whole stacking. |
| Bar chart | Compare values across discrete categories or show distributions with histogram buckets. |
| Metric chart | Highlight a single KPI or a small set of critical numbers. |
| Table chart | Present precise values, rankings, or multi-metric details in a compact layout. |
| Pie chart | Show simple part-to-whole composition with a small number of categories (generally ≤ 5). |
| Treemap chart | Visualize hierarchical part-to-whole across categories and subcategories. |
| Mosaic chart | Compare part-to-whole across two categorical dimensions in a tiled layout. |
| Gauge chart | Show progress toward a target or status against thresholds for a single metric. |
| Heat map chart | Reveal patterns by magnitude across two binned dimensions using color. |
| Region chart | Show geospatial patterns by coloring regions based on aggregated values (choropleth). |
| Waffle chart | Show part-to-whole as a grid of equal cells where filled cells represent proportion. |
| Tag cloud chart | Emphasize the most frequent terms; font size reflects relative magnitude. |
| Legacy metric chart | Maintain existing legacy panels; prefer the modern Metric chart for new visuals. |

## Best practices

- Keep composition simple
  - Prefer Donut/Pie only with a few categories; otherwise use Treemap, Waffle, or Bar.
- Customize the appearance
  - Adjust the appearance options as suggested in [Customize the visualization display](./lens.md#configure-the-visualization-components)
- Be thoughtful with color
  - Use consistent, meaningful color mapping for categories. Check [Assign colors to terms](./lens.md#assign-colors-to-terms).
- Mind accessibility
  - Ensure contrast and avoid relying on color alone to convey meaning.
- Show uncertainty and gaps appropriately
  - For time series, choose how to handle missing values. See options in [Visualization appearance](./lens.md#customize-visualization-appearance).
- Choose the right level of precision
  - Use Tables for exact values; use charts to reveal patterns and trends at a glance.

## Next steps in Lens

Create and refine a visualization: [Create visualizations](./lens.md#create-the-visualization-panel)


