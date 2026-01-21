---
applies_to:
  stack: preview 9.2
  serverless: preview
description: Make the most of Discover to explore metrics data.
products:
  - id: observability
  - id: security
---

# Explore metrics data with Discover in Kibana

:::{important}
This functionality is experimental and not supported. It may change or be removed at anytime.
:::

**Discover** offers a dedicated experience for exploring metrics data. When **Discover** recognizes metrics data, it enables specific features and default behaviors to optimize your data exploration. Metrics-specific exploration in Discover automatically generates a grid of charts showing available metrics from your data. Use this view to quickly search and filter metrics, break metrics down by dimension, review the ES|QL query that generates the charts, and add metrics to dashboards with a single click.

If you're just getting started with **Discover** and want to learn its main principles, you should get familiar with the [default experience](../../../explore-analyze/discover.md).

:::{image} /solutions/images/explore-metrics-ui.png
:alt: Screenshot of adding a dimension.
:screenshot:
:::

## Requirements

### Data recognition
By default, all data stored in a `metrics-*` index is recognized as metrics data and triggers the **Discover** experience described on this page.

### Required Kibana privileges

Viewing metrics data in **Discover** requires at least `read` privileges for **Discover**.

For more on assigning Kibana privileges, refer to the [Kibana privileges documentation](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Load metrics data

:::{note}
To visualize your metrics data as charts, its data stream needs its **Index mode** set to **Time series**. Open **Index Management** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Data Streams** tab to find your data stream's index mode.
:::

The dedicated metrics view is only available in ES|QL mode. From the **Discover** main page, select **Try ES|QL** to open ES|QL mode.

Use the `TS` command to select the data source. For example, the following query returns all of your metrics data:

```esql
TS metrics-*
```

You can also query a specific index:

```esql
TS metrics-index-1
```

## Metrics-specific Discover options

With your data loaded, use the metrics charts to:

**Search for specific metrics**

Use the search function to find and visualize specific metric data:

:::{image} /solutions/images/explore-metrics-search.png
:alt: Screenshot of searching for a specific metric.
:screenshot:
:::

**Break down metrics by dimension**

Break down your metrics by dimension to find metrics that contain those dimensions and identify which values in those dimensions contribute the most to each metric.

:::{image} /solutions/images/explore-metrics-host-ip.png
:alt: Screenshot of adding a dimension.
:screenshot:
:::

**Filter dimensions by a specific value**

Select specific values to focus on within the dimension. You can select up to 10 values to filter your dimension by.

:::{image} /solutions/images/explore-metrics-host-ip-values.png
:alt: Screenshot of adding a filtering a dimension by a value.
:screenshot:
:::

**View metric charts in full screen**

Select full screen ({icon}`full_screen`) to view the metric charts in full-screen mode.

### Actions

For each metric chart, you can perform the following actions:

* **Explore in Discover** ({icon}`app_discover`): Open Discover filtered to focus on that specific metric.
* **Inspect** ({icon}`inspect`): Show details about the query request and response.
* **View details** ({icon}`eye`): Get additional information about the metric like metric type, dimensions, and ES|QL query.
* **Copy to dashboard** ({icon}`app_dashboard`): Save the metric chart to an existing or new [dashboard](/explore-analyze/dashboards.md).
* **Add to case** ({icon}`app_cases`): Add the metric chart to a [case](/solutions/observability/incident-management/cases.md).