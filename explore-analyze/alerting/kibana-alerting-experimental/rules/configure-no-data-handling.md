---
navigation_title: No-data handling
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure no-data handling for rules in Kibana's experimental alerting system to control what happens when a query returns no results."
---

# No-data handling in the {{alerting-v2-system}} [no-data-handling]

Use `no_data_strategy` to control what the rule records when the base query returns no results. Setting this correctly prevents false recoveries and misleading `no_data` events when data sources stop reporting.

Set `no_data_strategy` to one of the following values:

| Value | Description |
| --- | --- |
| `emit` | Record a no-data event. |
| `last_known_status` | Hold the last known lifecycle state. An active breach stays active; a recovered episode stays recovered. |
| `recover` | Treat absence as recovery. |
| `none` | Turn off no-data detection |

:::{note}
`no_data_strategy` does not detect when a specific host or data source stops reporting while others continue. Refer to [No-data detection](esql-no-data-detection.md) for an {{esql}} pattern that surfaces silent sources as alert rows.
:::

## Examples

### Maintain alert state during a metrics collection outage

This rule monitors infrastructure CPU. If the metrics collection agent stops sending data, you don't want an active CPU breach to auto-recover just because the query returned nothing. Set `no_data_strategy` to `last_known_status`. The rule holds the alert in its current state until data resumes.

Use this when an empty query result most likely means a pipeline problem rather than a genuine recovery.

### Surface a broken data pipeline as an alert

This rule monitors for login events from an identity provider. If no events appear in the lookback window, it's unusual enough to warrant attention: either the pipeline is broken or something has suppressed activity. Set `no_data_strategy` to `emit`. The absence is recorded as a `no_data` event in `.rule-events`, making it visible alongside other rule activity.

Use this when receiving no data is itself a signal worth investigating.
