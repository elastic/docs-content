---
navigation_title: View and manage alerts
applies_to:
  stack: unavailable
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

### Episode scope versus group scope

| Action | Scope |
|---|---|
| Acknowledge / Unacknowledge | Episode |
| Snooze / Unsnooze | Group (`group_hash`) |
| Resolve / Unresolve | Group |
| Edit tags | Episode |

[CONTENT NEEDED for M2: `group_hash` is being replaced by `series.key` throughout the system. Update all instances of `group_hash` on this page (including the scope table above, the suppression table, and the suppression mechanics section) to use `series.key`. Also update the snooze descriptions to reference `series.key` and, where appropriate, note that `series.tracked_by` provides a human-readable view of what the series represents.]

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

## How suppression works [suppression-mechanics-v2]

$$$suppression-mechanics-v2$$$

Suppression controls whether a matched alert episode actually sends a notification. The dispatcher evaluates suppression before any action policy matcher runs, so a suppressed episode never reaches routing, grouping, or throttle checks.

There are three suppression patterns, each with a different scope:

| Pattern | Scope | How it works |
|---|---|---|
| **Acknowledge** | Per episode | If the last action in an `ack`/`unack` pair is `ack`, the episode is suppressed. Unacknowledging clears suppression for that episode. |
| **Deactivate** | Per episode | Same pair logic using `deactivate`/`activate` actions. Useful for manually pausing a specific alert while keeping the rule active. |
| **Snooze** | Per series (all episodes) | Suppresses all episodes sharing the same `group_hash` for a time-bounded window. The snooze expires automatically; you don't need to clear it manually. |

### Ack and deactivate versus snooze

The key distinction is **scope**:

- **Ack** and **deactivate** target a specific *episode* (one instance of an alert for one series). Other episodes in the same series are unaffected.
- **Snooze** targets the entire *series* (all current and future episodes that share the same `rule_id` and `group_hash` combination), until the snooze expires.

Use ack or deactivate when you are actively working on a specific breach and want to silence notifications for it. Use snooze when you want to quiet an entire alert series for a defined period, such as during a known noisy window for a host.

### Suppression query strategy

Mechanically, each suppression pattern is stored as a separate document type in `.alert-actions`. When the dispatcher evaluates whether to send a notification, it runs a targeted suppression query scoped to only the relevant `(rule_id, group_hash)` pairs from the current evaluation, rather than re-reading the entire `.rule-events` index. This two-query approach keeps dispatch evaluation efficient even at high episode volumes.

[CONTENT NEEDED for M2: M2 makes severity a first-class episode property and leaves open the question of whether a severity *decrease* (de-escalation) should trigger a notification. If de-escalation notifications are added, they will require a new suppression decision point: a snoozed or acknowledged episode that de-escalates may need different suppression behavior than one that escalates. Monitor the M2 severity design and update this section if new suppression rules are added around severity changes.]
