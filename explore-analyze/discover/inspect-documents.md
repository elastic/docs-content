---
navigation_title: Inspect documents
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Find a value in your results, read every field of a document in the document flyout, and check the request behind your results in Discover.
---

# Inspect documents and requests in Discover

When a table row doesn't tell you enough about a result, **Discover** offers several ways to look closer: finding a value across all loaded results, reading every field of a document, and checking the request that produced the results.

## Before you begin

Open **Discover** and run a query that returns results.

## Find and highlight values in the table [in-table-search]

To find a value anywhere in the results loaded in the table, including rows you haven't scrolled to, select **Find in table** in the table toolbar and enter your text. **Discover** highlights the matches.

The in-table search looks for all matching values in all results and pages loaded in the table. In classic mode, the number of results loaded depends on the [Sample size](document-explorer.md#document-explorer-sample-size). In {{esql}} mode, it depends on the rows that your query returns, so the `LIMIT` of your query sets the ceiling. If you load more results, the search automatically updates and reflects the new number of matching values, if any more are found.

:::{tip}
To go to the next match, press **Enter**. To go to the previous match, press **Shift + Enter**.
:::

![In-table search highlighting the matching values in the table and moving between the matches](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt30bf5f8b9a45ab74/67c234a787966d9fbc994ce0/in-table-search-demo.gif)

## What a dash or `(null)` in your results means [missing-values-in-results]

:::{include} ../_snippets/missing-value-placeholders.md
:::

## Look inside a document [look-inside-a-document]

$$$document-explorer-expand-documents$$$
When you need every field of a result, open the document in the document flyout.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To filter or copy values in the table without opening the flyout, switch **View mode** to **JSON**. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

1. In the document table, select {icon}`maximize` **View details** (**Toggle dialog with details** in {{stack}} 9.5 and earlier) to show document details.

    :::{image} /explore-analyze/images/kibana-document-table-expanded.png
    :alt: Results table with one document opened in the document flyout, listing all its fields and values
    :screenshot:
    :::

2. Scan through the fields and their values. To narrow the list or act on a value, use any of the following:

   * To filter results by a field or value, hover over it in the **Field** or **Value** column and select one of the actions that appear.
   * To narrow the list of fields, use the search field to look for specific fields or values, or filter by field type with the options next to it.
   * To keep a field visible while you filter the list, pin it from the first column.
   * To hide fields that have no value, turn on the **Hide null fields** toggle.
     * {applies_to}`stack: ga 9.0-9.3` In these versions, the toggle is available only in {{esql}} mode.

   ::::{tip}
   You can restrict the fields listed in the detailed view to the fields that you explicitly added to the **Discover** table, using the **Selected only** toggle. The toggle is unavailable until you add at least one field as a column. **Selected only** isn't available from the **View single document** page.
   ::::

In classic mode, you can also [open the document on a page of its own, or view the documents that occurred before and after it](#open-single-document).

::::{tip}
:applies_to: {"serverless": "ga", "stack": "ga 9.6+"}

To copy a link that reopens this document, select {icon}`link` **Copy link** in the flyout header. Refer to [Share a link to a document](copy-and-share-documents.md#share-a-document-link).
::::

## Open a document on its own page or view its neighbors [open-single-document]

In classic mode, you can open a document on a page that you can bookmark and share, or view the documents that occurred before and after it. These actions aren't available in {{esql}} mode, where the document flyout is the way to read a document.

To use them, open **Discover** in classic mode and run a search that returns results. If **Discover** opens in {{esql}} mode, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode). To view the surrounding documents, select a data view that has a time field.

1. In the document table, select {icon}`maximize` **View details** (**Toggle dialog with details** in {{stack}} 9.5 and earlier) on the row of the document you want to look at.
2. In the flyout, select one of the following:
   - **View single document** to open the document on its own page. You can bookmark the page and share its link.
   - **View surrounding documents** to inspect the documents that occurred before and after this document. Only [pinned filters](search-and-filter-classic.md#filter-pill-actions), the filters you pinned across apps, remain active in this view.

**Result:** **Discover** opens the document on a page that you can bookmark, or shows the documents that occurred before and after it.

## Inspect the request behind your results [inspect-discover-request]

:::{include} ../_snippets/inspect-request.md
:::

## Next steps

- To compare several results side by side, refer to [Compare documents in Discover](compare-documents.md).
- To copy a link to a document, refer to [Copy results and share links to documents in Discover](copy-and-share-documents.md).
