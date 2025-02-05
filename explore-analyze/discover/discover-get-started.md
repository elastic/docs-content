---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-get-started.html
---

# Explore fields and data with Discover [discover-get-started]

Learn how to use **Discover** to:

* **Select** and **filter** your {{es}} data.
* **Explore** the fields and content of your data in depth.
* **Present** your findings in a visualization.

**Prerequisites:**

* If you don’t already have {{kib}}, [start a free trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs) on Elastic Cloud.
* You must have data in {{es}}. Examples on this page use the [ecommerce sample data set](../overview/kibana-quickstart.md#gs-get-data-into-kibana), but you can use your own data.
* You should have an understanding of [{{es}} documents and indices](../../manage-data/data-store/index-basics.md) and [{{kib}} concepts](../overview/kibana-quickstart.md).


## Load data into Discover [find-the-data-you-want-to-use]

Select the data you want to explore, and then specify the time range in which to view that data.

1. Find **Discover** in the navigation menu or by using the [global search field](../../get-started/the-stack.md#kibana-navigation-search).
2. Select the data view that contains the data you want to explore.
   ::::{tip}
   By default, {{kib}} requires a [{{data-source}}](../find-and-organize/data-views.md) to access your Elasticsearch data. A {{data-source}} can point to one or more indices, [data streams](../../manage-data/data-store/index-types/data-streams.md), or [index aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html). When adding data to {{es}} using one of the many integrations available, sometimes data views are created automatically, but you can also create your own.
   
   You can also [try {{esql}}](try-esql.md), that let's you query any data you have in {{es}} without specifying a {{data-source}} first.
   ::::
   If you’re using sample data, data views are automatically created and are ready to use.
   :::{image} ../../images/kibana-discover-data-view.png
   :alt: How to set the {{data-source}} in Discover
   :class: screenshot
   :width: 300px
   :::

3. If needed, adjust the [time range](../query-filter/filtering.md), for example by setting it to the **Last 7 days**.
    The range selection is based on the default time field in your data view. If you are using the sample data, this value was set when the data view was created. If you are using your own data view, and it does not have a time field, the range selection is not available.


**Discover** is populated with your data and you can view various areas with different information:

* All fields detected are listed in a dedicated panel.
* A chart allows you to visualize your data.
* A table displays the results of your search. By default, the table includes a column for the time field and a **Summary** column with an overview of each result. You can modify the document table to display your fields of interest.

You can later filter the data that shows in the chart and in the table by specifying a query and changing the time range.


## Explore the fields in your data [explore-fields-in-your-data]

**Discover** provides utilities designed to help you make sense of your data:

1. In the sidebar, check the available fields. It’s very common to have hundreds of fields. Use the search at the top of that sidebar to look for specific terms in the field names.
   In this example, we’ve entered `ma` in the search field to find the `manufacturer` field.
   ![Fields list that displays the top five search results](../../images/kibana-discover-sidebar-available-fields.png "title =40%")
   ::::{tip}
   You can combine multiple keywords or characters. For example, `geo dest` finds `geo.dest` and `geo.src.dest`.
   ::::

2. Select a field to view its most frequent values.
  **Discover** shows the top 10 values and the number of records used to calculate those values.

3. Select the **Plus** icon to add fields to the results table. You can also drag them from the list into the table.
   ![How to add a field as a column in the table](../../images/kibana-discover-add-field.png "title =50%")
   When you add fields to the table, the **Summary** column is replaced.
   ![Document table with fields for manufacturer](../../images/kibana-document-table.png "")

4. Arrange the view to your liking to display the fields and data you care most about using the various display options of **Discover**. For example, you can change the order and size of columns, expand the table to be in full screen or collapse the chart and the list of fields. Check [Customize the Discover view](document-explorer.md).
5. **Save** your changes to be able to open the same view later on and explore your data further.


### Add a field to your {{data-source}} [add-field-in-discover]

What happens if you forgot to define an important value as a separate field? Or, what if you want to combine two fields and treat them as one? This is where [runtime fields](../../manage-data/data-store/mapping/runtime-fields.md) come into play. You can add a runtime field to your {{data-source}} from inside of **Discover**, and then use that field for analysis and visualizations, the same way you do with other fields.

1. In the sidebar, select **Add a field**.
2. Select the **Type** of the new field.
3. **Name** the field. Name it in a way that corresponds to the way other fields of the data view are named. You can set a custom label and description for the field to make it more recognizable in your data view.
4. Define the value that you want the field to show. By default, the field value is retrieved from the source data if it already contains a field with the same name. You can customize this with the following options:
   - **Set value**: Define a script that will determine the value to show for the field. For more information on adding fields and Painless scripting language examples, refer to [Explore your data with runtime fields](../find-and-organize/data-views.md#runtime-fields).
   - **Set format**: Set your preferred format for displaying the value. Changing the format can affect the value and prevent highlighting in Discover.

5. In the advanced settings, you can adjust the field popularity to make it appear higher or lower in the fields list. By default, Discover orders popular fields from most selected to least selected.
6. **Save** your new field.

You can now find it in the list of fields and add it to the table.

In the following example, we’re adding 2 fields: A simple "Hello world" field, and a second field that combines and transforms the `customer_first_name` and `customer_last_name` fields of the sample data into a single "customer" field:

**Hello world field example**:

* **Name**: `hello`
* **Type**: `Keyword`
* **Set value**: enabled
* **Script**:

    ```ts
    emit("Hello World!");
    ```


**Customer field example**:

* **Name**: `customer`
* **Type**: `Keyword`
* **Set value**: enabled
* **Script**:

    ```ts
    String str = doc['customer_first_name.keyword'].value;
    char ch1 = str.charAt(0);
    emit(doc['customer_last_name.keyword'].value + ", " + ch1);
    ```



### Visualize aggregated fields [_visualize_aggregated_fields]

If a field can be [aggregated](../aggregations.md), you can quickly visualize it in detail by opening it in **Lens** from **Discover**. **Lens** is the default visualization editor in {{kib}}.

1. In the list of fields, find an aggregatable field. For example, with the sample data, you can look for `day_of_week`.
   ![Top values for the day_of_week field](../../images/kibana-discover-day-of-week.png "title =60%")

2. In the popup, click **Visualize**.
   {{kib}} creates a **Lens** visualization best suited for this field.

3. In **Lens**, from the **Available fields** list, drag and drop more fields to refine the visualization. In this example, we’re adding the `manufacturer.keyword` field onto the workspace, which automatically adds a breakdown of the top values to the visualization.
   ![Visualization that opens from Discover based on your data](../../images/kibana-discover-from-visualize.png "")

4. Save the visualization if you’d like to add it to a dashboard or keep it in the Visualize library for later use.

For geo point fields (![Geo point field icon](../../images/kibana-geoip-icon.png "")), if you click **Visualize**, your data appears in a map.

![Map containing documents](../../images/kibana-discover-maps.png "")


### Compare documents [compare-documents-in-discover]

You can use **Discover** to compare and diff the field values of multiple results or documents in the table.

1. Select the results you want to compare from the Documents or Results tab in Discover.
2. From the **Selected** menu in the table toolbar, choose **Compare selected**. The comparison view opens and shows the selected results next to each other.
3. Compare the values of each field. By default the first result selected shows as the reference for displaying differences in the other results. When the value remains the same for a given field, it’s displayed in green. When the value differs, it’s displayed in red.
   ::::{tip}
   You can change the result used as reference by selecting **Pin for comparison** in the contextual menu of any other result.
   ::::


   ![Comparison view in Discover](../../images/kibana-discover-compare-rows.png "")

4. Optionally, customize the **Comparison settings** to your liking. You can for example choose to not highlight the differences, to show them more granularly at the line, word, or character level, or even to hide fields where the value matches for all results.
5. Exit the comparison view at any time using the **Exit comparison mode** button.


### Copy results as text or JSON [copy-row-content]

You can quickly copy the content currently displayed in the table for one or several results to your clipboard.

1. Select the results you want to copy.
2. Open the **Selected** menu in the table toolbar, and select **Copy selection as text** or **Copy documents as JSON**.

The content is copied to your clipboard in the selected format. Fields that are not currently added to the table are ignored.


### Explore individual result or document details in depth [look-inside-a-document]

$$$document-explorer-expand-documents$$$
Dive into an individual document to view its fields and the documents that occurred before and after it.

1. In the document table, click the expand icon ![double arrow icon to open a flyout with the document details](../../images/kibana-expand-icon-2.png "") to show document details.

    ![Table view with document expanded](../../images/kibana-document-table-expanded.png "")

2. Scan through the fields and their values. You can filter the table in several ways:

   * If you find a field of interest, hover your mouse over the **Field** or **Value** columns for filters and additional options.
   * Use the search above the table to filter for specific fields or values, or filter by field type using the options to the right of the search field.
   * You can pin some fields by clicking the left column to keep them displayed even if you filter the table.

   ::::{tip}
   You can restrict the fields listed in the detailed view to just the fields that you explicitly added to the **Discover** table, using the **Selected only** toggle. In ES|QL mode, you also have an option to hide fields with null values.
   ::::

3. To navigate to a view of the document that you can bookmark and share, select **View single document**.
4. To view documents that occurred before or after the event you are looking at, select **View surrounding documents**.


## Search and filter data [search-in-discover]


### Default mode: Search and filter using KQL [_default_mode_search_and_filter_using_kql]

One of the unique capabilities of **Discover** is the ability to combine free text search with filtering based on structured data. To search all fields, enter a simple string in the query bar.

![Search field in Discover](../../images/kibana-discover-search-field.png "")

To search particular fields and build more complex queries, use the [Kibana Query language](../query-filter/languages/kql.md). As you type, KQL prompts you with the fields you can search and the operators you can use to build a structured query.

For example, search the ecommerce sample data for documents where the country matches US:

1. Enter `g`, and then select **geoip.country_iso_code**.
2. Select **:** for equals, and **US** for the value, and then click the refresh button or press the Enter key.
3. For a more complex search, try:

    ```ts
    geoip.country_iso_code : US and products.taxless_price >= 75
    ```


$$$filter-in-discover$$$
With the query input, you can filter data using the KQL or Lucene languages. You can also use the **Add filter** function available next to the query input to build your filters one by one or define them as Query DSL.

For example, exclude results from the ecommerce sample data view where day of week is not Wednesday:

1. Click ![Add icon](../../images/kibana-add-icon.png "") next to the query bar.
2. In the **Add filter** pop-up, set the field to **day_of_week**, the operator to **is not**, and the value to **Wednesday**.

    ![Add filter dialog in Discover](../../images/kibana-discover-add-filter.png "")

3. Click **Add filter**.
4. Continue your exploration by adding more filters.
5. To remove a filter, click the close icon (x) next to its name in the filter bar.


### Search and filter using ES|QL [_search_and_filter_using_esql]

You can use **Discover** with the Elasticsearch Query Language, ES|QL. When using ES|QL, you don’t have to select a data view. It’s your query that determines the data to explore and display in Discover.

You can switch to the ES|QL mode of Discover from the application menu bar.

Note that in ES|QL mode, the **Documents** tab is named **Results**.

Learn more about how to use ES|QL queries in [Using ES|QL](try-esql.md).


### Save your Discover session for later use [save-discover-search]

Save your Discover session so you can use it later, generate a CSV report, or use it to create visualizations, dashboards, and Canvas workpads. Saving a Discover session saves the query text, filters, and current view of **Discover**, including the columns selected in the document table, the sort order, and the {{data-source}}.

1. In the application menu bar, click **Save**.
2. Give your session a title and a description.
3. Optionally store [tags](../find-and-organize/tags.md) and the time range with the session.
4. Click **Save**.


### Share your Discover session [share-your-findings]

To share your search and **Discover** view with a larger audience, click **Share** in the application menu bar. For detailed information about the sharing options, refer to [Reporting](../report-and-share.md).


## Generate alerts [alert-from-Discover]

From **Discover**, you can create a rule to periodically check when data goes above or below a certain threshold within a given time interval.

1. Ensure that your data view, query, and filters fetch the data for which you want an alert.
2. In the application menu bar, click **Alerts > Create search threshold rule**.

    The **Create rule** form is pre-filled with the latest query sent to {{es}}.

3. [Configure your query](../alerts/kibana/rule-type-es-query.md) and [select a connector type](../../deploy-manage/manage-connectors.md).
4. Click **Save**.

For more about this and other rules provided in {{alert-features}}, go to [Alerting](../alerts/kibana.md).


## What’s next? [_whats_next_4]

* [Search for relevance](discover-search-for-relevance.md).
* [Configure the chart and document table](document-explorer.md) to better meet your needs.


## Troubleshooting [_troubleshooting]

This section references common questions and issues encountered when using Discover. Also check the following blog post: [Learn how to resolve common issues with Discover.](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load)

**Some fields show as empty while they should not be, why is that?**

This can happen in several cases:

* With runtime fields and regular keyword fields, when the string exceeds the value set for the [ignore_above](https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-above.html) setting used when indexing the data into {{es}}.
* Due to the structure of nested fields, a leaf field added to the table as a column will not contain values in any of its cells. Instead, add the root field as a column to view a JSON representation of its values. Learn more in [this blog post](https://www.elastic.co/de/blog/discover-uses-fields-api-in-7-12).
