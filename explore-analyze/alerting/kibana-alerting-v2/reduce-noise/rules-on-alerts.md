---
navigation_title: Rules on alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Replace many individual Kibana alerting v2 alert notifications with a single meaningful one using rules that correlate across alerts."
---

# Kibana alerting v2 rules on alerts [reduce-noise-rules-on-alerts-v2]

Rules on alerts are a noise reduction strategy that replaces many individual low-level notifications with a single meaningful one. Instead of notifying on every alert, you create higher-order rules that detect patterns across alerts and notify only when the pattern is significant.

## The pattern

1. **Low-level rules** detect individual conditions (CPU high, memory high, disk full, error rate elevated) and run in detect mode or with notification policies that only log.
2. **A correlation rule** queries the alert events index and detects when multiple low-level alerts converge on the same entity (for example, the same service or host).
3. **Only the correlation rule** triggers high-priority notifications.

This replaces N individual alert notifications with 1 situation notification.

## Example

Five rules monitor different aspects of each service. Without rules on alerts, each rule generates its own notifications — potentially 5 notifications per service per issue.

With rules on alerts:

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 10 MINUTES AND status == "breached"
| STATS
    distinct_rules = COUNT_DISTINCT(rule.id),
    total_alerts = COUNT(*)
  BY data.service
| WHERE distinct_rules >= 2 AND total_alerts >= 3
```

This rule fires only when a service has 2+ distinct rules alerting with 3+ total alerts in a 10-minute window. Instead of receiving 5 individual notifications, you receive 1 escalation notification for the service.

## Setting up the pattern

1. **Keep low-level rules running** — they continue to produce alert events for investigation and history.
2. **Reduce low-level notifications** — either run them in detect mode (no notifications) or configure notification policies that log but do not page.
3. **Create the correlation rule** — write a rule whose `FROM` targets `.alerts-events-*` and whose `WHERE` and `STATS` logic detects the multi-alert pattern.
4. **Attach notification policies to the correlation rule** — route the escalation alert to PagerDuty, Slack, or other high-priority channels.

## Benefits

- **Reduced notification volume**: fewer notifications to process during incidents.
- **Better signal-to-noise ratio**: notifications represent situations, not individual symptoms.
- **Preserved investigation detail**: all low-level alerts remain available in the inbox and Discover for investigation.
- **Flexible patterns**: you can define any correlation logic using ES|QL — by service, by host, by time window, by alert type.

Refer to [Rules on alerts (authoring)](/explore-analyze/alerting/kibana-alerting-v2/author-rules/rules-on-alerts.md) for detailed configuration guidance.
