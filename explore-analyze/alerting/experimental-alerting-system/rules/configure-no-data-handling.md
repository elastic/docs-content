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

No-data handling is an optional setting for Alert-mode rules in the {{alerting-v2-system}}. Use `no_data_strategy` to control what the rule does when it can't tell whether an episode has genuinely recovered or the data just stopped showing up. Setting this correctly prevents false recoveries and misleading `no_data` events when data sources stop reporting.

## How no-data handling fits into recovery [no-data-and-recovery]

When a breached group stops matching, the rule re-runs the [base query](configure-rule-query.md#query-base) to confirm the group is actually gone before recovering the episode:

* **Group still there** - The base query still returns the group, confirming this is a genuine [recovery](configure-rule-recovery.md) rather than a data gap.
* **Group missing too** - The base query returns nothing for the group either, so the rule can't tell whether the problem actually cleared up or the data source just stopped reporting. What happens next depends on how you've configured `no_data_strategy`.

The check described above is part of the recovery process, so it only runs when `recovery_strategy` is **Default** or **Custom recovery**.

If `recovery_strategy` is **No recovery** instead, episodes stay open until someone closes them manually, the base-query check above doesn't run, and `no_data_strategy` has no effect.

## No-data strategy options [no-data-strategy-options]

Choose one of the following options. Each maps to a `no_data_strategy` value if you're editing YAML directly.

| Option | `no_data_strategy` value | Description |
| --- | --- | --- |
| Keep last status | `last_known_status` | Hold the last known lifecycle state. An active breach stays active and a recovered episode stays recovered. |
| Recover | `recover` | Treat absence as recovery. |
| Do nothing | `none` | Skip the no-data check. An empty result is treated the same as **Recover**, but the rule doesn't confirm that the data pipeline is actually working. |

:::{note}
`no_data_strategy` only triggers when the base query returns **zero rows**. If one host or data source goes quiet but others keep reporting, the query still returns rows for the ones still reporting, so `no_data_strategy` won't trigger. To catch a single silent source in that situation, use the {{esql}} pattern in [No-data detection](esql-no-data-detection.md), which turns a silent source into its own alert row.
:::

## When to configure no-data handling [no-data-when-to-use]

Configure `no_data_strategy` when:

* The data source your rule monitors can go silent. Examples include a metrics agent that stops reporting, a pipeline that breaks, or a service that stops generating events.
* A false recovery caused by an empty query result would be more harmful than holding the current alert state.
* Absence of data is itself a signal worth surfacing, such as missing heartbeat events from a critical service.

Do not configure `no_data_strategy`, or set it to **Do nothing**, when:

* Your data source reliably produces output on every evaluation and a gap in data would indicate a genuine recovery. 
* You are still tuning the rule and don't yet know how it behaves when data is absent.

## Examples

### Maintain alert state during a metrics collection outage

Create a rule that monitors infrastructure CPU. Configure the no-data strategy as **Keep last status** (`last_known_status`) so that if the metrics collection agent ever stops sending data, an active CPU breach doesn't auto-recover just because the query returned nothing. Instead, the rule holds the alert in its current state until data resumes.

### Close the episode when a queue empties out

Create a rule that monitors how many jobs are waiting in a queue and opens an episode when the backlog gets too large. Configure the no-data strategy as **Recover** (`recover`) so that once the queue is empty and the query has nothing to return, the episode closes.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md): How no-data handling fits into the recovery process.
- [No-data detection](esql-no-data-detection.md): An {{esql}} pattern for detecting one specific silent source, rather than an empty base query result.
