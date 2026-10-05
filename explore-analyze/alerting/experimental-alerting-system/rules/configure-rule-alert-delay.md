---
navigation_title: Alert delay (alert episodes only)
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure alert delay for rules that group matches into an alert episode, to reduce noise from brief spikes before the alert episode opens."
---

# Alert delay in the {{alerting-v2-system}} [alert-delay]

Alert delay is an optional setting for rules that group matches into an alert episode. It controls when a breached rule transitions from pending to active, reducing noise from brief spikes that don't reflect a real state change. In YAML, alert delay corresponds to the following fields: 

*  {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: ga` `state_transition.pending.count`, `state_transition.pending.timeframe`, and `state_transition.pending.operator`
* {applies_to}`stack: experimental =9.5` `state_transition.pending_*` fields

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
| `pending_count` | integer | 0–1000 | Number of consecutive breach evaluations required before the alert episode opens. Appears as **Consecutive breaches** in Breaches mode. Set to `0` to skip the pending phase and transition directly to active on the first breach. |
| `pending_timeframe` | duration | Any duration string | How long the condition must remain breached before the alert episode opens. Appears as **Active for** in Duration mode. |
| `pending_operator` | string | `AND` or `OR` {applies_to}`stack: experimental =9.5`<br><br> `and` or `or` {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: ga` | Whether both `pending_count` and `pending_timeframe` must be met, or either one is enough, when both fields are set. |


To combine Breaches and Duration, set both `pending_count` and `pending_timeframe`, then use `pending_operator` to control how they interact. `and` requires both conditions before the alert episode opens. `or` opens it as soon as either one is met.

:::{note}
Alert delay only controls the delay before an alert episode opens. For the matching delay before an alert episode closes, refer [](configure-rule-recovery.md#recovery-delay).
:::

#### Field names in the YAML rule schema

The `pending_count`, `pending_timeframe`, and `pending_operator` fields map to the `state_transition.pending` fields in the [YAML rule schema reference](yaml-rule-schema-reference.md#state-transition-fields). The YAML field name depends on your version:

- {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: ga` Nested under `state_transition.pending`. For example, `pending_count` is `state_transition.pending.count`. The `pending` object must set `count` or `timeframe`; `operator` is allowed only when both are set.
- {applies_to}`stack: experimental =9.5` Prefixed with `state_transition.`. For example, `pending_count` is `state_transition.pending_count`.


## Examples

### Ignore brief CPU spikes

Create a rule that monitors CPU usage and runs every minute. A single high reading is often a process starting up. Set `pending_count` to `3` so the rule requires 3 consecutive breaches before opening an alert episode, meaning the condition has been true for at least 3 minutes. This filters out noise without losing real signals.

### Require sustained breach before escalating

Create a rule that monitors a payment error rate. Brief spikes happen during deployments and are expected. Set `pending_count` to `5`, `pending_timeframe` to `2m`, and `pending_operator` to `AND` (`and` on Stack 9.6+ and Serverless). The rule only fires when the error rate has breached on 5 consecutive evaluations and has been continuously elevated for at least 2 minutes. Either condition alone isn't enough.

:::{note}
:applies_to: stack: experimental 9.6+ :applies_to: serverless: ga
In {{stack}} version 9.6 and in {{serverless-short}}, set `pending_operator` to `and` instead of `AND`.
:::

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md#recovery-delay): The equivalent delay before an alert episode closes.
