---
navigation_title: Alert delay (Alert mode only)
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure alert delay for Alert-mode rules in Kibana's experimental alerting system to reduce noise from brief spikes before opening an episode."
---

# Alert delay in the {{alerting-v2-system}} (Alert mode only) [alert-delay]

Alert delay is an optional setting for Alert-mode rules in the {{alerting-v2-system}}. It controls when a breached rule transitions from pending to active, reducing noise from brief spikes that don't reflect a real state change. In YAML, this corresponds to the `state_transition.pending_*` fields.

## When to configure alert delay [alert-delay-when-to-use]

Configure alert delay when:

* The metric being monitored fluctuates and a single breach doesn't reflect a real state change. Examples include CPU usage that briefly spikes during process startup or a connection pool that crosses the threshold on alternating evaluations.
* The cost or urgency of a notification is high enough that you need confidence the condition is sustained before alerting on it.

Leave alert delay set to Immediate when:

* Any single breach warrants immediate attention and you cannot tolerate the added latency of waiting for consecutive evaluations.
* The rule is in Signal mode. Alert delay only applies to Alert-mode rules and has no effect on signal document output.

## Alert delay modes

| Mode | Behavior | When to use |
| --- | --- | --- |
| Immediate | Opens an alert episode as soon as the threshold is breached on the first evaluation. | Use when any single breach warrants attention and latency matters. |
| Breaches | Opens an alert episode after the threshold is breached a set number of times in a row. | Use when a single breach isn't enough reason to act, for example when brief spikes are normal and you only care if the condition keeps firing. |
| Duration | Opens an alert episode after the threshold has been continuously breached for a set time. | Use when duration of the problem matters more than how many evaluations caught it, for example sustained high CPU rather than a momentary spike. |

### Alert delay fields

Use the following fields to configure the Breaches and Duration modes. Timeframe fields accept duration strings between `5s` and `365d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

:::{note}
In the YAML rule schema, these fields are prefixed with `state_transition.`. For example, `pending_count` here is `state_transition.pending_count` in the [YAML rule schema reference](yaml-rule-schema-reference.md#state-transition-fields). They are the same fields.
:::

| Field | Type | Description |
| --- | --- | --- |
| `pending_count` | Integer, 0–1000 | Number of consecutive breach evaluations required before the alert episode opens. Appears as **Consecutive breaches** in Breaches mode. Set to `0` to skip the pending phase and transition directly to active on the first breach. |
| `pending_timeframe` | Duration string | How long the condition must remain breached before the alert episode opens. Appears as **Active for** in Duration mode. |
| `pending_operator` | `AND` or `OR` | When both `pending_count` and `pending_timeframe` are set, controls whether both must be satisfied (`AND`) or either one is enough (`OR`). |

You can combine Breaches and Duration by setting both `pending_count` and `pending_timeframe`. Use `pending_operator: AND` to require both conditions before the episode opens, or `pending_operator: OR` if either condition alone is enough.

:::{note}
Looking for the equivalent delay before an episode closes? Refer to [Recovery condition](configure-rule-recovery.md#recovery-delay).
:::

## Examples

### Ignore brief CPU spikes

This rule monitors CPU usage and runs every minute. A single high reading is often a process starting up. Set `pending_count` to `3` so the rule requires 3 consecutive breaches before opening an episode, meaning the condition has been true for at least 3 minutes. This filters out noise without losing real signals.

### Require sustained breach before escalating

This rule monitors a payment error rate. Brief spikes happen during deployments and are expected. Set `pending_count` to `5`, `pending_timeframe` to `2m`, and `pending_operator` to `AND`. The rule only fires when the error rate has breached on 5 consecutive evaluations and has been continuously elevated for at least 2 minutes. Either condition alone isn't enough.
