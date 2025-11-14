---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-get-started.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Explore Elasticsearch data with Kibana Discover. Select data views, filter and search documents, analyze field values, add runtime fields, and visualize findings to understand patterns.
---

# Get started with Discover [discover-get-started]

Discover is your starting point for exploring data in {{product.elasticsearch}}. Whether you're investigating an issue, learning about your data's structure, or building insights, Discover provides an interactive environment to search, filter, and analyze documents. This tutorial helps you learn the essential workflows and features that make data exploration effective.

**Prerequisites:**

* If you don't already have {{product.kibana}}, [start a free trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs) on {{ecloud}}.
* You must have data in {{product.elasticsearch}}. The examples on this page use the [ecommerce sample data set](../index.md#gs-get-data-into-kibana), but you can use your own data.
* You should have an understanding of [{{product.elasticsearch}} documents and indices](../../manage-data/data-store/index-basics.md).

## Context-aware data exploration [context-aware-discover]

**Discover** provides tailored interfaces and features for the following data types when accessed from Observability or Security project types or {{product.kibana}} solution views:

* Observability:
  * **[Logs exploration](/solutions/observability/logs/discover-logs.md)**
  * **[Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md)** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview`
% LINK/PAGE TBD  * **Traces exploration**
% * Security:
% LINK/PAGE TBD  * **Security data exploration**

This context-aware experience is determined by both your solution context and the type of data you query. When both conditions align, **Discover** provides specific capabilities useful for exploring that specific type of data, and integrates features or paths to other relevant solution applications.

When you access **Discover** outside of a specific solution context, or when working with data types that don't have specialized experiences, you get the default **Discover** interface with all its core functionality for general-purpose data exploration.

### Context-awareness with multiple data types

Your query may include multiple data types that each have tailored experiences; for example, if you query both `logs-*` and `traces-*` indices within an Observability context.

In this case **Discover** provides the default experience until it detects that you're interacting with a single type of data. For example, when you [](#look-inside-a-document).

### View active context-aware experience

You can check which experience is currently active for your current Discover session. This can help you confirm whether the type of data you're currently exploring is properly detected or if Discover is currently using its default experience.

1. Select **Inspect** from Discover's toolbar.
1. Open the **View** dropdown, then select **Profiles**.

The various profiles listed show details such as the active solution and data source contexts, which determine Discover's context-aware experiences.

## Load data into Discover [find-the-data-you-want-to-use]

Select the data you want to explore, and then specify the time range in which to view that data.

1. Find **Discover** in the navigation menu or by using the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the data view that contains the data you want to explore.
   ::::{tip}
   By default, {{product.kibana}} requires a [{{data-source}}](../find-and-organize/data-views.md) to access your Elasticsearch data. A {{data-source}} can point to one or more indices, [data streams](../../manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md). When adding data to {{product.elasticsearch}} using one of the many integrations available, sometimes data views are created automatically, but you can also create your own.

   You can also [try {{esql}}](try-esql.md), that lets you query any data you have in {{product.elasticsearch}} without specifying a {{data-source}} first.
   ::::
   If you’re using sample data, data views are automatically created and are ready to use.
   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: How to set the {{data-source}} in Discover
   :screenshot:
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

1. In the sidebar, check the available fields. It's common to have hundreds of fields. Use the search at the top of that sidebar to look for specific terms in the field names.
   In this example, we’ve entered `ma` in the search field to find the `manufacturer` field.
   ![Fields list that displays the top five search results](/explore-analyze/images/kibana-discover-sidebar-available-fields.png "title =40%")
   ::::{tip}
   You can combine multiple keywords or characters. For example, `geo dest` finds `geo.dest` and `geo.src.dest`.
   ::::

   {applies_to}`stack: ga 9.2` For some searches, Discover suggests recommended fields to explore. These suggestions are based on the data you query and are managed by Elastic.

2. Select a field to view its most frequent values.
  **Discover** shows the top 10 values and the number of records used to calculate those values.

3. Select the **Plus** icon to add fields to the results table. You can also drag them from the list into the table.

   ![How to add a field as a column in the table](/explore-analyze/images/kibana-discover-add-field.png "title =50%")

   When you add fields to the table, the **Summary** column is replaced.
   ![Document table with fields for manufacturer](/explore-analyze/images/kibana-document-table.png "")

4. Arrange the view to your liking to display the fields and data you care most about using the various display options of **Discover**. For example, you can change the order and size of columns, expand the table to be in full screen or collapse the chart and the list of fields. Check [Customize the Discover view](document-explorer.md) for more information.
5. **Save** your changes to be able to open the same view later on and explore your data further.


### Add a field to your {{data-source}} [add-field-in-discover]

What happens if you forgot to define an important value as a separate field? Or, what if you want to combine two fields and treat them as one? This is where [runtime fields](../../manage-data/data-store/mapping/runtime-fields.md) come into play. You can add a runtime field to your {{data-source}} from inside of **Discover**, and then use that field for analysis and visualizations the same way you do with other fields.

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

If a field can be [aggregated](../query-filter/aggregations.md), you can quickly visualize it in detail by opening it in **Lens** from **Discover**. **Lens** is the default visualization editor in {{product.kibana}}.

1. In the list of fields, find an aggregatable field. For example, with the sample data, you can look for `day_of_week`.

   ![Top values for the day_of_week field](/explore-analyze/images/kibana-discover-day-of-week.png "title =60%")

2. In the popup, click **Visualize**.
   {{product.kibana}} creates a **Lens** visualization best suited for this field.

3. In **Lens**, from the **Available fields** list, drag and drop more fields to refine the visualization. In this example, we’re adding the `manufacturer.keyword` field onto the workspace, which automatically adds a breakdown of the top values to the visualization.
   ![Visualization that opens from Discover based on your data](/explore-analyze/images/kibana-discover-from-visualize.png "")

4. Save the visualization if you’d like to add it to a dashboard or keep it in the Visualize library for later use.

For geo point fields (![Geo point field icon](/explore-analyze/images/kibana-geoip-icon.png "kibana-geoip-icon =4%x4%")), if you click **Visualize**, your data appears in a map.

![Map containing documents](/explore-analyze/images/kibana-discover-maps.png "")


### Find and highlight values in the table [in-table-search]

Use the in-table search to find and highlight specific values beyond what's currently visible on your screen.

The in-table search looks for all matching values in all results and pages currently loaded in the table. The number of results loaded depends on the [Sample size](document-explorer.md#document-explorer-sample-size). If you load more results, the search automatically updates and reflects the new number of matching values, if any more are found.

```{tip}
You can navigate between results with your keyboard by pressing "Enter" to go to the next result, and "Shift + Enter" to go to the previous result.
```

![Using the in-table search and navigating through the matches](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt30bf5f8b9a45ab74/67c234a787966d9fbc994ce0/in-table-search-demo.gif)


### Compare documents [compare-documents-in-discover]

You can use **Discover** to compare and diff the field values of multiple results or documents in the table.

1. Select the results you want to compare from the Documents or Results tab in Discover.
2. From the **Selected** menu in the table toolbar, choose **Compare selected**. The comparison view opens and shows the selected results next to each other.
3. Compare the values of each field. By default the first result selected shows as the reference for displaying differences in the other results. When the value remains the same for a given field, it’s displayed in green. When the value differs, it’s displayed in red.
   ::::{tip}
   You can change the result used as reference by selecting **Pin for comparison** in the contextual menu of any other result.
   ::::


   ![Comparison view in Discover](/explore-analyze/images/kibana-discover-compare-rows.png "")

4. Optionally, customize the **Comparison settings** to your liking. You can for example choose to not highlight the differences, to show them more granularly at the line, word, or character level, or even to hide fields where the value matches for all results.
5. Exit the comparison view at any time using the **Exit comparison mode** button.


### Copy results as text or JSON [copy-row-content]

You can quickly copy the content currently displayed in the table for one or several results to your clipboard.

1. Select the results you want to copy.
2. Open the **Selected** menu in the table toolbar, and select **Copy selection as text** or **Copy documents as JSON**.

The content is copied to your clipboard in the selected format. Fields that are not currently added to the table are ignored.

:::{tip}
You can copy the content of a single cell to your clipboard from the quick actions that appear when hovering over the cell.
:::


### Explore individual result or document details in depth [look-inside-a-document]

$$$document-explorer-expand-documents$$$
Dive into an individual document to view its fields and the documents that occurred before and after it.

1. In the document table, click the expand icon ![double arrow icon to open a flyout with the document details](/explore-analyze/images/kibana-expand-icon-2.png "") to show document details.

    ![Table view with document expanded](/explore-analyze/images/kibana-document-table-expanded.png "")

2. Scan through the fields and their values. You can filter the table in several ways:

   * If you find a field of interest, hover your mouse over the **Field** or **Value** columns for filters and additional options.
   * Use the search above the table to filter for specific fields or values, or filter by field type using the options to the right of the search field.
   * You can pin some fields by clicking the left column to keep them displayed even if you filter the table.

   ::::{tip}
   You can restrict the fields listed in the detailed view to the fields that you explicitly added to the **Discover** table, using the **Selected only** toggle. In ES|QL mode, you also have an option to hide fields with null values. This toggle isn't available from the **View single document** page.
   ::::

3. To navigate to a view of the document that you can bookmark and share, select **View single document**.
4. To view documents that occurred before or after the event you are looking at, select **View surrounding documents**.


## Search and filter data [search-in-discover]


### Default mode: Search and filter using KQL [_default_mode_search_and_filter_using_kql]

One of the unique capabilities of **Discover** is the ability to combine free text search with filtering based on structured data. To search all fields, enter a simple string in the query bar.

![Search field in Discover](/explore-analyze/images/kibana-discover-search-field.png "")

:::{note}
Free text searches that don't specify a field may not return expected results depending on how the [`index.query.default_field` index setting](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-query-default-field) is configured for the indices matching the current data view.
:::

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

1. Click ![Add icon](/explore-analyze/images/kibana-add-icon.png "") next to the query bar.
2. In the **Add filter** pop-up, set the field to **day_of_week**, the operator to **is not**, and the value to **Wednesday**.

    ![Add filter dialog in Discover](/explore-analyze/images/kibana-discover-add-filter.png "")

3. Click **Add filter**.
4. Continue your exploration by adding more filters.
5. To remove a filter, click the close icon (x) next to its name in the filter bar.

#### Filter pill actions

:::{include} ../_snippets/global-filters.md
:::


### Search and filter using ES|QL [_search_and_filter_using_esql]

You can use **Discover** with the Elasticsearch Query Language, ES|QL. When using ES|QL, you don’t have to select a data view. It’s your query that determines the data to explore and display in Discover.

You can switch to the ES|QL mode of Discover from the application menu bar.
If you've entered a KQL or Lucene query in the default mode of Discover, it automatically converts to ES|QL.

In ES|QL mode, the **Documents** tab is named **Results**.

:::{important}
{applies_to}`stack: ga 9.1` When an ES|QL query times out, partial results that are available are shown. The timeout is defined by the `search:timeout` advanced setting, which is set to 10 minutes (600000 ms) by default. In serverless projects, this advanced setting is not customizable and the timeout is set to 10 minutes.
:::

Learn more about how to use ES|QL queries in [Using ES|QL](try-esql.md).

### Run multiple explorations with tabs
```{applies_to}
stack: preview 9.2
serverless: preview
```
**Discover** supports multiple tabs to help you explore different aspects of your data simultaneously. Each tab maintains its own independent state, including the query ({{esql}} or classic mode), time range, filters, selected data source, columns and sort order you defined, and the active [context-aware experience](#context-aware-discover).

This allows you to pivot quickly between different explorations without losing your place. For example:

* **Compare time periods:** Open multiple tabs with the same query but different time ranges
* **Test query variations:** Duplicate a tab to experiment with different {{esql}} queries or filters
* **Switch contexts:** Keep separate tabs for logs, metrics, and traces explorations
* **Test a hypothesis:** Switch between different data sources or field combinations

#### Manage Discover tabs

You can open new tabs or duplicate existing ones to compare different queries:
- To start a fresh exploration in a new tab, select the {icon}`plus` icon next to the existing tabs.
- To test variations of your current query in a new tab, hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Duplicate**.

To manage and organize your tabs, you can:
- Rename them: Double-click its label or hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Rename**.
- Reorder them: Drag and drop a tab to move it.
- Close them: Hover over a tab and select the {icon}`cross` icon.
- Close several tabs at once: When you hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, options let you **Close other tabs** to keep only the active tab open or **Close tabs to the right** to only keep your first tabs and discard any subsequent tabs.

  :::{tip}
  If you want to discard all open tabs, you can also start a {icon}`plus` **New session** from the toolbar. When you use this option, any unsaved changes to your current session are lost.
  :::
- Reopen recently closed tabs: If you close a tab by mistake, you can retrieve it by selecting the {icon}`boxes_vertical` **Tabs bar menu** icon located at the end of the tab bar.

To keep all of your tabs for later, you can [Save your Discover session](#save-discover-search). All currently open tabs are saved within the session and will be there when you open it again.

### Inspect your Discover queries

:::{include} ../_snippets/inspect-request.md
:::

### Run long-running queries in the background
```{applies_to}
stack: ga 9.2
serverless: unavailable
```

You can send your long-running KQL or {{esql}} queries to the background from **Discover** and let them run while you continue exploring your data. Refer to [Run queries in the background](/explore-analyze/discover/background-search.md).


### Save your Discover session for later use [save-discover-search]

Save your Discover session so you can use it later, generate a CSV report, or use it to create visualizations, dashboards, and Canvas workpads. Saving a Discover session saves all open tabs, along with their query text, filters, and current view of **Discover**, including the columns selected in the document table, the sort order, and the {{data-source}}.

1. In the application menu bar, click **Save**.
2. Give your session a title and a description.
3. Optionally store [tags](../find-and-organize/tags.md) and the time range with the session.
4. Click **Save**.


### Share your Discover session [share-your-findings]

To share your search and **Discover** view with a larger audience, click {icon}`share` **Share** in the application menu bar. For detailed information about the sharing options, refer to [Reporting](../report-and-share.md).


## Generate alerts [alert-from-Discover]

From **Discover**, you can create a rule to periodically check when data goes above or below a certain threshold within a given time interval.

1. Ensure that your data view, query, and filters fetch the data for which you want an alert.
2. In the application menu bar, click **Alerts > Create search threshold rule**.

    The **Create rule** form is pre-filled with the latest query sent to {{product.elasticsearch}}.

3. [Configure your query](../alerts-cases/alerts/rule-type-es-query.md) and [select a connector type](../../deploy-manage/manage-connectors.md).
4. Click **Save**.

For more about this and other rules provided in {{alert-features}}, go to [Alerting](../alerts-cases/alerts.md).


## What’s next? [_whats_next_4]

* [Search for relevance](discover-search-for-relevance.md).
* [Configure the chart and document table](document-explorer.md) to better meet your needs.


## Troubleshooting [_troubleshooting]

This section references common questions and issues encountered when using Discover. Also check the following blog post: [Learn how to resolve common issues with Discover.](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load)

**Some fields show as empty while they should not be, why is that?**

This can happen in several cases:

* With runtime fields and regular keyword fields, when the string exceeds the value set for the [ignore_above](elasticsearch://reference/elasticsearch/mapping-reference/ignore-above.md) setting used when indexing the data into {{product.elasticsearch}}.
* Due to the structure of nested fields, a leaf field added to the table as a column will not contain values in any of its cells. Instead, add the root field as a column to view a JSON representation of its values. Learn more in [this blog post](https://www.elastic.co/de/blog/discover-uses-fields-api-in-7-12).
