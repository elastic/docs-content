---
navigation_title: Alert episode details
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Understand alert episodes — the full lifecycle arc from first breach to recovery — including states, identity, and status tracking."
---

# Kibana alerting v2 alert episode details [alert-episode-details-v2]

An episode is one full lifecycle arc of an alert, from the first breach to final recovery. Each episode groups the state transitions for a single alert series and is identified by a unique `episode_id`.

## Episode lifecycle

An episode transitions through these states:

```
inactive → pending → active → recovering → inactive
```

| State | Meaning |
|---|---|
| **Inactive** | The condition is not met. No episode exists or the previous episode has completed. |
| **Pending** | The condition is met but activation thresholds have not been satisfied. |
| **Active** | The condition is met and activation thresholds are satisfied. The alert is actionable. |
| **Recovering** | The condition is no longer met but recovery thresholds have not been satisfied. |

When a new breach is detected and no episode exists for that series, a new episode is created. The episode remains open through all state transitions until recovery completes and it returns to `inactive`.

## Episode identity

Each episode is identified by:

- **`episode_id`** — a unique identifier assigned when the episode is created.
- **`group_hash`** — the series identity, computed from the rule ID and grouping field values.
- **`rule.id`** — the rule that created the episode.

## Episode status tracking

Each alert event document includes the current episode status:

- `episode.status` — the current state (`inactive`, `pending`, `active`, `recovering`).
- `episode.status_count` — for `pending` and `recovering` states, tracks how many consecutive evaluations have been in that state. Used by count-based activation and recovery thresholds.

## Viewing episode details

From the alert inbox or flyout:

1. Click on an alert to open the flyout.
2. The **Overview** tab shows the current episode status, duration, and triggered timestamp.
3. The **timeline** visualization shows all alert events in the episode with their statuses.
4. Click **View details** for the full episode view with complete event history.

## Episode and suppression

Suppression actions are scoped to episodes:

- **Acknowledge** — suppresses notifications for a specific episode. If a new episode starts for the same series, notifications resume.
- **Deactivate** — stops lifecycle processing and notifications for the episode. The rule continues running and can detect new episodes.

Refer to [Alert actions](alert-actions.md) for details on these and other actions.
