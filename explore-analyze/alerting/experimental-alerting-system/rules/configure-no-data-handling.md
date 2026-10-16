---
navigation_title: No-data handling
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to configure the no-data strategy for rules in the experimental alerting system: hold the last known alert state, trigger recovery, or ignore an empty query result."
---

# No-data handling in the {{alerting-v2-system}} [no-data-handling]

No-data handling controls what the rule does when it can't tell whether an alert has genuinely recovered or the data stopped showing up. Setting this correctly prevents false recoveries and misleading `no_data` events when data sources stop reporting.

Signal rules don't use no-data handling. For alert rules:

* {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` You must set `no_data`.
* {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` You can omit `no_data_strategy`.

## How no-data handling fits into recovery [no-data-and-recovery]

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: experimental 9.6+ }

For any strategy other than **Do nothing**, the rule needs a presence query so it can tell a group that stopped breaching from a group that has no data. Set `no_data.query`, or omit it and set `query.breach`. If you omit `no_data.query`, the rule uses `query.base` as the presence query.

* **Group still there.** The presence query still returns the group, so this is a [recovery](configure-rule-recovery.md) rather than a data gap.
* **Group missing too.** The presence query does not return the group. What happens next depends on `no_data.strategy`.

**Do nothing** (`ignore`) skips this check. Missing groups don't produce `no_data` events, and you can't set `no_data.query`.

::::

::::{applies-item} stack: experimental =9.5

When a breached group stops matching, the rule re-runs the [base query](configure-rule-query.md#query-base) to confirm the group is actually gone before recovering the alert:

* **Group still there** - The base query still returns the group, confirming this is a genuine [recovery](configure-rule-recovery.md) rather than a data gap.
* **Group missing too** - The base query returns nothing for the group either, so the rule can't tell whether the problem actually cleared up or the data source just stopped reporting. What happens next depends on how you've configured `no_data_strategy`.

The check described above is part of the recovery process, so it only runs when `recovery_strategy` is **Default** or **Custom recovery**.

If `recovery_strategy` is **No recovery** instead, alerts stay open until someone closes them manually, the base-query check above doesn't run, and `no_data_strategy` has no effect.

::::

:::::

## No-data strategy options [no-data-strategy-options]

Select one of the following options. If you're editing YAML directly, use the value for your version.

| Option | `no_data.strategy` value {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` | `no_data_strategy` value {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | Description |
| --- | --- | --- | --- |
| **Keep last known status** | `keep_last` | `last_known_status` | Hold the alert's current status when the rule finds no data for the group. An active alert stays active, and a recovered one stays recovered. |
| **Recover immediately** {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` <br><br> **Recover** {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | `resolve` | `recover` | {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` Close the alert the first time the rule finds no data for the group. The alert skips the recovering phase, so [recovery delay](configure-rule-recovery.md#recovery-delay) doesn't apply. <br><br> {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` Recover the alert when the rule finds no data for the group. The alert goes through the recovering phase, so [recovery delay](configure-rule-recovery.md#recovery-delay) applies. |
| **Do nothing** | `ignore` | `none` | Skip the no-data check. The rule's recovery strategy decides what happens to a group that stops appearing, even if its data source stopped reporting. <br><br> Use this option when your data source reports on every evaluation, so a gap in data means a genuine recovery. It's also a safe choice while you're still tuning the rule and don't yet know how it behaves when data is absent. |

:::{note}
If one host or data source goes quiet but others keep reporting, the presence query still returns rows for the sources that report, so no-data handling doesn't trigger. To catch a single silent source, use the {{esql}} pattern in [No-data detection](esql-no-data-detection.md), which turns a silent source into its own alert row.
:::

## When to configure no-data handling [no-data-when-to-use]

Configure no-data handling when:

* The data source your rule monitors can go silent. Examples include a metrics agent that stops reporting, a pipeline that breaks, or a service that stops generating events.
* A false recovery caused by missing data is more harmful than holding the current alert state.
* Absence of data is itself a signal worth surfacing, such as missing heartbeat events from a critical service.

## Examples

### Maintain alert state during a metrics collection outage

Create a rule that monitors infrastructure CPU. Set the no-data strategy to **Keep last known status**. If the metrics collection agent stops sending data, an active CPU breach doesn't recover when the query returns nothing. The rule holds the alert in its current state until data resumes.

### Close the alert when a queue empties out

Create a rule that monitors how many jobs are waiting in a queue and opens an alert when the backlog gets too large. Set the no-data strategy to **Recover immediately** {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` or **Recover** {applies_to}`{ stack: experimental =9.5, serverless: unavailable }`. When the queue is empty and the query returns nothing, the alert closes.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md): How no-data handling fits into the recovery process.
- [No-data detection](esql-no-data-detection.md): An {{esql}} pattern for detecting one specific silent source, rather than an empty base query result.
