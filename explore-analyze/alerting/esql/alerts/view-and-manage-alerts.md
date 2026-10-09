---
navigation_title: View and manage alerts
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Monitor alerts using KPI panels, a histogram, and filter controls. Triage and investigate alerts from the same interface."
---

# View and manage alerts [view-manage-alerts]

In {{alerting-v2-system}}, use the **Alerts** page to monitor alerts with KPI panels, a histogram, and filters. To open it, go to **Alerting** → **Alerts** in the Observability navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For triage actions (acknowledge, snooze, resolve, activate, and tag), refer to [Triage alerts](triage-alert-episodes.md). For alert lifecycle history, related alerts, and assignment, refer to [Investigate alerts](investigate-alert-episodes.md).

## Space scoping [episode-space-isolation]

Alerts belong to the current {{kib}} space and aren't visible in other spaces.

## Monitor alert health and trends [monitor-alert-trends]

The Alerts page includes two summary panels:

- **KPI panels** - Show aggregate alert counts for the current filter state and time range. Use them to understand the scale of a situation before reviewing individual alerts.
- **Histogram** - Shows the total number of alerts that existed within each time interval. A long-lived alert counts in every interval it was open, not only the one it started in. Brush the chart to update the time filter. You can break down the chart by status, rule, or assignee.

:::{note}
The histogram queries up to 10,000 alerts for each time range. Narrow the time range or add filters if you exceed this limit.
:::

## Filter and search [filter-and-search]

Use the following controls on the **Alerts** page to narrow the alert list:

- **Rule** - Limit to one or more rules.
- **Status** - Limit by lifecycle state (inactive, pending, active, recovering).
- **Tags** - Limit to alerts matching any selected tag. Tag choices come from tag actions in the selected time range.
- **Search** - Text search over alert event document fields.

:::{tip}
Narrow the time range when filters return too many results or tag options need refreshing.
:::