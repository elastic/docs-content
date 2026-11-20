A value is missing when its field is `null` or the document doesn't have the field. Instead of leaving the cell empty, {{kib}} shows a placeholder.


::::{applies-switch}

:::{applies-item} {serverless: ga, stack: "ga 9.6+"}

The placeholder matches the visualization that shows the value:

| Where you see the value | What you see |
|---|---|
| **Tables**, such as the results table in **Discover** or a table panel on a dashboard | A dash (`-`). Hover over the dash to see `(null)`. |
| **Charts**, for a missing category such as an axis label, a legend entry, or a slice | `(null)` |

The same placeholder carries over to the data in [the Inspector](/explore-analyze/dashboards/using.md#view-and-download-the-data-in-visualizations) and to formatted CSV files, including the files from the **Download CSV** action in a panel menu.

**Raw CSV** files are unformatted on purpose. A missing value is an empty cell.

**CSV reports** from **Discover** in classic mode use the same formatting as the table, so a missing value is a dash (`-`). In {{esql}} mode, the report exports raw values, and a missing value is an empty cell.

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
