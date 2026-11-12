A value is missing when its field is `null` or the document doesn't have the field. Instead of leaving the cell empty, {{kib}} shows a placeholder. The placeholder depends on where you see the value.

**In tables**, such as the results table in **Discover** or a table panel on a dashboard, the placeholder also depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` A dash (`-`). Hover over the dash to see `(null)`.
- {applies_to}`stack: ga 9.2-9.5` The label `(null)`.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` **In charts**, a missing value shows as the label `(null)`.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` **Empty strings** (`""`) are values, not missing values. Tables and charts show them as the label `(blank)`.

You can't change the placeholder, but you can filter missing values out of your results:

- In {{esql}}, add `WHERE <field> IS NOT NULL` to your query.
- In KQL, use `<field>: *`.
