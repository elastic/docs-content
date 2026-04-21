---
navigation_title: View and manage rules
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Use the {{alerting-v2}} rules list and rule details page: filters, search, bulk actions, and what you find in rule conditions."
---

# View and manage {{alerting-v2}} rules [manage-rules-v2]

$$$manage-rules-v2$$$

$$$open-the-list$$$

Open the rules list from **{{manage-app}} > V2 Alerting Preview > Rules**. From here you can search, filter, sort, and act on rules individually or in bulk.

## Rule details page

Select a rule name to open its details page. The details page shows:

- **Conditions**: The full {{esql}} base query, alert condition, schedule, lookback, grouping, and recovery settings.
- **Runbook**: If the rule has an investigation guide, it appears here alongside Conditions.

Use **Edit** to modify the rule, or the actions menu to enable, disable, clone, or delete it.

## Disable versus snooze

Use **Disable** when you want the rule to stop running entirely until you re-enable it. This is different from snoozing, which suppresses notifications or quiets a series or policy without stopping rule evaluation.

- To snooze alert episodes or series, refer to [View, manage, and reference alerts](../alerts/view-manage-and-reference-alerts-v2.md#alert-actions-v2).
- To snooze or stop an action policy, refer to [Manage action policies](../notifications/manage-action-policies-v2.md).

If you are unsure which to use, refer to [Validation checklist and noise controls](../troubleshooting-alerting-v2.md#reduce-noise-v2).
