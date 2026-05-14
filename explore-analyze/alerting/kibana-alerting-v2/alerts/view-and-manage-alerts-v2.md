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

<!--[CONTENT NEEDED for M2: UI. "V2 Alerting Preview" is a development-phase navigation label. Once the navigation and page name have been confirmed, add instructions for opening the Alerts page.]
-->

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
- **Edit tags:** Opens a flyout where you can add new tags to the episode or remove existing ones. Tag changes apply to the individual episode and are persisted as `tag` actions in `.alert-actions`. Tags added this way appear in the **Tags** filter on the alerts table and can be queried in Discover for reporting and triage workflows.

The same actions are available from the episode detail page.

### Snooze an episode [snooze-episode-v2]

$$$snooze-episode-v2$$$

Snoozing suppresses notifications for an alert series for a defined period. When you select **Snooze** on a row, a popover opens where you set a duration. During the snooze window, the rule continues to evaluate, and the episode stays visible in the alerts table, but notifications are not sent.

Snooze applies at the group level. All episodes sharing the same `group_hash` are silenced for the duration, not just the row you acted on. Use snooze when a known condition is expected to persist for a fixed time and you want to stop the noise without disabling the rule entirely. The snooze expires automatically when the duration ends.

## Open in Discover

Select **Discover** on a row to investigate source data. Discover opens with the rule {{esql}} query and a short time window around the episode so you can inspect matching documents in context.

For ad hoc analysis over `.rule-events` and `.alert-actions` with copy-paste {{esql}} examples, refer to [Query alerts and signals in Discover](query-alerts-and-signals-in-discover-v2.md).

## Episode detail page [alert-episode-details-v2]

$$$alert-episode-details-v2$$$
$$$investigate-respond-v2$$$

Open an episode's detail page by selecting its name or ID from the table row. The detail page shows:

- **Lifecycle:** A state-over-time visualization (pending, active, recovering, inactive) driven by events in `.rule-events`.
- **Actions and metadata:** Tags and action-driven status (acknowledge, snooze, resolve) consistent with the episodes table.
- **Related episodes:** Other episodes on the same rule or series, split into two subsections for easier triage.
- **Actors:** Users who have taken actions on the episode, visible so teams can track activity and accountability.
- **Metadata:** A dedicated tab surfacing additional fields from the source event that triggered the alert.
- **Grouping:** When the rule uses grouping, the detail view surfaces the field values that identify the series.

### Related episodes [related-episodes-v2]

$$$related-episodes-v2$$$

The **Related episodes** section is split into two subsections that help you distinguish between a condition that keeps recurring on one entity and a rule that is triggering across many different entities:

- **Same alert group:** Other episodes sharing the same `rule_id` and `group_hash` as the current episode. These represent recurrences of the exact same alert condition — the same rule firing on the same grouped entity (for example, the same host or service). If this list is long, the condition is repeating and the underlying issue may not be fully resolved each time.
- **Other groups for this rule:** Episodes from the same rule but with a different `group_hash`, or all other rule episodes if there is no group. These show broader rule activity — other entities or conditions the same rule is also triggering on. Use this list to understand the rule's overall blast radius and whether a problem is isolated to one entity or affecting many.

### Metadata tab [metadata-tab-v2]

$$$metadata-tab-v2$$$

The **Metadata** tab surfaces additional information about the alert episode that is not shown in the main detail view. This includes field values from the source event that triggered the alert, giving you direct access to the raw signal during triage without switching to Discover.

Use the **Metadata** tab when you need to inspect specific field values that are embedded in the alert's source data but not surfaced in the lifecycle or grouping sections. For example, use the tab to identify a rule's resources or version.

### Actors [actors-v2]

$$$actors-v2$$$

The **Actors** section lists the users who have taken actions on the episode (who acknowledged it, who snoozed it, and who resolved it) and when each action was taken. This gives teams visibility into the response history for an episode, which is useful for accountability and coordination.

## Alert actions [alert-actions-v2]

$$$alert-actions-v2$$$

When you take an action, {{kib}} writes a document to the `.alert-actions` data stream. You can query these documents in Discover for auditing and metrics such as mean time to acknowledge (MTTA). For a full field list and state definitions, refer to [Alert states and fields reference](alert-states-and-fields-reference-v2.md#alert-states-reference-v2).

### Episode scope versus group scope

Some actions apply only to the specific episode you acted on. Others apply to every episode in the same group, meaning all episodes that share the same rule and series. This matters when a rule tracks multiple services or hosts. Snoozing one episode silences the whole group, not only that service.

| Action | Scope |
|---|---|
| Acknowledge / Unacknowledge | Episode |
| Snooze / Unsnooze | Group |
| Resolve / Unresolve | Group |
| Edit tags | Episode |

## How suppression works [suppression-mechanics-v2]

$$$suppression-mechanics-v2$$$

Suppression controls whether a matched alert episode actually sends a notification. The dispatcher evaluates suppression before any action policy matcher runs, so a suppressed episode never reaches routing, grouping, or throttle checks.


There are three suppression options, each with a different scope:

| Option | Scope | When to use |
|---|---|---|
| Acknowledge | Per episode | You're actively working on a specific breach and want to silence notifications for it. To clear suppression, remove the acknowledgement. |
| Deactivate | Per episode | Marks the episode as inactive and stops notifications for it. Unlike acknowledge, this closes the episode rather than silencing it while leaving it active. Use when you want to manually close a specific episode, for example, when you've addressed the issue but the rule hasn't recovered automatically. |
| Snooze | Per series (all episodes) | You want to quiet an entire alert series for a defined period. For example, during a known noisy window for a host. Expires automatically. |

<!--[CONTENT NEEDED for M2: M2 makes severity a first-class episode property and leaves open the question of whether a severity *decrease* (de-escalation) should trigger a notification. If de-escalation notifications are added, they will require a new suppression decision point: a snoozed or acknowledged episode that de-escalates may need different suppression behavior than one that escalates. Monitor the M2 severity design and update this section if new suppression rules are added around severity changes.]
-->
