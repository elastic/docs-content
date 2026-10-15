---
navigation_title: View and manage alerts
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Monitor alert episodes in the experimental alerting system using KPI panels, a histogram, and filter controls. Triage and investigate alert episodes from the same interface."
---

# View and manage alerts in the {{alerting-v2-system}} [view-manage-alerts]

Use the **Alerts** page to monitor alert episodes with KPI panels, a histogram, and filters. Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts**.

For triage actions (acknowledge, snooze, resolve, activate, and tag), refer to [Triage alert episodes](triage-alert-episodes.md). For alert episode lifecycle history, related alert episodes, and assignment, refer to [Investigate alert episodes](investigate-alert-episodes.md).

## Space scoping [episode-space-isolation]

Alert episodes belong to the current {{kib}} space and aren't visible in other spaces.

## Monitor alert health and trends [monitor-alert-trends]

The Alerts page includes two summary panels:

- **KPI panels** - Show aggregate alert episode counts for the current filter state and time range. Use them to understand the scale of a situation before reviewing individual alert episodes.
- **Episode histogram** - Shows the total number of alert episodes that existed within each time interval. A long-lived alert episode counts in every interval it was open, not only the one it started in. Brush the chart to update the time filter. You can break down the chart by status, rule, or assignee.

:::{note}
The **Episode histogram** queries up to 10,000 alert episodes for each time range. Narrow the time range or add filters if you exceed this limit.
:::

## Filter and search [filter-and-search]

Use the following controls on the **Alerts** page to narrow the alert episode list:

- **Rule** - Limit to one or more rules.
- **Status** - Limit by lifecycle state (inactive, pending, active, recovering).
- **Tags** - Limit to alert episodes matching any selected tag. Tag choices come from tag actions in the selected time range.
- **Search** - Text search over alert event document fields.

:::{tip}
Narrow the time range when filters return too many results or tag options need refreshing.
:::