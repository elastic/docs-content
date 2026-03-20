---
navigation_title: Query alert indices
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Query alert indices [query-alert-indices-kibana]

This page explains how you should query alert indices when building rule queries, custom dashboards, or visualizations. It also lists index names and aliases by rule type and includes sample {{es}} queries for common cases. For field definitions shared by alert documents, review the [Alert schema](/reference/security/fields-and-object-schemas/alert-schema.md). For {{elastic-sec}} detection alerts only, see [Query alert indices](/solutions/security/detect-and-alert/query-alert-indices.md).

::::{important}

System indices, such as the alert indices, contain important configuration and internal data; do not change their mappings. Changes can lead to rule execution and alert indexing failures. Use [runtime fields](../../../manage-data/data-store/mapping/define-runtime-fields-in-search-request.md) at query time instead, which allow you to derive fields from existing alert documents without altering the index mapping.

::::


## Alert index aliases [_alert_index_aliases]

We recommend querying index aliases rather than backing indices directly. Alias names begin with the `.alerts-` prefix, then include the `context`, `dataset`, and `space-id` parts:

```shell
.alerts-{{context}}.{{dataset}}-{{space-id}}
```

For example, the alias for a sample {{es}} Query rule is:

```shell
.alerts-stack.alerts-default
```

To search across alerts from all contexts, use the `.alerts-*` pattern. You can narrow queries to a specific alias when you know the rule type (see the [table below](#_index_names_and_aliases_for_rule_types)).

::::{note}
{{elastic-sec}} rules are space-specific, and the space ID appears in the alias (for example, `.alerts-security.alerts-{{your-space-id}}`). All other rule types use the default space in the alias name.
::::


## Alert indices [_alert_indices]

For additional context, alert events are stored in hidden {{es}} indices on **self-managed** {{stack}} deployments and {{ech}}. On {{serverless-short}}, they are stored in [data streams](../../../manage-data/data-store/data-streams.md). We do not recommend querying these indices directly.

The naming convention for backing indices is:

```shell
.internal.alerts-{{context}}.{{dataset}}-{{space-id}}-{{version-number}}
```

`version-number` identifies the index generation; it starts at `000001` and increments by 1 when the index rolls over.

Each part of the name:

* **`.internal.alerts-` prefix:** Present on all alert backing index names.
* **`context`:** The product group for the rule type (for example {{stack-manage-app}}, {{observability}}, or {{elastic-sec}}).
* **`dataset`:** The `alerts` dataset segment in the index name.
* **`space-id`:** The {{kib}} space the index was created for. {{elastic-sec}} rules are space-specific; other rules use the default space in the index name.


## Index names and aliases for rule types [_index_names_and_aliases_for_rule_types]

The following table lists the index names and aliases associated with each rule type.

| Index name and alias                                                                                                                                                                                                          | Rule type                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <br> `default` <br><br> **Index name:** <br> `.internal.alerts-default.alerts-default-000001` <br><br> **Alias:**<br>`.alerts-default.alerts-default` <br><br><br><br><br><br><br><br><br><br>                              | <br> **STACK MONITORING** <br><br> CCR read exceptions, <br> Cluster health, <br>CPU Usage, <br> Disk Usage, <br> Elasticsearch version mismatch, <br> Kibana version mismatch, <br> License expiration, <br> Logstash version mismatch, <br> Memory Usage (JVM), <br> Missing monitoring data, <br> Nodes changed, <br> Shard size, <br> Thread pool search rejections, <br> Thread pool write rejections |
| `stack` <br><br> **Index name:**<br> `.internal.alerts-stack.alerts-default-000001` <br><br> **Alias:**<br> `.alerts-stack.alerts-default`                                                                                  | **STACK ALERTS** <br><br> Elasticsearch query, <br> Index threshold, <br> Degraded docs, <br> Tracking containment, <br> Transform health                                                                                                                                                                                                                                                                  |
| <br> `Observability.apm` <br><br> **Index name:** <br> `.internal.alerts-observability.apm.alerts-default-000001` <br><br> **Alias:**<br> `.alerts-observability.apm.alerts-default`                                        | <br> **APM AND USER EXPERIENCE** <br><br> APM Anomaly, <br> Error count threshold, <br> Failed transaction rate threshold,<br> Latency threshold <br><br> <br>                                                                                                                                                                                                                                             |
| <br> `ml.anomaly-detection-health` <br><br>**Index name:**<br>`.internal.alerts-ml.anomaly-detection-health.alerts-default-000001`<br><br> **Alias:**<br>`.alerts-ml.anomaly-detection-health.alerts-default`               | <br> **MACHINE LEARNING** <br> <br> Anomaly detection jobs health <br><br><br> <br><br>                                                                                                                                                                                                                                                                                                                    |
| <br> `ml.anomaly-detection` <br><br> **Index name:**<br> `.internal.alerts-ml.anomaly-detection.alerts-default-000001`<br><br>**Alias:**<br>`.alerts-ml.anomaly-detection.alerts-default`                                   | **MACHINE LEARNING** <br><br> Anomaly detection <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                       |
| <br> `ml.observability.uptime`<br><br> **Index name:**<br> `.internal.alerts-stack.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-stack.alerts-default`                                                             | <br> **SYNTHETICS AND UPTIME**<br><br> Synthetics monitor status,<br> Synthetics TLS certificate <br> <br> <br> <br>                                                                                                                                                                                                                                                                                       |
| <br> `ml.observability.metrics`<br><br> **Index name:**<br> `.internal.alerts-ml.observability.metrics.alerts-default-000001` <br><br> **Alias:** <br> `.alerts-ml.observability.metrics.alerts-default`                    | <br> **INFRASTRUCTURE** <br><br>Metric threshold, <br>Inventory<br><br><br><br><br>                                                                                                                                                                                                                                                                                                                        |
| <br> `ml.observability.threshold`<br><br> **Index name:**<br> `.internal.alerts-ml.observability.threshold.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.observability.threshold.alerts-default`                | <br> **OBSERVABILITY**<br><br> Custom Threshold <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                       |
| <br> `ml.observability.slo`<br><br> **Index name:**<br> `.internal.alerts-ml.observability.slo.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.observability.slo.alerts-default`                                | <br> **SLOs**<br><br> SLO burn rate <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                                   |
| <br> `ml.observability.logs`<br><br> **Index name:**<br> `.internal.alerts-ml.observability.logs.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.observability.logs.alerts-default`                                 | <br> **LOGS**<br><br> Log Threshold <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                                   |
| <br> `ml.dataset.quality`<br><br> **Index name:**<br> `.internal.alerts-ml.dataset.quality.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.dataset.quality.alerts-default`                                        | <br> Degraded docs <br><br><br><br><br><br> <br>                                                                                                                                                                                                                                                                                                                                                           |
| <br> `ml.streams`<br><br> **Index name:**<br> `.internal.alerts-ml.streams.alerts-default-000001`<br><br>**Alias:**<br>`.alerts-ml.streams.alerts-default`                                                                  | <br> **STREAMS** <br><br> ES\|QL Rule <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                                 |
| <br> `security.attack.discovery`<br><br> **Index name:**<br> `.internal.alerts-security.attack.discovery.alerts-{{your-space-id}}-000001`<br><br>**Alias:**<br>`.alerts-security.attack.discovery.alerts-{{your-space-id}}` | <br> **SECURITY** <br><br> Attack Discovery Schedule <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                  |
| <br> `security`<br><br> **Index name:**<br> `.internal.alerts-security.alerts-{{your-space-id}}-000001`<br><br>**Alias:**<br>`.alerts-security.alerts-{{your-space-id}}`                                                    | <br> **SECURITY** <br><br> All the other security rules <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                               |

## Sample queries [_sample_queries]

The examples below use the `.internal.alerts-*` index pattern or the `.alerts-*` alias pattern. Prefer aliases for production queries when possible.

### Get all the alerts

The following query returns the top 100 alerts from all alert indices.

```json
GET /.internal.alerts-*/_search
{
 "query": {
   "match_all": {}
 },
 "size":100
}
```

### Retrieve alert index mappings

The following sample request retrieves index mappings for a sample {{es}} rule:

```json
GET /.internal.alerts-stack.alerts-default-000001/_mapping
```

If you want to use the alias instead, use:

```shell
GET /.alerts-stack.alerts-default/_mapping
```

### Only get active and recovered alerts

The following sample request retrieves 100 recovered alerts:

```json
GET /.internal.alerts-*/_search
{
 "query": {
   "bool": {
     "filter": [{ "term": { "kibana.alert.status": "recovered" } }]
   }
 },
 "size": 100
}
```

The following sample request retrieves 100 active alerts:

```json
GET /.internal.alerts-*/_search
{
 "query": {
   "bool": {
     "filter": [{ "term": { "kibana.alert.status": "active" } }]
   }
 },
 "size": 100
}
```

### Query alerts generated by a specific rule

The following sample request searches for alerts generated by a rule with the UUID `0cc8ed92-cbe6-42bd-800b-19ba5134ffd2`.

```json
GET /.internal.alerts-*/_search
{
 "size": 100,
 "query": {
   "bool": {
     "filter": [
       { "term": { "kibana.alert.rule.uuid": "0cc8ed92-cbe6-42bd-800b-19ba5134ffd2" } }
     ]
   }
 }
}
```

### Search alerts that are generated within a specific time window

The following sample request searches for alerts that were generated during the last hour and have the `recovered` status:

```json
GET /.internal.alerts-*/_search
{
 "query": {
   "bool": {
     "filter": [
       { "term":  { "kibana.alert.status": "recovered"}},
       {
         "range": {
           "@timestamp": {
             "gte": "now-60m",
             "lte": "now"
           }
         }
       }
     ]
   }
 },
 "size": 100
}
```

### Query the alerts of a specific rule type

The following sample request searches for 100 alerts that were generated by the {{es}} rule type:

```json
GET /.internal.alerts-*/_search
{
 "query": {
   "bool": {
     "filter": [
       { "term":  { "kibana.alert.rule.category": "Elasticsearch query"}}
     ]
   }
 },
 "size": 100
}
```
