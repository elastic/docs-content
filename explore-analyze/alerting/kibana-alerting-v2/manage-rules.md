---
navigation_title: Manage rules
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Navigate Kibana alerting v2 rule management: rules list and details, bulk actions, snooze, and disabling rules."
---

# Manage {{kib}} alerting v2 rules [manage-rules-v2]

Use this section after rules exist in your space: find rules in the **Rules V2** list, open a rule to inspect configuration and execution history, run bulk operations, and change whether rules run or notify. **Managing rules** is separate from **authoring** definitions. Refer to [Author rules](author-rules.md) to create or edit the {{esql}} query, schedule, and mode.

**Where to work in {{kib}}:** **Management** → **Alerts and Insights** → **Rules V2**.

## In this section

| Page | Use it to |
|---|---|
| [View and manage rules](manage-rules/view-manage-rules.md) | Use the rules list (columns, filters, search, bulk enable, disable, delete) and open **rule details** for a single rule. |
| [Snooze and disable rules](manage-rules/snooze-disable-rules.md) | Temporarily suppress notifications (including per-series snooze) or **disable** a rule so it stops executing. |

## Related

- [Author rules](author-rules.md): Create rules, set detect or alert mode, and edit query and schedule.
- [Manage alerts](manage-alerts.md): Triage and respond to alerts produced by rules.
