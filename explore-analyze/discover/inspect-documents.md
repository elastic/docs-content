---
navigation_title: Inspect documents
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Look closer at your results in Discover by finding a value across results, reading every field of a document, and seeing the request behind them.
---

# Inspect documents and requests in Discover

To understand a result, you often need more than a table row. In **Discover**, you can find a value across all the results that are loaded, open a document to read every one of its fields, and see the request that produced the results.

## Before you begin

Open **Discover** and run a query that returns results.

## Find and highlight values in the table [in-table-search]

Use the in-table search to find and highlight specific values beyond what's currently visible on your screen.

The in-table search looks for all matching values in all results and pages currently loaded in the table. The number of results loaded depends on the [Sample size](document-explorer.md#document-explorer-sample-size). If you load more results, the search automatically updates and reflects the new number of matching values, if any more are found.

```{tip}
You can navigate between results with your keyboard by pressing "Enter" to go to the next result, and "Shift + Enter" to go to the previous result.
```

![Using the in-table search and navigating through the matches](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt30bf5f8b9a45ab74/67c234a787966d9fbc994ce0/in-table-search-demo.gif)

## Look inside a document [look-inside-a-document]

$$$document-explorer-expand-documents$$$
Dive into an individual document to view its fields and the documents that occurred before and after it.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To filter or copy values in the table without opening the flyout, switch **View mode** to **JSON**. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

1. In the document table, select {icon}`maximize` **View details** (**Toggle dialog with details** in earlier {{stack}} versions) to show document details.

    ![Table view with document expanded](/explore-analyze/images/kibana-document-table-expanded.png "")

2. Scan through the fields and their values. You can filter the table in several ways:

   * If you find a field of interest, hover your mouse over the **Field** or **Value** columns for filters and additional options.
   * Use the search above the table to filter for specific fields or values, or filter by field type using the options next to the search field.
   * You can pin fields by selecting the left column, so they stay displayed even if you filter the table.

   ::::{tip}
   You can restrict the fields listed in the detailed view to the fields that you explicitly added to the **Discover** table, using the **Selected only** toggle. In ES|QL mode, you also have an option to hide fields with null values. This toggle isn't available from the **View single document** page.
   ::::

3. In classic mode, you can also open the document on a page of its own, or view the documents that occurred before and after it. Refer to [View a single document or the documents around it](view-single-document.md). These actions aren't available in {{esql}} mode.

::::{tip}
:applies_to: {"serverless": "ga", "stack": "ga 9.6+"}

To copy a link that reopens this document, select {icon}`link` **Copy link** in the flyout header. Refer to [Share a link to a document](copy-and-share-documents.md#share-a-document-link).
::::

## Inspect the request behind your results [inspect-discover-request]

:::{include} ../_snippets/inspect-request.md
:::

## Check which context-aware experience is active [view-active-context-aware-experience]

You can check which experience is currently active for your current Discover session. This can help you confirm whether the type of data you're currently exploring is properly detected or if Discover is currently using its default experience.

1. Open the Inspector:
   * {applies_to}`serverless:` {applies_to}`stack: ga 9.4` Hover over the active tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Inspect**. You can also select **Inspect tab** from the application menu to inspect the active tab.
   * {applies_to}`stack: ga 9.0-9.3` Select **Inspect** from the application menu.
1. Open the **View** dropdown, then select **Profiles**.

The various profiles listed show details such as the active solution and data source contexts, which determine Discover's context-aware experiences.

## Related pages

- [Compare documents](compare-documents.md)
- [Copy results and share links to documents](copy-and-share-documents.md)
- [Introduction to Discover](discover-get-started.md#context-aware-discover)
