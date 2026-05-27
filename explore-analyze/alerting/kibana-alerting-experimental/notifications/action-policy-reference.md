---
navigation_title: Action policy reference
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Grouping modes, frequency options, dispatch outcomes, and match conditions field reference for action policies in the {{alerting-v2}}."
---

# Action policy reference [action-policy-reference]


Action policies are part of the {{alerting-v2}} in {{kib}}. This page is a reference for match conditions fields, grouping modes, frequency options, and dispatch outcomes. For step-by-step guidance, refer to [Create and configure an action policy](create-configure-action-policy.md).

## Match conditions fields [matcher-fields]

Use these fields in the **Match conditions** expression to filter which episodes a policy applies to. Combine them with standard KQL operators, for example `data.severity: "critical" AND episode_status: "active"`.

| Field | Description | Example |
|---|---|---|
| `episode_status` | Current lifecycle status of the episode. Accepted values: `active`, `inactive`, `pending`, `recovering`. | `episode_status: "active"` |
| `data.*` | Dynamic payload fields sent by the rule. Available fields depend on the rule type and configuration. | `data.severity: "critical"` or `data.host.name: "web-01"` |
| `rule.id` | Unique identifier for the rule that generated the episode. | `rule.id: "rule-001"` |
| `rule.name` | Display name of the rule. | `rule.name: "High CPU"` |
| `rule.tags` | Tags attached to the rule. Use to match episodes from rules with a specific tag. | `rule.tags: "payment-service"` |
| `rule.labels` | Key-value labels attached to the rule. Use dot notation to target a specific label key. | `rule.labels.env: "production"` |

<!--[CONTENT NEEDED for M2: M2 adds two first-class episode-level severity fields that will be directly matchable in KQL:

- `episode.severity` - The current severity of the episode (most recent evaluation). Enables matching like `episode.severity: "CRITICAL"`.
- `episode.severity_max` - The highest severity seen over the episode's lifetime. Enables matching like `episode.severity_max: "CRITICAL"` to catch episodes that were once critical even if they have since de-escalated.

Add both fields to this table with examples. Update the introductory sentence to include them. Also remove or deprecate the `data.severity` example once `episode.severity` is the preferred approach, otherwise users will get conflicting guidance about which field to use for severity matching.

There is also an open M2 question about whether a severity change mid-episode (de-escalation or escalation) triggers policy re-evaluation. If it does, document the re-evaluation behavior in the frequency options section below, since it interacts with frequency limits.]
-->

## Notify per options [notification-grouping]

Controls how the policy batches matching episodes before sending a notification.

| Option | Description | When to use |
|---|---|---|
| Episode | Each episode triggers its own notification independently. Default selection. | You need per-issue visibility and want to handle each problem separately. |
| Group | The policy bundles episodes that share the same value for a specified `data.*` field into one notification per unique value. Each unique value forms a **notification group**. | A rule produces many related episodes, such as one per service or host, and you want to reduce noise by batching them into shared notifications. |
| Digest | The policy combines all matching episodes into a single notification, regardless of what they have in common. | You want a single periodic summary of everything that matched, rather than individual alerts. |

## Frequency [throttle-strategies]

**Frequency** controls how often the policy fires for a given episode or notification group. The available options depend on the **Notify per** setting. Not all options are valid for all modes.

| Option | Description | When to use |
|---|---|---|
| On status change | Notifies when the episode status changes, for example from active to recovering. One notification per transition. | You only need to know when something breaks and when it's resolved. No reminders needed. |
| On status change + repeat at interval | Notifies on status change, then resends notifications at a regular interval while the episode remains in the same status. | You want status change alerts plus periodic notifications that a problem is still unresolved, in case it has been missed or pushed aside. |
| At most once every… | Caps notifications at one per episode or notification group within the chosen interval, regardless of rule frequency. | You want to limit alert volume for noisy rules without missing new or ongoing issues. |
| Every evaluation | Notifies on every rule evaluation. Can be noisy. Use sparingly and only with infrequent rule schedules. | You need a full audit trail of every evaluation, or the rule runs infrequently enough that noise isn't a concern. |

<!--[CONTENT NEEDED for M2: An open M2 question is whether a severity change mid-episode (escalation or de-escalation of `episode.severity`) triggers policy re-evaluation independently of episode status changes. If it does, this table needs a new strategy option or a note explaining the interaction between severity changes and the "On status change" option. Confirm the M2 decision before updating.]
-->

### Frequency options for Episode [frequency-when-episode-per_episode]

Available frequency options when you set **Notify per** to **Episode**.

| Option | Description | Example |
|---|---|---|
| On status change | Notifies once when the episode opens and once when it recovers. No repeat notifications while it remains active. Best for when you trust your ticketing or incident workflow to track ongoing issues | A host goes down at 9:00am → one notification. Recovers at 11:00am → one notification. No notifications between them. |
| On status change + repeat at interval | Same as On status change, but also sends a reminder at a set interval while the episode is still active. | A host goes down at 9:00am → notification. With a 1h repeat: reminder at 10:00am, 11:00am. Recovers at 11:30am → notification. |
| Every evaluation | Fires on every rule evaluation, regardless of status. Can be noisy on frequent rule schedules. Avoid in production. | A rule running every 5 minutes with one active episode produces up to 288 notifications per day. |

### Frequency options for Group

Available frequency options when you set **Notify per** to **Group**.

| Option | Description | Example |
|---|---|---|
| At most once every… | Limits how often each notification group can notify, regardless of how many episodes match or how often the rule runs. | 10 episodes share `data.host.name: "web-01"`. With a 1h limit, you get at most one notification per hour for that notification group. |
| Every evaluation | Fires on every rule evaluation for each unique value in the group-by field. Still noisy on frequent rule schedules. | A rule running every 10 minutes with 5 unique host values produces up to 6 notifications per host per hour. |

### Frequency options for Digest

Available frequency options when you set **Notify per** to **Digest**.

| Option | Description | Example |
|---|---|---|
| Every evaluation | The only option for Digest. Fires on every rule run, bundling all matching episodes into one message. Pair with a longer rule schedule to avoid frequent summary messages. | A rule running every 30 minutes with 20 matching episodes produces one summary notification every 30 minutes containing all 20. |

## Dispatch outcomes

The system records each notification attempt with one of the following outcomes. To investigate delivery issues, query the `.alert-actions` data stream in Discover and filter by the `outcome` field.

| Outcome | What happened |
|---|---|
| `dispatched` | The system sent the notification successfully. |
| `throttled` | The system skipped delivery because the **frequency** interval had not elapsed. This is expected behavior, not an error. |
| `suppressed` | Dispatch was blocked before the notification went out. The episode was acknowledged, snoozed, or deactivated, or the space is currently in a [maintenance window](../../alerts/maintenance-windows.md). |
| `unmatched` | No action policy matched this episode, so no workflow ran. |
| `error` | An error occurred during processing. Check {{kib}} logs to identify the cause. |