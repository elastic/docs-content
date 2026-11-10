A value is missing when its field is `null` or the document doesn't have the field. {{kib}} then shows a placeholder instead of leaving the cell empty. In a table, such as the results table in **Discover** or a table panel on a dashboard, the placeholder depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` A dash (`-`). Hover over the dash to see `(null)`.
- {applies_to}`stack: ga 9.2-9.5` The label `(null)`.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Charts show `(null)` for a missing value. Tables and charts show `(blank)` for an empty string (`""`), which is a value that exists but has no characters.

You can't change the placeholder, but you can leave missing values out of your results by filtering them out. In {{esql}}, add `WHERE <field> IS NOT NULL` to your query. In KQL, use `<field>: *`.
