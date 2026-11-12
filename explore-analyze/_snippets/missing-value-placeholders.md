A value is missing when its field is `null` or the document doesn't have the field. Instead of leaving the cell empty, {{kib}} shows a placeholder. The placeholder depends on where you see the value and on your version. Select the tab for your version.

:::{note}
An empty string (`""`) is a value, not a missing value. Tables and charts show it as a label that depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The label `(blank)`.
- {applies_to}`stack: ga 9.0-9.1` The label `(empty)`.
:::

::::{applies-switch}

:::{applies-item} {serverless: ga, stack: "ga 9.6+"}

| Where you see the value | What you see |
|---|---|
| Tables, such as the results table in **Discover** or a table panel on a dashboard | A dash (`-`). Hover over the dash to see `(null)`. |
| Chart categories, such as an axis label, a legend entry, or a slice | The label `(null)` |
| **Formatted CSV** files from tables that you build with the point-and-click editor or an {{esql}} query | A dash (`-`) |
| **Formatted CSV** files from charts and other visualizations | The label `(null)` |
| **Raw CSV** files from a panel or visualization | An empty cell |
| CSV reports from **Discover** | A dash (`-`) in classic mode, and an empty cell in {{esql}} mode |

:::

:::{applies-item} stack: ga 9.2-9.5

| Where you see the value | What you see |
|---|---|
| Tables, such as the results table in **Discover** or a table panel on a dashboard | The label `(null)` |
| Chart categories, such as an axis label, a legend entry, or a slice | The label `(null)` |
| **Formatted CSV** files from tables and charts | The label `(null)` |
| **Raw CSV** files from a panel or visualization | An empty cell |
| CSV reports from **Discover** | A dash (`-`) in classic mode, and an empty cell in {{esql}} mode |

:::

:::{applies-item} stack: ga 9.0-9.1

| Where you see the value | What you see |
|---|---|
| Tables, such as the results table in **Discover** or a table panel on a dashboard | A dash (`-`) |
| Chart categories, such as an axis label, a legend entry, or a slice | A dash (`-`) in bar, line, area, heat map, and tag cloud charts, and the label `(empty)` in pie, donut, treemap, mosaic, and waffle charts |
| **Formatted CSV** files from tables and charts | A dash (`-`) |
| **Raw CSV** files from a panel or visualization | An empty cell |
| CSV reports from **Discover** | A dash (`-`) in classic mode, and an empty cell in {{esql}} mode |

:::

::::

The **Download CSV** action in a panel menu produces a formatted CSV file.

To leave missing values out of your results, filter them out:

- In {{esql}}, add `WHERE <field> IS NOT NULL` to your query.
- In KQL, use `<field>: *`.
