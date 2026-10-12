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

When you write a query in {{esql}} mode, the editor includes two browsers that help you find the data sources and field names you can use.

## Before you begin

- Make sure you're using **Discover**'s {{esql}} mode and that the editor is visible. If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).

## Find a data source or field [discover-esql-resource-browsers]

The browsers are:

- **Data source browser**: lists the data sources of the following types that you can query: **Alias**, [**External data**](elasticsearch://reference/query-languages/esql/esql-data-federation.md), **Index**, **Integration**, **Lookup Index**, **Stream**, **Timeseries**, and [**View**](elasticsearch://reference/query-languages/esql/esql-views.md). The browser supports multi-select: you can add or remove several sources in one session, and sources already present in your query appear preselected. The browser inserts your selections into the `FROM` or `TS` command and keeps the existing sources. When the query starts with `TS`, only time series data sources are listed.
- **Fields browser**: lists fields for the data sources in your query and lets you insert one field at a time at the cursor position.

:::{note}
:applies_to: { stack: preview 9.4-9.5 }
[{{esql}} views](elasticsearch://reference/query-languages/esql/esql-views.md) aren't shown in the data source browser but they're visible through the autocomplete menu suggestions.
:::

1. In the {{esql}} editor, put the cursor where the name belongs. For a data source, edit a `FROM` or `TS` command. For a field, edit a position that accepts a field name, for example, after `KEEP`, `WHERE`, or `SORT`.

2. Open the browser from either location:

   - **The autocomplete menu**: select **Browse data sources** when you edit a `FROM` or `TS` command, or **Browse fields** when you edit a field position.
   - **The data source badge**: the editor shows the first `FROM` or `TS` keyword in the query as a badge. Select it to open the data source browser.

3. Select the data sources or the field you want to insert.

Both browsers operate on the main query only and don't apply to subqueries.

**Result:** The editor inserts the sources into `FROM` or `TS`, or inserts the field at the cursor.

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Work with {{esql}} results in Discover](esql-results.md)
- [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md)
