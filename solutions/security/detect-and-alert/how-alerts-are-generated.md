---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Learn how detection rules generate alerts, including the execution pipeline, deduplication, alert limits, and alert types.
---

# How alerts are generated [how-alerts-are-generated]

When a detection rule runs, it follows a multi-step pipeline to create alerts from matching events. This page explains that pipeline, how alerts are deduplicated, limits on alert volume, and the different types of alerts the engine can produce.


## Alert generation pipeline [alert-generation-pipeline]

The following sequence occurs each time a detection rule runs:

:::::{stepper}
::::{step} Schedule triggers
The {{kib}} alerting framework triggers the rule at its configured interval (for example, every 5 minutes).
::::
::::{step} Time range is calculated
The engine determines the time window to search based on the rule's schedule and look-back setting. If previous executions were missed, catch-up windows are calculated automatically.
::::
::::{step} Query runs
The rule's query runs against the configured source indices. The query mechanism varies by [rule type](/solutions/security/detect-and-alert/about-detection-rules.md):

| Rule type | Query mechanism |
|-----------|-----------------|
| Custom query | KQL/Lucene search with pagination |
| EQL | EQL search API (events or sequences) |
| ES\|QL | ES\|QL query |
| Threshold | Aggregation search with bucket counting |
| {{ml-cap}} | {{ml-cap}} anomaly job results search |
| New terms | Composite aggregation comparing recent terms to a history window |
| Indicator match | Join between source events and threat indicator indices |
::::
::::{step} Exceptions are applied
Events matching any [rule exceptions](/solutions/security/detect-and-alert/rule-exceptions.md) are filtered out before alert creation.
::::
::::{step} Events are enriched
Optional enrichment adds context like host risk scores, user risk scores, and asset criticality to the alert document.
::::
::::{step} Alerts are deduplicated
Each alert receives a deterministic ID based on a hash of the source document's index, document ID, version, and rule ID. Before writing, the engine checks whether alerts with the same IDs already exist and drops duplicates. This prevents the same event-rule combination from producing duplicate alerts across rule executions.
::::
::::{step} Alerts are written
Alert documents are bulk-indexed into the alerts index using idempotent `create` operations.
::::
:::::


## Alert limits [alert-limits]

The detection engine enforces limits on how many alerts a single rule execution can produce. Understanding these limits helps you tune rules and avoid missing detections.

### Max alerts per rule execution

Each rule execution has a maximum number of alerts it can create, controlled by the rule's `max_signals` setting (default: 100). This limit can also be capped by the {{kib}} `xpack.alerting.rules.run.alerts.max` setting.

When a rule execution reaches this limit, it stops creating alerts for that run even if more matching events exist. The rule processes remaining events on subsequent executions. If a rule consistently hits this limit, consider:

* Narrowing the rule's query to reduce matches
* Increasing the `max_signals` value
* Adding [exceptions](/solutions/security/detect-and-alert/rule-exceptions.md) to filter out known-benign activity
* Enabling [alert suppression](/solutions/security/detect-and-alert/suppress-detection-alerts.md) to group similar alerts

::::{note}
Suppressed alerts count toward the max alerts limit. However, because suppression groups multiple events into a single alert, it effectively allows the rule to cover more events within the same limit.
::::

### Preview alerts

Rule previews generate temporary alerts stored in a separate `.preview.alerts-security.alerts-*` index. These are automatically deleted after 1 day.


## Alert types [alert-types]

Not all detection alerts are the same. The detection engine produces different types of alerts depending on how the rule is configured, and each type appears differently in the Alerts table.

### Regular alerts

Most rules create one alert per matching event. Each alert contains the full context from the source event plus rule metadata and workflow fields.

### Building block alerts [building-block-alerts]

[Building block rules](/solutions/security/detect-and-alert/about-building-block-rules.md) generate alerts that are hidden from the Alerts page by default. They serve two purposes:

* **Low-noise record keeping.** Track low-risk indicators without cluttering the Alerts table.
* **Inputs for other rules.** Building block alerts are written to the alert index, allowing other rules to query `.alerts-security.alerts-*` and correlate multiple building block alerts into a higher-confidence detection.

EQL sequence rules also produce building block alerts. When a sequence rule matches, it creates:

* One **shell alert** representing the full sequence
* One **building block alert** per event in the sequence, linked to the shell alert through the `kibana.alert.group.id` field

Building block alerts have `kibana.alert.building_block_type` set to `default`. They do not trigger rule notification actions.

### Suppressed alerts [suppressed-alerts]

When [alert suppression](/solutions/security/detect-and-alert/suppress-detection-alerts.md) is configured, the rule groups matching events by specified fields and creates one alert per group instead of one alert per event. The alert includes:

* `kibana.alert.suppression.docs_count`: the number of events grouped into this alert
* `kibana.alert.suppression.terms.field`: the fields used for grouping
* `kibana.alert.suppression.terms.value`: the values in the grouping fields
* `kibana.alert.suppression.start` and `kibana.alert.suppression.end`: the time window covered

You can still investigate all original events associated with a suppressed alert.
