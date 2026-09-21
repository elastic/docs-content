---
navigation_title: Switch query mode
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
description: Switch Discover between ES|QL and classic mode, and see what happens to your query, filters, and the mode Discover opens next.
---

# Switch between {{esql}} and classic mode

**Discover** has two query modes: {{esql}}, and classic mode, which uses data views with Kibana Query Language (KQL) or Lucene. Switch when you want the query to select the data, or when you want the data view and filter bar back. This page explains what Discover does with the query you already have.

## Before you begin

- You need a **Discover** session. If you are new to {{esql}} mode, start with [Get started with {{esql}} in Discover](try-esql.md).

## Switch to {{esql}} [switch-discover-query-mode]

1. Open the Discover tab you want to switch.

2. Switch from either location:

   - {icon}`code` **Query in ES|QL** (**ES|QL** or **Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` **Switch to ES|QL** in the contextual menu ({icon}`boxes_vertical`) of the active Discover tab. This affects only that tab.

If you've entered a KQL or Lucene query in classic mode, Discover converts it to {{esql}} when you switch:

- The query text becomes an {{esql}} query.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Active filters from the filter bar become `WHERE` clauses where possible.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Filters that can't be converted, such as scripted filters, are dropped.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Discover remembers the query mode you last used. A new Discover session opens in that mode.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` By default, Discover derives your starting query from your data sources. Administrators can set a different starting query for the space with the [**Default ES|QL query** (`discover:defaultEsqlQuery`)](kibana://reference/advanced-settings.md#kibana-discover-settings) setting. This setting doesn't apply after you edit the query or switch query modes.

**Result:** The tab opens in {{esql}} mode. A KQL or Lucene query you had already entered is converted into the {{esql}} editor.

## Revert to Discover's classic mode [revert-to-classic-mode]

You can go back to the classic data view and KQL mode in Discover at any time. When you switch from {{esql}} mode to classic mode, Discover discards the {{esql}} query, including one it built by converting KQL or Lucene, and opens classic mode with an empty KQL query.

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

**Result:** The tab opens in classic mode with an empty KQL query. The {{esql}} query is gone.

## Next steps

- [Browse data sources and fields from the editor](browse-esql-sources.md)
- [Work with {{esql}} results in Discover](esql-results.md)

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Explore fields and data with Discover](discover-get-started.md)
