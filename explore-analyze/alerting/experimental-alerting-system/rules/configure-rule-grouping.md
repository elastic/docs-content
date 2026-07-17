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

In Alert mode, each group becomes its own alert episode with an independent lifecycle. One group can be active while another has recovered, and notifications apply per episode, not across all groups combined. Snooze state is also per series. Snoozing one group does not affect other groups tracked by the same rule.

## When to configure grouping [grouping-when-to-use]

Configure grouping when:

* Your {{esql}} query uses a `BY` clause to aggregate across multiple subjects such as hosts, services, or users, and you want each subject to have an independent alert lifecycle.
* You need to track that one host has recovered while another is still breaching, rather than treating all subjects as a single combined series.
* You want action policy notifications to apply per subject rather than firing once for the entire rule.

Skip grouping when:

* Your query does not use a `BY` clause. Grouping requires `BY` columns in the query output to be meaningful.
* You intentionally want a single alert series for the rule regardless of how many subjects match. An example is a rule that fires when any host in a cluster is down and the individual host identity doesn't matter for the notification.

Rule grouping controls how alert series are created. Notification grouping, configured on an action policy, controls how those alert episodes are batched into messages. These are separate settings.

## Configure grouping fields [grouping-fields-config]

The {{alerting-v2-system}} does not automatically infer grouping from your {{esql}} query. When your query uses `BY` to produce one row per group, the system still treats all rows as a single series unless you explicitly declare which fields define series identity in the grouping configuration. The fields you declare in `grouping.fields` are what the system uses to separate rows into independent alert series and track each one through its own lifecycle.

The fields you declare in `grouping.fields` must match the column names produced by the `BY` clause in your {{esql}} `STATS` command. If they don't match, the system can't correlate query rows to alert series and the grouping configuration has no effect.

:::{tip}
Write the query first, then set the group fields. That way the `BY` columns are already defined and you can select them directly. If you later add or remove a `BY` field in the query, update the group fields to match.
:::

## Examples

### Track error rates per service

Create a rule that counts HTTP errors per service and opens a separate alert series for each service that exceeds the threshold. Each service gets its own lifecycle. If the checkout service recovers but the payments service stays critical, those are tracked independently.

Without a matching `grouping.fields` entry, the rule treats all services as a single combined series. A spike in one service would activate the alert for everything, and recovery requires all services to drop below the threshold at the same time.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT_IF(http.response.status_code >= 500) BY service.name  // Group field: one series per service
| WHERE error_count > 10
| KEEP service.name, error_count
```

### Track CPU usage per host and region

Create a rule that tracks average CPU usage across hosts in multiple cloud regions. Because the query groups by both `host.name` and `cloud.region`, include both fields in `grouping.fields` to create one alert series per unique host-region combination.

```esql
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name, cloud.region  // Group fields: one series per host+region pair
| WHERE avg_cpu > 0.90
| KEEP host.name, cloud.region, avg_cpu
```
