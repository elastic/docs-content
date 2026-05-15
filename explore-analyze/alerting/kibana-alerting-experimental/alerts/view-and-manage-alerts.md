---
navigation_title: View and manage alerts
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Open the experimental alerting features alert episodes table, triage actions, and episode details. Field and state tables live on a separate reference page."
---

# View and manage alerts [manage-alerts]


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

From any row in the table you can take the following row-level actions:

- **Acknowledge / Unacknowledge:** Applies to the individual episode.
- **Snooze / Unsnooze:** Applies to the series (`group_hash`), so all rows in that series are affected.
- **Resolve / Unresolve:** Applies to the series. The episode shows as inactive in the UI when resolved, even if the underlying lifecycle data has not yet caught up.
- **Activate:** Manually moves the episode to `active` state. Use when the episode is in `pending` and you want to confirm the problem and start the notification flow without waiting for the activation threshold to be met.
- **Edit tags:** Opens a flyout where you can add new tags to the episode or remove existing ones. Tag changes apply to the individual episode and are persisted as `tag` actions in `.alert-actions`. Tags added this way appear in the **Tags** filter on the alerts table and can be queried in Discover for reporting and triage workflows.

The same actions are available from the episode detail page. To assign an episode to a specific user, open the episode detail page.

### Bulk actions [bulk-actions]


Select one or more rows using the checkboxes in the table to apply an action to multiple episodes at once. The same actions available at the row level (acknowledge, unacknowledge, snooze, unsnooze, resolve, activate, and edit tags) can be applied in bulk.

Bulk actions follow the same scope rules as row-level actions: acknowledge and activate apply per episode, while snooze and resolve apply per group. When you snooze a selection of episodes that belong to different groups, each group is snoozed independently for the duration you set.

### Snooze an episode [snooze-episode]


Snoozing suppresses notifications for an alert series for a defined period. The rule continues to evaluate during the snooze window and the episode stays visible in the alerts table, but no notifications are sent until the snooze expires.

To snooze a single episode, select **Snooze** on any row. A quick-snooze popover opens with preset duration options so you can silence the episode in one click. Snooze applies at the group level. All episodes sharing the same `group_hash` are silenced for the duration, not just the row you acted on. The snooze expires automatically when the duration ends.

Use snooze when a known condition is expected to persist for a fixed time and you want to stop the noise without disabling the rule entirely. For example, during a scheduled maintenance window or a known noisy period for a specific host.

### Unsnooze an episode [unsnooze-episode]


To end a snooze early for a single episode, select **Unsnooze** on the row. Because snooze applies at the group level, unsnoozing one row clears the snooze for all episodes in the same group. Every episode sharing the same `group_hash` starts receiving notifications again immediately.

To unsnooze multiple episodes at once, select rows using the checkboxes and choose **Unsnooze** from the bulk actions menu. Bulk unsnooze follows the same group-level scope, where each selected episode's entire group is cleared.

## Open in Discover [open-episode-in-discover]


Select **Discover** on a row to open the rule's base query in Discover. The base query is the {{esql}} statement the rule runs on each evaluation. It reflects the data the alert is monitoring, not just the specific rows that breached the condition. Discover opens scoped to a time window around the episode so you can see the underlying data in context.
Snooze applies at the series level. All episodes sharing the same `group_hash` are silenced for the duration, not just the row you acted on. Use snooze when a known condition is expected to persist for a fixed time and you want to stop the noise without disabling the rule entirely. The snooze expires automatically when the duration ends.

Use this when you want to understand why an episode opened, verify that the rule is querying the data you expect, or investigate whether a condition is genuinely a problem or an artifact of the data shape.

<!--[CONTENT NEEDED for M2: This feature may change in M2 to surface both the base query and the alert condition query, giving a more complete view of what triggered the episode. Verify whether the behavior changes in M2 and update this section accordingly.]-->

