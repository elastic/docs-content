---
navigation_title: Alert actions
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Actions you can take on Kibana alerting v2 alerts, including acknowledge, snooze, deactivate, assign, tag, resolve, and add to cases."
---

# Kibana alerting v2 alert actions [alert-actions-v2]

Alert actions are operations you perform on Kibana alerting v2 alerts to manage their lifecycle, suppress notifications, and organize your triage workflow.

## Where action records are stored

When you take an action on an alert, {{kib}} records it in the `.alert-actions` data stream. You can query these documents in Discover (ES|QL) for auditing, reporting, and metrics such as mean time to acknowledge (MTTA).

## Action types

The `action.type` field identifies what happened. Common values include:

| `action.type` | Description |
|---|---|
| `fire` | Notification or escalation fired for the episode |
| `acknowledge` | User acknowledged the alert |
| `snooze` | Notifications snoozed for a period |
| `deactivate` | Alert or episode deactivated |
| `suppress` | Suppression applied |
| `assign` | Assignment changed |
| `tag` | Tag applied to the alert (recorded action) |
| `resolve` | Episode or alert resolved |
| `unmatched` | No notification policy matched the episode, so no workflow ran for it under those policies |

The `untag` action type is not used. Tagging is recorded with the `tag` action type.

## Available actions in the UI

From the alert and episode views you can:

- Acknowledge, snooze, deactivate, assign, resolve, and add to cases as described in the triage workflow.
- Tag alerts for organization. Tagging is persisted as a `tag` action in `.alert-actions`, consistent with bulk-get and query behavior for recorded actions.

For field-level detail on action documents, refer to [Rule event and action field reference](../../alert-event-field-reference.md).
