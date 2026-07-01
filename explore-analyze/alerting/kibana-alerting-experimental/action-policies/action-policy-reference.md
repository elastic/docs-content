---
navigation_title: Action policy reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Grouping modes, frequency options, dispatch outcomes, and match conditions field reference for action policies in the experimental alerting system."
---

# Action policy reference for the {{alerting-v2-system}} [action-policy-reference]

Action policies are part of the {{alerting-v2-system}} in {{kib}}. This page is a reference for match conditions fields, grouping modes, frequency options, and dispatch outcomes. For step-by-step guidance, refer to [Create and configure an action policy](create-configure-action-policy.md).

## Match conditions fields [matcher-fields]

Use these fields in the **Match conditions** expression to filter which alert episodes a policy applies to. Combine them with standard [KQL](../../../query-filter/languages/kql.md) operators, for example `severity: "critical" AND episode_status: "active"`.

| Field | Type | Description | Accepted values | Example |
|---|---|---|---|---|
| `episode_id` | string | Unique identifier of the alert episode. | Any string | `episode_id: "ep-001"` |
| `episode_status` | string | Current lifecycle status of the alert episode. | `inactive`, `pending`, `active`, `recovering` | `episode_status: "active"` |
| `severity` | string | Current severity of the alert episode. Populated when the rule's {{esql}} query includes a `severity` column whose value matches a supported level (case-insensitive). Unrecognized values are silently ignored and the field is absent. Not set during recovery. Use to route high-severity episodes to dedicated workflows. | `info`, `low`, `medium`, `high`, `critical` | `severity: "critical" OR severity: "high"` |
| `group_hash` | string | Stable hash identifying the alert series the alert episode belongs to. | Any string | `group_hash: "abc123"` |
| `last_event_timestamp` | string | ISO 8601 timestamp of the most recent event recorded for the alert episode. | ISO 8601 timestamp | `last_event_timestamp > "2026-01-01"` |
| `rule.id` | string | Unique identifier of the rule that generated the alert episode. | Any string | `rule.id: "rule-001"` |
| `rule.name` | string | Display name of the rule. | Any string | `rule.name: "High CPU"` |
| `rule.tags` | string[] | Tags attached to the rule. Use to match alert episodes from rules with a specific tag. | Any string | `rule.tags: "payment-service"` |
| `data.*` | object | Dynamic payload fields sent by the rule. Available fields depend on the rule type and configuration. Use for rule-specific fields not covered by the standard episode fields above. | Depends on rule type | `data.host.name: "web-01"` |

<!--[CONTENT NEEDED: 
When rule authoring docs are created (issue #6689), link from this table row to the rule authoring page that explains how to include a `severity` column in the ES|QL query. The full severity contract (column name, case-insensitivity, silent-ignore behavior) belongs in the rule authoring reference, not here.]
-->

## Notify per options [notification-grouping]

Controls how the policy batches matching episodes before sending a notification.

| Option | Description | When to use |
|---|---|---|
| Episode | The policy sends one notification per alert episode, independently of other episodes. Default selection. | You need per-issue visibility and want to handle each problem separately. |
| Group | The policy bundles alert episodes that share the same value for a specified `data.*` field into one notification per unique value. Each unique value forms a **notification group**. | A rule produces many related alert episodes, such as one per service or host, and you want to reduce noise by batching them into shared notifications. |
| Digest | The policy combines all matching alert episodes into a single notification, regardless of what they have in common. | You want a single periodic summary of everything that matched, rather than individual alert episodes. |

## Frequency [throttle-strategies]

Frequency controls how often the policy fires for a given alert episode or notification group. The available options depend on the **Notify per** setting. Not all options are valid for all modes.

| Option | Description | When to use |
|---|---|---|
| On status change | Notifies when the alert episode status changes, for example from active to recovering. One notification per transition. | You only need to know when something breaks and when it's resolved. Use this when you trust your ticketing or incident workflow to track ongoing issues. |
| On status change + repeat at interval | Notifies on status change, then resends notifications at a regular interval while the alert episode remains in the same status. | You want status change notifications plus periodic reminders that a problem is still unresolved, in case it has been missed or pushed aside. |
| At most once every… | Caps notifications at one per alert episode or notification group within the chosen interval, regardless of rule frequency. | You want to limit notification volume for noisy rules without missing new or ongoing issues. |
| Every evaluation | Notifies on every rule evaluation. Can be noisy. Use sparingly and only with infrequent rule schedules. | You need a full audit trail of every evaluation, or the rule runs infrequently enough that noise isn't a concern. |

### Frequency options for Episode [frequency-when-episode-per_episode]

Available frequency options when you set **Notify per** to **Episode**.

| Option | Description | Example |
|---|---|---|
| On status change | Notifies once when the alert episode opens and once when it recovers. No repeat notifications while it remains active. | A host goes down at 9:00am → one notification. Recovers at 11:00am → one notification. No notifications between them. |
| On status change + repeat at interval | Same as On status change, but also sends a reminder at a set interval while the alert episode is still active. | A host goes down at 9:00am → notification. With a 1h repeat: reminder at 10:00am, 11:00am. Recovers at 11:30am → notification. |
| Every evaluation | Fires on every rule evaluation, regardless of status. Can be noisy on frequent rule schedules. Avoid in production. | A rule running every 5 minutes with one active alert episode produces up to 288 notifications per day. |

### Frequency options for Group

Available frequency options when you set **Notify per** to **Group**.

| Option | Description | Example |
|---|---|---|
| At most once every… | Limits how often each notification group can notify, regardless of how many alert episodes match or how often the rule runs. | 10 alert episodes share `data.host.name: "web-01"`. With a 1h limit, you get at most one notification per hour for that notification group. |
| Every evaluation | Fires on every rule evaluation for each unique value in the group-by field. Still noisy on frequent rule schedules. | A rule running every 10 minutes with 5 unique host values produces up to 6 notifications per host per hour. |

### Frequency options for Digest

Available frequency options when you set **Notify per** to **Digest**.

| Option | Description | Example |
|---|---|---|
| At most once every… (default) | Caps digest delivery to at most one bundled summary within the chosen interval, regardless of how often the rule runs. | A rule running every 5 minutes with a 1h digest interval sends one bundled summary per hour containing all matching alert episodes from that period. |
| Every evaluation | Fires on every rule run, bundling all matching alert episodes into one message. Can be noisy on frequent rule schedules. | A rule running every 30 minutes with 20 matching alert episodes produces one summary every 30 minutes containing all 20. |

## Dispatch outcomes

The dispatcher records each run with one of the following outcomes. To investigate delivery issues, open Discover, query the `.alert-actions` index, and filter by the `action_type` field.

| Outcome | What happened |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert episode. |
| `throttled` | The alert episode matched a policy but was rate-limited by the frequency setting. No workflow ran. This is expected behavior, not an error. |
| `suppressed` | Dispatch was blocked. The alert episode was acknowledged, snoozed, or deactivated, or the space is currently in a [maintenance window](../../alerts/maintenance-windows.md). |
| `unmatched` | No action policy matched the alert episode. No workflow ran. |

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md) to apply these fields and options when setting up a policy.
- [Manage action policies in {{alerting-v2-system}}](manage-action-policies.md) to enable, disable, snooze, or audit your policies.
- [About action policies](about-action-policies.md) to understand how action policies evaluate and gate alert episodes.