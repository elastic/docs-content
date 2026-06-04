---
navigation_title: Alert states and fields
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Status values and field definitions for alert episodes in Kibana's experimental alerting system. Covers episode lifecycle states, rule event status, and alert action document fields."
---

# Alert states and fields reference [alert-states-reference]


Alert states and fields are part of the {{alerting-v2-system}} in {{kib}}. Use these tables when you read alert UI state, query `.rule-events` or `.alert-actions` in Discover, or align API payloads with what operators see. For triage controls (acknowledge, snooze, resolve, tags) and how they map to storage, refer to [Alert actions](view-and-manage-alerts.md#alert-actions).
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
For rule evaluation fields on `.rule-events`, refer to [Rule event and field reference](../rules/rule-event-field-reference.md#rule-reference).
-->

## Alert episode status

The `episode.status` field appears on documents with `type: alert` in `.rule-events`. It represents the current lifecycle state of the alert episode.

| Value | Description |
|---|---|
| `inactive` | Alert episode not in an active breach state in the lifecycle model. |
| `pending` | Condition met but activation thresholds not yet satisfied. |
| `active` | Alert episode is actively breaching per rule logic. |
| `recovering` | Condition clearing but recovery thresholds not yet satisfied. |

<!--[CONTENT NEEDED for M2: M2 adds two first-class severity fields to the episode document:

- `episode.severity` - The severity from the most recent rule event (current state). Updated each evaluation.
- `episode.severity_max` - The highest severity seen over the episode's lifetime. Never decreases; enables "peaked at CRITICAL" display in the episode detail UI.

Add a new table or rows for these fields once M2 ships. The episode detail UI is also expected to change to surface these fields directly. Several M2 details are still open: the enforced value set (or lack thereof), whether de-escalation triggers policy re-evaluation, and whether manual override is supported. Do not document specifics until resolved.]
-->

## Rule event status

The `status` field appears on all documents in `.rule-events`, for both `type: signal` and `type: alert`. It reflects the outcome of a single rule evaluation row, independent of the alert episode lifecycle.

| Value | Description |
|---|---|
| `breached` | Condition met for this evaluation row. |
| `recovered` | Recovery path satisfied for this evaluation row. |
| `no_data` | No-data handling produced a no-data style outcome for this evaluation. |

## Alert action document fields

When a user or the system records an action on an alert episode, {{kib}} writes a document to `.alert-actions`. Use this stream for triage history, operational metrics such as mean time to acknowledge (MTTA), and auditing. It does not store what your rule query returned on each run — that output is in `.rule-events`.

| Field | Type | Description |
|---|---|---|
| `@timestamp` | date | When the action was recorded. |
| `episode.id` | keyword | Target alert episode. |
| `rule.id` | keyword | Rule that owns the alert episode. |
| `action.type` | keyword | The action type, for example: <br>- `acknowledge`: User acknowledged the alert episode.<br>- `snooze`: Notifications snoozed for a period.<br>- `tag`: Tag applied to the alert episode.<br>- `fire`: Notification or escalation fired for the alert episode.<br>- `unmatched`: No action policy matched the alert episode, so no workflow ran for it under these policies. <br><br> For the full set of action types and UI behavior, refer to [Alert actions](view-and-manage-alerts.md#alert-actions). |
| `episode.status_count` | long | Count of consecutive evaluations in the current `episode.status`. Only set when `episode.status` is `pending` or `recovering`.<br>For example, if the alert episode stays `pending` for three rule evaluations in a row, the value is `3`. |
