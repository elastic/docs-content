---
navigation_title: Query alert history
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Use ES|QL in Discover to replay incidents, audit triage actions, and measure response times for alert episodes in Kibana's experimental alerting system."
---

# Query {{alerting-v2-system}} alert history in Discover [query-alert-history-discover]

Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts**. The **Alerts** page shows current episode state. Discover lets you go further and replay how an incident unfolded, view who acknowledged or snoozed it, measure time-to-acknowledge trends, or correlate alert history with other data in your environment.

For field definitions for both streams, refer to [Field reference](field-reference.md). For triage in the product UI, refer to [View and manage alerts](view-and-manage-alerts.md).

## Before you begin [add-data-views-before-begin]

Before you can query alert history in Discover, add the alert data streams as data views. Repeat these steps for each stream.

1. Open **Discover**, and then open the data view menu.
2. Select **Create a data view**.
3. Give your data view a name, for example `.rule-events` or `.alert-actions`.
4. In the **Index pattern** field, enter the data stream name:
   - `.ds-.rule-events-*` for rule evaluation history.
   - `.ds-.alert-actions-*` for triage actions recorded on alert episodes.
5. Open the **Timestamp field** dropdown and select `@timestamp`.
6. Select **Save data view to Kibana**.

For more details on data view options, refer to [Data views](../../../find-and-organize/data-views.md).

## Query episode and signal history [query-episode-signal-history]

Each rule evaluation produces one document in `.rule-events`. {{kib}} never overwrites these documents, which means you can reconstruct the full history of any episode by querying all documents that share the same `episode.id`. The following sections provide example queries for common scenarios.

### Reconstruct the lifecycle of a specific episode [replay-episode]

Use the `group_hash` to pull all evaluations for one series in chronological order. This shows exactly how the episode moved through its lifecycle states from open to close.

```esql
FROM .rule-events
// Scope to a single series by its group_hash
| WHERE group_hash == "<hash>"
// Sort oldest-first to read the progression forward in time
| SORT @timestamp ASC
// Keep the fields most relevant to reading the lifecycle sequence
| KEEP @timestamp, status, episode.id, episode.status, episode.status_count
```

### Find all currently active episodes [find-active-episodes]

Returns one row for each episode currently in `active` state, along with the timestamp of its most recent evaluation.

```esql
FROM .rule-events
// Only include rows where the episode lifecycle state is active
| WHERE episode.status == "active"
// Deduplicate to one row per episode, showing the most recent evaluation
| STATS latest = MAX(@timestamp) BY episode.id, group_hash
```

### List all breaches for a specific rule [list-rule-breaches]

Returns every evaluation row where the rule met its condition for a given rule. Use this to understand how often and how severely a rule fires across all its series.

```esql
FROM .rule-events
// Filter to one rule and only rows where the condition was met
| WHERE rule.id == "my-rule-id" AND status == "breached"
// Return fields that identify severity, series context, and the rule-defined payload
| KEEP @timestamp, group_hash, severity, episode.id, episode.status, data
```

### Identify evaluation gaps [identify-no-data]

`no_data` rows appear when the rule finds no matching data during an evaluation cycle. A cluster of these can indicate a data pipeline issue or a misconfigured rule.

```esql
FROM .rule-events
// no_data means the rule ran but found nothing to evaluate against
| WHERE status == "no_data"
| SORT @timestamp DESC
| LIMIT 50
```

## Query triage and action history [query-triage-action-history]

{{kib}} writes one document to `.alert-actions` for every action a user or the system takes on an episode. Use it to audit who did what, measure acknowledgment response times, or check current snooze and assignment state. The following sections provide example queries for common scenarios.

### View the full triage history for an episode [full-triage-history]

Returns all actions recorded for a single episode in chronological order. Use this to see the complete response sequence: who acknowledged it, whether a user snoozed it, and how it was eventually resolved.

```esql
FROM .alert-actions
// Scope to a single episode by its ID
| WHERE episode_id == "<episode-id>"
// Sort oldest-first to read the response sequence forward in time
| SORT @timestamp ASC
// Keep the fields most relevant to understanding what happened and who did it
| KEEP @timestamp, action_type, actor, episode_status, reason
```

### Find all acknowledgments in a time window [find-acknowledgments]

Returns every acknowledgment action across all episodes. Useful for tracking team response activity or measuring time-to-acknowledge trends.

```esql
FROM .alert-actions
// Filter to acknowledgment actions only
| WHERE action_type == "ack"
| SORT @timestamp DESC
```

### Check episode assignment state [check-assignments]

Returns all assign actions, showing which episodes carry an assignment and to whom. Use this to audit ownership or find unacknowledged handoffs.

```esql
FROM .alert-actions
// Filter to assignment actions only
| WHERE action_type == "assign"
// Return the fields that identify the episode, who assigned it, and the target user
| KEEP @timestamp, episode_id, actor, assignee_uid
```

### Audit dispatcher outcomes for a rule [audit-dispatcher-outcomes]

Returns all system-written actions for a rule, covering episodes the dispatcher opened, suppressed due to throttling, or didn't match to any action policy.

```esql
FROM .alert-actions
// Filter to one rule and only the three system-written dispatcher action types
| WHERE rule_id == "my-rule-id" AND action_type IN ("fire", "suppress", "unmatched")
| SORT @timestamp DESC
```

### Find snoozed series [find-snoozed-series]

Returns all snooze actions, including which series a user snoozed, who snoozed it, and when the snooze expires. Use this to find active snoozes or audit snooze history.

```esql
FROM .alert-actions
// Filter to snooze actions only
| WHERE action_type == "snooze"
// Return the fields needed to identify the series, the actor, and the expiry time
| KEEP @timestamp, group_hash, episode_id, expiry, actor
```

## Trace the full story of an incident [trace-incident]

To get the complete picture of an incident, filter both streams by the same identifier. Both streams share `group_hash` as a flat keyword, making it the most reliable join key. `episode.id` in `.rule-events` and `episode_id` in `.alert-actions` hold the same value but use different naming conventions: dot-notation in `.rule-events` and flat snake_case in `.alert-actions`.

:::{note}
Filter by `episode_id` to return user actions (`ack`, `assign`, `deactivate`, and similar) and notifications for one episode. Dispatcher-level entries might be missing because system-written action types (`fire`, `suppress`, `unmatched`, `notified`) key to `group_hash` and might not carry an `episode_id`. Filter by `group_hash` to include the complete dispatcher history.
:::

1. Run a `.rule-events` query to find the `episode.id` or `group_hash` you care about.
2. Query `.alert-actions` using that value:

```esql
FROM .alert-actions
// Use group_hash to include dispatcher actions that may not carry an episode_id
| WHERE group_hash == "<group-hash>"
| SORT @timestamp ASC
| KEEP @timestamp, action_type, actor, episode_id, reason
```

If you need to join both streams in a single query, use `LOOKUP JOIN`. This requires configuring `.alert-actions` as a lookup index, which is an extra setup step beyond standard Discover analysis:

```esql
FROM .rule-events
// Only include rows that belong to an alert episode (signals have no episode.id)
| WHERE episode.id IS NOT NULL
// Rename to match the join key naming convention in .alert-actions
| EVAL episode_id = episode.id
// Join with .alert-actions to surface triage actions alongside evaluation data
| LOOKUP JOIN .alert-actions ON episode_id
| KEEP @timestamp, status, action_type, actor
| SORT @timestamp DESC
```

For most exploratory analysis, running separate queries filtered by `group_hash` is simpler and avoids the `episode_id` optionality issue.
