---
navigation_title: Severity escalation
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to manage notifications when alert severity changes, including escalation, de-escalation, and duplicate notification prevention."
---

# Manage severity escalation notifications [severity-escalation]

Use this page to control when {{alerting-v2-system}} runs a workflow as an alert's severity changes, including first-time matches, duplicate invocations, and de-escalation. Not every severity change invokes a workflow. The outcome depends on whether the action policy has already matched the alert and which frequency option you've selected.

## Notify when an alert escalates into a new severity threshold

Scope an action policy to the severity level you want a workflow to run for. When an alert escalates into that severity level for the first time, the action policy invokes a workflow because it has no prior invocation record for the alert.

The following example uses an action policy scoped to `severity: "critical"`. An alert starts at `low` severity, so the action policy doesn't match. When the alert escalates to `critical`, the action policy now matches and invokes a workflow regardless of the frequency setting, because it has never invoked a workflow for this alert before.

| Field | Value |
|---|---|
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Alert |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Prevent duplicate notifications when severity changes within an existing match

If an action policy already matched an alert, a severity escalation alone doesn't trigger re-notification when the alert's status stays the same. With `On status change` frequency, a severity change doesn't count as a status change.

In this example, Action Policy A matches all alerts regardless of severity and notified when the alert was `low`. When the alert escalates to `critical`, Action Policy A still matches, but the throttle blocks re-notification because the status hasn't changed. To re-notify on escalation, use a time-based throttle or create separate action policies for each severity level as described in [Route alerts by severity](route-by-severity.md).

| Field | Value |
|---|---|
| **Match conditions** | (None, matches all alerts) |
| **Notify per** | Alert |
| **Frequency** | On status change |
| **Destinations** | Slack workflow |

## Stop notifications when an alert de-escalates below an action policy's threshold

If an alert drops below an action policy's severity threshold, the action policy stops matching and doesn't invoke a workflow. If the alert later escalates back above the threshold, the action policy invokes a workflow again as if it were the first match.

In this example, Action Policy B targets only `severity: "critical"` alerts. An alert de-escalates from `critical` to `high`. Action Policy B no longer matches and stops invoking a workflow. If the alert later escalates back to `critical`, Action Policy B invokes a workflow again.

| Field | Value |
|---|---|
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Alert |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Related pages

- [Route alerts by severity](route-by-severity.md): Configure severity-scoped action policies to route alerts to separate workflows.
- [Re-notify for persistently active alerts](re-notification.md): Set up time-based frequency options to re-notify when an alert stays active.
- [Action policy reference](action-policy-reference.md): Look up match condition fields and frequency options.
