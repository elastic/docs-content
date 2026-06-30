---
navigation_title: Grouping
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure rule grouping in Kibana's experimental alerting system to track multiple subjects as independent alert series."
---

# Rule grouping in the {{alerting-v2-system}} [rule-grouping]

Rule grouping is an optional setting in the {{alerting-v2-system}} that lets a single rule track multiple things independently. For example, a rule monitoring CPU usage across hosts can produce a separate alert series for each host, rather than one alert for everything combined.

<!-- TODO: Confirm with engineering before adding a sentence here:
1. Is snooze state per series or per rule? If rule-level only, do not include it.
2. Does "lifecycle" mean the standard inactive → pending → active → recovering episode states? If so, rewrite as: "In Alert mode, each group becomes its own alert episode with an independent lifecycle. One group can be active while another has recovered, and notifications apply per episode, not across all groups combined."
-->

:::{note}
Rule grouping controls how alert series are created. Notification grouping (configured on an action policy) controls how those alert episodes are batched into messages. These are separate settings.
:::

## Aligning `BY` fields with your rule's query

The `BY` fields you specify for grouping must match the columns in the `BY` clause of your {{esql}} `STATS` command. If they don't match, the grouping configuration won't work as expected.

:::{tip}
Write the query first, then set the group fields. That way the `BY` columns are already defined and you can select them directly. If you later add or remove a `BY` field in the query, update the group fields to match.
:::

<!--[CONTENT NEEDED for M2: M2 replaces the current `grouping.fields` approach with a `track_by` concept and introduces a `series.*` block that gives each series a stable, explicit identity. Update this section to document the `track_by` configuration, explain how the `series.*` block differs from the current `group_hash` approach, and revise any references to `grouping.fields` or the `BY` clause alignment requirement once the M2 schema is finalized.]
-->

## Examples

### Track error rates per service

This rule counts HTTP errors per service and opens a separate alert series for each service that exceeds the threshold. Each service gets its own lifecycle: if the checkout service recovers but the payments service stays critical, those are tracked independently.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT_IF(http.response.status_code >= 500) BY service.name  // Group field: one series per service
| WHERE error_count > 10
| KEEP service.name, error_count
```

Without a matching `grouping.fields` entry, the rule treats all services as a single combined series. A spike in one service would activate the alert for everything, and recovery requires all services to drop below the threshold at the same time.

### Track CPU usage per host and region

When the query groups by multiple fields, include all of them in `grouping.fields` to create one alert series per unique combination.

```esql
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name, cloud.region  // Group fields: one series per host+region pair
| WHERE avg_cpu > 0.90
| KEEP host.name, cloud.region, avg_cpu
```
