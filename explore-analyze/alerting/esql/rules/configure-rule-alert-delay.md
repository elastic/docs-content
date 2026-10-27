---
navigation_title: Alert delay
applies_to:
  stack: ga 9.6+
  serverless: ga
products:
  - id: kibana
description: "Configure alert delay for rules that group matches into an alert, to reduce noise from brief spikes before the alert opens."
---

# Alert delay in {{alerting-v2-system}} [alert-delay]

Alert delay is an optional setting for {{alerting-v2-system}} rules that group matches into an alert. It controls when a breached rule transitions from pending to active, reducing noise from brief spikes that don't reflect a real state change.

In YAML, alert delay corresponds to the `state_transition.pending` object.

## When to configure alert delay [alert-delay-when-to-use]

Configure alert delay when:

* The metric being monitored fluctuates and a single breach doesn't reflect a real state change. Examples include CPU usage that briefly spikes during process startup or a connection pool that crosses the threshold on alternating evaluations.
* The cost or urgency of a notification is high enough that you need confidence the condition is sustained before alerting on it.

Leave alert delay set to **Immediate** when:

* Any single breach warrants immediate attention and you cannot tolerate the added latency of waiting for consecutive evaluations.
* The rule records matches without grouping them into an alert.

## Alert delay modes

| Mode | Behavior | When to use |
| --- | --- | --- |
| Immediate | Opens an alert as soon as the threshold is breached on the first evaluation. | Use when any single breach warrants attention and latency matters. |
| Breaches | Opens an alert after the threshold is breached a set number of times in a row. | Use when brief spikes are normal and you only want to act after the condition keeps firing—a single breach on its own isn't enough. |
| Duration | Opens an alert after the threshold has been continuously breached for a set time. | Use when duration of the problem matters more than how many evaluations caught it, for example sustained high CPU rather than a momentary spike. |

### Alert delay fields

Use the following fields to configure the Breaches and Duration modes. Timeframe fields accept duration strings between `5s` and `365d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

| Field | Type | Accepted values | Description |
| --- | --- | --- | --- |
| `state_transition.pending.count` | integer | 0–1000 | Consecutive matches the alert spends in `pending` before it becomes `active` on the next match. For example, `2` opens the alert on the third consecutive match. Appears as **Consecutive breaches** in Breaches mode. Set to `0` to open the alert on the first match. |
| `state_transition.pending.timeframe` | duration | Any duration string | How long the condition must remain breached before the alert opens. Appears as **Active for** in Duration mode. |
| `state_transition.pending.operator` | string | `and` or `or` | When you set both `count` and `timeframe`, controls whether both must be satisfied (`and`) or either one is enough (`or`). Defaults to `or`. |

You can combine Breaches and Duration by setting both `count` and `timeframe`. Use `operator: and` to require both conditions before the alert opens, or `operator: or` if either condition alone is enough. For field details, refer to the [YAML rule schema reference](yaml-rule-schema-reference.md#state-transition-fields).

:::{note}
Looking for the equivalent delay before an alert closes? Refer to [Recovery condition](configure-rule-recovery.md#recovery-delay).
:::

## Examples

### Ignore brief CPU spikes

Create a rule that monitors CPU usage and runs every minute. A single high reading is often a process starting up. Set the alert delay mode to **Breaches** and **Consecutive breaches** to `3` so the rule requires 3 consecutive breaches before opening an alert, meaning the condition has been true for at least 3 minutes. This filters out noise without losing real signals.

### Require sustained breach before escalating

Create a rule that monitors a payment error rate. Brief spikes happen during deployments and are expected. Set a count of `5` and a timeframe of `2m`, and require both. The rule only fires when the error rate has breached on 5 consecutive evaluations and has been continuously elevated for at least 2 minutes. Either condition alone isn't enough.

```yaml
state_transition:
  pending:
    count: 5
    timeframe: 2m
    operator: and
```

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md#recovery-delay): The equivalent delay before an alert closes.
