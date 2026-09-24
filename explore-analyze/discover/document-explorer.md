---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/document-explorer.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Customize the Discover document table, chart, and sidebar. Adjust columns, density, and row height, or inspect documents as JSON.
---

# Customize the Discover view [document-explorer]

**Discover** offers flexible customization options to optimize your data exploration experience. Adjust the document table layout, modify column arrangements, control chart, results table, and sidebar visibility, and configure display density to focus on the data that matters most. These customizations persist across sessions and help you work more efficiently with your {{product.elasticsearch}} data.

:::{tip}
Discover provides default [context-aware experiences](/explore-analyze/discover/discover-get-started.md#context-aware-discover) tailored to the type of data that you're exploring, and you can further customize your Discover view on top of them.
:::

:::{image} /explore-analyze/images/kibana-hello-field.png
:alt: A view of the Discover app
:screenshot:
:::


## Hide or resize areas [document-explorer-c]

* To show or hide sections of the Discover view:
  * {applies_to}`serverless:` {applies_to}`stack: ga 9.4` Use the **Panels visibility** button group to show or hide areas of **Discover** independently. The button group stays in a fixed position regardless of which sections are shown or hidden.
      * {icon}`transition_top_out` / {icon}`transition_top_in` to show or hide the chart
      * {icon}`transition_bottom_out` / {icon}`transition_bottom_in` to show or hide the results table
      * {icon}`transition_left_out` / {icon}`transition_left_in` to show or hide the fields list
  * {applies_to}`stack: ga 9.0-9.3` Use the available collapse and expand button in the corresponding area to show or hide the chart and the fields list.
* Adjust the width and height of each area by dragging their border to the size you want. The size of each area is saved in your browser for the next time you open **Discover**.


## Modify the document table [document-explorer-customize]

Customize the appearance of the document table and its contents to your liking.

![Options to customize the table in Discover](/explore-analyze/images/kibana-discover-customize-table.png "")

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To inspect documents as a tree, set **View mode** to **JSON**. Refer to [View documents as JSON](#document-explorer-view-mode).


### Reorder and resize the columns [document-explorer-columns]

* To move a single column, drag its header and drop it to the position you want. You can also open the column’s contextual options, and select **Move left** or **Move right** in the available options.
* To move multiple columns, click **Columns**. In the pop-up, drag the column names to their new order.
* To resize a column, drag the right edge of the column header until the column is the width that you want.
  ::::{tip}
  Column widths are stored with a Discover session. When you add a Discover session as a dashboard panel, it appears the same as in **Discover**.
  ::::


{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Density** and header and body row height apply to the column layout. They are not available in **JSON** view.


### Customize the table density [document-explorer-density]

You can adjust the density of the table from the **Display options** located in the table toolbar. This can be particularly useful when scrolling through many results.


### Adjust header and body row height [document-explorer-row-height]

Open **Display options** in the table toolbar. Set **Max header cell lines** and **Body cell lines** to **Auto** to fit the contents, or to **Custom** and enter a line count.


### Limit the sample size [document-explorer-sample-size]

When the number of results returned by your search query (displayed at the top of the **Documents** or **Results** tab) is greater than the value of [`discover:sampleSize`](kibana://reference/advanced-settings.md#kibana-discover-settings), the number of results displayed in the table is limited to the configured value by default. You can adjust the initial sample size for searches to any number between 10 and `discover:sampleSize` from the **Display options** located in the table toolbar.

![Limit sample size in Discover](/explore-analyze/images/kibana-discover-limit-sample-size.png "title =50%")

On the last page of the table, a message indicates that you’ve reached the end of the loaded search results. From that message, you can choose to load more results to continue exploring.

### Sort the fields [document-explorer-sort-data]

Sort the data by one or more fields, in ascending or descending order. The default sort is based on the time field, from new to old.

To add or remove a sort on a single field, click the column header, and then select the sort order.

To sort by multiple fields:

1. Click the **Sort fields** option.
   
   ![Pop-up in document table for sorting columns](/explore-analyze/images/kibana-document-explorer-sort-data.png "title =50%")

2. To add fields to the sort, select their names from the dropdown menu.
   By default, columns are sorted in the order they are added.
   :::{image} /explore-analyze/images/kibana-document-explorer-multi-field.png
   :alt: Multi field sort in the document table
   :screenshot:
   :width: 50%
   :::

3. To change the sort order, select a field in the pop-up, and then drag it to the new location.


### Edit a field [document-explorer-edit-field]

Change how {{kib}} displays a field.

1. Click the column header for the field, and then select **Edit data view field.**
2. In the **Edit field** form, change the field name and format.
   For detailed information on formatting options, refer to [Format data fields](../find-and-organize/data-views/field-formatters.md).



### Filter the documents [document-explorer-compare-data]

Narrow your results to a subset of documents so you're comparing the data of interest.

1. Select the documents you want to compare.
2. Click the **Selected** option, and then select **Show selected documents only**.
   :::{image} /explore-analyze/images/kibana-document-explorer-compare-data.png
   :alt: Compare data in the document table
   :screenshot:
   :width: 50%
   :::


You can also compare individual field values using the [**Compare selected** option](discover-get-started.md#compare-documents-in-discover).


### Set the number of results per page [document-explorer-configure-table]

To change the numbers of results you want to display on each page, use the **Rows per page** menu. The default is 100 results per page.

:::{image} /explore-analyze/images/kibana-document-table-rows-per-page.png
:alt: Menu with options for setting the number of results in the document table
:screenshot:
:::


## View documents as JSON [document-explorer-view-mode]
```{applies_to}
serverless: ga
stack: ga 9.6+
```

**JSON** view shows each document as a collapsible tree in the table. Use it to inspect nested fields, copy a value or the whole document, and filter without opening the flyout.

Open **Display options** in the table toolbar, then set **View mode** to **JSON**. If you add fields to the table, the tree shows only those fields. If you don't, it shows the full document.

:::{image} /explore-analyze/images/kibana-discover-json-view.png
:alt: Discover table in JSON view with Display options open
:screenshot:
:::

Use **Expand all** and **Collapse all** to open or close nested objects and arrays. Hover a field or value to copy it, or to filter for or filter out that value. Select **Copy all** to copy the document as JSON. To expand only one object's children, hold Command (or Ctrl) and select that object or array.

Use **Display options** to change how each tree looks, and how many documents the table loads:

* **Lines shown**: How much of the tree is open in each cell. The range is 10 to 200. The default is 50.
* **Hide nulls**: When **On**, **Discover** omits null values from the tree. The default is **Off**.
* **Wrap lines**: When **On**, long values wrap onto more lines. When **Off**, each value is truncated to one line. The default is **On**.
* [**Sample size**](#document-explorer-sample-size): How many documents the table loads. To page through one document and the documents around it, use the [document flyout](discover-get-started.md#look-inside-a-document).

You can't filter on values {{es}} ignored at index time, or on values inside a JSON string that **Discover** expanded in the tree. If a document is too large to render in full, **Discover** shows a warning and displays the first 10,000 values.

To go back to columns, set **View mode** to **Table**. You can then change [**Density**](#document-explorer-density) and [header and body row height](#document-explorer-row-height).

If you save the session in **JSON** view, you get the same tree and the same **Lines shown**, **Hide nulls**, and **Wrap lines** values when you open it again. A dashboard panel from that session, or from [**Save table to dashboard**](save-open-search.md#save-table-to-dashboard), looks the same.
