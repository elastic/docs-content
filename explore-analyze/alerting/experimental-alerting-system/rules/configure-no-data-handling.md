---
navigation_title: No-data handling
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to configure the no-data strategy for rules in the experimental alerting system. Controls whether an empty query result emits a no-data event, holds the last known alert state, triggers recovery, or is ignored."
---

# No-data handling in the {{alerting-v2-system}} [no-data-handling]

No-data handling is an optional setting for rules in the {{alerting-v2-system}}. Use `no_data_strategy` to control what the rule records when the base query returns no results. Setting this correctly prevents false recoveries and misleading `no_data` events when data sources stop reporting.

## No-data strategy options [no-data-strategy-options]

<!-- TODO: Confirm with jasonrhodes before publishing. He indicated (PR elastic/docs-content#7375) that the UI friendly names below are "Keep last status," "Recover," and "Do nothing," but that `emit` may have been removed for M2 and isn't guaranteed to still be a selectable option. Verify the current option list and exact labels before relying on this mapping. -->

Choose one of the following options. Each maps to a `no_data_strategy` value if you're editing YAML directly.

| Option | `no_data_strategy` value | Description |
| --- | --- | --- |
| Keep last status | `last_known_status` | Hold the last known lifecycle state. An active breach stays active and a recovered episode stays recovered. |
| Recover | `recover` | Treat absence as recovery. |
| Do nothing | `none` | Turn off no-data detection. |
| _(unconfirmed)_ | `emit` | Record a no-data event. |

:::{note}
`no_data_strategy` only applies when the base query returns **no rows at all**. If one host or data source goes silent while others continue reporting, the query still returns results for the active sources and `no_data_strategy` does not trigger. Refer to [No-data detection](esql-no-data-detection.md) for an {{esql}} pattern that surfaces individual silent sources as alert rows.
:::

## When to configure no-data handling [no-data-when-to-use]

Configure `no_data_strategy` when:

* The data source your rule monitors can go silent. Examples include a metrics agent that stops reporting, a pipeline that breaks, or a service that stops generating events.
* A false recovery caused by an empty query result would be more harmful than holding the current alert state.
* Absence of data is itself a signal worth surfacing, such as missing heartbeat events from a critical service.

Leave `no_data_strategy` unconfigured (or set to **Do nothing**) when:

* Your data source reliably produces output on every evaluation and a gap in data would indicate a genuine recovery.
* You are still tuning the rule and don't yet know how it behaves when data is absent. Set the strategy once the rule's normal behavior is understood.

## Examples

### Maintain alert state during a metrics collection outage

This rule monitors infrastructure CPU. If the metrics collection agent stops sending data, you don't want an active CPU breach to auto-recover because the query returned nothing. Set the no-data strategy to **Keep last status** (`last_known_status`). The rule holds the alert in its current state until data resumes.

Use this when an empty query result most likely means a pipeline problem rather than a genuine recovery.

### Surface a broken data pipeline as an alert

<!-- TODO: Confirm `emit` is still available for M2 before publishing this example; see the TODO above the options table. -->

This rule monitors for login events from an identity provider. If no events appear in the lookback window, it's unusual enough to warrant attention. Either the pipeline is broken or something has suppressed activity. Set `no_data_strategy` to `emit`. The absence is recorded as a `no_data` event in `.rule-events`, making it visible alongside other rule activity.

Use this when receiving no data is itself a signal worth investigating.
