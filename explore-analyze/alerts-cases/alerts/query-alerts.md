---
navigation_title: How to query alert indices
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/query-alerts.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# How to query alert indices [view-alerts]

## Index Names

On **Serverless** alerts are stored in [datastreams](https://www.elastic.co/docs/manage-data/data-store/data-streams), on on-prem and Elastic Cloud Hosted (ECH) they are stored in the indices.

All the alert index names consist of 5 parts:

All of them start with `.internal.alerts-` prefix.
Then the `context`, `dataset`, `space-Id` and `version number` parts follow it.

An index name template:<br>
`.internal.alerts-{{context}}.{{dataset}}-{{space-id}}-{{version-number}}`

<blockquote>
<br>

**context:** Usually the product group that the rule type belongs to. Such as Stack, Observability and Security.

**dataset:** “alert” for the alert indices.

**space-id:** Only the security rules are space-specific. All the other rules write into default for all spaces.

**version-number:** This starts from 000001 and gets increased by 1 as the index is rolled over
<br><br>

</blockquote>

An example alert index name of the Elasticsearch Query rule:<br>
**.internal.alerts-stack.alerts-default-000001**

## Index aliases

All the alert indices have an alias too.

They start with `.alerts` prefix, then `context`, `dataset`, `space-Id` follows it.

Alias template:<br>
`.alerts-{{context}}.{{dataset}}-{{space-id}}`

An example alias for the Elasticsearch Query rule index:<br>
`.alerts-stack.alerts-default`

**Note:** Only the security rules are space-specific, other rule types use the `default` space.

<hr>

You can find the index names and aliases per rule type in the below table.

| Index name / Alias                                                                                                                                                                                                          | Rules                                                                                                                                                                                                                                                                                                                                                                                                      |
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

## Queries

You can simply search for an alert by using `.internal.alerts-*` **index pattern** or the **index alias**.
<br><br>

### To get all the alerts:

The below query returns top 100 alerts you have from all the alert indices you have.

```json
GET /.internal.alerts-*/_search
{
 "query": {
   "match_all": {}
 },
 "size":100
}
```

### To get mapping of an alert index:

An example for the Elasticsearch query rule:

With its index name:

```json
GET /.internal.alerts-stack.alerts-default-000001/_mapping
```

Or with its alias:

```
GET /.alerts-stack.alerts-default/_mapping
```

### To get only the active/recovered alerts

Replace the `kibana.alert.status` value with recovered for the recovered alerts

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

### To query the alerts of a specific rule

Replace the `kibana.alert.rule.uuid` value with your rule id

```json
GET /.internal.alerts-*/_search
{
 "size": 100,
 "query": {
   "bool": {
     "filter": [
       { "term": { "kibana.alert.rule.uuid": "--your-rule-id--" } }
     ]
   }
 }
}
```

### To query the alerts that are generated within a specific time window

Replace the `kibana.alert.status` value with recovered for the recovered alerts

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

### To query the alerts of a specific rule type

Replace the `kibana.alert.rule.category` value with your rule type name

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
