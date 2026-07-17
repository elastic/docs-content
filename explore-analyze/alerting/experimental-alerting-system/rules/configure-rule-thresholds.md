---
navigation_title: Activation and recovery thresholds (Alert mode only)
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure activation and recovery thresholds for Alert-mode rules in Kibana's experimental alerting system to reduce noise from brief spikes and rapid state changes."
---

# Activation and recovery thresholds in the {{alerting-v2-system}} (Alert mode only) [activation-recovery-thresholds]

Activation and recovery thresholds are optional settings for Alert-mode rules in the {{alerting-v2-system}}. They control when alerts transition between lifecycle states, reducing noise from brief spikes and rules that alternate rapidly between breaching and recovering.

## When to configure thresholds [thresholds-when-to-use]

Configure activation and recovery thresholds when:

* The metric being monitored fluctuates and a single breach or recovery doesn't reflect a real state change. Examples include CPU usage that briefly spikes during process startup or a connection pool that crosses the threshold on alternating evaluations.
* You want to reduce notification noise from rules that alternate rapidly between breaching and recovering on consecutive evaluations.
* The cost or urgency of a notification is high enough that you need confidence the condition is sustained before alerting on it.

Skip activation and recovery thresholds when:

* Any single breach warrants immediate attention and you cannot tolerate the added latency of waiting for consecutive evaluations. Leave the activation mode set to Immediate.
* The rule is in Signal mode. Thresholds only apply to Alert-mode rules and have no effect on signal document output.

## Activation thresholds

Activation thresholds control when a breached rule transitions from pending to active. Three delay modes are available:

| Mode | Behavior | When to use |
| --- | --- | --- |
| Immediate | Opens an alert episode as soon as the threshold is breached on the first evaluation. | Use when any single breach warrants attention and latency matters. |
| Breaches | Opens an alert episode after the threshold is breached a set number of times in a row. | Use when a single breach isn't enough reason to act, for example when brief spikes are normal and you only care if the condition keeps firing. |
| Duration | Opens an alert episode after the threshold has been continuously breached for a set time. | Use when duration of the problem matters more than how many evaluations caught it, for example sustained high CPU rather than a momentary spike. |

### Activation fields

Use the following fields to configure the Breaches and Duration modes. Timeframe fields accept duration strings between `5s` and `365d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

:::{note}
In the YAML rule schema, these fields are prefixed with `state_transition.` — for example, `pending_count` here is `state_transition.pending_count` in the [YAML rule schema reference](yaml-rule-schema-reference.md#state-transition-fields). They are the same fields.
:::

| Field | Type | Description |
| --- | --- | --- |
| `pending_count` | Integer, 0–1000 | Number of consecutive breach evaluations required before the alert episode opens. Set to `0` to skip the pending phase and transition directly to active on the first breach. |
| `pending_timeframe` | Duration string | How long the condition must remain breached before the alert episode opens. |
| `pending_operator` | `AND` or `OR` | When both `pending_count` and `pending_timeframe` are set, controls whether both must be satisfied (`AND`) or either one is enough (`OR`). |

You can combine Breaches and Duration by setting both `pending_count` and `pending_timeframe`. Use `pending_operator: AND` to require both conditions before the episode opens, or `pending_operator: OR` if either condition alone is enough.

## Recovery thresholds

Recovery thresholds control when an active alert episode transitions back to inactive. The same delay modes available for activation apply. You can require a set number of consecutive recoveries, a minimum recovery duration, or both.

### Recovery fields

| Field | Type | Description |
| --- | --- | --- |
| `recovering_count` | Integer, 0–1000 | Number of consecutive non-breaching evaluations required before the alert episode closes. Set to `0` to skip the recovering phase and transition directly to inactive on recovery. |
| `recovering_timeframe` | Duration string | How long the condition must remain non-breaching before the alert episode closes. |
| `recovering_operator` | `AND` or `OR` | When both `recovering_count` and `recovering_timeframe` are set, controls whether both must be satisfied (`AND`) or either one is enough (`OR`). |

Time frame fields accept the same `5s` to `365d` bounds as activation time frames. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

:::{note}
`recovery_strategy` is a separate field that controls how recovery is detected, independent of how many recoveries these thresholds require. Refer to [Recovery strategy](configure-rule-recovery.md) for when to configure each option.
:::

## Examples

### Ignore brief CPU spikes

This rule monitors CPU usage and runs every minute. A single high reading is often a process starting up. Set `pending_count` to `3` so the rule requires 3 consecutive breaches before opening an episode, meaning the condition has been true for at least 3 minutes. This filters out noise without losing real signals.

### Require sustained breach before escalating

This rule monitors a payment error rate. Brief spikes happen during deployments and are expected. Set `pending_count` to `5`, `pending_timeframe` to `2m`, and `pending_operator` to `AND`. The rule only fires when the error rate has breached on 5 consecutive evaluations and has been continuously elevated for at least 2 minutes. Either condition alone isn't enough.

### Require consecutive recoveries before closing an episode

This rule monitors database connection pool saturation. After the condition clears, set `recovering_count` to `3` to require 3 consecutive non-breaching evaluations before closing the episode. Without this, a rule that alternates between breaching and recovering on consecutive evaluations generates a constant stream of open and closed notifications.
