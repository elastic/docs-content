A value is missing when its field is `null` or the document doesn't have the field. Instead of leaving the cell empty, {{kib}} shows a placeholder. The placeholder depends on where you see the value.

**In tables**, such as the results table in **Discover** or a table panel on a dashboard, the placeholder also depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` A dash (`-`). Hover over the dash to see `(null)`.
- {applies_to}`stack: ga 9.2-9.5` The label `(null)`.
- {applies_to}`stack: ga 9.0-9.1` A dash (`-`).

**In charts**, the label for a missing category, such as an axis label, a legend entry, or a slice, depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The label `(null)`.
- {applies_to}`stack: ga 9.0-9.1` A dash (`-`) in bar, line, area, heat map, and tag cloud charts, and the label `(empty)` in pie, donut, treemap, mosaic, and waffle charts.

**In CSV files**, the placeholder depends on the kind of file:

- **Formatted CSV** files from a panel or visualization, including files from the **Download CSV** action in a panel menu:
  - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Tables built with the point-and-click editor write a dash (`-`). Charts and other tables, such as aggregation-based data tables, write `(null)`.
  - {applies_to}`stack: ga 9.2-9.5` Tables and charts write `(null)`.
  - {applies_to}`stack: ga 9.0-9.1` Tables and charts write a dash.
- **Raw CSV** files from a panel or visualization write an empty cell.
- **CSV reports from Discover** write a dash (`-`) in classic mode and an empty cell in {{esql}} mode.

To leave missing values out of your results, filter them out:

- In {{esql}}, add `WHERE <field> IS NOT NULL` to your query.
- In KQL, use `<field>: *`.

:::{note}
An empty string (`""`) is a value, not a missing value. Tables and charts show it as a label that depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The label `(blank)`.
- {applies_to}`stack: ga 9.0-9.1` The label `(empty)`.
:::
