---
navigation_title: View and manage alerts
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Open the {{alerting-v2}} alert episodes table, triage actions, and episode details. Field and state tables live on a separate reference page."
---

# View and manage alerts [manage-alerts-v2]

$$$manage-alerts-v2$$$

The **Alerts** page is the main place to view {{alerting-v2}} episodes, filter and sort them, and start triage. Open it from **{{manage-app}} > V2 Alerting Preview** > **Alerts**.

## Filter and search

- **Rule:** Limit rows to one or more rules.
- **Status:** Limit by episode lifecycle state (active, recovered, pending, inactive).
- **Tags:** Limit to episodes whose last tag set matches any selected tag (OR logic). Tag choices come from tag actions in the selected time range.
- **Search:** Text search runs over alert event document fields. Combine with **Rule** or **Tags** filters when looking for a specific rule or label.

Narrow the time range when filters return too many rows or when tag options need refreshing.

## Episode actions

From any row in the table you can:

- **Acknowledge / Unacknowledge:** Applies to the individual episode.
- **Snooze / Unsnooze:** Applies to the group (`group_hash`), so all rows sharing that group are affected.
- **Resolve / Unresolve:** Applies to the group. The episode shows as inactive in the UI when resolved, even if the underlying lifecycle data has not yet caught up.
- **Edit tags:** Opens a flyout to add tags; persisted as `tag` actions in `.alert-actions`.

The same actions are available from the episode detail page.

## Open in Discover

Select **Discover** on a row to investigate source data. Discover opens with the rule {{esql}} query and a short time window around the episode so you can inspect matching documents in context.

For ad hoc analysis over `.rule-events` and `.alert-actions` with copy-paste {{esql}} examples, refer to [Query alerts and signals in Discover](query-alerts-and-signals-in-discover-v2.md).

## Episode detail page [alert-episode-details-v2]

$$$alert-episode-details-v2$$$
$$$investigate-respond-v2$$$

Open an episode's detail page by selecting its name or ID from the table row. The detail page shows:

- **Lifecycle:** A state-over-time visualization (pending, active, recovering, inactive) driven by events in `.rule-events`.
- **Actions and metadata:** Tags and action-driven status (acknowledge, snooze, resolve) consistent with the episodes table.
- **Related episodes:** Other episodes on the same rule or series.
- **Grouping:** When the rule uses grouping, the detail view surfaces the field values that identify the series.

## Alert actions [alert-actions-v2]

$$$alert-actions-v2$$$

When you take an action, {{kib}} writes a document to the `.alert-actions` data stream. You can query these documents in Discover for auditing and metrics such as mean time to acknowledge (MTTA).

### Episode scope vs. group scope

| Action | Scope |
|---|---|
| Acknowledge / Unacknowledge | Episode |
| Snooze / Unsnooze | Group (`group_hash`) |
| Resolve / Unresolve | Group |
| Edit tags | Episode |

### Action types in storage

The `action_type` field identifies the operation in `.alert-actions` documents:

| action_type | Meaning |
|---|---|
| ack / unack | Episode acknowledged or unacknowledged. |
| snooze / unsnooze | Notifications snoozed or cleared for the group. |
| deactivate / activate | Group resolved or reopened (UI labels: Resolve / Unresolve). |
| tag | Tags applied to an episode. |
| suppress | Suppression recorded for the episode or dispatch pipeline. |
| fire | Notification or workflow dispatch recorded. |
| unmatched | No action policy matched, so no workflow ran. |

For a full field list and state definitions, refer to [Alert states and fields reference](alert-states-and-fields-reference-v2.md#alert-states-reference-v2).
