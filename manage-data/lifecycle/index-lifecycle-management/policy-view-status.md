---
navigation_title: View the lifecycle status of an index or data stream
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-lifecycle-policy.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# View the lifecycle status of an index or data stream [view-lifecycle-status]

For any existing managed index or data stream in your cluster, you can access the {{ilm-init}} policy applied to it and its current status.

You can view the lifecycle status of an index or data stream in {{kib}} or using the {{es}} API.

:::{tip}
If you're investigating an {{ilm-init}}-related problem, refer to [Troubleshoot index and snapshot lifecycle management](/troubleshoot/elasticsearch/start-ilm.md) and [Fix index lifecycle management errors](/troubleshoot/elasticsearch/index-lifecycle-management-errors.md) in the {{es}} chapter of the **Troubleshoot** section.
:::

:::::{tab-set}
:group: kibana-api
::::{tab-item} {{kib}}
:sync: kibana
**To view the current lifecycle status for one or more indices:**

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Open the **Indices** tab.
1. Enable **Include hidden indices** to view all indices, including those managed by ILM. If you're using data streams, you can find the data stream associated with any index listed in the **Data stream** column.
1. Use the search tool to find the index you're looking for. You can also filter the results by lifecycle status and lifecycle phase.
1. Select the index to view details.
1. Open the **Index lifecycle** tab to view ILM details such as the current lifecycle phase, the ILM policy name, the current [index lifecycle action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md), and other details.

   ![Index lifecycle status page](/manage-data/images/elasticsearch-reference-ilm-status.png "")

:::{tip}
{{es}} comes with many built-in ILM policies. For standard Observability or Security use cases, you will have two {{ilm-init}} policies configured automatically: `logs@lifecycle` for logs and `metrics@lifecycle` for metrics.

To learn how to create and adjust copies of built-in {{ilm-init}} policies for managed data streams, such as those created when you install an Elastic Integration, refer to our tutorial [](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md).
:::

**To view the current lifecycle status for a datastream:**

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Open the **Data Streams** tab.
1. Use the search tool to find the data stream you're looking for.
1. Select the data stream to view details. The flyout that opens includes direct links to the ILM policy and the index template.

   ![Data stream status page](/manage-data/images/elasticsearch-reference-datastream-status.png "")


**To view the current lifecycle status for a datastream on the Streams page:** {applies_to}`"stack": "ga 9.2, preview 9.1"` 

Starting with {{stack}} version 9.2, the [**Streams**](/solutions/observability/streams/streams.md) page provides a centralized interface for common data management tasks in {{kib}}.

1. Go to the **Streams** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. A stream maps directly to an {{es}} data stream. Select a stream to view its details.
1. Go to the **Retention** tab to see how long your stream retains data and to get insight into your stream's data ingestion and storage size. A stream can retain the data indefinitely, for a custom period, or by following an existing ILM policy. For more information, refer to [](/solutions/observability/streams/management/retention.md).

::::

:::{tab-item} API
:sync: api
Use the [Explain the lifecycle state API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-explain-lifecycle) to view the current lifecycle status for an index:

```console
GET .ds-metrics-system.process-default-2025.06.04-000001/_ilm/explain
```

Tthe API response shows the current ILM phase and other details:

```json
{
  "indices": {
    ".ds-metrics-system.process-default-2025.06.04-000001": {
      "index": ".ds-metrics-system.process-default-2025.06.04-000001",
      "managed": true,
      "policy": "metrics",
      "index_creation_date_millis": 1749060710358,
      "time_since_index_creation": "22.91d",
      "lifecycle_date_millis": 1749060710358,
      "age": "22.91d",
      "phase": "hot",
      "phase_time_millis": 1749060711038,
      "action": "rollover",
      "action_time_millis": 1749060712038,
      "step": "check-rollover-ready",
      "step_time_millis": 1749060712038,
      "phase_execution": {
        "policy": "metrics",
        "phase_definition": {
          "min_age": "0ms",
          "actions": {
            "rollover": {
              "max_age": "30d",
              "max_primary_shard_docs": 200000000,
              "min_docs": 1,
              "max_primary_shard_size": "50gb"
            }
          }
        },
        "version": 1,
        "modified_date_in_millis": 1749059754363
      }
    }
  }
}
```

You can also call this API for a data stream:

```console
GET metrics-system.process-default/_ilm/explain
```

When called for a data stream, the API retrieves the current lifecycle status for the stream's backing indices:

```json
{
  "indices": {
    ".ds-metrics-system.process-default-2025.06.04-000001": {
      "index": ".ds-metrics-system.process-default-2025.06.04-000001",
      "managed": true,
      "policy": "metrics",
      "index_creation_date_millis": 1749060710358,
      "time_since_index_creation": "22.91d",
      "lifecycle_date_millis": 1749060710358,
      "age": "22.91d",
      "phase": "hot",
      "phase_time_millis": 1749060711038,
      "action": "rollover",
      "action_time_millis": 1749060712038,
      "step": "check-rollover-ready",
      "step_time_millis": 1749060712038,
      "phase_execution": {
        "policy": "metrics",
        "phase_definition": {
          "min_age": "0ms",
          "actions": {
            "rollover": {
              "max_age": "30d",
              "max_primary_shard_docs": 200000000,
              "min_docs": 1,
              "max_primary_shard_size": "50gb"
            }
          }
        },
        "version": 1,
        "modified_date_in_millis": 1749059754363
      }
    }
  }
}
```
::::
:::::