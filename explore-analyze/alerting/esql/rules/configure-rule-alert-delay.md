---
navigation_title: Alert delay (alert episodes only)
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Configure alert delay for rules that group matches into an alert episode, to reduce noise from brief spikes before the alert episode opens."
---

# Alert delay [alert-delay]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

Alert delay is an optional setting for rules that group matches into an alert episode. It controls when a breached rule transitions from pending to active, reducing noise from brief spikes that don't reflect a real state change. In YAML, alert delay corresponds to the following fields:

* {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` `state_transition.pending.count`, `state_transition.pending.timeframe`, and `state_transition.pending.operator`
* {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` `state_transition.pending_*` fields

## When to configure alert delay [alert-delay-when-to-use]

Configure alert delay when:

* The metric being monitored fluctuates and a single breach doesn't reflect a real state change. Examples include CPU usage that briefly spikes during process startup or a connection pool that crosses the threshold on alternating evaluations.
* The cost or urgency of a notification is high enough that you need confidence the condition is sustained before alerting on it.

Leave alert delay set to **Immediate** when:

* Any single breach warrants immediate attention and you cannot tolerate the added latency of waiting for consecutive evaluations.
* The rule records matches without grouping them into an alert episode.

## Alert delay modes

| Mode | Behavior | When to use |
| --- | --- | --- |
| Immediate | Opens an alert episode as soon as the threshold is breached on the first evaluation. | Use when any single breach warrants attention and latency matters. |
| Breaches | Opens an alert episode after the threshold is breached a set number of times in a row. | Use when brief spikes are normal and you only want to act after the condition keeps firing—a single breach on its own isn't enough. |
| Duration | Opens an alert episode after the threshold has been continuously breached for a set time. | Use when duration of the problem matters more than how many evaluations caught it, for example sustained high CPU rather than a momentary spike. |

## Alert delay fields

Use the following fields to configure the Breaches and Duration modes. Timeframe fields accept duration strings between `5s` and `365d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

| Field | Type | Accepted values | Description |
| --- | --- | --- | --- |
| `pending_count` | integer | 0–1000 | {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` Number of consecutive breaching evaluations the alert episode spends in the pending phase. It opens on the next breach, so `3` opens it on the 4th consecutive breach. <br><br> {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` Number of consecutive breach evaluations required before the alert episode opens. <br><br> Appears as **Consecutive breaches** in Breaches mode. Set to `0` to skip the pending phase and transition directly to active on the first breach. {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` If you also set `pending_timeframe` with `pending_operator` set to `and`, a count of `0` still waits for the timeframe. |
| `pending_timeframe` | duration | Any duration string | How long the condition must remain breached before the alert episode opens. Appears as **Active for** in Duration mode. |
| `pending_operator` | string | `and` or `or` {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` <br><br> `AND` or `OR` {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | Whether the rule requires both `pending_count` and `pending_timeframe`, or only one, when you set both. |

To combine Breaches and Duration, set both `pending_count` and `pending_timeframe`, then use `pending_operator` to decide whether the alert episode opens after both conditions hold or after either one does.

:::{note}
Alert delay only controls the delay before an alert episode opens. For the matching delay before an alert episode closes, refer to [](configure-rule-recovery.md#recovery-delay).
:::

### Field names in the YAML rule schema

The `pending_count`, `pending_timeframe`, and `pending_operator` fields map to the `state_transition.pending` fields in the [YAML rule schema reference](yaml-rule-schema-reference.md#state-transition-fields). The YAML field name depends on your version:

- {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` Nested under `state_transition.pending`. For example, `pending_count` is `state_transition.pending.count`. The `pending` object must set `count` or `timeframe`. You can set `operator` only when you set both.
- {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` Prefixed with `state_transition.`. For example, `pending_count` is `state_transition.pending_count`.


## Examples

### Ignore brief CPU spikes

Create a rule that monitors CPU usage and runs every minute. A single high reading is often a process starting up. Set `pending_count` to `3` so a brief spike doesn't open an alert episode. The alert episode opens on the 4th consecutive breach {applies_to}`{ serverless: ga, stack: experimental 9.6+ }`, or the 3rd {applies_to}`{ stack: experimental =9.5, serverless: unavailable }`, so the condition has to hold for several minutes in a row. This filters out noise without losing real signals.

### Require sustained breach before escalating

Create a rule that monitors a payment error rate. Brief spikes happen during deployments and are expected. Set `pending_count` to `5`, `pending_timeframe` to `2m`, and `pending_operator` to `and`. The rule fires only when the error rate has stayed elevated for at least 2 minutes and has breached on 6 consecutive evaluations {applies_to}`{ serverless: ga, stack: experimental 9.6+ }`, or 5 {applies_to}`{ stack: experimental =9.5, serverless: unavailable }`. Either condition alone isn't enough.

:::{note}
:applies_to: { stack: experimental =9.5, serverless: unavailable }
Set `pending_operator` to `AND` instead.
:::

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md#recovery-delay): The equivalent delay before an alert episode closes.
