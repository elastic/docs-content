---
navigation_title: Deactivate alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Stop lifecycle processing and notifications for a Kibana alerting v2 alert episode while the rule continues detecting new episodes."
---

# Deactivate Kibana alerting v2 alerts [deactivate-alerts-v2]

Deactivating an alert episode stops lifecycle processing and notifications for that episode. The rule continues running and can detect new episodes, but the deactivated episode is no longer tracked.

## How deactivation works

1. You deactivate an alert episode from the alert inbox, flyout, or detail page.
2. The dispatcher records a `deactivate` action for the episode.
3. On subsequent runs, the dispatcher checks for the deactivation and suppresses the episode with reason `deactivate`.
4. The episode is effectively closed — no further state transitions or notifications occur.

If the same condition later produces a new breach for the same series, a new episode is created and tracked independently.

## When to use deactivation

- **Known issues**: the alert represents a known condition that is being addressed but has not yet been fixed (for example, a planned capacity addition).
- **False positives**: the alert was triggered by a data anomaly and is not a real issue.
- **Stale alerts**: the alert is no longer relevant but has not recovered naturally (for example, the monitored host was decommissioned).

## Deactivate vs. other suppression

| Mechanism | What it does | Episode continues | New episodes affected |
|---|---|---|---|
| **Deactivate** | Stops all processing for the episode | No | No — new episodes are tracked normally |
| **Acknowledge** | Suppresses notifications for the episode | Yes — lifecycle continues | No |
| **Snooze** | Suppresses notifications for the series | Yes | Yes — affects all episodes during snooze |

Deactivation is the strongest per-episode action. Use it when you want to permanently close an episode. Use acknowledge when you want to suppress notifications but keep tracking the episode's lifecycle.

## Reactivation

You can reactivate a deactivated episode by selecting **Activate** from the alert actions menu. This resumes lifecycle processing and notifications.
