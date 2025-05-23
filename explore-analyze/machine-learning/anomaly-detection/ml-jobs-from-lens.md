---
navigation_title: Anomaly detection jobs from visualizations
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-jobs-from-lens.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Anomaly detection jobs from visualizations [ml-jobs-from-lens]

You can create {{anomaly-jobs}} from the compatible Lens charts on **Dashboard**.

## Prerequisites and limitations [prereqs]

* Only chart-like visualizations are compatible. Supported chart types are `area`, `area_percentage_stacked`, `area_stacked`, `bar`, `bar_horizontal`, `bar_horizontal_stacked`, `bar_percentage_stacked`, `bar_stacked`, and `line`.
* Supported {{anomaly-detect}} functions are `average`, `count`, `max`, `median`, `min`, `sum`, `unique_count`.
* The chart must contain a date field on one axis and it must be the same as the default date field for the {{data-source}}.
* In case of a multi-layered chart, only the compatible layers can be used to create an {{anomaly-job}}.
* Chart layers which contain a field that uses a [time shift](../../dashboards/create-dashboard-of-panels-with-ecommerce-data.md#compare-time-ranges) or a field that has a `filter by` setting applied cannot be used to create an {{anomaly-job}}.

## Creating the job [create-job]

::::{note}
You need to have a compatible visualization on **Dashboard** to create an {{anomaly-job}}. If you don’t have one but you want to try the feature out, go to **Analytics > Dashboard** and select the `[Flight] Global Flight Dashboard` which is based on the {{kib}} sample flight data set. Select the `Flight count` visualization from the dashboard.
::::

1. Go to **Analytics > Dashboard** from the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md). Select a dashboard with a compatible visualization.
2. Open the **Options (…) menu** for the panel, then select **More**.
3. Select **Create {{anomaly-job}}**. The option is only displayed if the visualization can be converted to an {{anomaly-job}} configuration.
4. (Optional) Select the layer from which the {{anomaly-job}} is created.

:::{image} /explore-analyze/images/machine-learning-create-ad-job-from-lens.jpg
:alt: A screenshot of a chart with the Options menu opened
:screenshot:
:::

If the visualization has multiple compatible layers, you can select which layer to use for creating the {{anomaly-job}}.

:::{image} /explore-analyze/images/machine-learning-select-layer-for-job.jpg
:alt: A screenshot of a chart with the Options menu opened
:screenshot:
:::

If multiple fields are added to the chart or you selected a `Break down by` field, the multi metric job wizard is used for creating the job. For a single metric chart, the single metric wizard is used.

If the configured time range of the chart is relative, it is converted to absolute start and end times in the job configuration. If the conversion of these times fails, the whole time range from the index is used.

## What’s next [ml-job-lens-next]

* [Learn more about **Dashboard**](../../dashboards.md)
* [Learn more about creating visualizations with **Lens**](../../visualize/lens.md)