For ad hoc analysis over `.rule-events` and `.alert-actions` with copy-paste {{esql}} examples, refer to [Query alerts and signals in Discover](query-alerts-and-signals-in-discover.md).

## Episode detail page [alert-episode-details]


Open an episode's detail page by selecting its name or ID from the table row. The detail page shows:

- **Lifecycle:** A state-over-time visualization (pending, active, recovering, inactive) driven by events in `.rule-events`.
- **Actions and metadata:** Tags and action-driven status (acknowledge, snooze, resolve) consistent with the episodes table.
- **Assignee:** The user currently responsible for the episode. Only one user can be assigned at a time.
- **Related episodes:** Other episodes on the same rule or series, split into two subsections for easier triage.
- **Actors:** Users who have taken actions on the episode, visible so teams can track activity and accountability.
- **Metadata:** A dedicated tab surfacing additional fields from the source event that triggered the alert.
- **Grouping:** When the rule uses grouping, the detail view surfaces the field values that identify the series.

### Related episodes [related-episodes]


The **Related episodes** section is split into two subsections that help you distinguish between a condition that keeps recurring on one entity and a rule that is triggering across many different entities:

- **Same alert series:** Other episodes sharing the same `rule_id` and `group_hash` as the current episode. These represent recurrences of the exact same alert condition — the same rule firing on the same series (for example, the same host or service). If this list is long, the condition is repeating and the underlying issue may not be fully resolved each time.
- **Other series for this rule:** Episodes from the same rule but with a different `group_hash`, or all other rule episodes when the rule does not use grouping. These show broader rule activity — other entities or conditions the same rule is also triggering on. Use this list to understand the rule's overall blast radius and whether a problem is isolated to one entity or affecting many.

### Metadata tab [metadata-tab]


The **Metadata** tab surfaces additional information about the alert episode that is not shown in the main detail view. This includes field values from the source event that triggered the alert, giving you direct access to the raw signal during triage without switching to Discover.

Use the **Metadata** tab when you need to inspect specific field values that are embedded in the alert's source data but not surfaced in the lifecycle or grouping sections. For example, use the tab to identify a rule's resources or version.

### Actors [actors]


The **Actors** section lists the users who have taken actions on the episode (who acknowledged it, who snoozed it, and who resolved it) and when each action was taken. This gives teams visibility into the response history for an episode, which is useful for accountability and coordination.

### Assign an episode [assign-episode]


From the episode detail page, you can assign the episode to a specific user to indicate who is responsible for investigating or resolving it. Only one user can be assigned at a time — assigning replaces any existing assignee. To remove an assignment without replacing it, clear the assigned user.

Use assignment when your team needs clear ownership during triage. When multiple people are working through the alerts table at the same time, assigning an episode signals that someone has taken responsibility for it, which prevents duplicate work and makes it easier to track who is handling which issues.

## Action scope reference [alert-actions]


### Episode scope versus series scope

Some actions apply only to the specific episode you acted on. Others apply to every episode in the same series, meaning all episodes that share the same rule and `group_hash`. This matters when a rule tracks multiple services or hosts. Snoozing one episode silences the whole series, not only that service.

| Action | Scope |
|---|---|
| Acknowledge / Unacknowledge | Episode |
| Activate | Episode |
| Snooze / Unsnooze | Group |
| Resolve / Unresolve | Group |
| Edit tags | Episode |
| Assign | Episode |

<!-- TODO: Uncomment after PR #6521 merges and toc.yml in this branch is updated to nest files under kibana-alerting-experimental.md. The anchor exists but can't be indexed until the toc parent chain is complete.
For field definitions and state descriptions, refer to [Alert states and fields reference](alert-states-and-fields-reference.md#alert-states-reference).
-->
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged and restore full sentence:
For field definitions and state descriptions, refer to [Alert states and fields reference](alert-states-and-fields-reference.md#alert-states-reference). For how {{kib}} records actions in `.alert-actions` and how notification gating works, refer to [Notification gating](../notifications/notification-gating.md#notification-gating).
-->
