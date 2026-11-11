---
navigation_title: Work with tabs
applies_to:
  serverless: preview
  stack: preview 9.2
products:
  - id: kibana
type: how-to
description: Run several explorations side by side in Discover tabs, then open, duplicate, rename, reorder, close, and restore tabs as you work.
---

# Run multiple explorations with tabs in Discover

If you want to compare two queries, or keep one exploration while you try another, open each one in its own tab. Each tab keeps its own query ({{esql}} or classic mode), time range, filters, {{data-source}}, columns, sort order, and the layout that **Discover** [adapts to your data](discover-get-started.md#context-aware-discover). You can switch between tabs without losing your place.

For example, you can:

* **Compare time periods:** Open multiple tabs with the same query but different time ranges.
* **Test query variations:** Duplicate a tab to try different {{esql}} queries or filters.
* **Switch contexts:** Keep separate tabs for logs, metrics, and traces explorations.
* **Test a hypothesis:** Switch between different data sources or field combinations.

## Before you begin

Open **Discover**. To keep your tabs for later, you also need the privilege to save Discover sessions. Refer to [Save and manage Discover sessions](save-open-search.md#save-search-requirements).

## Open a tab [open-tab]

1. To start a fresh exploration, select the {icon}`plus` icon next to the existing tabs. What the new tab does when it opens depends on your version:
   - {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` The tab starts without results. In classic mode, it keeps your current {{data-source}}. In {{esql}} mode, it starts with an empty query, and **Discover** offers recommended queries for you to start from. It doesn't run any search until you run a query, and auto-refresh stays paused.
   - {applies_to}`stack: preview 9.2-9.5` The tab opens on the same data source as the tab you came from and, by default, runs a search right away.
2. To test variations of your current query instead, hover over a tab, select the {icon}`boxes_vertical` **Actions** icon, then select **Duplicate**.

**Result:** The new tab appears in the tab bar and becomes the active tab.

You can have up to 25 tabs open at once. When you reach the limit, the {icon}`plus` icon and **Duplicate** disappear until you close a tab. Restoring closed tabs is also unavailable until then.

If you open a background search from **Discover**, it opens in a new tab and counts toward the same limit. Refer to [Run Discover and Dashboards queries in the background](background-search.md).

## Rename, reorder, and close tabs [manage-tabs]

To keep your tabs organized:

- To rename a tab, double-click its label, or hover over the tab, select the {icon}`boxes_vertical` **Actions** icon, then select **Rename**.
- To reorder tabs, drag a tab to a new position.
- To close a tab, hover over it and select the {icon}`cross` icon.
- To close several tabs at once, hover over a tab, select the {icon}`boxes_vertical` **Actions** icon, then select **Close other tabs** to keep only the tab you opened the menu on. To close every tab after that tab, select **Close tabs to the right**.

  :::{tip}
  To start over, select {icon}`plus` **New session** in the application menu. **Discover** closes all open tabs and moves them to the **Recently closed** list in the **Tabs menu**. You can [restore them](#reopen-tab) later, and they join your new session.
  :::

## Reopen a closed tab [reopen-tab]

If you close a tab by mistake, you can get it back. **Discover** keeps the last 50 closed tabs in your browser.

1. Open the **Tabs menu** at the end of the tab bar.
2. In the **Recently closed** list, select the tab to restore.

   {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4` Tabs that close together appear as one group in the **Tabs menu**. Tabs close together when you use **Close other tabs** or **Close tabs to the right**, start a new session, or open another **Discover** session. Expand a group to restore a specific tab, or restore all tabs in the group at once. If restoring a group would exceed the 25-tab limit, **Discover** restores the first tabs in the group, up to the remaining capacity, and shows a warning.

**Result:** The tab reappears in the tab bar.

## Next steps

- [Save and manage Discover sessions](save-open-search.md): To keep all your tabs for later, save the session. All open tabs are saved with it, and they are there when you open it again.

## Related pages

- [How Discover works](discover-get-started.md)
