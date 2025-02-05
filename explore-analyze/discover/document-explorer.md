---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/document-explorer.html
---

# Customize the Discover view [document-explorer]

Fine tune your explorations by customizing **Discover** to bring out the the best view of your documents.

:::{image} ../../images/kibana-hello-field.png
:alt: A view of the Discover app
:class: screenshot
:::


## Hide or resize areas [document-explorer-c]

* You can hide and show the chart and the fields list using the available collapse and expand button in the corresponding area.
* Adjust the width and height of each area by dragging their border to the size you want. The size of each area is saved in your browser for the next time you open **Discover**.


## Modify the document table [document-explorer-customize]

Customize the appearance of the document table and its contents to your liking.

![Options to customize the table in Discover](../../images/kibana-discover-customize-table.png "")


### Reorder and resize the columns [document-explorer-columns]

* To move a single column, drag its header and drop it to the position you want. You can also open the column’s contextual options, and select **Move left** or **Move right** in the available options.
* To move multiple columns, click **Columns**. In the pop-up, drag the column names to their new order.
* To resize a column, drag the right edge of the column header until the column is the width that you want.

    Column widths are stored with a Discover session. When you add a Discover session as a dashboard panel, it appears the same as in **Discover**.



### Customize the table density [document-explorer-density]

You can adjust the density of the table from the **Display options** located in the table toolbar. This can be particularly useful when scrolling through many results.


### Adjust the row height [document-explorer-row-height]

To set the row height to one or more lines, or automatically adjust the height to fit the contents, open the **Display options** in the table toolbar, and adjust it as you need.

You can define different settings for the header row and body rows.


### Limit the sample size [document-explorer-sample-size]

When the number of results returned by your search query (displayed at the top of the **Documents** or **Results** tab) is greater than the value of [`discover:sampleSize`](https://www.elastic.co/guide/en/kibana/current/advanced-options.html#kibana-discover-settings), the number of results displayed in the table is limited to the configured value by default. You can adjust the initial sample size for searches to any number between 10 and `discover:sampleSize` from the **Display options** located in the table toolbar.

On the last page of the table, a message indicates that you’ve reached the end of the loaded search results. From that message, you can choose to load more results to continue exploring.

![Limit sample size in Discover](../../images/kibana-discover-limit-sample-size.png "")


### Sort the fields [document-explorer-sort-data]

Sort the data by one or more fields, in ascending or descending order. The default sort is based on the time field, from new to old.

To add or remove a sort on a single field, click the column header, and then select the sort order.

To sort by multiple fields:

1. Click the **Sort fields** option.

    :::{image} ../../images/kibana-document-explorer-sort-data.png
    :alt: Pop-up in document table for sorting columns
    :class: screenshot
    :::

2. To add fields to the sort, select their names from the dropdown menu.

    By default, columns are sorted in the order they are added.

    :::{image} ../../images/kibana-document-explorer-multi-field.png
    :alt: Multi field sort in the document table
    :class: screenshot
    :::

3. To change the sort order, select a field in the pop-up, and then drag it to the new location.


### Edit a field [document-explorer-edit-field]

Change how {{kib}} displays a field.

1. Click the column header for the field, and then select **Edit data view field.**
2. In the **Edit field** form, change the field name and format.

    For detailed information on formatting options, refer to [Format data fields](../find-and-organize/data-views.md#managing-fields).



### Filter the documents [document-explorer-compare-data]

Narrow your results to a subset of documents so you’re comparing just the data of interest.

1. Select the documents you want to compare.
2. Click the **Selected** option, and then select **Show selected documents only**.

    :::{image} ../../images/kibana-document-explorer-compare-data.png
    :alt: Compare data in the document table
    :class: screenshot
    :::


You can also compare individual field values using the [**Compare selected** option](discover-get-started.md#compare-documents-in-discover).


### Set the number of results per page [document-explorer-configure-table]

To change the numbers of results you want to display on each page, use the **Rows per page** menu. The default is 100 results per page.

:::{image} ../../images/kibana-document-table-rows-per-page.png
:alt: Menu with options for setting the number of results in the document table
:class: screenshot
:::
