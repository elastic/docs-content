---
navigation_title: Switch query mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Switch Discover between ES|QL and classic mode, and see what happens to your query and filters when you do.
---

# Switch between {{esql}} and classic mode in Discover

**Discover** has two query modes. In {{esql}} mode, you write a query in [{{esql}}](elasticsearch://reference/query-languages/esql.md), the {{es}} query language, and the query names the data to explore. In classic mode, you select a [data view](../find-and-organize/data-views.md), which is a definition of the data to query that you usually save, then search it with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md) and narrow the results with filters.

You can switch between the two modes at any time. When you move to {{esql}} mode, **Discover** converts your KQL or Lucene search into an {{esql}} query. When you move back to classic mode, you keep the data you were querying but start with an empty search.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Each tab keeps its own mode, so tabs in the same **Discover** session can use different modes.

## Before you begin

- Open **Discover**. If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).
- Switching modes applies only to the selected [Discover tab](work-with-tabs.md). To switch several tabs, repeat the operation for each tab.

The mode that Discover opens in by default depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Discover opens in {{esql}} mode.
- {applies_to}`stack: ga 9.0-9.5` Discover opens in classic mode.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Discover remembers the last query mode you used in your browser. New Discover sessions open in that mode, and a new tab opens in the same mode as the tab you opened it from.

The switch controls, and {{esql}} as the default mode, depend on the **Enable ES|QL** advanced setting (`enableESQL`), which is on by default. When you open **Discover** from a link or a saved session, it opens in the mode that the link or session uses.

## Switch to Discover's {{esql}} mode [switch-discover-query-mode]

When you switch from classic mode to {{esql}} mode, Discover builds an {{esql}} query from your data view, your search, and your filters. The switch also clears the filter bar, including pinned filters, and resets the selected columns and the sort. The query changes as follows:

- A KQL query becomes a `WHERE KQL("""<your query text>""")` clause, and a Lucene query becomes a `WHERE QSTR("""<your query text>""")` clause.
- If the data view uses a time field and has no `@timestamp` field, the query also gets a `WHERE` condition on the time field that uses `?_tstart` and `?_tend`. These parameters hold the start and end of the time range, so the time range keeps applying.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Active and pinned filters become `WHERE` clauses where possible. Discover leaves out filters that are turned off, and it drops filters that have no {{esql}} equivalent, such as scripted filters. Discover doesn't tell you which filters it dropped.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the data view has a time field, Discover adds `SORT` on that field so the newest records appear first. The `SORT` comes right after the source command, before any converted `WHERE` conditions, which stay in the query.
- The source command and the row limit depend on your version:

  - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Discover starts the query with `TS` instead of `FROM` only for a time series data view with no search or filters.
  - {applies_to}`stack: ga 9.3-9.5` For a time series data view, the query starts with `TS` instead of `FROM`.
  - {applies_to}`stack: ga 9.0-9.1` The query ends with `| LIMIT 10`.

To switch:

1. Open the Discover tab you want to switch.

2. Switch from either location:

   - {icon}`code` **Query in ES|QL** (**Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **Switch to ES|QL** in the {icon}`boxes_vertical` contextual menu of the active Discover tab. This affects only that tab.

**Result:** The tab changes to {{esql}} mode. If a KQL or Lucene query exists, Discover converts it and runs it.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` If the tab hasn't run a search yet, Discover shows recommended queries that you can run as a starting point.

## Switch to Discover's classic mode [revert-to-classic-mode]

When you switch from {{esql}} mode to classic mode, Discover drops the {{esql}} query and keeps the data you were querying:

- Classic mode opens with an empty KQL query and no filters. Discover doesn't restore the search or filters that it converted when you switched to {{esql}}.
- If the data view has a time field, the table sorts on that field, with the newest records first by default. The **Default sort direction** advanced setting controls the direction.
- The selected columns reset.
- The time range and refresh interval stay unchanged.

Which data view classic mode opens on depends on your version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Discover uses the saved data view whose index pattern matches the data source in the `FROM` command of the {{esql}} query. If no saved data view matches, it creates a temporary data view for that data source.
- {applies_to}`stack: ga 9.0-9.5` Discover uses the data view that the tab was using.

To switch:

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: ga 9.4+ }
1. Open the Discover tab that you want to switch to classic mode.

2. Switch the active tab from either location:

   - From the tab's {icon}`boxes_vertical` contextual menu, select **Switch to classic**.
   - From the application menu, select **Switch to Classic**.

   This affects only the active Discover tab.

:::{tip}
The contextual menu shows **Switch to classic** and **Switch to ES|QL** only for the active tab. To see the option for another tab, select that tab to make it the active tab.
:::
::::

::::{applies-item} stack: ga 9.0-9.3
From the application menu, select **Switch to classic**.
::::

:::::

{applies_to}`stack: ga 9.0-9.5` If the session is unsaved, or the tab has unsaved changes, Discover first opens an **Unsaved changes** window. It warns that switching removes the current {{esql}} query. Select **Save and switch** to save the session first, or **Discard and switch** to continue without saving. The window also has a checkbox that stops it from opening again.

**Result:** The tab opens in classic mode with an empty KQL query, on the data you were querying.

## Next steps

- [Browse data sources and fields from the {{esql}} editor in Discover](browse-esql-sources.md)
- [Work with {{esql}} results in Discover](esql-results.md)
- [How to query in Discover's classic mode](use-classic-mode.md)

## Related pages

- [How to query in Discover's {{esql}} mode](use-esql.md)
- [How Discover works](discover-get-started.md)
