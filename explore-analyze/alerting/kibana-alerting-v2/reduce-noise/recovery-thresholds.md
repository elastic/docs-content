---
navigation_title: Recovery thresholds
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Require sustained recovery before a Kibana alerting v2 alert deactivates, preventing rapid toggling between active and recovered."
---

# Kibana alerting v2 recovery thresholds [recovery-thresholds-v2]

Recovery thresholds require a condition to be absent for a certain number of consecutive evaluations or for a minimum duration before an alert transitions from `recovering` to `inactive`. This prevents alerts from rapidly toggling between active and recovered (flapping).

## How it works

When an active alert's condition is no longer met, the alert enters `recovering` state instead of immediately returning to `inactive`. The alert remains in `recovering` until the recovery threshold is satisfied:

- **Count-based**: the condition must be absent for N consecutive evaluations.
- **Timeframe-based**: the condition must be absent for a minimum duration.
- **Combined**: both conditions (AND) or either one (OR).

If the condition returns before the threshold is satisfied, the alert goes back to `active`. The recovery counter resets.

## Configuration

```yaml
state_transition:
  recovering_count: 2
  recovering_timeframe: 10m
  recovering_operator: AND
```

This configuration requires 2 consecutive evaluations without a breach **and** at least 10 minutes of absence before the alert fully recovers.

## When to use

- **Intermittent conditions** that briefly resolve and then return (for example, network timeouts that clear for one evaluation cycle).
- **Rules where recovery notifications are disruptive** and you want to confirm the issue is truly resolved before notifying.
- **Environments with alert fatigue** from frequent active/recovered/active cycles.

## Relationship to activation thresholds

Activation and recovery thresholds work together:

- Activation thresholds gate the `pending` → `active` transition (require sustained breach).
- Recovery thresholds gate the `recovering` → `inactive` transition (require sustained recovery).

Together, they create a hysteresis effect that stabilizes alert lifecycle transitions.
