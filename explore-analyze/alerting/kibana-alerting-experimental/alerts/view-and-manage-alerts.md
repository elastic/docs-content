---
navigation_title: View and manage alerts
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Examine, triage, and investigate alert episodes in Kibana's experimental alerting system. Acknowledge, snooze, assign, or resolve episodes from the table, flyout, or episode detail page."
---

# View and manage alerts [manage-alerts]

Alert episodes are part of the {{alerting-v2-system}} in {{kib}}. When a rule detects a problem, use the Alerts UI to understand what's happening and decide what to do about it. 

This page covers how to read health and trend summaries above the episodes table, filter and search alert episodes, take triage actions (acknowledge, snooze, resolve, activate, and tag), and use the episode detail page to investigate lifecycle history, related episodes, assignees, and raw metadata.

<!--[CONTENT NEEDED for M2: UI. "V2 Alerting Preview" is a development-phase navigation label. Once the navigation and page name have been confirmed, add instructions for opening the Alerts page.]
-->

## Alert episodes scope in {{kib}} spaces [episode-space-isolation]

Alert episodes in the {{alerting-v2-system}} are scoped to the current {{kib}} space. Alert episodes created in one space aren't visible when viewing a different space, including the Default space. 

## Monitor alert health and trends [monitor-alert-trends]

Above the alert episodes table, two sets of panels give you an at-a-glance summary of your alert environment.

**KPI panels** surface aggregate counts for the current filter state and time range. Use these counts to understand the scale of a situation before drilling into individual rows — for example, whether a single noisy rule is responsible for most activity, or whether many rules are firing at the same time. Counts update dynamically as you change filters or adjust the time range.

<!-- [CONTENT NEEDED: The specific metrics shown in each KPI panel (total episodes, distinct firing rules, assigned to current user, unassigned, acknowledged, snoozed) are accurate as of 9.5.0 but the panel layout and labels may change before GA. Add a labeled breakdown of each panel once the UI stabilizes.] -->

**Episode histogram** shows how episode counts have changed across the selected time range. Use it to identify when a wave of alert episodes began, whether the situation is improving, and whether a spike was an isolated event or part of a broader pattern. You can break down the chart by dimensions such as status, rule, or assignee. Selecting a range directly in the histogram narrows the global time filter and focuses the table on that interval.

:::{note}
The episode histogram queries up to 10,000 alert episodes per time range. If your environment exceeds this limit, a warning appears in the chart. Narrow the time range or add filters to stay within this cap.
:::

## Filter and search

- **Rule:** Limit rows to one or more rules.
- **Status:** Limit by episode lifecycle state (active, recovered, pending, inactive).
- **Tags:** Limit to episodes whose last tag set matches any selected tag (OR logic). Tag choices come from tag actions in the selected time range.
- **Search:** Text search runs over alert event document fields. Combine with **Rule** or **Tags** filters when looking for a specific rule or label.

Narrow the time range when filters return too many rows or when tag options need refreshing.

## Alert episode actions

From any row in the table you can take the following row-level actions:

- **Acknowledge / Unacknowledge:** Applies to the individual episode.
- **Snooze / Unsnooze:** Applies to the series (`group_hash`), so all rows in that series are affected.
- **Resolve / Unresolve:** Applies to the series. The episode shows as inactive in the UI when resolved, even if the underlying lifecycle data has not yet caught up.
- **Activate:** Manually moves the episode to `active` state. Use when the episode is in `pending` and you want to confirm the problem and start the notification flow without waiting for the activation threshold to be met.
- **Edit tags:** Opens a flyout where you can add new tags to the episode or remove existing ones. Tag changes apply to the individual episode and are persisted as `tag` actions in `.alert-actions`. Tags added this way appear in the **Tags** filter on the alerts table and can be queried in Discover for reporting and triage workflows.

The same actions are available from the alert episode detail page. To assign an alert episode to a specific user, open the alert episode detail page.

### Bulk actions [bulk-actions]


Select one or more rows using the checkboxes in the table to apply an action to multiple episodes at once. The same actions available at the row level (acknowledge, unacknowledge, snooze, unsnooze, resolve, activate, and edit tags) can be applied in bulk.

Bulk actions follow the same scope rules as row-level actions: acknowledge and activate apply per episode, while snooze and resolve apply per group. When you snooze a selection of episodes that belong to different groups, each group is snoozed independently for the duration you set.

### Snooze an alert episode [snooze-episode]

Snoozing suppresses notifications for an alert series for a defined period. The rule continues to evaluate during the snooze window and the alert episode stays visible in the alerts table, but no notifications are sent until the snooze expires.

To snooze a single alert episode, select **Snooze** on any row. A quick-snooze popover opens with preset duration options so you can silence the alert episode in one click. Snooze applies at the group level. All episodes sharing the same `group_hash` are silenced for the duration, not just the row you acted on. The snooze expires automatically when the duration ends.

Use snooze when a known condition is expected to persist for a fixed time and you want to stop the noise without disabling the rule entirely. For example, during a scheduled maintenance window or a known noisy period for a specific host.

