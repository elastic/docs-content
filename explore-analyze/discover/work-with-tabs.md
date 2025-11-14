---
navigation_title: Work with tabs
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html#discover-tabs
applies_to:
  stack: preview 9.2
  serverless: preview
products:
  - id: kibana
description: Work with multiple tabs in Discover to explore different aspects of your data simultaneously. Each tab maintains independent queries, filters, and views.
---

# Work with multiple tabs in Discover [discover-tabs]

Use multiple tabs in **Discover** to run different explorations simultaneously. Each tab maintains its own independent query, filters, time range, and view settings, letting you compare different queries, test variations, or monitor multiple data streams without losing your work.

## What's preserved in each tab

Each tab maintains:

* Query mode ({{esql}} or classic mode)
* Query text and filters
* Time range
* Selected data source
* Columns and sort order in the document table
* Active [context-aware experience](context-aware-discover.md)

This independence means you can have completely different explorations running side by side, each tailored to a specific question or investigation.

## Common use cases

Multiple tabs are particularly useful for:

* **Compare time periods**: Open multiple tabs with the same query but different time ranges to see how patterns change over time
* **Test query variations**: Duplicate a tab to experiment with different {{esql}} queries or filters without losing your original work
* **Switch contexts**: Keep separate tabs for logs, metrics, and traces explorations, each with its specialized interface
* **Test hypotheses**: Switch between different data sources or field combinations to compare approaches
* **Monitor multiple data streams**: Track different aspects of your system simultaneously

## Create and open tabs

**Start a new exploration**
: Select the {icon}`plus` icon next to the existing tabs to open a fresh tab with default settings.

**Duplicate an existing tab**
: Hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Duplicate**. This creates a new tab with all the settings from the current tab, perfect for testing variations.

## Manage tabs

**Rename a tab**
: Double-click the tab label, or hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Rename**. Give your tabs meaningful names to track different investigations.

**Reorder tabs**
: Drag and drop a tab to move it to a new position in the tab bar. Organize your tabs in the order that makes sense for your workflow.

**Close a tab**
: Hover over a tab and select the {icon}`cross` icon.

**Close multiple tabs at once**
: Hover over a tab and select the {icon}`boxes_vertical` **Actions** icon for options to:
  * **Close other tabs** - Keep only the active tab open
  * **Close tabs to the right** - Keep your first tabs and discard subsequent tabs

**Start fresh**
: Select {icon}`plus` **New session** from the toolbar to discard all open tabs and start with a clean slate. Warning: Any unsaved changes to your current session are lost.

**Reopen recently closed tabs**
: If you close a tab by mistake, select the {icon}`boxes_vertical` **Tabs bar menu** icon located at the end of the tab bar to retrieve recently closed tabs.

## Save and restore tabs

When you [save your Discover session](save-open-search.md), all currently open tabs are saved within the session. This means:

* Your entire multi-tab workspace is preserved
* Each tab retains its individual settings
* When you reopen the saved session, all tabs are restored exactly as you left them

This makes it easy to create saved workspaces for different investigation patterns you use regularly.

## Tips for working with tabs

* **Name your tabs meaningfully**: Use descriptive names like "Last 24h errors", "Prod versus Dev comparison", or "CPU metrics" instead of the default names
* **Keep related explorations together**: Group tabs by investigation topic and use the reorder feature to keep them adjacent
* **Save often**: Don't lose your work - save your multi-tab session when you've set up a useful workspace
* **Start with one good tab**: When you have a solid query, duplicate it to test variations rather than building from scratch

