---
navigation_title: "ES|QL"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-kibana.html
  - https://www.elastic.co/guide/en/kibana/current/esql.html
description: Overview of the ES|QL editor in Kibana, including query structure, editor tools, time filtering, variables, and query management.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Use ES|QL in the {{kib}} UI [esql-kibana]

The {{esql}} editor lets you write, run, and manage [{{esql}}](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md) queries across {{kib}}. Use it to query and aggregate your data, create visualizations, and set up alerts.

The {{esql}} editor is available in the following areas of {{kib}}:

- [**Discover**](/explore-analyze/discover/try-esql.md): Explore and analyze your data using {{esql}} queries, visualize results, and save your findings to dashboards.
- [**Dashboards**](/explore-analyze/dashboards.md): Create {{esql}}-powered visualization panels and interactive controls.
- [**Alerting**](/explore-analyze/alerts-cases/alerts/rule-type-es-query.md): Create alerting rules based on {{esql}} queries.
- [**{{elastic-sec}} solution**](/solutions/security/esql-for-security.md): Use {{esql}} for threat hunting, detection rules, and investigation workflows.

:::{tip}
Find the complete list of supported commands, functions, and operators in the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).
:::


## Write queries with the {{esql}} editor [esql-kibana-get-started]


### Query structure [esql-kibana-query-bar]

Every {{esql}} query starts with a [source command](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-source-commands) that retrieves data:

- [`FROM`](elasticsearch://reference/query-languages/esql/commands/source-commands.md#esql-from) retrieves data from data streams, indices, or aliases.
- [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) is optimized for querying time series data streams.

You can then chain one or more [processing commands](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-processing-commands) using pipe (`|`) characters. For example, [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) filters rows and [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) aggregates data:

```esql
FROM kibana_sample_data_logs
| WHERE response.keyword == "200"
| STATS total_bytes = SUM(bytes) BY geo.dest
```

When querying many indices at once without filters, the response might be too large. If you encounter a content length error, use [`DROP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-drop) or [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) to limit the number of fields returned.

::::{note}
{{esql}} keywords are case-insensitive. `FROM`, `from`, and `From` are all equivalent.
::::


### Editor tools

The {{esql}} editor includes several built-in tools to help you write queries efficiently.

#### Autocomplete and in-app help

{{esql}} features in-app help, inline suggestions, and an autocomplete menu so you can get started faster and don't have to leave the application to check syntax.

![The ES|QL syntax reference and the autocomplete menu](/explore-analyze/images/kibana-esql-in-app-help.png "")

#### Query formatting [_make_your_query_readable]

For readability, you can put each processing command on a new line and add indentation. Use the {icon}`pipeBreaks` **Prettify query** button from the query editor's footer to format your query automatically. You can also adjust the editor's height by dragging its bottom border.

:::{image} /explore-analyze/images/esql-line-breakdown.gif
:alt: Automatic line breaks and indentation for ES|QL queries
:width: 75%
:::

#### Warnings [_warnings]

A query might result in warnings, for example when querying an unsupported field type. When that happens, the query bar displays a warning symbol. To see the detailed warning, expand the query bar, and select **warnings**.

#### Keyboard shortcuts

| Mac                | Windows/Linux       | Description                 |
|--------------------|---------------------|-----------------------------|
| {kbd}`cmd+enter`   | {kbd}`ctrl+enter`   | Run a query                 |
| {kbd}`cmd+/`       | {kbd}`ctrl+/`       | Comment or uncomment a line |
| {kbd}`cmd+i`       | {kbd}`ctrl+i`       | Prettify query              |
| {kbd}`cmd+k`       | {kbd}`ctrl+k`       | Open [Quick search](#esql-kibana-quick-search) |

:::{tip}
You can find the list of shortcuts directly from the editor. Look for the ![keyboard](../../images/keyboard.svg "keyboard =2%") icon.
:::


### Free-text quick search [esql-kibana-quick-search]
```{applies_to}
serverless: preview
stack: preview 9.3+
```

You can use the **Quick search** functionality of the {{esql}} editor to translate a free-text or KQL search into a functioning {{esql}} query with a `WHERE KQL()` clause. This can be useful if you're getting started with {{esql}} or are familiar with [KQL](kql.md).

1. Select **Quick search** in the editor's footer, or press {kbd}`cmd+k` (Mac) or {kbd}`ctrl+k` (Windows/Linux) to open the **Quick search** bar.
2. Select the data sources to search.
3. Type the text you want to search for as free text or using [KQL](kql.md) syntax.
4. Submit your search by pressing **Enter**. The editor generates a new {{esql}} query that overwrites the current query and runs it. It includes a `FROM` command based on the data sources you selected (or `TS` if the data source is a time series data stream), and a `WHERE KQL()` command that contains the text you typed in the search bar. The editor saves previously run queries in the query history if you need to restore them. 

   The **Quick search** bar closes automatically when you press **Enter**, start typing in the editor or click outside of it.

5. Refine your query with any other {{esql}} command or function that you need.

![Quick search bar in the ES|QL editor](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltc8165d27051bdac3/6997303fcf7e250008e681d8/esql-quick-search.gif "=60%")


### Commands with additional editor support

Some {{esql}} commands have dedicated editor features beyond autocomplete, such as in-editor index or policy creation.

#### LOOKUP JOIN command and lookup indices

The {{esql}} editor supports [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) commands and suggests lookup mode indices and join condition fields.

{applies_to}`stack: ga 9.2.0` Remote lookup joins are supported in [cross-cluster queries](elasticsearch://reference/query-languages/esql/esql-cross-clusters.md). The lookup index must exist on _all_ remote clusters being queried, because each cluster uses its local lookup index data.

![Using the LOOKUP JOIN command to autocomplete an ES|QL query](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte43a30a93241d650/67c23670045f5839e5bfd1e4/lookup-join-demo.gif)

In **Discover**, LOOKUP JOIN commands let you create or edit lookup indices directly from the editor. Find more information in [](/explore-analyze/discover/try-esql.md#discover-esql-lookup-join).


#### ENRICH command and enrich policies [esql-kibana-enrich]

The {{esql}} [`ENRICH`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-enrich) command enables you to [enrich](elasticsearch://reference/query-languages/esql/esql-enrich-data.md) your query dataset with fields from another dataset. Before you can use `ENRICH`, you need to [create and execute an enrich policy](elasticsearch://reference/query-languages/esql/esql-enrich-data.md#esql-set-up-enrich-policy). If a policy exists, autocomplete suggests it. If not, select **Click to create** to create one.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-enrich-autocomplete.png
:alt: esql kibana enrich autocomplete
:width: 50%
:::

For detailed steps to create an enrich policy from the editor, refer to [Enrich your data](elasticsearch://reference/query-languages/esql/esql-enrich-data.md).


## Filter by time [esql-kibana-time-filter]

To display data within a specified time range, you can use the standard time filter, custom time parameters, or a WHERE command.


### Standard time filter [_standard_time_filter]

{{kib}} enables the standard [time filter](../filtering.md) when the indices you're querying have a field named `@timestamp`.


### Custom time parameters [_custom_time_parameters]

If your indices do not have a field named `@timestamp`, you can use the `?_tstart` and `?_tend` parameters to specify a time range. These parameters work with any timestamp field and automatically sync with the [time filter](../filtering.md).

```esql
FROM my_index
| WHERE custom_timestamp >= ?_tstart AND custom_timestamp < ?_tend
```

You can also use the `?_tstart` and `?_tend` parameters with the [`BUCKET`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions.md#esql-bucket) function to create auto-incrementing time buckets in {{esql}} visualizations. For example:

```esql
FROM kibana_sample_data_logs
| STATS average_bytes = AVG(bytes) BY BUCKET(@timestamp, 50, ?_tstart, ?_tend)
```


### Time ranges with WHERE [_where_command]

You can also limit the time range using the [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) command and the [`NOW`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-now) function. For example, if the timestamp field is called `timestamp`, to query the last 15 minutes of data:

```esql
FROM kibana_sample_data_logs
| WHERE timestamp > NOW() - 15minutes
```


## Use variables and controls [add-variable-control]

{{esql}} variables help you add interactive controls to your queries and make them more dynamic.

They're available for:
* [Discover queries](/explore-analyze/discover/try-esql.md#add-variable-control) {applies_to}`stack: ga 9.2`
* [{{esql}} visualizations in dashboards](/explore-analyze/dashboards/add-controls.md#add-variable-control)

:::{include} ../../_snippets/variable-control-procedure.md
:::

:::{include} ../../_snippets/variable-control-examples.md
:::

% Link from the product
### Multi-value variable controls [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../../_snippets/multi-value-esql-controls.md
:::


## Manage queries

The {{esql}} editor keeps track of your queries so you can reuse and organize them.

### Query history [esql-kibana-query-history]

You can reuse your recent {{esql}} queries in the query bar. In the query bar, select **Show recent queries**.

You can then: 
- scroll through your most recent queries
- {applies_to}`stack: ga 9.2` search for specific queries of your history

:::{image} /explore-analyze/images/esql-history.gif
:alt: esql discover query history
:width: 75%
:::

:::{note}
The maximum number of queries in the history depends on the version you're using:
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The query history can keep up to 50 KB of queries, which represents about 200 large queries, or about 300 short queries.
- {applies_to}`stack: ga 9.0-9.1` The query history keeps your 20 most recent queries.
:::

### Starred queries [esql-kibana-starred-queries]

From the query history, you can mark some queries as favorite to find and access them faster later.

In the query bar, select **Show recent queries**.

From the **Recent** tab, you can star any queries you want.

In the **Starred** tab, find all the queries you have previously starred.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-discover-query-starred.png
:alt: esql discover query starred
:::


## Related pages

- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Complete list of commands, functions, and operators.
- [Using {{esql}} in Discover](/explore-analyze/discover/try-esql.md): Hands-on tutorial and Discover-specific features like result tables, visualizations, and lookup indices.
- [{{esql}} for {{elastic-sec}}](/solutions/security/esql-for-security.md): Use cases and examples for threat hunting and detection rules.
- [{{esql}} visualizations](/explore-analyze/visualize/esorql.md): Create and edit {{esql}}-based visualizations in dashboards.
- [Dashboard controls](/explore-analyze/dashboards/add-controls.md): Add {{esql}}-powered controls to dashboards.