### Unsnooze an alert episode [unsnooze-episode]

To end a snooze early for a single alert episode, select **Unsnooze** on the row. Because snooze applies at the group level, unsnoozing one row clears the snooze for all alert episodes in the same group. Every alert episode sharing the same `group_hash` starts receiving notifications again immediately.

To unsnooze multiple alert episodes at once, select rows using the checkboxes and choose **Unsnooze** from the bulk actions menu. Bulk unsnooze follows the same group-level scope, where each selected alert episode's entire group is cleared.

## Open in Discover [open-episode-in-discover]

Select **Discover** on a row to open the rule's base query in Discover. The base query is the {{esql}} statement the rule runs on each evaluation. It reflects the data the alert is monitoring, not just the specific rows that breached the condition. Discover opens with the time range set to 15 minutes before and after the alert episode timestamp, so you can see the data the rule evaluated when the alert episode opened.

Use this when you want to understand why an alert episode opened, verify that the rule is querying the data you expect, or investigate whether a condition is genuinely a problem or an artifact of the data shape.

<!--[CONTENT NEEDED for M2: This feature may change in M2 to surface both the base query and the alert condition query, giving a more complete view of what triggered the episode. Verify whether the behavior changes in M2 and update this section accordingly.]-->

For ad hoc analysis over `.rule-events` and `.alert-actions` with copy-paste {{esql}} examples, refer to [Query alerts and signals in Discover](query-alerts-and-signals-in-discover.md).

## Alert episode detail page [alert-episode-details]

Select any row in the alert episodes table to open the alert episode details flyout. The flyout provides a quick-inspection view of the alert episode (including its metadata, actions, the associated rule, lifecycle heatmap, and related alert episodes) without leaving the list. To open the full alert episode detail page, select **View details** in the flyout header.

<!-- TODO: Issue #6838 lists a runbook section in the flyout. Confirm whether runbooks are a user-configurable feature in the {{alerting-v2-system}} and add a cross-reference once that documentation exists. -->

The full detail page shows:

- **Lifecycle:** A state-over-time visualization (pending, active, recovering, inactive) driven by events in `.rule-events`.
- **Actions and metadata:** Tags and action-driven status (acknowledge, snooze, resolve) consistent with the alert episodes table.
- **Assignee:** The user currently responsible for the alert episode. Only one user can be assigned at a time.
- **Related alert episodes:** Other alert episodes on the same rule or series, split into two subsections for easier triage.
- **Actors:** Users who have taken actions on the alert episode, visible so teams can track activity and accountability.
- **Metadata:** A dedicated tab surfacing additional fields from the source event that triggered the alert episode.
- **Grouping:** When the rule uses grouping, the grouping field values that identify the series — for example, `host.name: web-01` — are visible in the episodes table and throughout the alert episode detail page. These values show which entity the alert episode belongs to and reflect how the rule partitioned its alert data.

### Related alert episodes [related-episodes]


The **Related alert episodes** section is split into two subsections that help you distinguish between a condition that keeps recurring on one entity and a rule that is triggering across many different entities:

- **Same alert series:** Other alert episodes sharing the same `rule_id` and `group_hash` as the current alert episode. These represent recurrences of the exact same alert condition — the same rule firing on the same series (for example, the same host or service). If this list is long, the condition is repeating and the underlying issue may not be fully resolved each time.
- **Other series for this rule:** Alert episodes from the same rule but with a different `group_hash`, or all other rule alert episodes when the rule does not use grouping. These show broader rule activity — other entities or conditions the same rule is also triggering on. Use this list to understand the rule's overall blast radius and whether a problem is isolated to one entity or affecting many.

### Metadata tab [metadata-tab]


The **Metadata** tab surfaces additional information about the alert episode that is not shown in the main detail view. This includes field values from the source event that triggered the alert episode, giving you direct access to the raw signal during triage without switching to Discover.

Use the **Metadata** tab when you need to inspect specific field values that are embedded in the alert's source data but not surfaced in the lifecycle or grouping sections. For example, use the tab to identify a rule's resources or version.

### Actors [actors]


The **Actors** section lists the users who have taken actions on the alert episode (who acknowledged it, who snoozed it, and who resolved it) and when each action was taken. This gives teams visibility into the response history for an alert episode, which is useful for accountability and coordination.

### Assign an alert episode [assign-episode]


From the alert episode detail page, you can assign the alert episode to a specific user to indicate who is responsible for investigating or resolving it. Only one user can be assigned at a time — assigning replaces any existing assignee. To remove an assignment without replacing it, clear the assigned user.

Use assignment when your team needs clear ownership during triage. When multiple people are working through the alerts table at the same time, assigning an alert episode signals that someone has taken responsibility for it, which prevents duplicate work and makes it easier to track who is handling which issues.

## Action scope reference [alert-actions]


### Episode scope versus series scope

Some actions apply only to the specific alert episode you acted on. Others apply to every alert episode in the same series, meaning all alert episodes that share the same rule and `group_hash`. This matters when a rule tracks multiple services or hosts. Snoozing one alert episode silences the whole series, not only that service.

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
