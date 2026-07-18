---
navigation_title: Severity escalation
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to manage notifications when alert episode severity changes in the experimental alerting system, including escalation, de-escalation, and duplicate notification prevention."
---

# Manage severity escalation notifications for the {{alerting-v2-system}} [severity-escalation]

Not every severity change fires a notification. The outcome depends on whether the action policy has already matched the episode and which frequency option you've selected.

## Notify when an episode escalates into a new severity threshold

Scope an action policy to the severity level you want notifications for. When an episode escalates into that severity level for the first time, the action policy fires because it has no prior notification record for the episode.

The following example uses an action policy scoped to `severity: "critical"`. An episode starts at `low` severity, so the action policy doesn't match. When the episode escalates to `critical`, the action policy now matches and fires regardless of the frequency setting, because it has never notified for this episode before.

| Field | Value |
|---|---|
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Prevent duplicate notifications when severity changes within an existing match

If an action policy already matched an episode, a severity escalation alone doesn't trigger re-notification when the episode's status stays the same. With `On status change` frequency, a severity change doesn't count as a status change.

In this example, Action Policy A matches all episodes regardless of severity and notified when the episode was `low`. When the episode escalates to `critical`, Action Policy A still matches, but the throttle blocks re-notification because the status hasn't changed. To re-notify on escalation, use a time-based throttle or create separate action policies for each severity level as described in [Route alert episodes by severity](route-by-severity.md).

| Field | Value |
|---|---|
| **Match conditions** | (None, matches all episodes) |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | Slack workflow |

## Stop notifications when an episode de-escalates below an action policy's threshold

If an episode drops below an action policy's severity threshold, the action policy stops matching and sends no further notifications. If the episode later escalates back above the threshold, the action policy fires again as if it were the first match.

In this example, Action Policy B targets only `severity: "critical"` episodes. An episode de-escalates from `critical` to `high`. Action Policy B no longer matches and stops sending notifications. If the episode later escalates back to `critical`, Action Policy B fires again.

| Field | Value |
|---|---|
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Related pages

- [Route alert episodes by severity](route-by-severity.md): Configure severity-scoped action policies to route episodes to separate workflows.
- [Re-notify for persistently active episodes](re-notification.md): Set up time-based frequency options to re-notify when an episode stays active.
- [Action policy reference](action-policy-reference.md): Look up match condition fields and frequency options.
