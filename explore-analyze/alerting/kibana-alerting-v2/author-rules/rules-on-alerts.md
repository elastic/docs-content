---
navigation_title: Rules on alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Write Kibana alerting v2 rules that query alert events for correlation, escalation, and noise reduction across multiple rules."
---

# Kibana alerting v2 rules on alerts [rules-on-alerts-v2]

Because Kibana alerting v2 alert events are stored as queryable data in standard {{es}} indices, you can write rules that use the alert events index as their data source. This enables correlation, escalation, and noise reduction patterns that are not possible when alerts are isolated in opaque system indices.

## How rules on alerts work

A rule on alerts is a standard Kibana alerting v2 rule whose `FROM` command points to `.alerts-events-*` instead of a source data index. The rule queries alert events produced by other rules and creates higher-order alerts when patterns are detected.

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 10 MINUTES AND status == "breached"
| STATS
    alert_types = COUNT_DISTINCT(rule.id),
    alert_count = COUNT(*)
  BY data.service
| WHERE alert_types >= 2 AND alert_count >= 3
| KEEP data.service, alert_types, alert_count
```

This rule detects when a service has 2 or more distinct rules firing with 3 or more total alerts in a 10-minute window — indicating a situation that warrants escalation.

## Use cases

### Escalation

Create a high-severity alert when multiple low-level alerts converge on the same entity:

- Multiple rules firing for the same host → escalate to an incident.
- Error rate alert + latency alert + disk pressure alert for the same service → create a "service degradation" situation alert.

### Correlation

Detect patterns across rules that individual rules cannot see:

- Alert from a deployment change rule followed by an error rate alert → correlate deployment impact.
% - External alert from Datadog + internal Elastic alert for the same service → cross-vendor correlation. (post-MVP)

### Noise reduction

Replace many individual low-level notifications with a single meaningful one:

- Instead of notifying on each CPU alert for every host, create a rule on alerts that fires when more than 5 hosts in the same cluster are alerting simultaneously.
- Only the cluster-level alert triggers notifications; the individual host alerts remain as signals for investigation.

## Example: multi-signal escalation

```yaml
kind: alert

metadata:
  name: service-degradation-escalation
  labels: ["escalation"]

schedule:
  every: 1m
  lookback: 10m

evaluation:
  query:
    base: |
      FROM .alerts-events-*
      | WHERE status == "breached"
      | STATS
          rule_count = COUNT_DISTINCT(rule.id),
          total_alerts = COUNT(*),
          rules = MV_SORT(VALUES(data.rule_name))
        BY data.service
    condition: "WHERE rule_count >= 2 AND total_alerts >= 3"

grouping:
  fields: [data.service]

state_transition:
  pending_count: 2

notification_policies:
  - ref: "policies/pagerduty-sev1"
```

## Considerations

- **Data access**: the rule's API key must have read access to `.alerts-events-*`.
- **Flattened fields**: alert event payloads are stored in the `data` field with flattened mapping. Query fields using `data.field_name` syntax.
- **Latency**: rules on alerts run after the source rules produce events. Account for the execution interval of both the source rules and the correlation rule when setting lookback windows.
- **Cascading**: you can chain multiple layers of rules on alerts (rule A feeds rule B feeds rule C), but be mindful of latency accumulation and circular dependencies.
