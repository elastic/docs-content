---
navigation_title: View and manage alerts
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Monitor alerts with KPI panels, a histogram, and filters. Triage and investigate alerts from the same page."
---

# View and manage alerts [view-manage-alerts]

In {{alerting-v2-system}}, use the **Alerts** page to monitor alerts with KPI panels, a histogram, and filters. To open it, go to **Alerting** → **Alerts** in the Observability navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

{applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` The page also lists alerts from {{alerting-v1-system}} rules, so you can monitor and triage alerts from both systems in one table. Refer to [View alerts from both alerting systems](#alerts-from-both-systems).

To silence, close, or tag alerts, refer to [Triage alerts](triage-alert-episodes.md). For alert lifecycle history, related alerts, and assignment, refer to [Investigate alerts](investigate-alert-episodes.md).

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
- **Alert tags** or **Tags** (depending on your {{stack}} version): Limit to alerts matching any selected tag. Tag choices come from the tags on alerts in the selected time range.
- **Assignee**: Limit to alerts assigned to one or more users.
- **Search**: Text search over alert event document fields.

:::{tip}
Narrow the time range when filters return too many results or tag options need refreshing.
:::

## View alerts from both alerting systems [alerts-from-both-systems]
```{applies_to}
serverless: ga
stack: experimental 9.6+
```

To tell alerts from the two systems apart, check the **Source** column: **Universal** for {{alerting-v2-system}} or **Classic** for {{alerting-v1-system}}. To act on {{alerting-v1-system}} alerts from the **Alerts** page, refer to [Triage alerts from {{alerting-v1-system}}](triage-alert-episodes.md#triage-classic-alerts).

### Which alerts from {{alerting-v1-system}} appear [classic-alerts-included]

You see a {{alerting-v1-system}} alert only if your role can view alerts from its rule type. For the privileges, refer to [Configure access](../manage/configure-access.md#alerting-classic-alert-privileges).

The table includes {{alerting-v1-system}} alerts from these rule types:

- **Observability rules**: APM, Synthetics, Uptime, Metric threshold, Inventory, Log threshold, SLO burn rate, and Custom threshold
- **Stack rules**: {{es}} query, Index threshold, Tracking containment, Transform health, and Anomaly detection

### How alerts from {{alerting-v1-system}} differ [classic-alert-differences]

{{alerting-v1-system-cap}} alerts appear in the KPI panels, histogram, and filters like any other alert, with these differences:

- They use only the **Active** and **Inactive** statuses. A recovered or [untracked](/explore-analyze/alerting/alerts/view-alerts.md#alert-status) alert shows as **Inactive**.
- They can have the **Warning**, **Minor**, and **Major** severity levels, and can show the [**Flapping**](/explore-analyze/alerting/alerts/create-manage-rules.md#defining-rules-flapping-details) icon in the **Status** column.
- You can't assign them, so the **Assignee** filter doesn't apply to them and the KPI panels count them as unassigned.
- A search matches each alert's own fields. For example, a query on `kibana.alert.rule.name` matches {{alerting-v1-system}} alerts but not {{alerting-v2-system}} alerts.