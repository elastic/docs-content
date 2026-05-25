---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create threshold rules to alert when the number of matching events exceeds a specified count within a rule run.
---

# Threshold rules [threshold-rule-type]

## Overview

Threshold rules search your {{es}} indices and generate an alert when the number of events matching a query meets or exceeds a specified threshold within a single rule execution. Optionally, events can be grouped by one or more fields so that each unique combination is evaluated independently.

### When to use a threshold rule

Threshold rules are the right fit when:

* You want to detect **volume-based anomalies**, such as a brute-force attack (many failed logins from a single source IP) or a data exfiltration attempt (an unusually high number of outbound connections).
* The signal is not a single event but a **count crossing a boundary** within a time window.
* You need to group counts by fields like `source.ip`, `user.name`, or `destination.ip` and alert on each group independently.

Threshold rules are **not** the best fit when:

* A single matching event is sufficient. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) instead.
* You need to detect a specific **order** of events. Use an [EQL rule](/solutions/security/detect-and-alert/eql.md) instead.
* You need full aggregation pipelines with transformations. Use an [{{esql}} rule](/solutions/security/detect-and-alert/esql.md) instead.

### Data requirements

Threshold rules require at least one {{es}} index pattern or {{data-source}}. The data should contain the fields you plan to group by and enough event volume for meaningful threshold evaluation.

<!-- CRAFT LAYER - COMMENTED OUT FOR REVIEW
## Writing effective threshold rules [craft-threshold]

### Choosing Group by fields

The **Group by** field determines how events are bucketed before counting. Select fields that represent the entity you want to monitor:

* **Single field:** `source.ip` with a threshold of `100` alerts on any source IP that generates 100 or more matching events.
* **Multiple fields:** `source.ip, destination.ip` with a threshold of `10` alerts on every unique source-destination pair that appears at least 10 times.
* **No field:** Omit **Group by** to count all matching events together. The rule fires when the total count meets the threshold.

### Adding cardinality constraints

Use the **Count** field to add a cardinality requirement. This is useful when volume alone is not enough and you need to ensure diversity across a field.

For example, with **Group by** set to `source.ip`, **Threshold** set to `5`, and **Count** limiting by `destination.port` >= `3`, an alert fires only for source IPs that connect to at least three unique destination ports across five or more events. This pattern surfaces port-scanning behavior while filtering out noisy but benign repeated connections.

### Understanding threshold alerts

Threshold alerts are **synthetic**. They do not contain the original source document fields:

* Only the **Group by** fields and the count appear in the alert.
* All other source fields are omitted because they can vary across the counted documents.
* The actual count is available in `kibana.alert.threshold_result.count`.
* The grouped field values are in `kibana.alert.threshold_result.terms`.

Keep this in mind when configuring severity overrides, risk score overrides, or rule name overrides, as only the aggregated fields contain usable data.

### Best practices

* **Set thresholds conservatively at first.** Start with a higher threshold to understand baseline volumes, then lower it as you tune out false positives.
* **Combine with additional look-back time.** A look-back buffer of at least 1 minute helps avoid gaps between executions.
* **Be cautious with high-cardinality Group by fields.** Fields with many unique values can cause rule timeouts or circuit-breaker errors.

::::{tip}
**See it in practice.** These prebuilt rules use thresholds effectively:

* **Potential Brute Force Attack** groups failed authentication attempts by `source.ip` and fires when the count crosses a threshold, detecting credential-stuffing patterns.
* **High Number of Process Terminations** counts process termination events per host, surfacing hosts where mass process termination may indicate ransomware activity.
* **Multiple Alerts Involving a Single User** groups existing alerts by `user.name` to detect users generating an unusually high volume of alerts, a useful meta-detection pattern.
::::
END CRAFT LAYER -->

## Annotated examples [threshold-examples]

