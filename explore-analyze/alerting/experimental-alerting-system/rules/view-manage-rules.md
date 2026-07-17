---
navigation_title: View and manage rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Search, filter, and bulk-manage rules in Kibana's experimental alerting system. Use inline editing, the rule summary flyout, and the rule details page to manage rules."
---

# View and manage rules in the {{alerting-v2-system}} [manage-rules]

After you create rules in the {{alerting-v2-system}}, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Rules** to keep track of them. Search and filter to find the ones you need, check status and recent activity at a glance, and make changes without losing your place in the list.

## Find and filter rules [find-filter-rules]

Use the search bar to find rules by name or description. Each space-separated term is matched independently using prefix matching. Tags and grouping fields appear in results but aren't searchable.

Combine text search with filter controls to narrow by rule type, status, or tags. Select any column header to sort, or use bulk actions to enable, disable, or delete multiple rules at once.

## Edit a rule inline [quick-edit-rule]

To update common rule settings without opening the full rule details page, use the inline edit option on any row on the **Rules** page. The inline editor also opens from the rule summary flyout header.

Use inline edit when you need to adjust metadata or scheduling settings quickly without navigating away from the list.

## Inspect a rule with the summary flyout [rule-summary-flyout]

To inspect a rule without navigating away from the **Rules** page, select the expand icon on any row. The rule summary flyout opens alongside the list and shows a snapshot of the rule: its status, last run time, recent alert episode activity, and quick actions such as enable, disable, and snooze.

Use the flyout when you want to confirm a rule is healthy or take a quick action without committing to a full page load. To open the complete rule configuration with all settings and edit controls, select the rule name in the table row or in the flyout header.

## Review rule configuration and activity [rule-details-page]

The rule details page is organized into tabs that let you review a rule's configuration and activity history.

- **Overview** (Alert mode only): Shows a color-coded alert activity timeline per series, with summary statistics (episodes started, recovered, still open, and median duration) and a link to view matching episodes.
- **Conditions**: The rule's base query, alert condition, schedule, lookback, grouping, and recovery settings.
- **Runbook**: The rule's investigation guide, if one has been added. Use it to document steps for diagnosing or responding to alerts produced by this rule.

Use **Edit** to modify the rule, or the actions menu to enable, disable, clone, or delete it.

## Disable or snooze a rule [disable-snooze-rule]

Use **Disable** when you want the rule to stop running entirely until you re-enable it. Snoozing is different: the rule keeps evaluating, but you suppress notifications or quiet a specific series or action policy.

## Related pages

- [Create a rule](create-a-rule.md): Compare rule creation paths and choose the one that fits your workflow.
- [Review rule execution history](review-rule-execution-history.md): Monitor rule execution outcomes across all rules in a space.