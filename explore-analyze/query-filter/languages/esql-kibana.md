---
navigation_title: "{{kib}}"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-kibana.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Use ES|QL in Kibana [esql-kibana]

You can use {{esql}} in {{kib}} to query and aggregate your data, create visualizations, and set up alerts.

More specifically, {{esql}} is a powerful tool in Kibana that can help you with specific solution use cases. For example:

- {{observability}}: {{esql}} makes it much easier to analyze metrics, logs and traces from a single query. Find performance issues fast by defining fields on the fly, enriching data with lookups, and using simultaneous query processing. Combining {{esql}} with {{ml}} and AiOps can improve detection accuracy and use aggregated value thresholds.
- Security: Use {{esql}} to retrieve important information for investigation by using lookups. Enrich data and create new fields on the go to gain valuable insight for faster decision-making and actions. For example, perform a lookup on an IP address to identify its geographical location, its association with known malicious entities, or whether it belongs to a known cloud service provider all from one search bar. {{esql}} ensures more accurate alerts by incorporating aggregated values in detection rules.

This guide shows you how to use {{esql}} in Kibana. To follow along with the queries, load the "Sample web logs" sample data set by selecting **Sample Data** from the **Integrations** page in {{kib}}, selecting **Other sample data sets**, and clicking **Add data** on the **Sample web logs** card.

:::{tip}
Find the complete list of supported commands, functions, and operators in the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).
:::

## Enable or disable {{esql}} [esql-kibana-enable]

