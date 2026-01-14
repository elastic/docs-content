---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-get-started.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Step-by-step tutorial for exploring data with Discover by selecting data views, filtering documents, analyzing fields, and creating visualizations using sample or your own data.
---

# Get started with Discover [discover-get-started]

This tutorial teaches you the fundamentals of exploring data in **Discover**. You'll work through the core workflows for data exploration: selecting data sources, investigating field values, creating visualizations, and saving your work. By the end, you'll be comfortable with the essential features of **Discover** and ready to explore more advanced capabilities.

You'll learn how to:

* Select data and set the time range
* Explore fields and their values
* Add fields to the document table
* Create quick visualizations from fields
* Save your work for later use

## Prerequisites
Learn how to explore your {{product.elasticsearch}} data using **Discover**. This tutorial walks you through selecting {{data-sources}}, filtering documents, analyzing field structures, and creating visualizations from your data.

## Context-aware data exploration [context-aware-discover]

**Discover** provides tailored interfaces and features for the following data types when accessed from Observability or Security project types or {{kib}} solution views:

* Observability:
  * **[Logs exploration](/solutions/observability/logs/discover-logs.md)**
  * **[Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md)** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview`
% LINK/PAGE TBD  * **Traces exploration**
% * Security:
% LINK/PAGE TBD  * **Security data exploration**

This context-aware experience is determined by both your solution context and the type of data you query. When both conditions align, **Discover** provides specific capabilities useful for exploring that specific type of data, and integrates features or paths to other relevant solution applications.

When you access **Discover** outside of a specific solution context, or when working with data types that don't have specialized experiences, you get the default **Discover** interface with all its core functionality for general-purpose data exploration.

* If you don't already have {{kib}}, [start a free trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs) on {{ecloud}}.
* You must have data in {{es}}. This tutorial uses the [ecommerce sample data set](../index.md#gs-get-data-into-kibana), but you can use your own data.
* You should have an understanding of [{{es}} documents and indices](../../manage-data/data-store/index-basics.md).

::::{note}
**Discover** adapts its interface based on the type of data you're exploring (logs, metrics, traces, security events) and your solution context. For details about these specialized experiences, see [Context-aware experiences in Discover](context-aware-discover.md). This tutorial focuses on the core **Discover** features available in all contexts.
::::

## Step 1: Load data into Discover [find-the-data-you-want-to-use]

First, select the data you want to explore and set the time range.

1. Open **Discover** from the navigation menu or by using the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).

2. Select the {{data-source}} that contains the data you want to explore. For this tutorial, select **{{kib}} Sample Data eCommerce** if you've installed the sample data.
   
   ::::{tip}
   By default, {{kib}} requires a {{data-source}} to access your {{es}} data. A {{data-source}} can point to one or more indices, [data streams](../../manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md). 
   
   Alternatively, you can try {{esql}}, which lets you query any data you have in {{es}} without selecting a {{data-source}} first.
   ::::

   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: How to set the {{data-source}} in Discover
   :screenshot:
   :width: 300px
   :::

3. Adjust the [time range](../query-filter/filtering.md) to **Last 7 days** using the time picker in the upper right.

**Discover** now displays your data with three main areas:

* **Fields panel** (left sidebar): Lists all fields detected in your data
* **Chart** (top): Visualizes the distribution of your data over time
* **Document table** (bottom): Shows individual results with a time column and a **Summary** column by default

You can modify these areas as you explore. Next, let's dive into the fields in your data.


## Step 2: Explore fields in your data [explore-fields-in-your-data]

Now that you have data loaded, explore the fields to understand your data's structure.

1. Look at the **fields panel** on the left. You'll see hundreds of fields. Use the search box at the top to find specific fields.
   
   Try searching for `ma` to find the `manufacturer` field.
   
   ![Fields list that displays the top five search results](/explore-analyze/images/kibana-discover-sidebar-available-fields.png "title =40%")
   
   ::::{tip}
   You can combine multiple keywords. For example, `geo dest` finds both `geo.dest` and `geo.src.dest`.
   ::::

2. Click on a field name to view its most frequent values.
   
   **Discover** shows the top 10 values and the number of documents containing each value.

3. Add fields to the document table to see them as columns:
   
   * Click the **+** icon next to a field name, or
   * Drag a field from the list directly into the table

   ![How to add a field as a column in the table](/explore-analyze/images/kibana-discover-add-field.png "title =50%")

   When you add fields, the default **Summary** column is replaced with your selected fields.
   
   ![Document table with fields for manufacturer](/explore-analyze/images/kibana-document-table.png "")

4. Try adding these fields from the ecommerce sample data:
   * `manufacturer.keyword`
   * `products.product_name.keyword`
   * `customer_first_name.keyword`
   * `total_quantity`

5. Rearrange columns by dragging their headers to new positions.


## Step 3: Visualize aggregated fields [_visualize_aggregated_fields]

**Discover** lets you create quick visualizations from aggregatable fields without leaving the application.

1. In the fields list, find an aggregatable field such as `day_of_week`.

   ![Top values for the day_of_week field](/explore-analyze/images/kibana-discover-day-of-week.png "title =60%")

2. In the field popup, click **Visualize**.
   
   {{kib}} creates a **Lens** visualization best suited for this field.

3. In **Lens**, drag and drop more fields from the **Available fields** list to refine the visualization. Try adding the `manufacturer.keyword` field to the workspace, which automatically adds a breakdown of the top values.
   
   ![Visualization that opens from Discover based on your data](/explore-analyze/images/kibana-discover-from-visualize.png "")

4. Save the visualization to add it to a dashboard or keep it in the Visualize library for later use.

::::{tip}
For geo point fields (![Geo point field icon](/explore-analyze/images/kibana-geoip-icon.png "kibana-geoip-icon =4%x4%")), clicking **Visualize** opens your data in a map.

![Map containing documents](/explore-analyze/images/kibana-discover-maps.png "")
::::


## Step 4: Explore individual documents [look-inside-a-document]

Dive deeper into individual documents to view all their fields and values.

1. In the document table, click the expand icon (![double arrow icon to open a flyout with the document details](/explore-analyze/images/kibana-expand-icon-2.png "")) next to any document.

    ![Table view with document expanded](/explore-analyze/images/kibana-document-table-expanded.png "")

2. Scan through the fields and their values in the flyout:

   * Hover over a **Field** or **Value** to see filter options and other actions
   * Use the search box to find specific fields or values
   * Pin important fields by clicking the pin icon to keep them visible when filtering

3. Try these additional actions:
   * Click **View single document** to open a standalone view you can bookmark and share
   * Click **View surrounding documents** to see documents that occurred before and after this one in time


## Step 5: Search and filter your data [search-in-discover]

Now let's narrow down your results with a search query and filters.

1. In the query bar at the top, try a simple search. For the ecommerce sample data, search for documents where the country is US:
   
   ```ts
   geoip.country_iso_code : US
   ```

   Press Enter to run the query.

2. Add a filter to further refine your results:
   
   * Click the **Add filter** button (![Add icon](/explore-analyze/images/kibana-add-icon.png "")) next to the query bar
   * Set **Field** to `day_of_week`
   * Set **Operator** to `is not`
   * Set **Value** to `Wednesday`
   * Click **Add filter**

   ![Add filter dialog in Discover](/explore-analyze/images/kibana-discover-add-filter.png "")

3. Notice how the results update to match your query and filters. The chart also adjusts to show only the matching data.

::::{tip}
As you type in the query bar, KQL suggests fields and operators to help you build structured queries. You can also create filters by clicking the **+** or **-** icons next to field values in the fields panel.
::::

For more detailed information on searching and filtering, see [Search and filter data](search-and-filter.md).

## Step 6: Save your session [save-discover-search]

Save your Discover session so you can return to it later or share it with others.

1. Click **Save** in the toolbar.
2. Give your session a meaningful name like "US ecommerce purchases".
3. Optionally add a description and [tags](../find-and-organize/tags.md).
To manage and organize your tabs, you can:
- Rename them: Double-click its label or hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Rename**.
- Reorder them: Drag and drop a tab to move it.
- Close them: Hover over a tab and select the {icon}`cross` icon.
- Close several tabs at once: When you hover over a tab and select the {icon}`boxes_vertical` **Actions** icon, options let you **Close other tabs** to keep only the active tab open or **Close tabs to the right** to only keep your first tabs and discard any subsequent tabs.

  :::{tip}
  If you want to discard all open tabs, you can also start a {icon}`plus` **New session** from the toolbar. When you use this option, any unsaved changes to your current session are lost.
  :::
- Reopen recently closed tabs: If you close a tab by mistake, you can retrieve it by selecting the {icon}`boxes_vertical` **Tabs menu** icon located at the end of the tab bar.

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

Your session is now saved with all your settings: the query, filters, selected fields, time range, and {{data-source}}. You can reopen it anytime by clicking **Open** in the toolbar.


## What's next

Now that you're familiar with the basics of **Discover**, explore these guides to learn more:

**Common tasks**
* **[Search and filter data](search-and-filter.md)** - Learn advanced query techniques and filtering strategies
* **[Customize the Discover view](document-explorer.md)** - Adjust the layout, table, and display options
* **[Compare documents](compare-documents.md)** - Compare field values across multiple documents
* **[Add fields to your {{data-source}}](add-fields-to-data-views.md)** - Create runtime fields to extend your data

**Advanced features**
* **[Using {{esql}}](try-esql.md)** - Query your data with the {{es}} Query Language
* **[Work with tabs](work-with-tabs.md)** - Run multiple explorations simultaneously
* **[Run queries in the background](background-search.md)** - Send long-running queries to the background
* **[Generate alerts from Discover](generate-alerts-from-discover.md)** - Create rules to monitor your data

**Analysis tools**
* **[View field statistics](show-field-statistics.md)** - Explore field distributions and statistics
* **[Run pattern analysis](run-pattern-analysis-discover.md)** - Find patterns in log messages
* **[Search for relevance](discover-search-for-relevance.md)** - Sort documents by relevance score
