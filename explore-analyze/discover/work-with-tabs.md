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

# Run multiple explorations with tabs

**Discover** supports multiple tabs to help you explore different aspects of your data simultaneously. Each tab maintains its own independent state, including the query ({{esql}} or classic mode), time range, filters, selected data source, columns and sort order you defined, and the active [context-aware experience](discover-get-started.md#context-aware-discover).

This allows you to pivot quickly between different explorations without losing your place. For example:

* **Compare time periods:** Open multiple tabs with the same query but different time ranges
* **Test query variations:** Duplicate a tab to experiment with different {{esql}} queries or filters
* **Switch contexts:** Keep separate tabs for logs, metrics, and traces explorations
* **Test a hypothesis:** Switch between different data sources or field combinations

## Manage Discover tabs

You can open new tabs or duplicate existing ones to compare different queries:
- To start a fresh exploration in a new tab, select the {icon}`plus` icon next to the existing tabs. What the new tab does when it opens depends on your version:
  - {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` The tab starts empty. It doesn't run any search until you enter a query and run it.
  - {applies_to}`stack: preview 9.2-9.5` The tab opens on the same data source as the tab you came from and, by default, runs a search right away.
- To test variations of your current query in a new tab, hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Duplicate**.

A session supports a maximum of 25 open tabs. When the limit is reached, the {icon}`plus` icon and **Duplicate** are disabled. You can't add more tabs until you close some.

To manage and organize your tabs, you can:
- Rename them: Double-click its label or hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Rename**.
- Reorder them: Drag a tab to move it.
- Close them: Hover over a tab and select the {icon}`cross` icon.
- Close several tabs at once: When you hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, options let you **Close other tabs** to keep only the active tab open or **Close tabs to the right** to only keep your first tabs and discard any subsequent tabs.

  :::{tip}
  If you want to discard all open tabs, you can also start a {icon}`plus` **New session**/**New** from the application menu. When you use this option, any unsaved changes to your current session are lost.
  :::
- Reopen recently closed tabs: If you close a tab by mistake, you can retrieve it by selecting the {icon}`arrow_down` **Tabs menu** icon located at the end of the tab bar.
  - {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` Tabs closed at the same time (for example, when navigating away from Discover) are grouped together in the {icon}`arrow_down` **Tabs menu**. You can expand a group to view the individual tabs, restore a specific tab, or restore all tabs in the group at once. If restoring a group would exceed the 25-tab limit, only the first tabs in the group are restored up to the remaining capacity.

To keep all your tabs for later, you can [save your Discover session](save-open-search.md). All currently open tabs are saved within the session and will be there when you open it again.

## Related pages

- [Save a Discover session for reuse](save-open-search.md)
- [Introduction to Discover](discover-get-started.md)
