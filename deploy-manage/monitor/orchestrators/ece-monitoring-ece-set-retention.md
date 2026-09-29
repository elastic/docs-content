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

{{ece}} sets up {{ilm}} ({{ilm-init}}) policies for the [ECE platform monitoring](./ece-platform-monitoring.md) data it collects inside the `logging-and-metrics` [system deployment](/deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md).

By default, metrics indices are retained for two days and logging indices for eight days, as defined in the `ece_metrics` and `ece_logs` {{ilm-init}} policies of the deployment. This accounts for daily rollover plus the additional retention periods of one day for metrics and seven days for logs. These default policies and their associated index templates are managed by {{ece}} and should not be modified.

You might need to adjust the retention period for one of the following reasons:

* If your business requires you to retain logs and metrics for longer than the default period.
* If the volume of logs and metrics collected is high enough to require reducing the amount of storage space consumed.

::::{important}
Before increasing retention, ensure the `logging-and-metrics` system deployment has sufficient resources and disk capacity. Longer retention increases storage usage and cluster workload, and can result in a busy or overloaded cluster if the deployment is not scaled appropriately. Refer to [ECE system deployments configuration](/deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md) for more information.
::::

To customize the retention period, create a new {{ilm-init}} policy with the required settings and apply it to the target data streams. On ECE 4.1.1 or later, [apply it through a component template](#customize-retention-component-templates), which is the recommended approach. On earlier versions, you can [clone the relevant index template](#customize-retention-index-templates) and configure it to use your custom {{ilm-init}} policy, though this requires repeating the procedure after upgrades that change template names.

## Available index templates [available-templates]

The following list contains the names of the most relevant index templates and data streams in the ECE `logging-and-metrics` system deployment. You can check the entire list directly in {{kib}} on the **Index Management -> Index templates** page:

| Index template and data stream name              | Default ILM policy                                | Description |
|--------------------------------------------------|---------------------------------------------------|-------------|
| cluster-logs-<version>                           | ece_logs                      | Logs from all deployments managed by ECE |
| proxy-logs-<version>                             | ece_logs                      | ECE proxy logs |
| service-logs-<version>                           | ece_logs                      | Logs produced by internal ECE services |
| metricbeat-<version>                             | ece_metrics                   | Metrics from all containers and hosts |
| allocator-metricbeat-<version>                   | ece_metrics                   | Metrics from the {{stack}} containers running in the allocators|

::::{note}
Index templates and data streams include a `<version>` tag as part of their name. This corresponds to the {{stack}} version of the internal component that sends data into the cluster, for example, `proxy-logs-8.18.8`. This version can change after an {{ece}} upgrade and must be taken into account when you apply any type of customization.
::::

## Customize retention using component templates [customize-retention-component-templates]
```{applies_to}
deployment:
  ece: ga 4.1+
```

You can customize logs and metrics retention using a component template with a reserved name.

Each index template in the `logging-and-metrics` cluster includes a `composed_of` array that references these reserved names. If you create a matching component template, {{es}} merges its settings into new backing indices. The names do not include a version tag, so they continue to match after an ECE upgrade.

```{note}
This method is only available in ECE 4.1.1 or later.
```

The following component template names are reserved for customization. Define only the templates that match the scope you need:

| Component template | Applies to |
|---|---|
| `cluster-logs@custom` | `cluster-logs-<version>` data streams |
| `proxy-logs@custom` | `proxy-logs-<version>` data streams |
| `service-logs@custom` | `service-logs-<version>` data streams |
| `metricbeat@custom` | `metricbeat-<version>` data streams |
| `allocator-metricbeat@custom` | `allocator-metricbeat-<version>` data streams |
| `ece-logs@custom` | All logging data streams |
| `ece-metrics@custom` | All metrics data streams |
| `ece-all@custom` | All logging and metrics data streams |

If you define multiple `@custom` component templates, the most specific one takes precedence: an index-specific template (for example, `cluster-logs@custom`) overrides `ece-logs@custom`, which in turn overrides `ece-all@custom`.

To customize the retention period:

1. [Create a new {{ilm-init}} policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) with the required retention settings.

2. [Create a component template](/manage-data/data-store/templates.md#component-templates) using the name that matches your target scope, and set `index.lifecycle.name` to the {{ilm-init}} policy you created. You can do this from {{kib}} **Index Management → Component templates**, or from the [{{kib}} Console](/explore-analyze/query-filter/tools/console.md). For example, to apply a custom {{ilm-init}} policy to all `cluster-logs` data streams:

    ```console
    PUT _component_template/cluster-logs@custom
    {
      "template": {
        "settings": {
          "index.lifecycle.name": "<MY_CUSTOM_ILM_POLICY>"
        }
      }
    }
    ```

3. If you want the changes to take effect immediately, you can [manually roll over the associated data stream](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) using the [{{kib}} Console](/explore-analyze/query-filter/tools/console.md). For example:

    ```console
    POST /cluster-logs-<version>/_rollover/
    ```

## Customize retention by cloning index templates [customize-retention-index-templates]

::::{note}
This method works on all ECE versions but requires repeating the procedure after upgrades that change index template names. If you are on ECE 4.1.1 or later, use the [component template method](#customize-retention-component-templates) instead.
::::

To customize the retention period for the different data streams, [create a new {{ilm-init}} policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) with the required settings, and apply it to the relevant data sets as follows:

1. In {{kib}}, go to **Index Management → Index Templates** and identify the template that applies to the data stream or indices whose retention you want to change. Refer to [Available index templates](#available-templates) for a list of the most common templates.

2. Open the template's contextual menu and select **Clone** to [create a new template](/manage-data/data-store/templates.md). When cloning the template:

    1. Assign a higher `priority` to the new template so it takes precedence over the default template.
    2. In the **Index settings** section, set `index.lifecycle.name` to the custom {{ilm-init}} policy that has the required retention settings.

    ::::{note}
    Cloning an existing index template is recommended over creating one from scratch, so as to ensure that all required mappings and settings are preserved.
    ::::

3. Save the new template and verify that it differs from the default template only in the `priority` and `index.lifecycle.name` settings.

4. If you want the changes to take effect immediately, you can [manually roll over the associated data stream](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) using the [{{kib}} Console](/explore-analyze/query-filter/tools/console.md). For example:

    ```console
    POST /cluster-logs-<version>/_rollover/
    ```

    After the rollover completes, a new backing index is created using the new index template and is associated with the custom {{ilm-init}} policy. You can verify this by checking the data stream information:

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
    1. Previous backing indices remain associated with the original {{ilm-init}} policy.
    2. The `ilm_policy` for the new backing index and the data stream should match the custom {{ilm-init}} policy.
    3. The `template` value should match the name of the new index template.
    :::::

::::{important}
In {{ece}}, the names of default index templates and data streams include the {{stack}} version of the internal component that sends the data (for example, `cluster-logs-8.18.8`). After an {{ece}} upgrade, new templates and data stream names can be created with updated version numbers. When this happens, your cloned template might no longer apply, and you must repeat this procedure to ensure your custom {{ilm-init}} policy continues to be applied.
::::
