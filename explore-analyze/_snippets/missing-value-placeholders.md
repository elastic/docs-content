A value is missing when its field is `null` or the document doesn't have the field. Instead of leaving the cell empty, {{kib}} shows a placeholder. The placeholder depends on where you see the value.

**In tables**, such as the results table in **Discover** or a table panel on a dashboard, the placeholder also depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` A dash (`-`). Hover over the dash to see `(null)`.
- {applies_to}`stack: ga 9.2-9.5` The label `(null)`.
- {applies_to}`stack: ga 9.0-9.1` A dash (`-`).

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` **In charts**, a missing value shows as the label `(null)`.

**Empty strings** (`""`) are values, not missing values. Tables and charts show them as a label that depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` `(blank)`
- {applies_to}`stack: ga 9.0-9.1` `(empty)`

**In CSV files**, the placeholder depends on the kind of file:

- **Formatted CSV** files from a panel or visualization, including files from the **Download CSV** action in a panel menu:
  - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Tables write a dash (`-`) and charts write `(null)`.
  - {applies_to}`stack: ga 9.2-9.5` Tables and charts write `(null)`.
  - {applies_to}`stack: ga 9.0-9.1` Tables and charts write a dash (`-`).
- **Raw CSV** files from a panel or visualization write an empty cell.
- **CSV reports from Discover** write a dash (`-`) in classic mode and an empty cell in {{esql}} mode.

You can't change the placeholder, but you can filter missing values out of your results:

- In {{esql}}, add `WHERE <field> IS NOT NULL` to your query.
- In KQL, use `<field>: *`.