{{esql}} is enabled by default in {{kib}}. It can be disabled using the `enableESQL` setting from the [Advanced Settings](kibana://reference/advanced-settings.md).

This will hide the {{esql}} user interface from various applications. However, users will be able to access existing {{esql}} artifacts like saved searches and visualizations.


## The {{esql}} editor [esql-kibana-get-started]

To get started with {{esql}}, go to **Discover**. Next, select **Try ES|QL** from the application menu bar.


### The query bar [esql-kibana-query-bar]

After switching to {{esql}} mode, the query bar shows your previous KQL or Lucene query converted into {{esql}}. If the query was empty, it shows a sample query. For example:

```esql
FROM kibana_sample_data_logs | LIMIT 10
```

Every query starts with a [source command](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-source-commands). In this query, the source command is [`FROM`](elasticsearch://reference/query-languages/esql/commands/source-commands.md#esql-from). `FROM` retrieves data from data streams, indices, or aliases. In this example, the data is retrieved from `kibana_sample_data_logs`.

A source command can be followed by one or more [processing commands](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-processing-commands). In this query, the processing command is [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-limit). `LIMIT` limits the number of rows that are retrieved.

::::{tip}
Click the **ES|QL help** button to open the in-product reference documentation for all commands and functions or to get recommended queries that will help you get started.
::::


To make it easier to write queries, auto-complete offers suggestions with possible commands and functions:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-auto-complete.png
:alt: esql kibana auto complete
:::

::::{note}
{{esql}} keywords are case-insensitive. The following query is identical to the previous one:

```esql
FROM kibana_sample_data_logs | LIMIT 10
```

::::



### Make your query readable [_make_your_query_readable]

For readability, you can put each processing command on a new line. The following query is identical to the previous one:

```esql
FROM kibana_sample_data_logs
| LIMIT 10
```

You can do that using the **Add line breaks on pipes** button from the query editor’s footer.

:::{image} /explore-analyze/images/esql-line-breakdown.gif
:alt: Automatic line breaks for ES|QL queries
:width: 50%
:::

You can adjust the editor’s height by dragging its bottom border to your liking.


### Warnings [_warnings]

A query may result in warnings, for example when querying an unsupported field type. When that happens, a warning symbol is shown in the query bar. To see the detailed warning, expand the query bar, and click **warnings**.


### Query history [esql-kibana-query-history]

You can reuse your recent {{esql}} queries in the query bar. In the query bar, click **Show recent queries**.

You can then scroll through your recent queries:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-discover-query-history.png
:alt: esql discover query history
:::

### Query help

{{esql}} features in-app help and suggestions, so you can get started faster and don’t have to leave the application to check syntax.

![The ES|QL syntax reference and the autocomplete menu](/explore-analyze/images/kibana-esql-in-app-help.png "")


### Starred queries [esql-kibana-starred-queries]

From the query history, you can mark some queries as favorite to find and access them faster later.

In the query bar, click **Show recent queries**.

From the **Recent** tab, you can star any queries you want.

In the **Starred** tab, find all the queries you have previously starred.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-discover-query-starred.png
:alt: esql discover query starred
:::


### Organize the query results [esql-kibana-results-table]

For the example query, the results table shows 10 rows. Omitting the `LIMIT` command, the results table defaults to up to 1000 rows. Using `LIMIT`, you can increase the limit to up to 10,000 rows.

::::{note}
the 10,000 row limit only applies to the number of rows that are retrieved by the query and displayed in Discover. Any query or aggregation runs on the full data set.
::::


Each row shows two columns for the example query: a column with the `@timestamp` field and a column with the full document. To display specific fields from the documents, use the [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) command:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
```

To display all fields as separate columns, use `KEEP *`:

```esql
FROM kibana_sample_data_logs
| KEEP *
```

::::{note}
The maximum number of columns in Discover is 50. If a query returns more than 50 columns, Discover only shows the first 50.
::::



### Sorting [_sorting]

To sort on one of the columns, click the column name you want to sort on and select the sort order. Note that this performs client-side sorting. It only sorts the rows that were retrieved by the query, which may not be the full dataset because of the (implicit) limit. To sort the full data set, use the [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) command:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
| SORT bytes DESC
```


### Time filtering [esql-kibana-time-filter]

To display data within a specified time range, you can use the standard time filter, custom time parameters, or a WHERE command.


#### Standard time filter [_standard_time_filter]

The standard [time filter](../filtering.md) is enabled when the indices you’re querying have a field named `@timestamp`.


#### Custom time parameters [_custom_time_parameters]

If your indices do not have a field named `@timestamp`, you can use the `?_tstart` and `?_tend` parameters to specify a time range. These parameters work with any timestamp field and automatically sync with the [time filter](../filtering.md).

```esql
FROM my_index
| WHERE custom_timestamp >= ?_tstart AND custom_timestamp < ?_tend
```

You can also use the `?_tstart` and `?_tend` parameters with the [`BUCKET`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions.md#esql-bucket) function to create auto-incrementing time buckets in {{esql}} [visualizations](#esql-kibana-visualizations). For example:

```esql
FROM kibana_sample_data_logs
| STATS average_bytes = AVG(bytes) BY BUCKET(@timestamp, 50, ?_tstart, ?_tend)
```

This example uses `50` buckets, which is the maximum number of buckets.


#### WHERE command [_where_command]

You can also limit the time range using the [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) command and the [`NOW`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-now) function. For example, if the timestamp field is called `timestamp`, to query the last 15 minutes of data:

```esql
FROM kibana_sample_data_logs
| WHERE timestamp > NOW() - 15minutes
```

### LOOKUP JOINs

The ES|QL editor supports [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) commands and suggests lookup mode indices and join condition fields.

![Using the LOOKUP JOIN command to autocomplete an ES|QL query](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte43a30a93241d650/67c23670045f5839e5bfd1e4/lookup-join-demo.gif)


### Keyboard shortcuts

The ES|QL editor supports several shortcuts to help you write and run your queries faster:

| Mac           | Windows/Linux  | Description                 |
|---------------|----------------|-----------------------------|
| `Cmd + Enter` | `Ctrl + Enter` | Run a query                 |
| `Cmd + /`     | `Ctrl + /`     | Comment or uncomment a line |

:::{tip}
You can find the list of shortcuts directly from the editor. Look for the ![keyboard](../../images/keyboard.svg "keyboard =2%") icon.
:::

## Analyze and visualize data [esql-kibana-visualizations]

Between the query bar and the results table, Discover shows a date histogram visualization. By default, if the indices you’re querying do not contain a `@timestamp` field, the histogram is not shown. But you can use a custom time field with the `?_tstart` and `?_tend` parameters to enable it.

The visualization adapts to the query. A query’s nature determines the type of visualization. For example, this query aggregates the total number of bytes per destination country:

```esql
FROM kibana_sample_data_logs
| STATS total_bytes = SUM(bytes) BY geo.dest
| SORT total_bytes DESC
| LIMIT 3
```

The resulting visualization is a bar chart showing the top 3 countries:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-bar-chart.png
:alt: esql kibana bar chart
:::

To make changes to the visualization, like changing the visualization type, axes and colors, click the pencil button (![esql icon edit visualization](/explore-analyze/images/elasticsearch-reference-esql-icon-edit-visualization.svg "")). This opens an in-line editor:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-in-line-editor.png
:alt: esql kibana in line editor
:::

You can save the visualization to a new or existing dashboard by clicking the save button (![esql icon save visualization](/explore-analyze/images/elasticsearch-reference-esql-icon-save-visualization.svg "")). Once saved to a dashboard, you’ll be taken to the Dashboards page. You can continue to make changes to the visualization. Click the options button in the top-right (![esql icon options](/explore-analyze/images/elasticsearch-reference-esql-icon-options.svg "")) and select **Edit ES|QL visualization** to open the in-line editor:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-edit-on-dashboard.png
:alt: esql kibana edit on dashboard
:::


### Add a panel to a dashboard [esql-kibana-dashboard-panel]

You can use {{esql}} queries to create panels on your dashboards. To add a panel to a dashboard, under **Dashboards**, click the **Add panel** button and select {{esql}}.

Check the {{esql}} query by clicking the Panel filters button (![Panel filters button on panel header](/explore-analyze/images/elasticsearch-reference-dashboard_panel_filter_button.png "")):

:::{image} /explore-analyze/images/elasticsearch-reference-esql-dashboard-panel-query.png
:alt: esql dashboard panel query
:width: 50%
:::

You can also edit the {{esql}} visualization from here. Click the options button in the top-right (![esql icon options](/explore-analyze/images/elasticsearch-reference-esql-icon-options.svg "")) and select **Edit ESQL visualization** to open the in-line editor.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-dashboard-panel-edit-visualization.png
:alt: esql dashboard panel edit visualization
:width: 50%
:::

You can also [Add dashboard controls from your ES|QL visualization's query](/explore-analyze/dashboards/add-controls.md#add-esql-control)


## Create an enrich policy [esql-kibana-enrich]

The {{esql}} [`ENRICH`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-enrich) command enables you to [enrich](elasticsearch://reference/query-languages/esql/esql-enrich-data.md) your query dataset with fields from another dataset. Before you can use `ENRICH`, you need to [create and execute an enrich policy](elasticsearch://reference/query-languages/esql/esql-enrich-data.md#esql-set-up-enrich-policy). If a policy exists, it will be suggested by auto-complete. If not, click **Click to create** to create one.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-enrich-autocomplete.png
:alt: esql kibana enrich autocomplete
:width: 50%
:::

Next, you can enter a policy name, the policy type, source indices, and optionally a query:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-enrich-step-1.png
:alt: esql kibana enrich step 1
:width: 50%
:::

Click **Next** to select the match field and enrich fields:

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-enrich-step-2.png
:alt: esql kibana enrich step 2
:width: 50%
:::

Finally, click **Create and execute**.

Now, you can use the enrich policy in an {{esql}} query:

```esql
FROM kibana_sample_data_logs
| STATS total_bytes = SUM(bytes) BY geo.dest
| SORT total_bytes DESC
| LIMIT 3
| ENRICH countries
```


## Create an alerting rule [esql-kibana-alerting-rule]

You can use {{esql}} queries to create alerts. From Discover, click **Alerts** and select **Create search threshold rule**. This opens a panel that enables you to create a rule using an {{esql}} query. Next, you can test the query, add a connector, and save the rule.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-create-rule.png
:alt: esql kibana create rule
:width: 50%
:::


## Limitations [esql-kibana-limitations]

* The user interface to filter data is not enabled when Discover is in {{esql}} mode. To filter data, write a query that uses the [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) command instead.
* Discover shows no more than 10,000 rows. This limit only applies to the number of rows that are retrieved by the query and displayed in Discover. Queries and aggregations run on the full data set.
* Discover shows no more than 50 columns. If a query returns more than 50 columns, Discover only shows the first 50.
* CSV export from Discover shows no more than 10,000 rows. This limit only applies to the number of rows that are retrieved by the query and displayed in Discover. Queries and aggregations run on the full data set.
* Querying many indices at once without any filters can cause an error in kibana which looks like `[esql] > Unexpected error from Elasticsearch: The content length (536885793) is bigger than the maximum allowed string (536870888)`. The response from {{esql}} is too long. Use [`DROP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-drop) or [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) to limit the number of fields returned.
