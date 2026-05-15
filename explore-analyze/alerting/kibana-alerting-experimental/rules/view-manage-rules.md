---
navigation_title: View and manage rules
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Use the rules list and rule details page in the experimental alerting features: filters, search, bulk actions, and what you find in rule conditions."
---

# View and manage rules in the experimental alerting features [manage-rules]



Viewing and managing rules is part of the experimental alerting features in Kibana. After a rule is created, edit its settings, pause it, remove it, and more from the page listing rules. The rules list gives you search, filter, sort, and bulk actions across all rules in the space. Selecting a rule name opens its details page, where you can review the full configuration and edit or act on it directly.

## Find and filter rules [find-filter-rules]


Use the search bar at the top of the rules list to find rules by name. The search field accepts plain text and matches against rule names without requiring structured query syntax — type any part of a rule name to narrow the list. Combine text search with filter controls to narrow results further by rule type, status, or tags.

Select any column header to sort the list. Use bulk actions when you need to enable, disable, or delete multiple rules at once.

## Rule summary flyout [rule-summary-flyout]


To inspect a rule without navigating away from the rules list, select the expand icon on any row. The rule summary flyout opens alongside the list and shows a snapshot of the rule: its status, last run time, recent alert episode activity, and quick actions such as enable, disable, and snooze.

Use the flyout when you want to confirm a rule is healthy or take a quick action without committing to a full page load. To open the complete rule configuration with all settings and edit controls, select the rule name in the table row or in the flyout header.

## Rule details page

- **Conditions**: The full {{esql}} base query, alert condition, schedule, lookback, grouping, and recovery settings.
- **Runbook**: If the rule has an investigation guide, it appears here alongside Conditions.

Use **Edit** to modify the rule, or the actions menu to enable, disable, clone, or delete it.

## Disable versus snooze

Use **Disable** when you want the rule to stop running entirely until you re-enable it. This is different from snoozing, which suppresses notifications or quiets a series or policy without stopping rule evaluation.

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
- To snooze alert episodes or series, refer to [View, manage, and reference alerts](../alerts/view-and-manage-alerts.md#alert-actions).
-->
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- To snooze or stop an action policy, refer to [Manage action policies](../notifications/manage-action-policies.md).
-->
