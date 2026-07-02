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

Not every severity change fires a notification. The outcome depends on whether the action policy has already matched the episode and which frequency option is configured.

## Notify when an episode escalates into a new severity threshold

Scope a policy to the severity level you want to be notified about. When an episode escalates into that severity level for the first time, the policy fires because it has no prior notification record for the episode.

The following example uses a policy scoped to `severity: "critical"`. An episode starts at `low` severity, so the policy does not match. When the episode escalates to `critical`, the policy now matches and fires regardless of the frequency setting, because it has never notified for this episode before.

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Prevent duplicate notifications when severity changes within an existing match

If a policy already matched an episode at a lower severity and the episode escalates, the policy does not automatically re-notify. With `On status change` frequency, a severity change alone does not count as a status change.

In this example, Policy A matches all episodes regardless of severity. It notified when the episode was `low`. The episode escalates to `critical`, but Policy A still matches and the status has not changed, only the severity has. The throttle blocks re-notification. To re-notify on escalation, use a time-based throttle or create separate policies per severity level as described in [Route alert episodes by severity](route-by-severity.md).

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | (None, matches all episodes) |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | Slack workflow |

## Stop notifications when an episode de-escalates below a policy's threshold

If an episode drops below a policy's severity threshold, the policy stops matching and sends no further notifications. If the episode later escalates back above the threshold, the policy fires again as if it were the first match.

In this example, Policy B is scoped to `severity: "critical"`. An episode de-escalates from `critical` to `high`. Policy B no longer matches and stops sending notifications. If the episode later escalates back to `critical`, Policy B fires again.

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Related pages

- [Route alert episodes by severity](route-by-severity.md) for configuration examples that use severity-scoped policies to separate routing destinations.
- [Re-notify for persistently active episodes](re-notification.md) for time-based throttle options that re-notify when an episode stays active.
- [Action policy reference](action-policy-reference.md) for match condition fields and frequency options.
