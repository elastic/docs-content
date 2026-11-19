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

# Copy results and share links to documents in Discover

If you want to paste results into another tool, or show a teammate exactly what you're looking at, copy the results or send a link that reopens the same view or document.

## Before you begin

Open **Discover** and run a query that returns results.

## Copy results as text, JSON, or Markdown [copy-row-content]

To paste results into another tool, copy the rows you need from the table.

1. Select the rows you want to copy.
2. Open the **Selected** menu in the table toolbar, and select one of the available formats:
   - **Copy selection as text**.
   - **Copy documents as JSON**, or **Copy results as JSON** if you're in {{esql}} mode.
   - {applies_to}`stack: ga 9.3+` **Copy selection as Markdown**: Selected results are copied as a Markdown table.

**Result:** The text and Markdown formats copy the columns that are in the table. If you haven't added columns, they copy every field of the selected rows. The JSON format copies each selected document in full, whatever columns the table shows.

:::{tip}
To copy the content of a single cell, use the quick actions that appear when you hover over the cell.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` In the **Summary** column, select **Copy value** to copy the whole document.
:::

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` In **JSON** view, you can also copy a field, a nested object, or the whole document from the tree. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

## Share a link to the current view [share-your-findings]

To send someone to the view you're looking at, select {icon}`share` **Share** in the application menu and copy the link. For the link options, refer to [Reporting and sharing](../report-and-share.md).

The link holds your query, not the results. Whoever opens it signs in to {{kib}} and sees only the data that their role can access. If the session has unsaved changes, the link is temporary, so save the session first to get a permanent one.

In classic mode, you can also open a document on its own page, which you can bookmark. Refer to [Open a document on its own page](inspect-documents.md#open-single-document).

### Share a link to a document [share-a-document-link]
```{applies_to}
serverless: ga
stack: ga 9.6+
```

If you are investigating a result, you can copy a link that reopens **Discover** with that document's [flyout](inspect-documents.md#look-inside-a-document) open. Recipients land on the same document instead of only the surrounding query.

In {{esql}} mode, your query must return the `_id` and `_index` metadata fields. Add `METADATA _id, _index` on the `FROM` or `TS` line, run the query again, and open the document before you copy the link. For example:

```esql
FROM kibana_sample_data_logs METADATA _id, _index
```

1. In the document table, select {icon}`maximize` **View details** on the document's row.
2. In the flyout header, select {icon}`link` **Copy link**.

   :::{image} /explore-analyze/images/kibana-discover-copy-document-link.png
   :alt: Copy link tooltip in the flyout header
   :screenshot:
   :width: 400px
   :::

**Result:** Anyone who opens the link sees **Discover** with the same document flyout open. The link uses the absolute time range of the results on screen, so the document stays in that range.

If you open a document from a grouped {{esql}} result, the link keeps the grouping with [`INLINE STATS`](elasticsearch://reference/query-languages/esql/commands/inlinestats-by.md).

**Share** includes the open document when **Copy link** can copy it. If **Copy link** can't copy the document, the dialog says the link won't include it.

**Copy link** always uses an absolute time range. **Share** can keep a relative one, but then its dialog warns you to use an absolute time range so the document stays in the results.

**Copy link** stays available and shows a warning when it can't link to an individual result:

- If the query transforms rows, for example with `STATS` or `KEEP`, you can't copy a link to an individual result.
- If the query starts with a source command other than `FROM` or `TS`, such as `ROW`, you can't copy a link to an individual result.
- If `_id` and `_index` are missing, add `METADATA _id, _index` and run the query again.

## Next steps

- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md): Keep the results next to your other panels.
- [Export results and sessions from Discover](export-discover-session.md): Take the results or the session definition elsewhere.

## Related pages

- [Inspect documents and requests in Discover](inspect-documents.md)
- [Save and manage Discover sessions](save-open-search.md)