The following examples use the [detections API](/solutions/security/detect-and-alert/using-the-api.md) request format to show how threshold rules are defined. Each example is followed by a breakdown of the threshold-specific fields. For common fields like `name`, `severity`, and `interval`, refer to the [detections API documentation]({{kib-apis}}group/endpoint-detection-engine-rules-api).

### Brute-force detection with group by [threshold-example-brute-force]

This rule alerts when a single source IP generates 100 or more failed login attempts within a single rule execution window.

```json
{
  "type": "threshold",
  "language": "kuery",
  "name": "Brute-force login attempts by source IP",
  "description": "Alerts when a source IP produces 100 or more failed logins.",
  "query": "event.category: \"authentication\" and event.outcome: \"failure\"",
  "threshold": {
    "field": ["source.ip"],
    "value": 100
  },
  "index": ["filebeat-*", "logs-system.*", "winlogbeat-*"],
  "severity": "high",
  "risk_score": 73,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `type` | `"threshold"` | Identifies this as a threshold rule. |
| `query` | `event.category: "authentication" and event.outcome: "failure"` | A KQL filter that selects the events to count. Only failed authentication events are counted against the threshold. Uses `"kuery"` or `"lucene"`, the same query languages available in custom query rules. |
| `threshold.field` | `["source.ip"]` | Groups events by source IP. Each unique IP is evaluated independently against the threshold. Accepts up to 5 fields, or an empty array `[]` to count all matching events together without grouping. |
| `threshold.value` | `100` | The minimum event count required to generate an alert. Each source IP must produce at least 100 failed logins in a single rule execution window. Must be at least `1`. |

### Port scan detection with cardinality constraint [threshold-example-cardinality]

This rule alerts when a source IP connects to many unique destination ports, indicating potential port scanning. The cardinality constraint ensures alerts fire only for connections across multiple ports, filtering out repeated connections to the same port.

```json
{
  "type": "threshold",
  "language": "kuery",
  "name": "Possible port scan detected",
  "description": "Alerts when a source IP connects to 25 or more unique destination ports.",
  "query": "event.category: \"network\" and event.type: \"connection\"",
  "threshold": {
    "field": ["source.ip"],
    "value": 50,
    "cardinality": [
      { "field": "destination.port", "value": 25 }
    ]
  },
  "index": ["packetbeat-*", "logs-endpoint.events.*"],
  "severity": "medium",
  "risk_score": 47,
  "interval": "5m",
  "from": "now-6m"
}
```

| Field | Value | Purpose |
|---|---|---|
| `threshold.cardinality` | `[{ "field": "destination.port", "value": 25 }]` | Adds a cardinality constraint. An alert fires only for source IPs that connect to at least 25 unique destination ports across 50 or more events. This filters out high-volume but benign repeated connections to the same port. |
| `threshold.field` + `threshold.value` | `["source.ip"]` / `50` | Groups by source IP and requires at least 50 matching events. Both the event count and the cardinality constraint must be met for an alert to fire. |

## Threshold rule field reference [threshold-fields]

The following settings appear in the **Define rule** section when creating a threshold rule. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/common-rule-settings.md).

**Index patterns or {{data-source}}**
:   The {{es}} indices or {{data-source}} the rule searches.

**Custom query**
:   The KQL or Lucene query used to filter events before counting. Only matching documents are evaluated against the threshold.

**Group by** (optional)
:   One or more fields to group events by. Each unique combination of field values is evaluated independently against the threshold. 

    {applies_to}`stack: ga 9.0-9.1` You can specify up to 3 fields. 

    {applies_to}`stack: ga 9.2+` You can specify up to 5 fields. 

**Threshold**
:   The minimum number of matching events required to generate an alert. If **Group by** is defined, each group must independently meet this count.

**Count** (optional)
:   A cardinality constraint on an additional field. Limits alerts to groups where the specified field has at least the given number of unique values.

**Suppress alerts** (optional)
:   Reduce repeated or duplicate alerts. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).
