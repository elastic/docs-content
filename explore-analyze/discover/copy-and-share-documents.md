---
navigation_title: Copy and share results
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Copy results from Discover as text, JSON, or Markdown, or send a link that reopens the same view or the same document in Discover.
---

# Copy results and share links to documents

When you want to use results outside of **Discover**, you can copy them to your clipboard. When you want someone else to see what you see, you can send a link that reopens the same view or the same document.

## Copy results as text, JSON, or Markdown [copy-row-content]

You can quickly copy the content currently displayed in the table for one or several results to your clipboard.

1. Select the rows you want to copy.
2. Open the **Selected** menu in the table toolbar, and select one of the available formats:
   - **Copy selection as text**.
   - **Copy documents as JSON**, or **Copy results as JSON** if you're in {{esql}} mode.
   - {applies_to}`stack: ga 9.3+` **Copy selection as Markdown**: Selected results are copied as a Markdown table.

The content is copied to your clipboard in the selected format. Fields that are not currently added to the table are ignored.

:::{tip}
You can copy the content of a single cell to your clipboard from the quick actions that appear when hovering over the cell.
:::

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` In **JSON** view, you can also copy a field, a nested object, or the whole document from the tree. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

## Share your findings [share-your-findings]

You can share the current view, show the results on a dashboard, export the session, or copy a link that reopens a specific document.

- Select {icon}`share` **Share** in the application menu to copy a link to the current view. For the link options, refer to [Reporting and sharing](../report-and-share.md).
- To show the results on a dashboard, add the session, its chart, or its table, to the dashboard. Refer to [Use Discover sessions in dashboards](save-open-search.md#_add_search_results_to_a_dashboard).
- To export the rows from a saved session, select {icon}`ellipsis` **More** → {icon}`upload` **Export** → **Tab results as CSV**. Some limits apply. Refer to [](save-open-search.md#export-discover-session-csv) for details.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` To export the session definition as JSON, without the query results, select {icon}`ellipsis` **More** → {icon}`upload` **Export** → **Export JSON**. Refer to [Export a Discover session as JSON](save-open-search.md#export-discover-session-json).

In classic mode, you can also open a document on a bookmarkable page of its own. Refer to [View a single document or the documents around it](view-single-document.md).

### Share a link to a document [share-a-document-link]

```{applies_to}
serverless: ga
stack: ga 9.6+
```

When you are investigating a result, copy a link that reopens **Discover** with that document's flyout open. Recipients land on the same document instead of only the surrounding query.

1. In the document table, select {icon}`maximize` **View details** on the document's row.
2. In the flyout header, select {icon}`link` **Copy link**.

   :::{image} /explore-analyze/images/kibana-discover-copy-document-link.png
   :alt: Copy link tooltip in the flyout header
   :screenshot:
   :width: 400px
   :::

Opening the link brings back the same flyout.

The link uses the absolute time range of the results on screen, so the document stays in that range.

After you expand a grouped {{esql}} result and select a nested document, **Copy link** reopens that document in the default layout and keeps the grouping with [`INLINE STATS`](elasticsearch://reference/query-languages/esql/commands/inlinestats-by.md).

When **Copy link** can copy the open document, **Share** includes that document. The session link opens **Discover** with the same flyout. If the time range is relative, the **Share** dialog warns you to use an absolute time range so the document stays in the results. If **Copy link** cannot copy the document, the dialog says the link will not include it.

If you are using {{esql}}, add `METADATA _id, _index` on the `FROM` or `TS` line, then rerun the query and reopen the document before copying the link. For example:

```esql
FROM kibana_sample_data_logs METADATA _id, _index
```

If the query transforms rows, such as with `STATS` or `KEEP`, you cannot copy a link to an individual result. **Copy link** stays available and shows a warning. If `_id` and `_index` are missing, **Copy link** stays available and warns you to add `METADATA _id, _index`.

## Related pages

- [Inspect documents and requests in Discover](inspect-documents.md)
- [Save a Discover session for reuse](save-open-search.md)
