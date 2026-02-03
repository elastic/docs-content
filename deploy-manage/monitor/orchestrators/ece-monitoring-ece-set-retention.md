---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-ece-set-retention.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Set the retention period for logging and metrics indices [ece-monitoring-ece-set-retention]

{{ece}} sets up index lifecycle management (ILM) policies for the [ECE platform monitoring](./ece-platform-monitoring.md) data it collects inside the `logging-and-metrics` [system deployment](/deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md).

By default, metrics indices are retained for one day and logging indices for seven days, as defined in the `ece_metrics` and `ece_logs` ILM policies of the deployment. These default policies and their associated index templates are managed by {{ece}} and should not be modified.

You might need to adjust the retention period for one of the following reasons:

* If your business requires you to retain logs and metrics for longer than the default period.
* If the volume of logs and metrics collected is high enough to require reducing the amount of storage space consumed.

## Available index templates [available-templates]

The following list contains the most relevant index templates and data stream names in the ECE `logging-and-metrics` system deployment. You can check the entire list directly in {{kib}} **Index Management -> Index templates** page:

| Index template and data stream name              | Default ILM policy                                | Description |
|--------------------------------------------------|---------------------------------------------------|-------------|
| cluster-logs-<version>                           | ece_logs                      | Logs from all deployments managed by ECE |
| proxy-logs-<version>                             | ece_logs                      | ECE proxy logs |
| service-logs-<version>                           | ece_logs                      | Logs produced by internal ECE services |
| metricbeat-<version>                             | ece_metrics                   | Metrics from all containers and hosts |
| allocator-metricbeat-<version>                   | ece_metrics                   | Metrics from the {{stack}} containers running in the allocators|

::::{note}
Index templates and data stream names include a `<version>` tag as part of their names. This version can change after an {{ece}} upgrade and must be taken into account when applying any type of customization.
::::

## Customize retention period

To customize the retention period for the different data streams, [create a new ILM policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) with the required settings, and apply it to the relevant data sets as follows:

1. In {{kib}}, go to **Index Management → Index Templates** and identify the template that applies to the data stream or indices whose retention you want to change. Refer to [Availble index templates](#available-templates) for a list of common templates.

2. Open the template’s contextual menu and select **Clone** to [create a new template](/manage-data/data-store/index-basics.md#index-management-manage-index-templates). When cloning the template:

    1. Assign a higher `priority` to the new template so it takes precedence over the default template.
    2. In the **Index settings** section, set `index.lifecycle.name` to the custom ILM policy with the required retention settings.

    ::::{note}
    Cloning an existing index template is recommended over creating one from scratch to ensure all required mappings and settings are preserved.
    ::::

3. Save the new template and verify that it differs from the default template only in the `priority` and `index.lifecycle.name` settings.

4. If you want the changes to take effect immediately, you can [manually roll over the associated data stream](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) using the [{{kib}} Console](/explore-analyze/query-filter/tools/console.md). For example:

    ```console
    POST /cluster-logs-<version>/_rollover/
    ```

    After the rollover completes, a new backing index is created using the cloned index template and is associated with the custom ILM policy. You can verify this by checking the data stream information:

    ```console
    GET _data_stream/cluster-logs-8.18.8
    ```

    :::::{dropdown} Response example
    ```json
    {
      "data_streams": [
        {
          "name": "cluster-logs-<version>",
          ...
          "indices": [
            {
              "index_name": ".ds-cluster-logs-<version>-<date>-000001",
              "index_uuid": "6hPZZ0YbTdaflfBZ9UkVUw",
              "prefer_ilm": true,
              "ilm_policy": "ece_logs", <1>
              "managed_by": "Index Lifecycle Management"
            },
            ...
            {
              "index_name": ".ds-cluster-logs-<version>-<date>-000002",
              "index_uuid": "rGrlk1_iR-as_ZM3iw6EFg",
              "prefer_ilm": true,
              "ilm_policy": "<NEW_ILM_POLICY>", <2>
              "managed_by": "Index Lifecycle Management"
            }
          ],
          "template": "<CLONED_TEMPLATE>", <3>
          "ilm_policy": "<NEW_ILM_POLICY>", <2>
          ...
        }
      ]
    }
    ```
    1. Previous backing indices remain associated with the original ILM policy.
    2. The `ilm_policy` for the new backing index and the data stream should match the custom ILM policy.
    3. The `template` value should match the name of the cloned index template.
    :::::

::::{important}
In {{ece}}, the names of default index templates and data streams include the version of the internal component that sends the data (for example, `cluster-logs-8.18.8`). After an {{ece}} upgrade, new templates and data stream names can be created with updated version numbers. When this happens, your cloned template might no longer apply, and you must repeat this procedure to ensure your custom ILM policy continues to be applied.
::::
