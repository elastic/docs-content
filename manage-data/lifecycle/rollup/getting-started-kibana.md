---
navigation_title: Get started in Kibana
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/data-rollups.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: kibana
---

# Get started with the rollups in {{kib}}

::::{admonition} Deprecated in 8.11.0.
:class: warning

Rollups are deprecated and will be removed in a future version. Use [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) instead.
::::

A rollup job is a periodic task that aggregates data from indices specified by an index pattern, and then rolls it into a new index. Rollup indices are a good way to compactly store months or years of historical data for use in visualizations and reports.

You can go to the **Rollup Jobs** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /manage-data/images/kibana-management_rollup_list.png
:alt: List of currently active rollup jobs
:screenshot:
:::

## Required permissions [_required_permissions_4]

The `manage_rollup` cluster privilege is required to access **Rollup jobs**.

To add the privilege, go to the **Roles** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Create a rollup job [create-and-manage-rollup-job]

{{kib}} makes it easy for you to create a rollup job by walking you through the process. You fill in the name, data flow, and how often you want to roll up the data.  Then you define a date histogram aggregation for the rollup job and optionally define terms, histogram, and metrics aggregations.

When defining the index pattern, you must enter a name that is different than the output rollup index. Otherwise, the job will attempt to capture the data in the rollup index. For example, if your index pattern is `metricbeat-*`, you can name your rollup index `rollup-metricbeat`, but not `metricbeat-rollup`.

:::{image} /manage-data/images/kibana-management_create_rollup_job.png
:alt: Wizard that walks you through creation of a rollup job
:screenshot:
:::

## Start, stop, and delete rollup jobs [manage-rollup-job]

Once you’ve saved a rollup job, you’ll see it the **Rollup Jobs** overview page, where you can drill down for further investigation. The **Manage** menu enables you to start, stop, and delete the rollup job. You must first stop a rollup job before deleting it.

:::{image} /manage-data/images/kibana-management_rollup_job_details.png
:alt: Rollup job details
:screenshot:
:::

You can’t change a rollup job after you’ve created it. To select additional fields or redefine terms, you must delete the existing job, and then create a new one with the updated specifications. Be sure to use a different name for the new rollup job—reusing the same name can lead to problems with mismatched job configurations. Refer to [rollup job configuration](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-put-job).


## Try it: Create and visualize rolled up data [rollup-data-tutorial]

This example creates a rollup job to capture log data from sample web logs. Before you start, [add the web logs sample data set](/explore-analyze/index.md).

In this example, you want data that is older than 7 days in the `kibana_sample_data_logs` index to roll up into the `rollup_logstash` index. You’ll bucket the rolled up data on an hourly basis, using `60m` for the time bucket configuration.

For this example, the job will perform the rollup every minute. However, you’d typically roll up less frequently in production.


### Create the rollup job [_create_the_rollup_job]

As you walk through the **Create rollup job** UI, enter the data:

| **Field** | **Value** |
| --- | --- |
| Name | `logs_job` |
| Index pattern | `kibana_sample_data_logs` |
| Rollup index name | `rollup_logstash` |
| Frequency | Every minute |
| Page size | 1000 |
| Latency buffer | 7d |
| Date field | @timestamp |
| Time bucket size | 60m |
| Time zone | UTC |
| Terms | geo.src, machine.os.keyword |
| Histogram | bytes, memory |
| Histogram interval | 1000 |
| Metrics | bytes (average) |

On the **Review and save** page, click **Start job now** and **Save**.

The terms, histogram, and metrics fields reflect the key information to retain in the rolled up data: where visitors are from (geo.src), what operating system they are using (machine.os.keyword), and how much data is being sent (bytes).

You can now use the rolled up data for analysis at a fraction of the storage cost of the original index. The original data can live side by side with the new rollup index, or you can remove or archive it using [{{ilm}} ({{ilm-init}})](/manage-data/lifecycle/index-lifecycle-management.md).


### Visualize the rolled up data [_visualize_the_rolled_up_data]

Your next step is to visualize your rolled up data in a vertical bar chart. Most visualizations support rolled up data, with the exception of Timelion and Vega visualizations.

1. Go to the **Data Views** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create data view**, and select **Rollup data view** from the dropdown.
3. Enter **rollup_logstash,kibana_sample_logs** as your **Data View** and `@timestamp` as the **Time Filter field name**.

    The notation for a combination data view with both raw and rolled up data is `rollup_logstash,kibana_sample_data_logs`. In this data view, `rollup_logstash` matches the rollup index and `kibana_sample_data_logs` matches the raw data.

4. Go to **Dashboards**, then select **Create dashboard**.
5. Set the [time filter](../../../explore-analyze/query-filter/filtering.md) to **Last 90 days**.
6. On the dashboard, click **Create visualization**.
7. Choose `rollup_logstash,kibana_sample_data_logs` as your source to see both the raw and rolled up data.

    :::{image} /manage-data/images/kibana-management-create-rollup-bar-chart.png
    :alt: Create visualization of rolled up data
    :screenshot:
    :::

8. Select **Bar** in the chart type dropdown.
9. Add the `@timestamp` field to the **Horizontal axis**.
10. Add the `bytes` field to the **Vertical axis**, defaulting to an `Average of bytes`.

    {{kib}} creates a vertical bar chart of your data. Select a section of the chart to zoom in.

    :::{image} /manage-data/images/kibana-management_rollup_job_dashboard.png
    :alt: Dashboard with rolled up data
    :screenshot:
    :::
