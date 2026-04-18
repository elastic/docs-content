---
navigation_title: Rule settings
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Configure {{alerting-v2}} rules: schedule, lookback, activation and recovery thresholds, no-data handling, rule grouping, and maintenance windows."
---

# {{alerting-v2}} rule settings [rule-settings-v2]

$$$rule-settings-v2$$$

Rule settings control how a {{alerting-v2}} rule evaluates data and manages alert lifecycle. For **action policies**, matchers, notification grouping, throttling, and **workflows**, see [Send notifications](../send-notifications.md). {{alerting-v2}} does **not** use fixed **rule types**: you write ES\|QL directly.

## Schedule and lookback [schedule-lookback-v2]

$$$schedule-lookback-v2$$$

The schedule and lookback settings control how often a rule runs and how far back it looks when evaluating data.

### Execution interval

The execution interval (`schedule.every`) determines how frequently the rule evaluates.

{{kib}} enforces a minimum interval of 5 seconds and a maximum of 365 days for duration fields (including this one). The rule form and API reject values outside that range.

### Lookback window

The lookback window (`schedule.lookback`) determines the time range that the ES|QL query covers.

The lookback must not exceed 365 days. If the lookback is shorter than the execution interval, the rule form shows a warning because you can miss data between runs. Set the lookback to at least the execution interval unless you have a deliberate reason not to.

Select a lookback window that is at least as long as the execution interval to avoid gaps in coverage.

## Activation and recovery thresholds [activation-recovery-thresholds-v2]

$$$activation-recovery-thresholds-v2$$$

Activation and recovery thresholds control when alerts transition between lifecycle states. They prevent transient spikes from creating actionable alerts and prevent rapid toggling between active and recovered.

These settings are only available for alert-mode rules (`kind: alert`).

### Alert lifecycle states

An alert transitions through these states:

```
inactive → pending → active → recovering → inactive
```

### Activation thresholds

Configure activation using count, timeframe, or both:

| Field | Description |
|---|---|
| `pending_count` | Consecutive breaches required |
| `pending_timeframe` | Minimum duration the condition must persist |
| `pending_operator` | How to combine count and timeframe (`AND` or `OR`) |

Each timeframe value must be between 5 seconds and 365 days (the same bounds as schedule and lookback durations).

### Recovery thresholds

| Field | Description |
|---|---|
| `recovering_count` | Consecutive recoveries required |
| `recovering_timeframe` | Minimum duration for recovery |
| `recovering_operator` | How to combine count and timeframe (`AND` or `OR`) |

Timeframe fields use the same 5 seconds to 365 days bounds as activation timeframes.

## No-data handling [no-data-handling-v2]

No-data handling controls what happens when a rule executes and the base query returns no results. Proper configuration prevents **false recoveries** and misleading **`no_data`** events when data sources stop reporting.

### Behaviors

| Behavior | Effect |
|---|---|
| `no_data` (default) | Record a no-data event |
| `last_status` | Carry forward the previous status |
| `recover` | Treat absence as recovery |

## Rule grouping [rule-grouping-v2]

$$$rule-grouping-v2$$$

**Rule grouping** splits alert event generation by one or more fields so that each unique combination of field values produces its own alert series. Each series has independent lifecycle tracking, recovery detection, and per-series snooze.

### Configure grouping

In YAML:

```yaml
grouping:
  fields: [host.name]
```

The grouping fields must correspond to the `BY` clause in your ES\|QL query's `STATS` command.

(This is separate from **notification grouping** on an action policy, which controls how episodes batch into messages.)

## Maintenance windows [maintenance-windows-v2]

$$$maintenance-windows-v2$$$

**{{maint-windows-cap}}** are scheduled periods during which notifications are paused. Rule evaluation continues and **alert episodes** can still be recorded in **`.rule-events`**. Dispatch is what pauses. Use them for planned deployments, infrastructure changes, or recurring maintenance.
