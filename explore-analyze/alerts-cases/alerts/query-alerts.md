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

To search across alerts from all contexts, use the `.alerts-*` pattern. You can narrow queries to a specific alias when you know the rule type (see the [tables below](#_index_names_and_aliases_for_rule_types)).

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

The two tables below use the same **Context** values so you can match a rule type to both the recommended **alias** (for queries) and an **example backing index** (for debugging or mapping checks). Default {{kib}} space uses the `alerts-default` segment in names; {{elastic-sec}} uses your space ID instead—see [Alert index aliases](#_alert_index_aliases) and [Alert indices](#_alert_indices).

**Columns in the first table**

* **Context**: {{kib}}'s internal name for which alert index registration a rule type uses. For most rows, it's the same substring that appears after `.alerts-` in the alias (for example, `stack` in `.alerts-stack.alerts-default`). There is one exception: Synthetics and Uptime rules are registered under `ml.observability.uptime` but still write to the **`stack`** path (same alias and backing index as Stack rules).
* **Area**: The product or feature area those rules belong to (Stack monitoring, {{observability}}, {{elastic-sec}}, and so on). Use it when you are looking up indexes by what you are working on in the UI, not by the technical `context` string.
* **Index alias**: The name to use in searches and API calls. Prefer aliases over backing indices.
* **Rule types**: The rule types whose alerts are stored under that context.

**Columns in the second table**

* **Context**: Same **Context** value as the row in the first table.
* **Example backing index**: A typical first-generation backing index name (for example, suffix `-000001`). After rollover, the numeric suffix increases. Do not rely on a specific generation in automation; use the alias or a wildcard pattern when possible.

### Rule types and index aliases

| Context | Area | Index alias | Rule types |
| :--- | :--- | :--- | :--- |
| `default` | Stack monitoring | `.alerts-default.alerts-default` | CCR read exceptions; Cluster health; CPU usage; Disk usage; Elasticsearch version mismatch; Kibana version mismatch; License expiration; Logstash version mismatch; Memory usage (JVM); Missing monitoring data; Nodes changed; Shard size; Thread pool search rejections; Thread pool write rejections |
| `stack` | Stack rules | `.alerts-stack.alerts-default` | Elasticsearch query; Index threshold; Degraded docs; Tracking containment; Transform health |
| `Observability.apm` | APM | `.alerts-observability.apm.alerts-default` | APM Anomaly; Error count threshold; Failed transaction rate threshold; Latency threshold |
| `ml.anomaly-detection-health` | {{ml-app}} | `.alerts-ml.anomaly-detection-health.alerts-default` | Anomaly detection jobs health |
| `ml.anomaly-detection` | {{ml-app}} | `.alerts-ml.anomaly-detection.alerts-default` | Anomaly detection |
| `ml.observability.uptime` | Synthetics and Uptime | `.alerts-stack.alerts-default` (same alias as **Stack rules**) | Synthetics monitor status; Synthetics TLS certificate |
| `ml.observability.metrics` | Infrastructure | `.alerts-ml.observability.metrics.alerts-default` | Metric threshold; Inventory |
| `ml.observability.threshold` | {{observability}} | `.alerts-ml.observability.threshold.alerts-default` | Custom threshold |
| `ml.observability.slo` | SLOs | `.alerts-ml.observability.slo.alerts-default` | SLO burn rate |
| `ml.observability.logs` | Logs | `.alerts-ml.observability.logs.alerts-default` | Log threshold |
| `ml.dataset.quality` | Data set quality | `.alerts-ml.dataset.quality.alerts-default` | Degraded docs |
| `ml.streams` | Streams | `.alerts-ml.streams.alerts-default` | ES\|QL Rule |
| `security.attack.discovery` | {{elastic-sec}} | `.alerts-security.attack.discovery.alerts-{{your-space-id}}` | Attack Discovery Schedule |
| `security` | {{elastic-sec}} | `.alerts-security.alerts-{{your-space-id}}` | All other security detection rules |

### Example backing indices (first generation)

| Context | Example backing index |
| :--- | :--- |
| `default` | `.internal.alerts-default.alerts-default-000001` |
| `stack` | `.internal.alerts-stack.alerts-default-000001` |
| `Observability.apm` | `.internal.alerts-observability.apm.alerts-default-000001` |
| `ml.anomaly-detection-health` | `.internal.alerts-ml.anomaly-detection-health.alerts-default-000001` |
| `ml.anomaly-detection` | `.internal.alerts-ml.anomaly-detection.alerts-default-000001` |
| `ml.observability.uptime` | `.internal.alerts-stack.alerts-default-000001` (same backing index as **`stack`**) |
| `ml.observability.metrics` | `.internal.alerts-ml.observability.metrics.alerts-default-000001` |
| `ml.observability.threshold` | `.internal.alerts-ml.observability.threshold.alerts-default-000001` |
| `ml.observability.slo` | `.internal.alerts-ml.observability.slo.alerts-default-000001` |
| `ml.observability.logs` | `.internal.alerts-ml.observability.logs.alerts-default-000001` |
| `ml.dataset.quality` | `.internal.alerts-ml.dataset.quality.alerts-default-000001` |
| `ml.streams` | `.internal.alerts-ml.streams.alerts-default-000001` |
| `security.attack.discovery` | `.internal.alerts-security.attack.discovery.alerts-{{your-space-id}}-000001` |
| `security` | `.internal.alerts-security.alerts-{{your-space-id}}-000001` |

:::{note}
For {{elastic-sec}}, replace `{{your-space-id}}` with your {{kib}} space ID. Synthetics and Uptime alerts use the **stack** backing index and alias as Stack rules, not a separate `ml.observability.uptime` index name.
:::

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
