---
navigation_title: Browse data sources
applies_to:
  serverless: ga
  stack: ga 9.4+
products:
  - id: kibana
type: how-to
description: Browse data sources and fields from the ES|QL editor in Discover, and insert them into your query.
---

# Browse data sources and fields from the {{esql}} editor in Discover

If you don't remember the exact name of an index or field, the {{esql}} editor can list them for you and insert your pick into the query. In **Discover**, the editor includes two browsers for this: one for data sources, which are the indices and other places a query reads from, and one for fields.

## Before you begin

- Make sure **Discover** is in {{esql}} mode. Classic mode doesn't support this functionality. To switch, refer to [Switch to Discover's {{esql}} mode](switch-esql-mode.md#switch-discover-query-mode).
- If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).

## Find a data source or field [discover-esql-resource-browsers]

The browsers are:

- **Data source browser**: Lists the data sources you can query in one list, with the type of each source next to its name. To narrow the list, search by name or filter by type. The types are **Alias**, **Index**, **Integration**, **Lookup Index**, **Stream**, and **Timeseries**, plus the following types when your deployment supports them:
  - {applies_to}`stack: ga 9.6+` [**View**](elasticsearch://reference/query-languages/esql/esql-views.md): The browser lists views only if your role can read {{esql}} views.
  - {applies_to}`stack: preview 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` [**External data**](elasticsearch://reference/query-languages/esql/esql-data-federation.md): The browser lists the datasets that {{esql}} data federation provides.

  You can add or remove several sources in one session, and sources already in your query appear preselected. The browser inserts your selections into the `FROM` or `TS` command, which sets the data your query reads, and keeps the existing sources. When the query starts with `TS`, the browser lists only time series data sources.
- **Fields browser**: Lists the fields that are available at the cursor position, including fields that earlier commands in the query create, and inserts one field at a time at the cursor position.

:::{note}
:applies_to: { stack: preview 9.4-9.5 }
In these versions, [{{esql}} views](elasticsearch://reference/query-languages/esql/esql-views.md) don't appear in the data source browser. They still appear in the autocomplete menu suggestions.
:::

1. In the {{esql}} editor, put the cursor where the name belongs. For a data source, edit a `FROM` or `TS` command. For a field, edit a position that accepts a field name, for example, after `KEEP`, `WHERE`, or `SORT`.

2. Open the browser from either location:

   - **The autocomplete menu**: Select **Browse data sources** when you edit a `FROM` or `TS` command, or **Browse fields** when you edit a field position.
   - **The data source badge**: The editor shows the first `FROM` or `TS` keyword in the query as a badge. Select it to open the data source browser.

3. Select the data sources or the field you want to insert.

**Result:** The editor inserts the sources into `FROM` or `TS`, or inserts the field at the cursor.

The browsers work on the main query, not on a query nested inside another.

## Related pages

- [How to query in Discover's {{esql}} mode](use-esql.md)
- [Work with {{esql}} results in Discover](esql-results.md)
- [](../query-filter/languages/esql-kibana.md)
