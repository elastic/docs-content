---
navigation_title: Switch query mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Switch Discover between ES|QL and classic mode, and see what happens to your query and filters.
---

# Switch between {{esql}} and classic mode

**Discover** has two query modes: {{esql}}, and classic mode, which uses data views with Kibana Query Language (KQL) or Lucene. 

This page explains how to switch between modes, and what Discover does with your queries when you switch.

## Before you begin

- You need an open **Discover** session. If you are new to {{esql}} mode, start with [Get started with {{esql}} in Discover](try-esql.md).
- Switching modes applies to the selected tab of your Discover session only. To switch multiple tabs to a different mode, you must repeat the operation for each.

## Switch to Discover's {{esql}} mode [switch-discover-query-mode]

When switching from classic mode to {{esql}} mode, Discover converts the existing KQL or Lucene query as follows:

- The query text becomes an {{esql}} query with a `WHERE KQL("<your query text")` clause.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Active filters from the filter bar become `WHERE` clauses where possible. Filters that can't be converted, such as scripted filters, are dropped.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the data view has a time field, Discover adds `SORT` on that field so the newest records appear first. Converted `WHERE` conditions stay in the query.

To switch:

1. Open the Discover tab you want to switch.

2. Switch from either location:

   - {icon}`code` **Query in ES|QL** (**ES|QL** or **Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **Switch to ES|QL** in the contextual menu ({icon}`boxes_vertical`) of the active Discover tab. This affects only that tab.

**Result:** The tab changes to {{esql}} mode. If a KQL or Lucene query exists, Discover converts it and runs it.

## Switch to Discover's classic mode [revert-to-classic-mode]

When switching from {{esql}} mode to classic mode, Discover drops the {{esql}} query and keeps the data you were querying:

- Classic mode opens with an empty KQL query. A KQL or Lucene query that Discover converted when you switched to {{esql}} is not restored.
- The data view is the one for the index pattern in the {{esql}} query. A saved data view you selected before that switch is not selected again.
- If the data view has a time field, Discover sorts on that field so the newest records appear first.
- The time range and refresh interval stay unchanged.

To switch:

:::::{applies-switch}

::::{applies-item} {serverless:, stack: ga 9.4+ }
1. Open the Discover tab that you want to switch to classic mode.

2. Switch the active tab from either location:

   - From the tab's contextual menu ({icon}`boxes_vertical`), select **Switch to classic**.
   - From the application menu, select **Switch to Classic**.

   This affects only the active Discover tab.

:::{tip}
The contextual menu **Switch to classic** option only appears for the currently active tab. To see it for another tab, you must load that tab first.
:::
::::

::::{applies-item} stack: ga 9.2-9.3
From the application menu, select **Switch to classic**. This only affects your current Discover tab.
::::

::::{applies-item} stack: ga 9.0-9.1
From the application menu, select **Switch to classic**.
::::

:::::

**Result:** The tab opens in classic mode with an empty KQL query, on the data view for the index pattern you were querying.

## Next steps

- [Browse data sources and fields from the {{esql}} editor in Discover](browse-esql-sources.md)
- [Work with {{esql}} results in Discover](esql-results.md)

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Explore fields and data with Discover](discover-get-started.md)
