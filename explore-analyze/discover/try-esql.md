---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/try-esql.html
---

# Using ES|QL [try-esql]

The Elasticsearch Query Language, {{esql}}, makes it easier to explore your data without leaving Discover.

In this tutorial we’ll use the {{kib}} sample web logs in Discover and Lens to explore the data and create visualizations.

::::{tip}
For the complete {{esql}} documentation, including tutorials, examples and the full syntax reference, refer to the [{{es}} documentation](../query-filter/languages/esql.md). For a more detailed overview of {{esql}} in {{kib}}, refer to [Use {{esql}} in Kibana](../query-filter/languages/esql-kibana.md).

::::



## Prerequisite [prerequisite]

To view the {{esql}} option in **Discover**, the `enableESQL` setting must be enabled from Kibana’s **Advanced Settings**. It is enabled by default.


## Use {{esql}} [tutorial-try-esql]

To load the sample data:

1. [Install the web logs sample data](../overview/kibana-quickstart.md#gs-get-data-into-kibana).
2. Go to **Discover**.
3. Select **Try {{esql}}** from the application menu bar.

Let’s say we want to find out what operating system users have and how much RAM is on their machine.

1. Set the time range to **Last 7 days**.
2. Copy the query below:

    ```esql
    FROM kibana_sample_data_logs <1>
    | KEEP machine.os, machine.ram <2>
    ```

    1. We’re specifically looking for data from the sample web logs we just installed.
    2. We’re only keeping the `machine.os` and `machine.ram` fields in the results table.


    ::::{tip}
    Put each processing command on a new line for better readability.
    ::::

3. Click **▶Run**.

    ![An image of the query result](../../images/kibana-esql-machine-os-ram.png "")

    ::::{note}
    {{esql}} keywords are not case sensitive.

    ::::


Let’s add `geo.dest` to our query, to find out the geographical destination of the visits, and limit the results.

1. Copy the query below:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | LIMIT 10
    ```

2. Click **▶Run** again. You can notice that the table is now limited to 10 results. The visualization also updated automatically based on the query, and broke down the data for you.

    ::::{note}
    When you don’t specify any specific fields to retain using `KEEP`, the visualization isn’t broken down automatically. Instead, an additional option appears above the visualization and lets you select a field manually.
    ::::


    ![An image of the extended query result](../../images/kibana-esql-limit.png "")


We will now take it a step further to sort the data by machine ram and filter out the `GB` destination.

1. Copy the query below:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | SORT machine.ram desc
    | WHERE geo.dest != "GB"
    | LIMIT 10
    ```

2. Click **▶Run** again. The table and visualization no longer show results for which the `geo.dest` field value is "GB", and the results are now sorted in descending order in the table based on the `machine.ram` field.

    ![An image of the full query result](../../images/kibana-esql-full-query.png "")

3. Click **Save** to save the query and visualization to a dashboard.


### Edit the ES|QL visualization [_edit_the_esql_visualization]

You can make changes to the visualization by clicking the pencil icon. This opens additional settings that let you adjust the chart type, axes, breakdown, colors, and information displayed to your liking. If you’re not sure which route to go, check one of the suggestions available in the visualization editor.

If you’d like to keep the visualization and add it to a dashboard, you can save it using the floppy disk icon.


### ES|QL and time series data [_esql_and_time_series_data]

By default, ES|QL identifies time series data when an index contains a `@timestamp` field. This enables the time range selector and visualization options for your query.

If your index doesn’t have an explicit `@timestamp` field, but has a different time field, you can still enable the time range selector and visualization options by calling the `?_start` and `?_tend` parameters in your query.

For example, the eCommerce sample data set doesn’t have a `@timestamp` field, but has an `order_date` field.

By default, when querying this data set, time series capabilities aren’t active. No visualization is generated and the time picker is disabled.

```esql
FROM kibana_sample_data_ecommerce
| KEEP customer_first_name, email, products._id.keyword
```

:::{image} ../../images/kibana-esql-no-time-series.png
:alt: ESQL query without time series capabilities enabled
:::

While still querying the same data set, by adding the `?_start` and `?_tend` parameters based on the `order_date` field, **Discover** enables times series capabilities.

```esql
FROM kibana_sample_data_ecommerce
| WHERE order_date >= ?_tstart and order_date <= ?_tend
```

:::{image} ../../images/kibana-esql-custom-time-series.png
:alt: ESQL query with a custom time field enabled
:::
