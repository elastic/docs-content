A value is missing when its field is `null` or the document doesn't have the field. Instead of leaving the cell empty, {{kib}} shows a placeholder. The placeholder depends on your version. Select the tab for your version.

:::{note}
An empty string (`""`) is a value, not a missing value. How tables and charts show it depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Shown as `(blank)`.
- {applies_to}`stack: ga 9.0-9.1` Shown as `(empty)`.
:::

::::{applies-switch}

:::{applies-item} {serverless: ga, stack: "ga 9.6+"}

The placeholder matches the visualization that shows the value:

- **Tables**, such as the results table in **Discover** and table panels on a dashboard: Shown as a dash (`-`). Hover over the dash to see `(null)`.
- **Charts**, for a missing category such as an axis label, a legend entry, or a slice: Shown as the label `(null)`.

The same placeholder carries over to the data in [the Inspector](/explore-analyze/dashboards/using.md#view-and-download-the-data-in-visualizations) and to formatted CSV files, including the files from the **Download CSV** action in a panel menu. Tables that you build with the point-and-click editor or an {{esql}} query keep the dash. Charts and other visualizations use `(null)`.

**Raw CSV** files are unformatted on purpose, so a missing value is an empty cell. CSV reports from **Discover** write a dash (`-`) in classic mode and an empty cell in {{esql}} mode.

:::

:::{applies-item} stack: ga 9.2-9.5

Tables, charts, [the Inspector](/explore-analyze/dashboards/using.md#view-and-download-the-data-in-visualizations), and formatted CSV files show the label `(null)`.

**Raw CSV** files write an empty cell. CSV reports from **Discover** write a dash (`-`) in classic mode and an empty cell in {{esql}} mode.

:::

:::{applies-item} stack: ga 9.0-9.1

Tables, [the Inspector](/explore-analyze/dashboards/using.md#view-and-download-the-data-in-visualizations), and formatted CSV files show a dash (`-`). Charts show a dash in bar, line, area, heat map, and tag cloud charts, and the label `(empty)` in pie, donut, treemap, mosaic, and waffle charts.

**Raw CSV** files write an empty cell. CSV reports from **Discover** write a dash (`-`) in classic mode and an empty cell in {{esql}} mode.

:::

::::

To leave missing values out of your results, filter them out:

- In {{esql}}, add `WHERE <field> IS NOT NULL` to your query.
- In KQL, use `<field>: *`.
