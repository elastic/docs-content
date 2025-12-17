---
navigation_title: Query alert indices
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Query alert indices [how-to-query-alert-indices]

This page explains how to query alert indices, which you can use while building rule queries, custom dashboards, or visualizations. It also breaks down the components of alert index and alias names, lists alerts indices and aliases for each rule type, and provides sample queries for common use cases. 

::::{note} 
On **self-managed** {{stack}} deployments and {{ech}}, alerts are stored in {{es}} indices. On {{serverless-short}}, they are stored in [data streams](../../../manage-data/data-store/data-streams.md).
::::

## Understand the index name structure

Alert index names are divided into five parts. They begin with the `.internal.alerts-` prefix, and then include the `context`, `dataset`, `space-id`, and `version number` parts. For example:

```shell
    .internal.alerts-{{context}}.{{dataset}}-{{space-id}}-{{version-number}}
```

Here is the alert index name of a sample {{es}} Query rule:

```shell
    .internal.alerts-stack.alerts-default-000001
```

Each part of the index name is explained in more detail below:

* `.internal.alerts-` prefix: All alert index names start with this prefix.

* `context`: Identifies the product group that the rule type belongs to, such as {{stack-manage-app}}, {{observability}} and {{elastic-sec}}.

* `dataset`: The "alert" for the alert indices.

* `space-id`: The ID of the space that the index was created for. 

    ::::{note} 
    {{elastic-sec}} rules are space-specific. All the other rules use the default space in the index name.
    ::::

* `version-number`: Identifies the version of index. Version numbers start at 000001 and are incremented by 1 when the index rolls over.

## Understand the index alias name structure

Alert indices also have aliases, which are automatically created. Alias names begin with the `.alerts-` prefix, and then include the `context`, `dataset`, and `space-id` parts. For example:

```shell
    .alerts-{{context}}.{{dataset}}-{{space-id}}
```

Here is the alert index alias of a sample {{es}} Query rule:

```shell
    .alerts-stack.alerts-default
```

::::{note} 
{{elastic-sec}} rules are space-specific. All the other rules use the default space in the alias name.
::::

## Index names and aliases for rule types

The following table lists the index names and aliases that are associated with each rule type.

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
| <br> `ml.observability.slo`<br><br> **Index name:**<br> `.internal.alerts-ml.observability.logs.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.observability.logs.alerts-default`                                | <br> **SLOs**<br><br> SLO burn rate <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                                   |
| <br> `ml.observability.logs`<br><br> **Index name:**<br> `.internal.alerts-ml.observability.slo.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.observability.slo.alerts-default`                                 | <br> **LOGS**<br><br> Log Threshold <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                                   |
| <br> `ml.dataset.quality`<br><br> **Index name:**<br> `.internal.alerts-ml.dataset.quality.alerts-default-000001`<br><br> **Alias:**<br> `.alerts-ml.dataset.quality.alerts-default`                                        | <br> Degraded docs <br><br><br><br><br><br> <br>                                                                                                                                                                                                                                                                                                                                                           |
| <br> `ml.streams`<br><br> **Index name:**<br> `.internal.alerts-ml.streams.alerts-default-000001`<br><br>**Alias:**<br>`.alerts-ml.streams.alerts-default`                                                                  | <br> **STREAMS** <br><br> ES\|QL Rule <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                                 |
| <br> `security.attack.discovery`<br><br> **Index name:**<br> `.internal.alerts-security.attack.discovery.alerts-{{your-space-id}}-000001`<br><br>**Alias:**<br>`.alerts-security.attack.discovery.alerts-{{your-space-id}}` | <br> **SECURITY** <br><br> Attack Discovery Schedule <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                                  |
| <br> `security`<br><br> **Index name:**<br> `.internal.alerts-security.alerts-{{your-space-id}}-000001`<br><br>**Alias:**<br>`.alerts-security.alerts-{{your-space-id}}`                                                    | <br> **SECURITY** <br><br> All the other security rules <br><br><br><br><br>                                                                                                                                                                                                                                                                                                                               |

## Sample queries

Search for alerts by querying the `.internal.alerts-*` index pattern or the `.alerts-*` index alias. Sample queries for common use cases are provided in the following sections.

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

If you wanted to use the alias instead, you would modify the request like so:

```
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