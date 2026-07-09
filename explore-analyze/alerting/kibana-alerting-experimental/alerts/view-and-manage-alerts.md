---
navigation_title: View and manage alerts
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Monitor alert episodes in Kibana's experimental alerting system using KPI panels, an episode histogram, and filter controls. Triage and investigate episodes from the same interface."
---

# View and manage alerts [experimental-alerting-system-view-manage-alerts]

When a rule in the {{alerting-v2-system}} detects a problem, the Alerts page gives you health summaries and filtering tools to understand what's happening. For triage actions (acknowledge, snooze, resolve, activate, and tag), refer to [Triage alert episodes](triage-alert-episodes.md). For episode lifecycle history, related episodes, and assignment, refer to [Investigate alert episodes](investigate-alert-episodes.md).

## Space scoping [episode-space-isolation]

Alert episodes belong to the current {{kib}} space and aren't visible in other spaces.

## Monitor alert health and trends [monitor-alert-trends]

The Alerts page includes two summary panels:

- **KPI panels** - Show aggregate episode counts for the current filter state and time range. Use them to understand the scale of a situation before reviewing individual episodes.
- **Episode histogram** - Shows the total number of episodes that existed within each time interval. A long-lived episode counts in every interval it was open, not only the one it started in. Brush the chart to update the time filter. You can break down the chart by status, rule, or assignee.

:::{note}
The episode histogram queries up to 10,000 alert episodes for each time range. Narrow the time range or add filters if you exceed this limit.
:::

## Filter and search [filter-and-search]

- **Rule** - Limit to one or more rules.
- **Status** - Limit by lifecycle state (active, recovered, pending, inactive).
- **Tags** - Limit to episodes matching any selected tag. Tag choices come from tag actions in the selected time range.
- **Search** - Text search over alert event document fields.

:::{tip}
Narrow the time range when filters return too many results or tag options need refreshing.
:::