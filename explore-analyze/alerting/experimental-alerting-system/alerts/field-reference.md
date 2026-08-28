---
navigation_title: Field reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Query experimental alerting data in Discover with .rule-events and .alert-actions field schemas. Reference tables list shared rule event fields, episode-only fields, and all action_type values."
---

# Rule event and alert action field reference [field-reference]

This page is a field reference for the {{alerting-v2-system}}. It documents the fields written to the two data streams that back rule output and triage data:

- **`.rule-events` field schema**: Fields written on each [rule event](../rules/rule-event-field-reference.md). Signals (events with `type: signal`) and events that belong to an alert episode (`type: alert`) share this stream and most fields. The `episode.*` fields appear only on events with `type: alert`.
- **`.alert-actions` field schema**: Fields written when a user or the system acts on an episode, including all `action_type` values.

Use these schemas when writing {{esql}} queries in Discover, interpreting alert UI state, or aligning API payloads with stored data.

## `.rule-events` field schema [rule-events-field-schema]

{{kib}} writes one rule event per matching row, per run, to `.rule-events`. When {{kib}} tracks an alert episode, it can also write `recovered` and `no_data` events. Fields use dot-notation for nested objects. The `episode.*` fields are only present on events that belong to an alert episode (`type: alert`).

The **`signal`** and **`alert`** columns show which `type` values include the field.

| Field | Type | `signal` | `alert` | Description |
|---|---|---|---|---|
| `@timestamp` | date | ✅ | ✅ | When {{kib}} wrote this document. |
| `scheduled_timestamp` | date | ✅ | ✅ | The scheduled start time for this rule run. |
| `rule.id` | keyword | ✅ | ✅ | ID of the rule that produced this event. |
| `rule.version` | long | ✅ | ✅ | Version of the rule at evaluation time. |
| `group_hash` | keyword | ✅ | ✅ | Identifies the series this event belongs to. |
| `status` | keyword | ✅ | ✅ | Outcome of a single evaluation row, independent of episode lifecycle. Signals are always `breached`. Events with `type: alert` can be `breached`, `recovered`, or `no_data`. |
| `type` | keyword | ✅ | ✅ | Event kind: `signal` (a signal) or `alert` (part of an alert episode). |
| `severity` | keyword | ✅ | ✅ | Optional. Set on `breached` events when the query emits a recognized value. Can be one of the following: `info`, `low`, `medium`, `high`, `critical`. Not set on `recovered` or `no_data` events. |
| `data` | flattened | ✅ | ✅ | Rule-defined payload from the source query. |
| `source` | keyword | ✅ | ✅ | Source that produced the event. |
| `space_id` | keyword | ✅ | ✅ | {{kib}} space where the rule lives. |
| `episode.id` | keyword | — | ✅ | ID of the alert episode this event belongs to. Events that share this value are the same episode. |
| `episode.status` | keyword | — | ✅ | Lifecycle state of the alert episode at this evaluation. Can be one of the following: `inactive`, `pending`, `active`, `recovering`. |
| `episode.status_count` | long | — | ✅ | Count of consecutive evaluations in the current `episode.status`. Set only for `pending` or `recovering`. |

## `.alert-actions` field schema [alert-actions-field-schema]

When a user or the system records an action on an alert episode, {{kib}} writes a document to `.alert-actions`. Use this stream for triage history, operational metrics such as mean time to acknowledge (MTTA), and auditing. Signals never produce `.alert-actions` rows.

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

## Related pages

- [Rule events](../rules/rule-event-field-reference.md): What a rule event is and how it connects to signals and alert episodes.
- [Rule event data model](rule-event-data-model.md): How signals (events with `type: signal`) and events that belong to an alert episode (`type: alert`) share `.rule-events`.
- [Query signals](query-signals.md): Signal query examples in Discover.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode and triage query examples.
- [View and manage alerts](view-and-manage-alerts.md): Monitor and filter alert episodes in the UI.
- [Triage alert episodes](triage-alert-episodes.md): UI actions that write `.alert-actions` documents.
