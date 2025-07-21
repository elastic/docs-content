---
navigation_title: View the lifecycle status of an index
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-lifecycle-policy.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# View the lifecycle status of an index [view-lifecycle-status]

For any existing managed index in your cluster, you can access the ILM policy applied to it and details such as its current phase.

:::::{tab-set}
:group: kibana-api
::::{tab-item} {{kib}}
:sync: kibana
**To view the current lifecycle status for one or more indices:**

1. Go to **Stack Management > Index Management** and open the **Indices** tab.
1. Enable **Include hidden indices** to view all indices, including those managed by ILM. Note that if you're using data streams, you can find the data stream associated with any index listed in the **Data stream** column.
1. Use the search tool to find the index you're looking for. You can also filter the results by lifecycle status and lifecycle phase.
1. Select the index to view details.
1. Open the **Index lifecycle** tab to view ILM details such as the current lifecycle phase, the ILM policy name, the current [index lifecycle action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md), and other details.

   ![Index lifecycle status page](/manage-data/images/elasticsearch-reference-ilm-status.png "")

:::{tip}
{{es}} comes with many built-in ILM policies. For standard Observability or Security use cases, you will have two {{ilm-init}} policies configured automatically: `logs@lifecycle` for logs and `metrics@lifecycle` for metrics.

To learn how to create a specialized ILM policy for any data stream, such as those created when you install an Elastic Integration, refer to our tutorial [Customize built-in policies](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md).
:::

**To view the current lifecycle status for a datastream:**

1. Go to **Stack Management > Index Management** and open the **Data Streams** tab.
1. Use the search tool to find the data stream you're looking for.
1. Select the data stream to view details. The flyout that opens includes direct links to the ILM policy and the index template.

   ![Data stream status page](/manage-data/images/elasticsearch-reference-datastream-status.png "")
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