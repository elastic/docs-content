---
navigation_title: Activation and recovery thresholds
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Control when Kibana alerting v2 alerts transition between lifecycle states using consecutive-breach and duration-based thresholds."
---

# Kibana alerting v2 activation and recovery thresholds [activation-recovery-thresholds-v2]

Activation and recovery thresholds control when alerts transition between lifecycle states. They prevent transient spikes from creating actionable alerts and prevent rapid toggling between active and recovered.

These settings are only available for alert-mode rules (`kind: alert`).

## Alert lifecycle states

An alert transitions through these states:

```
inactive → pending → active → recovering → inactive
```

## Activation thresholds

Configure activation using count, timeframe, or both:

| Field | Description |
|---|---|
| `pending_count` | Consecutive breaches required |
| `pending_timeframe` | Minimum duration the condition must persist |
| `pending_operator` | How to combine count and timeframe (`AND` or `OR`) |

Each **timeframe** value must be between **5 seconds** and **365 days** (the same bounds as schedule and lookback durations).

## Recovery thresholds

| Field | Description |
|---|---|
| `recovering_count` | Consecutive recoveries required |
| `recovering_timeframe` | Minimum duration for recovery |
| `recovering_operator` | How to combine count and timeframe (`AND` or `OR`) |

**Timeframe** fields use the same **5 seconds** to **365 days** bounds as activation timeframes.
