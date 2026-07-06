---
navigation_title: Re-notification
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to configure action policies to re-notify when an alert episode stays active without a status change in the experimental alerting system."
---

# Re-notify for persistently active episodes in the {{alerting-v2-system}} [controlling-re-notification]

The `On status change` frequency option notifies once per status transition, for example when an episode activates or resolves. This is efficient for reducing noise from rules in the {{alerting-v2-system}}, but a persistently active episode that only changes in severity doesn't re-trigger a notification.

To re-notify for episodes that stay active without a status change, use a time-based throttle.

- **`At most once every…`** Re-notifies after the configured interval regardless of whether severity or status changed. Setting this to `1h` sends a follow-up notification every hour while the episode remains active and matched.
- **`On status change + repeat at interval`** Notifies on status change and then repeats at the configured interval while the episode stays in the same status.

In this example, you want to be re-paged if a critical episode stays open for more than an hour. Set the action policy frequency to `At most once every 1h`. The action policy fires when the episode first matches and then again each hour until the episode resolves or no longer matches.

| Field | Value |
|---|---|
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | At most once every 1 hour |
| **Destinations** | PagerDuty workflow |

## Related pages

- [Manage severity escalation notifications](severity-escalation.md) for scenarios where a severity change determines whether a notification fires.
- [Action policy reference](action-policy-reference.md) for descriptions of all frequency options.
- [Create and configure an action policy](create-configure-action-policy.md) to set up the frequency settings described on this page.
