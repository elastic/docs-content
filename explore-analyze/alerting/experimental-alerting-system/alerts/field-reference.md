---
navigation_title: Field reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Find field schemas for the .rule-events and .alert-actions data streams in the experimental alerting system. Covers shared signal and alert fields, alert-only episode fields, and all action_type values."
---

# Rule event and alert action field reference [field-reference]

This page is a field reference for the {{alerting-v2-system}}. It documents the fields written to the two data streams that back rule output and triage data:

- **`.rule-events` field schema**: Fields written for every rule evaluation. Alert episodes and signals share this stream and most fields. The `episode.*` fields appear only on alert documents.
- **`.alert-actions` field schema**: Fields written when a user or the system acts on an episode, including all `action_type` values.

Use this page when writing {{esql}} queries in Discover, interpreting alert UI state, or aligning API payloads with stored data. For how the shared schema works conceptually, refer to [Rule event data model](alert-data-model.md). For signal query examples, refer to [Observe and analyze signals](../observe-and-analyze-signals.md). For episode and triage query examples, refer to [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md). For triage controls in the UI, refer to [View and manage alerts](view-and-manage-alerts.md).

## `.rule-events` field schema [rule-events-field-schema]

Every rule evaluation writes a document to `.rule-events`. Fields use dot-notation for nested objects. The `episode.*` fields are only present on documents with `type: alert`.

| Field | Type | Signal | Alert episode | Description |
|---|---|---|---|---|
| `@timestamp` | date | ✅ | ✅ | When the evaluation ran. |
| `scheduled_timestamp` | date | ✅ | ✅ | The scheduled time for this evaluation. |
| `rule.id` | keyword | ✅ | ✅ | ID of the rule that produced this event. |
| `rule.version` | long | ✅ | ✅ | Version of the rule at evaluation time. |
| `group_hash` | keyword | ✅ | ✅ | Identifies the series this event belongs to. |
| `status` | keyword | ✅ | ✅ | Outcome of a single evaluation row, independent of episode lifecycle. Can be one of the following: `breached`, `recovered`, `no_data`. |
| `type` | keyword | ✅ | ✅ | Whether this document is a signal or an alert episode. Can be one of the following: `signal`, `alert`. |
| `severity` | keyword | ✅ | ✅ | Severity level assigned by the rule. Can be one of the following: `info`, `low`, `medium`, `high`, `critical`. |
| `data` | flattened | ✅ | ✅ | Rule-defined payload from the source query. |
| `source` | keyword | ✅ | ✅ | Source that produced the event. |
| `space_id` | keyword | ✅ | ✅ | {{kib}} space where the rule lives. |
| `episode.id` | keyword | — | ✅ | ID of the alert episode. |
| `episode.status` | keyword | — | ✅ | Lifecycle state of the alert episode. Can be one of the following: `inactive`, `pending`, `active`, `recovering`. |
| `episode.status_count` | long | — | ✅ | Count of consecutive evaluations in the current `episode.status`. Set only for `pending` and `recovering`. |

## `.alert-actions` field schema [alert-actions-field-schema]

When a user or the system records an action on an alert episode, {{kib}} writes a document to `.alert-actions`. Use this stream for triage history, operational metrics such as mean time to acknowledge (MTTA), and auditing. Signal documents never produce `.alert-actions` rows.

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

| Value | Written by | What happened |
|---|---|---|
| `ack` | user | Acknowledged the episode |
| `unack` | user | Removed the acknowledgment |
| `assign` | user | Assigned to a user (`assignee_uid`) |
| `tag` | user | Added tags |
| `snooze` | user | Snoozed until `expiry` |
| `unsnooze` | user | Removed the snooze |
| `activate` | user | Manually activated the episode |
| `deactivate` | user | Manually deactivated the episode, resuming automatic recovery without closing it |
| `resolve` | user | Closed the episode |
| `unresolve` | user | Reopened a resolved episode |
| `fire` | system | Episode opened or continued |
| `notified` | system | Workflow invoked |
| `suppress` | system | Notification throttled by the frequency limit |
| `unmatched` | system | No action policy matched the episode |
