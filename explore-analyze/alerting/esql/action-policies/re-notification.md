---
navigation_title: Re-notification
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to configure action policies so a workflow re-notifies when an alert stays active without a status change."
---

# Re-notify for persistently active alerts [re-notification]

Use this page to configure a {{alerting-v2-system}} action policy so a workflow keeps running while an alert stays active without a status change.

The `On status change` frequency option invokes a workflow once for each status transition, for example when an alert activates or resolves. This is efficient for reducing noise from rules in {{alerting-v2-system}}, but a persistently active alert that only changes in severity doesn't cause another invocation.

To re-notify for alerts that stay active without a status change, use a time-based throttle.

- **`At most once every…`** Invokes a workflow again after the configured interval regardless of whether severity or status changed. Setting this to `1h` invokes a workflow every hour while the alert remains active and matched.
- **`On status change + repeat at interval`** Invokes a workflow on status change and then repeats at the configured interval while the alert stays in the same status.

In this example, you want to be re-paged if a critical alert stays open for more than an hour. Set the action policy frequency to `At most once every 1h`. The action policy invokes a workflow when the alert first matches and then again each hour until the alert resolves or no longer matches.

| Field | Value |
|---|---|
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Alert |
| **Frequency** | At most once every 1 hour |
| **Destinations** | PagerDuty workflow |

## Related pages

- [Manage severity escalation notifications](severity-escalation.md): Understand how severity changes interact with action policy matching.
- [Action policy reference](action-policy-reference.md): Look up all frequency options.
- [Create and configure an action policy](create-configure-action-policy.md): Apply the frequency settings described on this page.
