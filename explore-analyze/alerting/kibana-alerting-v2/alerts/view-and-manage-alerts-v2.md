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

When a rule detects a problem, use the Alerts UI to understand what's happening and decide what to do about it. From here you can examine alert episodes, use filters to find what needs attention, triage alerts, and more. This is the operational surface for working through alerts day to day.

[CONTENT NEEDED for M2: UI. "V2 Alerting Preview" is a development-phase navigation label. Once the navigation and page name have been confirmed, add instructions for opening the Alerts page.]

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

When you take an action, {{kib}} writes a document to the `.alert-actions` data stream. You can query these documents in Discover for auditing and metrics such as mean time to acknowledge (MTTA). For a full field list and state definitions, refer to [Alert states and fields reference](alert-states-and-fields-reference-v2.md#alert-states-reference-v2).

### Episode scope versus group scope

Some actions apply only to the specific episode you acted on. Others apply to every episode in the same group — meaning all episodes that share the same rule and series. This matters when a rule tracks multiple services or hosts: snoozing one episode silences the whole group, not just that service.

| Action | Scope |
|---|---|
| Acknowledge / Unacknowledge | Episode |
| Snooze / Unsnooze | Group |
| Resolve / Unresolve | Group |
| Edit tags | Episode |

## How suppression works [suppression-mechanics-v2]

$$$suppression-mechanics-v2$$$

Suppression controls whether a matched alert episode actually sends a notification. The dispatcher evaluates suppression before any action policy matcher runs, so a suppressed episode never reaches routing, grouping, or throttle checks. Mechanically, each suppression option is stored as a separate document type in `.alert-actions`, and the dispatcher runs a targeted query scoped to only the relevant `(rule_id, group_hash)` pairs from the current evaluation — rather than re-reading the entire `.rule-events` index — to keep dispatch evaluation efficient at high episode volumes.

There are three suppression options, each with a different scope:

| Option | Scope | When to use |
|---|---|---|
| Acknowledge | Per episode | You're actively working on a specific breach and want to silence notifications for it. Unacknowledging clears suppression. |
| Deactivate | Per episode | Marks the episode as inactive and stops notifications for it. Unlike acknowledge, this closes the episode rather than silencing it while leaving it active. Use when you want to manually close a specific episode, For example, when you've addressed the issue but the rule hasn't recovered automatically. |
| Snooze | Per series (all episodes) | You want to quiet an entire alert series for a defined period. For example, during a known noisy window for a host. Expires automatically.

[CONTENT NEEDED for M2: M2 makes severity a first-class episode property and leaves open the question of whether a severity *decrease* (de-escalation) should trigger a notification. If de-escalation notifications are added, they will require a new suppression decision point: a snoozed or acknowledged episode that de-escalates may need different suppression behavior than one that escalates. Monitor the M2 severity design and update this section if new suppression rules are added around severity changes.]
