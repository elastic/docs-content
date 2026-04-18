---
navigation_title: Investigate and respond
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Open the {{alerting-v2}} episode detail page, read lifecycle context, and use triage actions. How actions are stored in `.alert-actions` and episode versus group scope."
---

# Investigate and respond to {{alerting-v2}} alerts [investigate-respond-v2]

$$$investigate-respond-v2$$$

When an episode needs attention, open its **detail page** to see lifecycle context, related episodes, grouping, and the same **acknowledge**, **snooze**, **resolve**, and **Edit tags** actions you have on the alert episodes table.

## Where to start

The usual path is **{{manage-app}}** > **Alerts and Insights** > **Rules V2** > **Alert episodes**, then open an episode into the detail experience. The same detail page may also be reachable from **{{observability}}** if your deployment links there.

## Episode detail page [alert-episode-details-v2]

$$$alert-episode-details-v2$$$

An **episode** is one full lifecycle arc for an alert **series**, from the first breach until recovery or manual closure. It is identified by a unique **episode id** and tied to a **rule** and **group** (`group_hash`) when the rule uses grouping.

### Open the episode detail page

1. Open **{{manage-app}}** > **Alerts and Insights** > **Rules V2** > **Alert episodes**.
2. Select an episode to open its **detail** page (exact control depends on your build—for example the episode name, id, or **View** action).

If your space includes a **{{observability}}** link to the same episodes experience, you can start there instead; the detail URL and page are the same.

### What you see on the detail page

- **Lifecycle.** A visualization of state over time (for example pending, active, recovering, inactive) driven by events in **`.rule-events`**.
- **Actions and metadata.** Context for triage, including tags and action-driven status (acknowledge, snooze, resolve) consistent with the episodes table.
- **Related episodes.** Links or cards for other episodes on the same rule or series when the product loads related data.
- **Grouping.** When the rule groups by fields, the detail view can surface grouping values that identify the series for this episode.

### Take action

Use the action bar (or equivalent) to **acknowledge**, **snooze**, **resolve**, or **Edit tags** with the same rules as on the list:

- **Acknowledge** / **Unacknowledge** apply to the **episode**.
- **Snooze** / **Unsnooze** apply to the **group** shared by `group_hash`.
- **Resolve** / **Unresolve** apply to the **group** and force the episode to an **inactive** presentation in the UI when resolved.

For how those operations are stored and how they interact with notifications, see [Alert actions](#alert-actions-v2).

## Alert actions [alert-actions-v2]

$$$alert-actions-v2$$$

Alert actions are operations you perform on {{alerting-v2}} episodes to manage lifecycle, quiet notifications, and organize triage. Each operation is persisted so the UI and Discover stay in sync with what operators did.

### Where action records are stored

When you take an action, {{kib}} writes a document to the **`.alert-actions`** data stream. You can query these documents in Discover ({{esql}}) for auditing and metrics such as mean time to acknowledge (MTTA).

The exact field names in each document are listed in the [Rule event and action field reference](../alert-event-field-reference.md). The tables below focus on **action types** and **UI behavior**.

### Episode scope versus group scope

Many controls apply to either one **episode** or the whole **group** (same `group_hash` / series):

| UI area | Scope | Notes |
|---|---|---|
| **Acknowledge** / **Unacknowledge** | **Episode** | One episode row at a time. |
| **Snooze** / **Unsnooze** | **Group** | Affects every episode row that shares the same group hash. |
| **Resolve** / **Unresolve** | **Group** | The UI may label this **Resolve**; storage uses deactivate/activate-style action types. Resolved presentation can show **inactive** even when raw lifecycle state in **`.rule-events`** differs until data catches up. |
| **Edit tags** | **Episode** | Opens a flyout; new tags are written with **`tag`** actions. |

### Action types in storage

The `action_type` field (see the field reference for the exact path in documents) identifies the operation. Examples that appear when querying **`.alert-actions`**:

| `action_type` (examples) | Meaning |
|---|---|
| `ack` / `unack` | Episode acknowledged or unacknowledged. |
| `snooze` / `unsnooze` | Notifications snoozed or cleared for the **group** until a chosen time. |
| `deactivate` / `activate` | Episode or group taken out of active triage or brought back (UI may say **Resolve** / **Unresolve**). |
| `tag` | Tags applied on an episode; there is **no** separate `untag` type—updates are expressed with `tag` actions. |
| `suppress` | Suppression recorded for the episode or dispatch pipeline. |
| `fire` | Notification or workflow dispatch recorded for the episode. |
| `unmatched` | No action policy matched the episode, so no workflow ran for it under those policies. |

For a full field list and types, use the [Rule event and action field reference](../alert-event-field-reference.md).

### Available actions in the UI

From the **Alert episodes** table and the **episode detail** page (opened from **{{manage-app}}** > **Alerts and Insights** > **Rules V2** > **Alert episodes**), you can typically:

- **Acknowledge** and **Unacknowledge** the episode.
- **Snooze** and **Unsnooze** the **group** (select an end time in the snooze control).
- **Resolve** and **Unresolve** at **group** scope (same scope as snooze for grouping).
- **Edit tags.** Add tags and select from suggestions; persisted as **`tag`** actions.

Other product areas (for example **cases** or **assignment**) may appear in future releases or in builds with additional plugins; rely on the controls visible in your environment.

Some deployments also reach the same pages from **{{observability}}**; actions behave the same.

## See also

- [View and manage alert episodes](../manage-alerts.md)
- [Rule event and action field reference](../alert-event-field-reference.md)
