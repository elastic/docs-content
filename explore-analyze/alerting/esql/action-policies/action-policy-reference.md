---
navigation_title: Action policy reference
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Grouping modes, frequency options, dispatch outcomes, and match conditions field reference for action policies."
---

# Action policy reference [action-policy-reference]

This page is a reference for {{alerting-v2-system}} action policy match condition fields, grouping modes, frequency options, and dispatch outcomes. For step-by-step guidance, refer to [Create and configure an action policy](create-configure-action-policy.md).

## Match conditions fields [action-policy-matcher-fields]

Use the following fields in the **Match conditions** expression to filter which alerts an action policy applies to. Combine them with standard [KQL](../../../query-filter/languages/kql.md) operators, for example `severity: "critical" AND alert_status: "active"`.

| Field | Description | Example |
|---|---|---|
| `alert_id` {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` | Unique identifier of the alert. | `alert_id: "alert-001"` <br> Match a specific alert by ID. |
| `episode_id` {applies_to}`stack: experimental =9.5` | Unique identifier of the alert. Replaced by `alert_id` in later versions. | `episode_id: "ep-001"` <br> Match a specific alert by ID. |
| `alert_status` {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` | Current lifecycle status of the alert. One of `inactive`, `pending`, `active`, or `recovering`. | `alert_status: "active"` <br> Match only active alerts. |
| `episode_status` {applies_to}`stack: experimental =9.5` | Current lifecycle status of the alert. Replaced by `alert_status` in later versions. | `episode_status: "active"` <br> Match only active alerts. |
| `severity` | Current severity level. One of `info`, `low`, `medium`, `high`, or `critical`. Populated when the rule's {{esql}} query includes a `severity` column. Not set during recovery, so a severity-scoped policy applies only to open alerts. Severity can change during an alert without reopening it. The action policy picks up the new value on the next dispatcher cycle. For how to configure severity in a rule, refer to [Severity](../rules/configure-rule-severity.md). | `severity: "critical" OR severity: "high"` <br> Route high-priority alerts to a dedicated workflow. |
| `group_hash` | Stable hash identifying the alert series the alert belongs to. | `group_hash: "abc123"` <br> Match all alerts in a specific alert series. |
| `last_event_timestamp` | ISO 8601 timestamp of the most recent event recorded for the alert. | `last_event_timestamp > "2026-01-01"` <br> Match alerts with activity after a specific date. |
| `data.*` | Dynamic payload fields sent by the rule. Available fields depend on the rule type and configuration. Use for rule-specific fields not covered by the standard fields in this table. | `data.host.name: "web-01"` <br> Match alerts from a specific host in a host-based rule. |

:::{note}
:applies_to: {"serverless": "ga", "stack": "experimental 9.6+"}
To apply a policy to alerts from a set of rules, give the policy and those rules the same routing tag. **Match conditions** can't select alerts by the rule's ID, name, or tags. To learn more, refer to [Apply the policy to alerts from specific rules](create-configure-action-policy.md#routing-tags).
:::

### Rule fields [action-policy-matcher-rule-fields]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

In addition to the alert fields, you can use the following fields in the **Match conditions** expression to select alerts by the rule that produced them.

| Field | Description | Example |
|---|---|---|
| `rule.id` | Unique identifier of the rule that generated the alert. | `rule.id: "rule-001"` <br> Match alerts from one specific rule. |
| `rule.name` | Display name of the rule. | `rule.name: "High CPU"` <br> Match alerts from rules with this display name. |
| `rule.tags` | Tags attached to the rule. | `rule.tags: "payment-service"` <br> Match alerts from all rules with this tag. |

:::{important}
After you upgrade from this version, action policies whose **Match conditions** use these rule fields, `episode_id`, or `episode_status` no longer select the alerts you expect. {{kib}} keeps the expression and doesn't show an error. A condition such as `rule.tags: "checkout"` stops matching any alert, so the policy stops invoking its workflows. A negated condition such as `NOT rule.tags: "checkout"` matches every alert. To fix these policies after you upgrade, add the same routing tag to each policy and its rules, and replace `episode_id` and `episode_status` with `alert_id` and `alert_status`.
:::

## Notify per options [action-policy-notification-grouping]

Controls how the action policy batches alerts before invoking a workflow.

| Option | Description | When to use |
|---|---|---|
| Alert | The action policy invokes a workflow once for each alert, independently of other alerts. Default selection. | You need issue-level visibility and want to handle each problem separately. |
| Group | The action policy bundles alerts that share the same value for a specified `data.*` field into one workflow invocation for each unique value. Each unique value forms a **notification group**. | A rule produces many related alerts, such as one for each service or host, and you want to reduce noise by batching them into shared notifications. |
| Digest | The action policy combines all matching alerts into a single workflow invocation, regardless of what they have in common. | You want a single periodic summary of everything in scope, rather than individual alerts. |

## Frequency [action-policy-throttle-strategies]

Frequency controls how often the action policy can invoke a workflow for a given alert or notification group. The available options depend on the **Notify per** setting. Not all options are valid for all modes.

:::{note}
The `.alert-actions` data stream records a throttled notification as `suppress`, not `throttled`. This is the same event described as `throttled` in the action policy execution history and event log. The two streams use different vocabulary. For the full mapping, refer to [Event-log outcomes and .alert-actions action types](review-action-policy-execution-history.md#outcome-vocab-mapping).
:::

| Option | Description | When to use |
|---|---|---|
| On status change | Invokes a workflow when the alert status changes, for example from active to recovering. One notification for each transition. | You only need to know when something breaks and when it's resolved. Use this when you trust your ticketing or incident workflow to track ongoing issues. |
| On status change + repeat at interval | Invokes a workflow on status change, then repeats at a regular interval while the alert remains in the same status. | You want status change notifications plus periodic reminders that a problem is still unresolved, in case it has been missed or pushed aside. |
| At most once every… | Limits notifications at one for each alert or notification group within the chosen interval, regardless of rule frequency. | You want to limit notification volume for noisy rules without missing new or ongoing issues. |
| Every evaluation | Invokes a workflow on every rule evaluation. Can be noisy. Use sparingly and only with infrequent rule schedules. | You need a full audit trail of every evaluation, or the rule runs infrequently enough that noise isn't a concern. |

### Frequency options for Alert [action-policy-frequency-episode]

Available frequency options when you set **Notify per** to **Alert**.

| Option | Description | Example |
|---|---|---|
| On status change | Invokes a workflow once when the alert opens and once when it recovers. No repeat notifications while it remains active. | A host goes down at 9:00am → one notification. Recovers at 11:00am → one notification. No notifications between them. |
| On status change + repeat at interval | Same as On status change, but also sends a reminder at a set interval while the alert is still active. | A host goes down at 9:00am → notification. With a 1h repeat: reminder at 10:00am, 11:00am. Recovers at 11:30am → notification. |
| At most once every… | Limits notifications at one for the alert within the chosen interval, regardless of severity or status changes. Use to re-notify for an alert that stays active without a status change. Refer to [Re-notify for persistently active alerts](re-notification.md). | A critical alert stays open for 3 hours. With a 1h limit, you get a notification when it opens and again every hour it remains open. |
| Every evaluation | Invokes a workflow on every rule evaluation, regardless of status. Can be noisy on frequent rule schedules. Avoid in production. | A rule running every 5 minutes with one active alert produces up to 288 notifications a day. |

### Frequency options for Group [action-policy-frequency-group]

Available frequency options when you set **Notify per** to **Group**.

| Option | Description | Example |
|---|---|---|
| At most once every… | Limits how often each notification group can invoke a workflow, regardless of how many alerts it contains or how often the rule runs. | 10 alerts share `data.host.name: "web-01"`. With a 1h limit, you get at most one notification an hour for that notification group. |
| Every evaluation | Invokes a workflow on every rule evaluation for each unique value in the group-by field. Still noisy on frequent rule schedules. | A rule running every 10 minutes with 5 unique host values produces up to 6 notifications an hour for each host. |

### Frequency options for Digest [action-policy-frequency-digest]

Available frequency options when you set **Notify per** to **Digest**.

| Option | Description | Example |
|---|---|---|
| At most once every… (default) | Limits digest delivery to at most one bundled summary within the chosen interval, regardless of how often the rule runs. | A rule running every 5 minutes with a 1h digest interval sends one bundled summary an hour containing all matching alerts from that period. |
| Every evaluation | Invokes a workflow on every rule run, bundling all matching alerts into one message. Can be noisy on frequent rule schedules. | A rule running every 30 minutes with 20 matching alerts produces one summary every 30 minutes containing all 20. |

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Apply these settings when configuring match conditions, grouping, and frequency.
- [About action policies](about-action-policies.md): Understand the eligibility, scope, and frequency gates that run before dispatch.
- [Review action policy execution history](review-action-policy-execution-history.md): Check dispatcher outcomes and investigate unexpected notification behavior.