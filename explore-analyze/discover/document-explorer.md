---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/document-explorer.html
applies_to:
  stack: ga
  serverless: ga
type: how-to
products:
  - id: kibana
description: Customize the Discover document table, chart, and sidebar. Adjust columns, density, and row height, or inspect documents as JSON.
---

# Customize the Discover view [document-explorer]

If the default **Discover** view doesn't show what you need, you can change which areas are visible, how the document table looks, and how documents are sorted and filtered, so the data that matters most stays in front of you. **Discover** keeps the size and visibility of its areas in your browser. Table settings such as density, row height, sample size, sort order, and column widths are stored with a Discover session when you save it.

:::{tip}
**Discover** adapts its layout to the type of data that you explore, such as logs or metrics. Refer to [How Discover works](/explore-analyze/discover/discover-get-started.md#context-aware-discover). Your customizations apply on top of that layout.
:::

:::{image} /explore-analyze/images/kibana-discover-try-esql-from.png
:alt: Discover in {{esql}} mode, with a query, a chart, and the results table
:screenshot:
:::


## Before you begin

Open **Discover** and run a query that returns results. To keep a customization with your work, save the session. Saving needs the **All** privilege for **Discover**. Refer to [Save and manage Discover sessions](save-open-search.md).

## Hide or resize areas [document-explorer-c]

To make room for the part of **Discover** you're working in, show or hide areas, or resize them.

* To show or hide areas of the **Discover** view:
  * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Use the **Panels visibility** button group to show or hide areas of **Discover** independently. The chart and the results table can't both be hidden, so one of them always stays visible.
      * {icon}`transition_top_out` / {icon}`transition_top_in` to show or hide the chart
      * {icon}`transition_bottom_out` / {icon}`transition_bottom_in` to show or hide the results table
      * {icon}`transition_left_out` / {icon}`transition_left_in` to show or hide the fields list in the sidebar
  * {applies_to}`stack: ga 9.0-9.3` Use the **Panels visibility** buttons or the collapse and expand button in the corresponding area to show or hide the chart and the fields list in the sidebar.
* Adjust the width and height of each area by dragging their border to the size you want.

**Result:** The areas you changed stay that way. **Discover** saves the size and visibility of each area in your browser for the next time you open it. When you save a Discover session, it also stores whether the chart is hidden.


## Modify the document table [document-explorer-customize]

Change the appearance of the document table and its contents so the data that matters stands out. Each of the following sections is a separate task.

:::{image} /explore-analyze/images/kibana-discover-customize-table.png
:alt: Options to customize the document table in Discover
:screenshot:
:::

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To inspect documents as a tree, set **View mode** to **JSON**. Refer to [View documents as JSON](#document-explorer-view-mode).


### Manage the columns in the table [document-explorer-columns]

Choose which columns the table shows and how they're arranged, so the data that matters stands out:

* To add a field as a column, select {icon}`plus` **Add field as column** next to it in the fields list, or drag it into the table. In {{esql}} mode, you can also return the fields you want with `KEEP` in your query. Refer to [Explore fields in Discover](explore-fields.md) and [Show specific columns in the results table](esql-results.md#esql-kibana-results-table).
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` By default, adding fields to the table replaces the **Summary** column. To keep it next to the fields you add, turn on **Pin summary** in the **Columns** menu.
* To move a single column, drag its header and drop it to the position you want. You can also open the column's contextual options, and select **Move left** or **Move right**.
* To move multiple columns, select **Columns**. In the pop-up, drag the column names to their new order.
* To resize a column, drag the right edge of the column header until the column is the width that you want.
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To remove all the fields you added at once, select {icon}`undo` **Clear selected fields** next to the **Selected fields** count in the fields list. The **Selected fields** group appears after you add a field.

  :::{image} /explore-analyze/images/kibana-discover-clear-selected-fields.png
  :alt: Selected fields group in the fields list with the Clear selected fields button next to the count of selected fields
  :screenshot:
  :width: 40%
  :::

**Result:** The table shows the columns you chose, in the order and width you set.

::::{tip}
Column widths are stored with a Discover session. When you add a Discover session as a dashboard panel, it appears the same as in **Discover**.
::::


### Customize the table density [document-explorer-density]

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Density** and the header and body row height apply to the column layout. They aren't available in **JSON** view.

To fit more rows on screen, or to give each row more room, open **Display options** in the table toolbar and change **Density**.

**Result:** The table rows use the density you selected.


### Adjust header and body row height [document-explorer-row-height]

To control how many lines of text each header or body cell shows, open **Display options** in the table toolbar. Set **Max header cell lines** and **Body cell lines** to **Auto** to fit the contents, or to **Custom** and enter a line count. A custom header can show up to 5 lines, and a custom body cell can show up to 20 lines.

**Result:** The table cells show up to the number of lines you set.


### Limit the sample size [document-explorer-sample-size]

To load fewer documents into the table, or to keep the number of results manageable, set the sample size. In classic mode, when the number of results returned by your search query (displayed at the top of the **Documents** tab) is greater than the value of [`discover:sampleSize`](kibana://reference/advanced-settings.md#kibana-discover-settings), the table shows only that many results by default. To change the initial sample size for searches, open **Display options** in the table toolbar and enter any number between 10 and the lower of `discover:sampleSize` and 10,000. The setting is 500 by default. The **Sample size** option isn't available in {{esql}} mode. In {{esql}} mode, the `LIMIT` command in your query sets how many rows the table loads. Refer to [Row and column limits](esql-results.md#esql-kibana-results-table-limitations).

:::{image} /explore-analyze/images/kibana-discover-limit-sample-size.png
:alt: The Sample size setting in the Display options of the document table
:screenshot:
:width: 50%
:::

When your search matches more documents than the table loaded, the last page shows a message that the results are limited. From that message, you can select **Load more** to continue exploring. **Load more** is unavailable while auto-refresh is on.

### Sort documents by one or more fields [document-explorer-sort-data]

Sort the data by one or more fields, in ascending or descending order. In classic mode, the default sort is based on the time field, from new to old. In {{esql}} mode, the query sets the order of the results. Sorting in the table reorders only the rows that are loaded and doesn't change the query.

To add or remove a sort on a single field, select the column header, and then select the sort order.

To sort by multiple fields:

1. Select the **Sort fields** option.

   :::{image} /explore-analyze/images/kibana-document-explorer-sort-data.png
   :alt: Pop-up in the document table for sorting columns
   :screenshot:
   :width: 50%
   :::

2. To add fields to the sort, select their names from the dropdown menu.
   By default, columns are sorted in the order they are added.
   :::{image} /explore-analyze/images/kibana-document-explorer-multi-field.png
   :alt: Multi field sort in the document table
   :screenshot:
   :width: 50%
   :::

3. To change the sort order, select a field in the pop-up, and then drag it to the new location.

**Result:** The table rows follow the sort you set.


### Edit a field [document-explorer-edit-field]

To change how {{kib}} displays a field, such as its name or format:

1. Select the column header for the field, and then select **Edit data view field**.
2. In the **Edit field** form, change the field name and format.
   For detailed information on formatting options, refer to [Format data fields](../find-and-organize/data-views/field-formatters.md).

**Result:** The table shows the field with the new name or format.



### Show only selected documents [document-explorer-compare-data]

Narrow your results to a subset of documents so you're comparing the data of interest.

1. Select the documents you want to compare.
2. Select the **Selected** option, and then select **Show selected documents only** (**Show selected results only** in {{esql}} mode).
   :::{image} /explore-analyze/images/kibana-document-explorer-compare-data.png
   :alt: Compare data in the document table
   :screenshot:
   :width: 50%
   :::


**Result:** The table shows only the documents you selected.

To compare field values across documents, refer to [Compare documents in Discover](compare-documents.md).


### Set the number of results per page [document-explorer-configure-table]

To see more or fewer results at a time, use the **Rows per page** menu. The default is 100 results per page. To change the default for everyone who uses the space, set [`discover:sampleRowsPerPage`](kibana://reference/advanced-settings.md#kibana-discover-settings) in **Advanced Settings**.

:::{image} /explore-analyze/images/kibana-document-table-rows-per-page.png
:alt: Menu with options for setting the number of results in the document table
:screenshot:
:::

**Result:** The table shows the number of results you selected on each page.


## View documents as JSON [document-explorer-view-mode]
```{applies_to}
serverless: ga
stack: ga 9.6+
```

**JSON** view shows each document as a collapsible tree in the table. Use it to inspect nested fields, copy a value or the whole document, and filter without opening the flyout.

Open **Display options** in the table toolbar, then set **View mode** to **JSON**. If you add fields to the table, the tree shows only those fields. If you don't, it shows the document's fields without metadata fields, such as `_id` and `_index`, and without multi-fields, such as `.keyword` fields.

:::{image} /explore-analyze/images/kibana-discover-json-view.png
:alt: Discover table in JSON view with Display options open
:screenshot:
:::

Use **Expand all** and **Collapse all** to open or close nested objects and arrays. Hover a field or value to copy it, or to filter for or filter out that value. Select **Copy all** to copy the document as JSON. To open or close one object or array, select it. To expand every nested level under it at once, hold Command (or Ctrl) while you select it.

Use **Display options** to change how each tree looks, and how many documents the table loads:

* **Lines shown**: How much of the tree is open in each cell. The range is 10 to 200. The default is 50.
* **Hide nulls**: When **On**, **Discover** omits null values from the tree. The default is **Off**.
* **Wrap lines**: When **On**, long values wrap onto more lines. When **Off**, each value is truncated to one line. The default is **On**.
* [**Sample size**](#document-explorer-sample-size): How many documents the table loads. This option isn't available in {{esql}} mode. To page through one document and the documents around it, use the [document flyout](inspect-documents.md#look-inside-a-document).

You can't filter on values {{es}} ignored at index time, or on values inside a JSON string that **Discover** expanded in the tree. If a document is too large to render in full, **Discover** shows a warning and displays the first 10,000 values.

To go back to columns, set **View mode** to **Table**. You can then change [**Density**](#document-explorer-density) and [header and body row height](#document-explorer-row-height).

If you save the session in **JSON** view, you get the same tree and the same **Lines shown**, **Hide nulls**, and **Wrap lines** values when you open it again. A dashboard panel from that session, or from [**Save table to dashboard**](use-sessions-in-dashboards.md#save-table-to-dashboard), looks the same.

**Result:** In **JSON** view, the table shows each document as a tree with your display options.

## Next steps

- [Save and manage Discover sessions](save-open-search.md): Keep your table layout with a saved session.
- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md): Show the table on a dashboard.

## Related pages

- [Inspect documents and requests in Discover](inspect-documents.md)
- [Compare documents in Discover](compare-documents.md)
- [How Discover works](discover-get-started.md)
