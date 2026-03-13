---
navigation_title: Set rule data sources
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Configure Kibana alerting v2 rule data sources using ES|QL FROM commands, including index patterns, cross-cluster search, and alert indices."
---

# Set Kibana alerting v2 rule data sources [set-rule-data-sources-v2]

Every Kibana alerting v2 rule evaluates data from one or more {{es}} indices. The data source is defined by the `FROM` command in the rule's ES|QL query.

## Specify data sources in ES|QL

The `FROM` command in your ES|QL query determines which indices the rule reads from:

```esql
FROM logs-*
| STATS error_count = COUNT(*) WHERE http.response.status_code >= 500 BY service.name
| WHERE error_count > 100
```

You can use:

- **Index patterns** — `FROM logs-*`, `FROM metrics-*`
- **Data streams** — `FROM logs-nginx-default`
- **Specific indices** — `FROM my-custom-index`
- **Multiple sources** — `FROM logs-*, metrics-*`
- **Cross-cluster search** — `FROM remote_cluster:logs-*`

## Cross-cluster search

Kibana alerting v2 rules support cross-cluster search. Use the `cluster_name:index_pattern` syntax in the `FROM` command:

```esql
FROM remote_cluster:metrics-*
| STATS last_seen = MAX(@timestamp) BY host.name
| WHERE last_seen < NOW() - 15 MINUTES
```

Cross-cluster search requires the remote cluster to be configured and the rule's API key to have the appropriate privileges on both the local and remote clusters.

## Alert events as a data source

You can use the alert events index (`.alerts-events-*`) as a data source for rules on alerts. This enables correlation and escalation patterns:

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 10 MINUTES AND status == "breached"
| STATS
    alert_types = COUNT_DISTINCT(rule.id),
    alert_count = COUNT(*)
  BY data.service
| WHERE alert_types >= 2 AND alert_count >= 3
```

Refer to [Rules on alerts](rules-on-alerts.md) for detailed guidance.

## Time field

By default, rules filter data using `@timestamp` for the lookback window. If your data uses a different time field, set `time_field` in the rule definition:

```yaml
time_field: "event.created"
```

The time field must be a `date` type in the index mapping.

## Permissions

The rule executes with the API key of the user who created or last updated it. That user must have read access to the indices referenced in the `FROM` command. If the user's privileges change, the rule's data access changes accordingly.
