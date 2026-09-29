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

**Discover** has two query modes: {{esql}} mode and classic mode. Classic mode uses data views with Kibana Query Language (KQL) or Lucene.

This page explains how to switch between modes, and what Discover does with your queries when you switch.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Discover remembers the last query mode you used in your browser. New Discover tabs and sessions open in that mode.

## Before you begin

- Open **Discover**. If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2+` Switching modes applies only to the selected Discover tab. To switch several tabs, repeat the operation for each tab.

## Switch to Discover's {{esql}} mode [switch-discover-query-mode]

When switching from classic mode to {{esql}} mode, Discover converts the existing KQL or Lucene query as follows:

- A KQL query becomes a `WHERE KQL("""<your query text>""")` clause, and a Lucene query becomes a `WHERE QSTR("""<your query text>""")` clause.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Active filters from the filter bar become `WHERE` clauses where possible. Discover drops filters that it can't convert, such as scripted filters.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the data view has a time field, Discover adds `SORT` on that field so the newest records appear first. Converted `WHERE` conditions stay in the query.

To switch:

1. Open the Discover tab you want to switch.

2. Switch from either location:

   - {icon}`code` **Query in ES|QL** (**Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **Switch to ES|QL** in the {icon}`boxes_vertical` contextual menu of the active Discover tab. This affects only that tab.

**Result:** The tab changes to {{esql}} mode. If a KQL or Lucene query exists, Discover converts it and runs it.

## Switch to Discover's classic mode [revert-to-classic-mode]

When switching from {{esql}} mode to classic mode, Discover drops the {{esql}} query and keeps the data you were querying:

- Classic mode opens with an empty KQL query. Discover doesn't restore a KQL or Lucene query that it converted when you switched to {{esql}}.
- The data view is the one for the data source in the `FROM` command of the {{esql}} query. Discover doesn't reselect a saved data view that you used before switching to {{esql}}.
- If the data view has a time field, Discover sorts on that field so the newest records appear first.
- The time range and refresh interval stay unchanged.

To switch:

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: ga 9.4+ }
1. Open the Discover tab that you want to switch to classic mode.

2. Switch the active tab from either location:

   - From the tab's {icon}`boxes_vertical` contextual menu, select **Switch to classic**.
   - From the application menu, select **Switch to Classic**.

   This affects only the active Discover tab.

:::{tip}
The contextual menu **Switch to classic** option appears only for the active tab. To see it for another tab, you must load that tab first.
:::
::::

::::{applies-item} stack: ga 9.2-9.3
From the application menu, select **Switch to classic**. This affects only your current Discover tab.
::::

::::{applies-item} stack: ga 9.0-9.1
From the application menu, select **Switch to classic**.
::::

:::::

**Result:** The tab opens in classic mode with an empty KQL query, on the data view for the data source you were querying.

## Next steps

- [Browse data sources and fields from the {{esql}} editor in Discover](browse-esql-sources.md)
- [Work with {{esql}} results in Discover](esql-results.md)

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Explore fields and data with Discover](discover-get-started.md)
