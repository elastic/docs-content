---
navigation_title: View and manage rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Search, filter, and bulk-manage rules in Kibana's experimental alerting system. Use inline editing, the rule summary flyout, and the Execution History page to manage rules and monitor rule health."
---

# View and manage rules in the {{alerting-v2-system}} [manage-rules]

Rule management is part of the {{alerting-v2-system}} in {{kib}}. This page covers how to find and filter rules in the rules list, quick-edit settings without leaving the list, use the rule summary flyout, navigate the rule details page including the alert activity timeline, and monitor rule health at scale from the Execution History page.

## Find and filter rules [find-filter-rules]

Use the search bar to find rules by name or description. Each space-separated term is matched independently using prefix matching. Tags and grouping fields appear in results but aren't searchable.

Combine text search with filter controls to narrow by rule type, status, or tags. Select any column header to sort, or use bulk actions to enable, disable, or delete multiple rules at once.

## Edit a rule inline [quick-edit-rule]

To update common rule settings without opening the full rule details page, use the inline edit option on any row in the rules list. The inline editor also opens from the rule summary flyout header.

Use inline edit when you need to adjust metadata or scheduling settings quickly without navigating away from the list.

## Inspect a rule with the summary flyout [rule-summary-flyout]

To inspect a rule without navigating away from the rules list, select the expand icon on any row. The rule summary flyout opens alongside the list and shows a snapshot of the rule: its status, last run time, recent alert episode activity, and quick actions such as enable, disable, and snooze.

Use the flyout when you want to confirm a rule is healthy or take a quick action without committing to a full page load. To open the complete rule configuration with all settings and edit controls, select the rule name in the table row or in the flyout header.

## Review rule configuration and activity [rule-details-page]

The rule details page is organized into tabs that let you review a rule's configuration and activity history.

- **Overview** (Alert mode only): Shows an alert activity timeline for each series the rule tracks. The timeline displays a color-coded history of alert episode state transitions per series, along with summary statistics: alert episodes started, recovered, still open, and median duration. A link to view all matching alert episodes is available, filtered to the current rule and time range. Lane labels appear only for grouped rules. The overview tab is not shown for Signal-mode rules, which don't open alert episodes.
- **Conditions**: The full {{esql}} base query, alert condition, schedule, lookback, grouping, and recovery settings.
- **Runbook**: If the rule has an investigation guide, it appears here.

Use **Edit** to modify the rule, or the actions menu to enable, disable, clone, or delete it.

## Monitor rule execution health [execution-history]

The Execution History page shows a cross-rule view of rule execution history, giving you a paginated, filterable log of every rule run across all rules in the space. Use this page to spot patterns that aren't visible when looking at individual rules, for example, a cluster of failures at the same timestamp pointing to a shared dependency issue.

The page has two tabs: **Rules** (default), which shows per-rule execution records, and **Policies**, which shows action policy dispatch records and outcomes.

The **Rules** tab displays a table of rule execution records with the following columns:

| Column | Description |
|---|---|
| **Timestamp** | When the rule execution ran. |
| **Rule** | The rule that ran. Selecting the rule name opens the rule summary flyout so you can inspect the rule without leaving the page. |
| **Duration** | How long the execution took. |
| **Response** | The outcome of the run: `success` or `failure`. |
| **Message** | An optional message included with the execution result, typically an error description for failed runs. |

Use the **Outcome** filter to narrow results by execution outcome: **All**, **Success**, or **Failure**. Filtering is applied server-side. Results are capped at 10,000 records.

## Disable or snooze a rule [disable-snooze-rule]

Use **Disable** when you want the rule to stop running entirely until you re-enable it. This is different from snoozing, which suppresses notifications or quiets a series or policy without stopping rule evaluation.

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
- To snooze alert episodes or series, refer to [View, manage, and reference alerts](../alerts/view-and-manage-alerts.md#alert-actions).
-->
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- To snooze or stop an action policy, refer to [Manage action policies](../notifications/manage-action-policies.md).
-->
