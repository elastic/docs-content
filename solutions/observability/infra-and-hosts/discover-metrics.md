---
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Make the most of Discover to explore metrics data.
products:
  - id: observability
  - id: security
---

# Explore metrics data with Discover in {{kib}}

**Discover** offers a dedicated experience for exploring metrics data. When **Discover** recognizes metrics data, it enables specific features and default behaviors to optimize your data exploration. Metrics-specific exploration in Discover automatically generates a grid of charts showing available metrics from your data. Use this view to quickly search and filter metrics, break metrics down by dimensions, review the ES|QL query that generates the charts, and add metrics to dashboards with a single click.

If you're just getting started with **Discover** and want to learn its main principles, you should get familiar with the [default experience](../../../explore-analyze/discover.md).

:::{image} /solutions/images/explore-metrics-ui.png
:alt: Screenshot of adding a dimension.
:screenshot:
:::

## Requirements

Use the `TS` command to select the data source. For example, the following query returns all of your metrics data:

  ```esql
  TS metrics-*
  ```

To visualize your metrics data as charts:
  - The data stream needs its **Index mode** set to **Time series**. Open **Index Management** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Data Streams** tab to find your data stream's index mode.
  - The metric must be a time series metric.

The dedicated metrics view is only available in ES|QL mode. Select {icon}`code` **{{esql}}** or **Try {{esql}}** from Discover.

You can also query a specific index:

```esql
TS metrics-index-1
```

:::{note}
By default, all data stored in a `metrics-*` index is recognized as metrics data and triggers the **Discover** experience described on this page.
:::

### Required {{kib}} privileges

Viewing metrics data in **Discover** requires at least `read` privileges for **Discover**.

For more on assigning {{kib}} privileges, refer to the [{{kib}} privileges documentation](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Metrics-specific Discover options

When the metrics profile is active, the documents table is collapsed by default so the chart grid takes the full view. You can expand the table at any time to view individual documents.

:::{important}
All metrics in the grid have data. If a metric appears empty, it's likely a counter metric where the scrape interval is smaller than the bucket size. To view the data, either expand the time range or click Explore for that metric and reduce the number of buckets in the query.
:::

With your data loaded, use the metrics charts to:

**Search for specific metrics**

Use the search function to find and visualize specific metric data:

:::{image} /solutions/images/explore-metrics-search.png
:alt: Screenshot of searching for a specific metric.
:screenshot:
:::

**Break down metrics by dimensions**

Break down your metrics by dimensions to find metrics that contain those dimensions and identify which values in those dimensions contribute the most to each metric.

:::{note}
Only fields mapped as dimensions in a [time series data stream](https://www.elastic.co/docs/reference/elasticsearch/index-settings/time-series) are available for metric breakdown. If an expected dimension is missing, verify that the field is mapped as a `time_series_dimension` in your 
[time series data stream (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) configuration.
:::

:::{image} /solutions/images/explore-metrics-host-ip.png
:alt: Screenshot of adding a dimension.
:screenshot:
:::

:::::{applies-switch}

::::{applies-item} stack: ga 9.4+
You can filter the view to focus on specific values in two ways:

- **Click a chart value**: After you break down by one or more dimensions, hover over a chart and click the value you want to filter by. This adds the corresponding dimension-value pairs to your query and updates the metrics view to show only metrics with those dimension values.
- **Edit the query directly**: Manually add a `| WHERE` clause to your ES|QL query. For example: `| WHERE <dimension> = <value>`
::::

::::{applies-item} stack: ga 9.2-9.3
**Filter dimensions by a specific value**

Select specific values to focus on within the dimension. You can select up to 10 values to filter your dimension by.

:::{image} /solutions/images/explore-metrics-host-ip-values.png
:alt: Screenshot of adding a filtering a dimension by a value.
:screenshot:
:::

::::

:::::

**View metric charts in full screen**

Select full screen ({icon}`full_screen`) to view the metric charts in full-screen mode.

### Actions

For each metric chart, you can perform the following actions:

* **Explore** ({icon}`app_discover`): Open Discover filtered to focus on that specific metric.
* **Inspect** ({icon}`inspect`): Show details about the query request and response.
* **View details** ({icon}`eye`): Get additional information about the metric like metric type, dimensions, and ES|QL query.
* **Copy to dashboard** ({icon}`app_dashboard`): Save the metric chart to an existing or new [dashboard](/explore-analyze/dashboards.md).
* **Add to case** ({icon}`app_cases`): Add the metric chart to a [case](/solutions/observability/incident-management/observability-cases.md).