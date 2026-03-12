---
navigation_title: Activation thresholds
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Require consecutive breaches or a minimum duration before a Kibana alerting v2 alert activates, filtering out transient spikes."
---

# Kibana alerting v2 activation thresholds [activation-thresholds-v2]

Activation thresholds require a condition to be met a certain number of consecutive times or for a minimum duration before an alert transitions from `pending` to `active`. This prevents transient spikes from creating actionable alerts.

## How it works

When a rule detects a breach, the alert enters `pending` state instead of immediately becoming `active`. The alert remains in `pending` until the activation threshold is satisfied:

- **Count-based**: the condition must be met for N consecutive evaluations.
- **Timeframe-based**: the condition must persist for a minimum duration.
- **Combined**: both count and timeframe conditions must be met (AND) or either one (OR).

If the condition stops being met before the threshold is satisfied, the alert returns to `inactive` without ever becoming `active`. No notifications are sent.

## Configuration

```yaml
state_transition:
  pending_count: 5
  pending_timeframe: 5m
  pending_operator: AND
```

This configuration requires 5 consecutive breaches **and** at least 5 minutes of persistence before the alert activates.

## When to use

- **High-frequency metrics** with brief spikes (for example, CPU momentarily hitting 100% during garbage collection).
- **Noisy data sources** where occasional outlier values are expected.
- **Rules with short execution intervals** (1 minute) where a single breach is not significant.

## Relationship to other noise reduction

Activation thresholds work at the rule evaluation stage, before notification policies are applied. They reduce the number of alerts that become actionable. Combine with [notification policy throttling](throttle.md) for additional control over notification volume.
