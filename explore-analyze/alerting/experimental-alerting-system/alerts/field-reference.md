---
navigation_title: Field reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Find field schemas for the .rule-events and .alert-actions data streams in Kibana's experimental alerting system. Covers evaluation event fields, triage action fields, and all action_type values."
---

# Alert data stream field reference [field-reference]

This page is a field reference for the {{alerting-v2-system}}. It documents the fields written to the two data streams that back alert history and triage data:

- **`.rule-events` field schema**: Fields written to the rule evaluation stream, including which fields are only present on alert documents.
- **`.alert-actions` field schema**: Fields written when a user or the system acts on an episode, including all `action_type` values.

Use this page when writing {{esql}} queries in Discover, interpreting alert UI state, or aligning API payloads with stored data. For query examples, refer to [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md). For triage controls in the UI, refer to [View and manage alerts](view-and-manage-alerts.md).

## `.rule-events` field schema [rule-events-field-schema]

Every rule evaluation writes a document to `.rule-events`. Fields use dot-notation for nested objects. The `episode.*` fields are only present on documents with `type: alert`.

| Field | Type | Description |
|---|---|---|
| `@timestamp` | date | When the evaluation ran. |
| `scheduled_timestamp` | date | The scheduled time for this evaluation. |
| `rule.id` | keyword | ID of the rule that produced this event. |
| `rule.version` | long | Version of the rule at evaluation time. |
| `group_hash` | keyword | Identifies the series this event belongs to. |
| `status` | keyword | Outcome of a single evaluation row, independent of episode lifecycle. Can be one of the following: `breached`, `recovered`, `no_data`. |
| `type` | keyword | Whether this document is a signal or an alert episode. Can be one of the following: `signal`, `alert`. |
| `severity` | keyword | Severity level assigned by the rule. Can be one of the following: `info`, `low`, `medium`, `high`, `critical`. |
| `episode.id` | keyword | ID of the alert episode. Only present on `type: alert` documents. |
| `episode.status` | keyword | Lifecycle state of the alert episode. Only present on `type: alert` documents. Can be one of the following: `inactive`, `pending`, `active`, `recovering`. |
| `episode.status_count` | long | Count of consecutive evaluations in the current `episode.status`. Set only for `pending` and `recovering`. |
| `data` | flattened | Rule-defined payload from the source query. |
| `source` | keyword | Source that produced the event. |
| `space_id` | keyword | {{kib}} space where the rule lives. |

## `.alert-actions` field schema [alert-actions-field-schema]

When a user or the system records an action on an alert episode, {{kib}} writes a document to `.alert-actions`. Use this stream for triage history, operational metrics such as mean time to acknowledge (MTTA), and auditing.

| Field | Type | Description |
|---|---|---|
| `@timestamp` | date | When {{kib}} wrote this action document. |
| `episode_id` | keyword | ID of the alert episode. |
| `episode_status` | keyword | Lifecycle state of the episode at the time of this action. Can be one of the following: `inactive`, `pending`, `active`, `recovering`. |
| `rule_id` | keyword | ID of the rule that owns the alert episode. |
| `group_hash` | keyword | Identifies the series the episode belongs to. |
| `action_type` | keyword | Identifies what happened and who initiated it. For more information, refer to [Action type values](#action-type-values). |
| `actor` | keyword | User who performed the action. Null for system-written action types. |
| `assignee_uid` | keyword | Target user for `assign` actions. |
| `last_series_event_timestamp` | date | Timestamp of the most recent event in the series, as of when this action occurred. |
| `expiry` | date | When the snooze expires. Only set for `snooze` actions. |
| `action_group_id` | keyword | The action group the episode belonged to at the time of this action. |
| `source` | keyword | Source that triggered the action. |
| `tags` | keyword[] | Tag values written by `tag` actions. |
| `reason` | text | Reason provided for `activate` or `deactivate` actions. |
| `space_id` | keyword | {{kib}} space where the alert episode lives. |

### Action type values [action-type-values]

Every `.alert-actions` document has an `action_type` that identifies what happened and who initiated it. Users trigger the user-written types through the API or UI. System-written types come from either rule evaluation (`fire`) or the dispatcher (`notified`, `suppress`, `unmatched`).

| Value | Written by | Meaning |
|---|---|---|
| `ack` | user | Acknowledge episode |
| `unack` | user | Remove acknowledgment |
| `assign` | user | Assign to user (`assignee_uid`) |
| `tag` | user | Add tags |
| `snooze` | user | Snooze until `expiry` |
| `unsnooze` | user | Remove snooze |
| `activate` | user | Manually activate the episode |
| `deactivate` | user | Manually deactivate the episode, resuming automatic recovery without closing it |
| `resolve` | user | Close the episode |
| `unresolve` | user | Reopen a resolved episode |
| `fire` | system | Episode opened or continued |
| `notified` | system | Workflow invoked |
| `suppress` | system | Notification throttled by the frequency limit |
| `unmatched` | system | No action policy matched the episode |
