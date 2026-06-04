---
navigation_title: View and manage rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Use the rules list and rule details page in the experimental alerting system."
---

# View and manage rules in the {{alerting-v2-system}} [manage-rules]

Rule management is part of the {{alerting-v2-system}} in {{kib}}. After a rule is created, edit its settings, pause it, remove it, and more from the page listing rules. The rules list gives you search, filter, sort, and bulk actions across all rules in the space. Selecting a rule name opens its details page, where you can review the full configuration and edit or act on it directly.

## Find and filter rules [find-filter-rules]

Use the search bar at the top of the rules list to find rules by name or description. The search field accepts plain text. Each space-separated term is matched independently (terms are AND'd) using prefix matching. Type any part of a rule name or description to narrow the list.

Search matches rule name and description only. Tags and grouping fields are displayed in search results but aren't included in free-text search. Special characters in rule names and descriptions, including consecutive hyphens, are handled correctly.

Combine text search with filter controls to narrow results further by rule type, status, or tags. Select any column header to sort the list. Use bulk actions when you need to enable, disable, or delete multiple rules at once.

## Quick-edit a rule [quick-edit-rule]

To update common rule settings without opening the full rule details page, use the inline edit option on any row in the rules list. The inline editor also opens from the rule summary flyout header.

Editable fields in this view include name, description, tags, grouping key, time field, interval, lookback window, alert delay, recovery type, and recovery delay. The {{esql}} query and alert tracking behavior are read-only in this view. For changes to the query or rule mode, open the full rule details page.

Use inline edit when you need to adjust metadata or scheduling settings quickly without navigating away from the list.

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
