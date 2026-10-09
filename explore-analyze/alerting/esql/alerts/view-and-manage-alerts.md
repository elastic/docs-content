---
navigation_title: View and manage alerts
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Monitor alerts using KPI panels, a histogram, and filter controls, including alerts from Kibana Classic Alerting rules. Triage and investigate alerts from the same interface."
---

# View and manage alerts [view-manage-alerts]

In {{alerting-v2-system}}, use the **Alerts** page to monitor alerts with KPI panels, a histogram, and filters. To open it, go to **Alerting** → **Alerts** in the Observability navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For triage actions (acknowledge, snooze, resolve, activate, and tag), refer to [Triage alerts](triage-alert-episodes.md). For alert lifecycle history, related alerts, and assignment, refer to [Investigate alerts](investigate-alert-episodes.md).

## View alerts from both alerting systems [alerts-from-both-systems]
```{applies_to}
serverless: ga
stack: experimental 9.6+
```

The **Alerts** page lists alerts from {{alerting-v1-system}} rules next to alerts from {{alerting-v2-system}} rules, so you can triage both in one table. The **Source** column shows where each alert comes from: **Classic** for {{alerting-v1-system}} or **Universal** for {{alerting-v2-system}}.

The table includes {{alerting-v1-system}} alerts from these rule types:

- **Observability rules**: APM, Synthetics, Uptime, Metric threshold, Inventory, Log threshold, SLO burn rate, and Custom threshold
- **Stack rules**: {{es}} query, Index threshold, Tracking containment, Transform health, and Anomaly detection

You see a {{alerting-v1-system}} alert only if your role can view alerts from its rule type. For the privileges, refer to [Give access to triage alerts without managing rules](/explore-analyze/alerting/alerts/alerting-setup.md#_give_access_to_triage_alerts_without_managing_rules).

Some parts of the page work differently for {{alerting-v1-system}} alerts:

- **Status**: An active alert shows as **Active**. A recovered or [untracked](/explore-analyze/alerting/alerts/view-alerts.md#alert-status) alert shows as **Inactive**. These alerts are never **Pending** or **Recovering**, so filtering by either status leaves them out.
- **Flapping**: A **Flapping** icon appears in the **Status** column while an alert is [flapping](/explore-analyze/alerting/alerts/create-manage-rules.md#defining-rules-flapping-details).
- **Assignee**: You can't assign these alerts. Filtering by **Assignee** leaves them out, and the KPI panels always count them as unassigned.
- **Search**: A query matches each alert's own fields. For example, a query on `kibana.alert.rule.name` matches {{alerting-v1-system}} alerts but not {{alerting-v2-system}} alerts.

The KPI panels and the histogram count alerts from both systems. To act on {{alerting-v1-system}} alerts from this page, refer to [Triage {{alerting-v1-system}} alerts](triage-alert-episodes.md#triage-classic-alerts).

## Space scoping [episode-space-isolation]

Alerts belong to the current {{kib}} space and aren't visible in other spaces.

## Monitor alert health and trends [monitor-alert-trends]

The Alerts page includes two summary panels:

- **KPI panels**: Show aggregate alert counts for the current filter state and time range. Use them to understand the scale of a situation before reviewing individual alerts.
- **Histogram**: Shows the total number of alerts that existed within each time interval. A long-lived alert counts in every interval it was open, not only the one it started in. Brush the chart to update the time filter. You can break down the chart by status, rule, acknowledgment, or assignee.

:::{note}
The histogram queries up to 10,000 alerts for each time range. Narrow the time range or add filters if you exceed this limit.
:::

## Filter and search [filter-and-search]

Use the following controls on the **Alerts** page to narrow the alert list:

- **Rule**: Limit to one or more rules.
- **Status**: Limit by lifecycle state (inactive, pending, active, recovering).
- **Severity**: Limit to one or more severity levels.
- **Alert tags** (**Tags** in earlier versions): Limit to alerts matching any selected tag. Tag choices come from the tags on alerts in the selected time range.
- **Assignee**: Limit to alerts assigned to one or more users.
- **Search**: Text search over alert event document fields.

:::{tip}
Narrow the time range when filters return too many results or tag options need refreshing.
:::