---
navigation_title: Alert states and fields
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Reference for {{alerting-v2}} episode status, `.rule-events` row status, and `.alert-actions` document fields."
---

# Alert states and fields reference [alert-states-reference-v2]

$$$alert-states-reference-v2$$$

Use these tables when you read alert UI state, query `.rule-events` or `.alert-actions` in Discover, or align API payloads with what operators see. For triage controls (acknowledge, snooze, resolve, tags) and how they map to storage, refer to [Alert actions](view-manage-and-reference-alerts.md#alert-actions-v2). For rule evaluation fields on `.rule-events`, refer to [Rule event and field reference](../rules/rule-event-field-reference.md#rule-reference-v2).

## Episode status

The `episode.status` field appears on documents with `type: alert` in `.rule-events`. It represents the current lifecycle state of the alert episode.

| Value | Description |
|---|---|
| inactive | Episode not in an active breach state in the lifecycle model. |
| pending | Condition met but activation thresholds not yet satisfied. |
| active | Episode is actively breaching per rule logic. |
| recovering | Condition clearing but recovery thresholds not yet satisfied. |

## Rule event status

The `status` field appears on all documents in `.rule-events`, for both `type: signal` and `type: alert`. It reflects the outcome of a single rule evaluation row, independent of the episode lifecycle.

| Value | Description |
|---|---|
| breached | Condition met for this evaluation row. |
| recovered | Recovery path satisfied for this evaluation row. |
| no_data | No-data handling produced a no-data style outcome for this evaluation. |

## Alert action document fields

When a user or the system records an action on an alert episode, {{kib}} writes a document to `.alert-actions`. Use this stream for triage history, operational metrics such as mean time to acknowledge (MTTA), and auditing. It does not store what your rule query returned on each run — that output is in `.rule-events`.

| Field | Type | Description |
|---|---|---|
| @timestamp | date | When the action was recorded. |
| episode.id | keyword | Target episode. |
| rule.id | keyword | Rule that owns the episode. |
| action.type | keyword | The action type, for example: <br>- `acknowledge`: User acknowledged the alert.<br>- `snooze`: Notifications snoozed for a period.<br>- `tag`: Tag applied to the alert.<br>- `fire`: Notification or escalation fired for the episode.<br>- `unmatched`: No action policy matched the episode, so no workflow ran for it under these policies. <br><br> For the full set of action types and UI behavior, refer to [Alert actions](view-manage-and-reference-alerts.md#alert-actions-v2). |
| episode.status_count | long | Count of consecutive evaluations in the current `episode.status`. Only set when `episode.status` is `pending` or `recovering`.<br>For example, if the episode stays `pending` for three rule evaluations in a row, the value is `3`. |
