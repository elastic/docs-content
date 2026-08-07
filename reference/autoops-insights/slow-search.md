---
navigation_title: Slow search
description: Describes what AutoOps detects and surfaces with the Slow search insight for sustained high search latency, including customization settings, example event content, and recommendations.
applies_to:
  deployment:
    ech: ga
    self: ga
    ece: ga
    eck: ga
products:
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elasticsearch
---

# Slow search [autoops-slow-search]

The **Slow search** insight is triggered when AutoOps detects search latency to be higher than your configured threshold for multiple consecutive samples. You might experience sluggish dashboards and API calls before requests start to fail.

## Insight details

| Field | Value |
| --- | --- |
| Component | {{es}} |
| Key | `SLOW_SEARCH` |
| Severity | High |
| Scope | Node |
| Domains | Performance, search |

## Customization settings

You can customize the thresholds for this insight to adjust when AutoOps detects the issue and surfaces it. Refer to [](/deploy-manage/monitor/autoops/ec-autoops-event-settings.md) for details.

The default customization settings are:

| Setting | Type | Default |
| --- | --- | --- |
| Search latency threshold (ms) | Integer | 250 |
| Consecutive samples above threshold | Integer | 5 |

:::{tip}
Raising these thresholds reduces noise but delays detection. Lowering them triggers the insight sooner but can increase alerts during minor blips.
:::

## Example: what you might see in AutoOps

The following is an example of what you might see when this insight is triggered. Real insights use live data and links from your deployment or cluster.

### Slow search detected on `es-data-01`

#### What was detected

Search latency on `es-data-01` and `es-data-02` stayed above your configured threshold for enough consecutive samples. Peak latency in the latest sample was 420 ms.

* Indices with high search activity: `logs-prod-000045`
* Indices with high indexing activity on the same node: `logs-prod-000045`

Review query logs or search slow logs on the affected node, tune expensive queries, and check CPU, heap, and indexing load on the same node if latency stays high.

#### Recommendations

:::{note}
AutoOps shows different recommendations depending on how their conditions match your deployment or cluster.
:::

::::{dropdown} Add replica for indices
**Condition**: Shown when the replica count is less than the number of data nodes minus one.

Set the replica count to `12` for `logs-prod-000045` with the [update index settings API]({{es-apis}}operation/operation-indices-put-settings):

```console
PUT logs-prod-000045/_settings
{
  "index": {
    "number_of_replicas": 12
  }
}
```

:::{note}
Requires the `manage` index privilege. This action changes index configuration.
:::
::::

::::{dropdown} Review query logs
**Condition**: Shown when query logging is available on the deployment or cluster ({{es}} version 9.4 or above).

Check the query logs on the affected node to identify long-running or expensive search queries. Query logs provide structured, per-query timing with less overhead than search slow logs. Set an appropriate threshold and review the top queries to tune or reroute the most expensive ones.

For setup and configuration, refer to [](/deploy-manage/monitor/logging-configuration/query-logs.md).
::::

::::{dropdown} Review search slow logs
**Condition**: Shown when query logging is not available on the deployment or cluster (below {{es}} version 9.4).

Check your search slow log file to identify slow-running searches. To activate slow logging, follow [](/deploy-manage/monitor/logging-configuration/slow-logs.md).

For example:

```console
PUT logs-prod-000045/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.query.debug": "2s",
  "index.search.slowlog.threshold.query.trace": "500ms",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.search.slowlog.threshold.fetch.info": "800ms",
  "index.search.slowlog.threshold.fetch.debug": "500ms",
  "index.search.slowlog.threshold.fetch.trace": "200ms"
}
```

:::{note}
Requires the `manage` index privilege. This action changes index configuration.
:::
::::

::::{dropdown} Add data node
**Condition**: Shown when an index has more than twice as many primary and replica shards as available data nodes.

Add a data node to increase search parallelism and capacity. For guidance on sizing and scaling, refer to [](/deploy-manage/production-guidance/scaling-considerations.md). For {{ech}}, you can also [customize deployment components](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md).
::::

#### Background and impact

Common causes of sustained high search latency include expensive or repeated queries, CPU or heap pressure, heavy indexing on the same node, and background work such as segment merges or snapshots.
