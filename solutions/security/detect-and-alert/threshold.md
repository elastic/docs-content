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

## Threshold field reference [threshold-fields]

The following settings are specific to threshold rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md).

**Index patterns or {{data-source}}**
:   The {{es}} indices or {{data-source}} the rule searches.

**Custom query**
:   The KQL or Lucene query used to filter events before counting. Only matching documents are evaluated against the threshold.

**Group by** (optional)
:   One or more fields to group events by. Each unique combination of field values is evaluated independently against the threshold. Nested fields are not supported.

**Threshold**
:   The minimum number of matching events required to generate an alert. If **Group by** is defined, each group must independently meet this count.

**Count** (optional)
:   A cardinality constraint on an additional field. Limits alerts to groups where the specified field has at least the given number of unique values.

**Suppress alerts** (optional)
:   Reduce repeated or duplicate alerts. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites).
