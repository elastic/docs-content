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

This page is a reference for action policy match condition fields, grouping modes, frequency options, and dispatch outcomes in the {{alerting-v2-system}}. For step-by-step guidance, refer to [Create and configure an action policy](create-configure-action-policy.md).

## Match conditions fields [action-policy-matcher-fields]

Use these fields in the **Match conditions** expression to filter which alert episodes an action policy applies to. Combine them with standard [KQL](../../../query-filter/languages/kql.md) operators, for example `severity: "critical" AND episode_status: "active"`.

| Field | Description | Example |
|---|---|---|
| `episode_id` | Unique identifier of the alert episode. | `episode_id: "ep-001"` <br> Match a specific episode by ID. |
| `episode_status` | Current lifecycle status of the alert episode. One of `inactive`, `pending`, `active`, or `recovering`. | `episode_status: "active"` <br> Match only active episodes. |
| `severity` | Current severity level. One of `info`, `low`, `medium`, `high`, or `critical`. Populated when the rule's {{esql}} query includes a matching `severity` column (case-insensitive). Not set during recovery. Unrecognized values are ignored. | `severity: "critical" OR severity: "high"` <br> Route high-priority episodes to a dedicated workflow. |
| `group_hash` | Stable hash identifying the alert series the episode belongs to. | `group_hash: "abc123"` <br> Match all episodes in a specific alert series. |
| `last_event_timestamp` | ISO 8601 timestamp of the most recent event recorded for the episode. | `last_event_timestamp > "2026-01-01"` <br> Match episodes with activity after a specific date. |
| `rule.id` | Unique identifier of the rule that generated the episode. | `rule.id: "rule-001"` <br> Match episodes from one specific rule. |
| `rule.name` | Display name of the rule. | `rule.name: "High CPU"` <br> Match episodes from rules with this display name. |
| `rule.tags` | Tags attached to the rule. | `rule.tags: "payment-service"` <br> Match episodes from all rules with this tag. |
| `data.*` | Dynamic payload fields sent by the rule. Available fields depend on the rule type and configuration. Use for rule-specific fields not covered by the standard fields in this table. | `data.host.name: "web-01"` <br> Match episodes from a specific host in a host-based rule. |

<!--[TODO after PR #6523 merges]: Replace the `severity` row above with this line:

| `severity` | Current severity level. One of `info`, `low`, `medium`, `high`, or `critical`. Populated when the rule's {{esql}} query includes a `severity` column. Not set during recovery; severity-scoped matchers only match open episodes. Severity can change mid-episode without reopening it — action policy matching picks up the new value on the next dispatcher cycle. For how to configure severity in a rule, refer to [Severity](../rules/configure-rule-severity.md). | `severity: "critical" OR severity: "high"` <br> Route high-priority episodes to a dedicated workflow. |

-->

## Notify per options [action-policy-notification-grouping]

Controls how the action policy batches matching episodes before sending a notification.

| Option | Description | When to use |
|---|---|---|
| Episode | The action policy sends one notification for each alert episode, independently of other episodes. Default selection. | You need issue-level visibility and want to handle each problem separately. |
| Group | The action policy bundles alert episodes that share the same value for a specified `data.*` field into one notification for each unique value. Each unique value forms a **notification group**. | A rule produces many related alert episodes, such as one for each service or host, and you want to reduce noise by batching them into shared notifications. |
| Digest | The action policy combines all matching alert episodes into a single notification, regardless of what they have in common. | You want a single periodic summary of everything that matched, rather than individual alert episodes. |

## Frequency [action-policy-throttle-strategies]

Frequency controls how often the action policy fires for a given alert episode or notification group. The available options depend on the **Notify per** setting. Not all options are valid for all modes.

| Option | Description | When to use |
|---|---|---|
| On status change | Notifies when the alert episode status changes, for example from active to recovering. One notification for each transition. | You only need to know when something breaks and when it's resolved. Use this when you trust your ticketing or incident workflow to track ongoing issues. |
| On status change + repeat at interval | Notifies on status change, then resends notifications at a regular interval while the alert episode remains in the same status. | You want status change notifications plus periodic reminders that a problem is still unresolved, in case it has been missed or pushed aside. |
| At most once every… | Caps notifications at one for each alert episode or notification group within the chosen interval, regardless of rule frequency. | You want to limit notification volume for noisy rules without missing new or ongoing issues. |
| Every evaluation | Notifies on every rule evaluation. Can be noisy. Use sparingly and only with infrequent rule schedules. | You need a full audit trail of every evaluation, or the rule runs infrequently enough that noise isn't a concern. |

### Frequency options for Episode [action-policy-frequency-episode]

Available frequency options when you set **Notify per** to **Episode**.

| Option | Description | Example |
|---|---|---|
| On status change | Notifies once when the alert episode opens and once when it recovers. No repeat notifications while it remains active. | A host goes down at 9:00am → one notification. Recovers at 11:00am → one notification. No notifications between them. |
| On status change + repeat at interval | Same as On status change, but also sends a reminder at a set interval while the alert episode is still active. | A host goes down at 9:00am → notification. With a 1h repeat: reminder at 10:00am, 11:00am. Recovers at 11:30am → notification. |
| Every evaluation | Fires on every rule evaluation, regardless of status. Can be noisy on frequent rule schedules. Avoid in production. | A rule running every 5 minutes with one active alert episode produces up to 288 notifications a day. |

### Frequency options for Group [action-policy-frequency-group]

Available frequency options when you set **Notify per** to **Group**.

| Option | Description | Example |
|---|---|---|
| At most once every… | Limits how often each notification group can notify, regardless of how many alert episodes match or how often the rule runs. | 10 alert episodes share `data.host.name: "web-01"`. With a 1h limit, you get at most one notification an hour for that notification group. |
| Every evaluation | Fires on every rule evaluation for each unique value in the group-by field. Still noisy on frequent rule schedules. | A rule running every 10 minutes with 5 unique host values produces up to 6 notifications an hour for each host. |

### Frequency options for Digest [action-policy-frequency-digest]

Available frequency options when you set **Notify per** to **Digest**.

| Option | Description | Example |
|---|---|---|
| At most once every… (default) | Caps digest delivery to at most one bundled summary within the chosen interval, regardless of how often the rule runs. | A rule running every 5 minutes with a 1h digest interval sends one bundled summary an hour containing all matching alert episodes from that period. |
| Every evaluation | Fires on every rule run, bundling all matching alert episodes into one message. Can be noisy on frequent rule schedules. | A rule running every 30 minutes with 20 matching alert episodes produces one summary every 30 minutes containing all 20. |

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Apply these settings when configuring match conditions, grouping, and frequency.
- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, and rotate API keys for your action policies.
- [Review action policy execution history](review-action-policy-execution-history.md): Check dispatcher outcomes and investigate unexpected notification behavior.
- [About action policies](about-action-policies.md): Understand the eligibility, match, and frequency gates that run before dispatch.