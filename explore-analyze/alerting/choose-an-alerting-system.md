---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: Compare Kibana alerting v1, Kibana alerting v2, and Watcher to decide which Elastic alerting system fits your monitoring needs.
---

# Choose an alerting system [choose-an-alerting-system]

If you already know which alerting system you are using, go directly to [Kibana alerting v1](kibana-alerting-v1.md), [Kibana alerting v2](kibana-alerting-v2.md), or [Watcher](watcher.md). This page is for readers who are not sure which system fits their needs.

## Choose by use case

| I want to... | Recommended system |
|---|---|
| Monitor metrics, logs, or uptime using prepackaged rules with minimal setup | [Kibana alerting v1](kibana-alerting-v1.md) |
| Use solution-specific rules for Security, Observability, APM, or Maps | [Kibana alerting v1](kibana-alerting-v1.md) |
| Write my own detection logic in ES\|QL and control exactly what data each alert carries | [Kibana alerting v2](kibana-alerting-v2.md) |
| Query alert history in Discover or build dashboards from alert data | [Kibana alerting v2](kibana-alerting-v2.md) |
| Manage notification routing, grouping, and throttling separately from rule definitions | [Kibana alerting v2](kibana-alerting-v2.md) |
| Correlate across multiple rules and reduce noise with rules on alerts | [Kibana alerting v2](kibana-alerting-v2.md) |
| Suppress notifications per host or service without silencing an entire rule | [Kibana alerting v2](kibana-alerting-v2.md) |
| Define complex alerting logic with Painless scripting or chained inputs | [Watcher](watcher.md) |

## Compare systems

| | Kibana alerting v1 | Kibana alerting v2 | Watcher |
|---|---|---|---|
| **Best for** | Teams using built-in rule types with form-based setup | Teams that need full control over detection and notification routing | Custom alerting logic requiring scripting |
| **Rule definition** | Select a rule type and fill in parameters | Write an ES\|QL query | Write a JSON watch definition |
| **Alert data** | Updated in place; limited queryability | Immutable, append-only events queryable with ES\|QL in Discover | Watch history index |
| **Notifications** | Configured per action on each rule | Centralized notification policies, reusable across rules | Action-level throttling and conditions |
| **Noise reduction** | Snooze per rule, maintenance windows | Per-series snooze, per-episode acknowledgment, activation thresholds, matcher-based routing, rules on alerts | Action conditions and throttling |
| **Availability** | All deployments | {{stack}} 9.4+ | Self-managed and {{ech}} only |

## Kibana alerting v1

Kibana alerting v1 provides prepackaged rule types integrated with Elastic solutions. Rules are configured through forms — no query language is required. Actions are triggered through built-in connectors such as email, Slack, PagerDuty, and webhooks.

Choose Kibana alerting v1 if you want broad rule type coverage out of the box and are working within Observability, Security, APM, Uptime, or Maps.

[Get started with Kibana alerting v1 →](kibana-alerting-v1.md)

## Kibana alerting v2

Kibana alerting v2 is built on ES|QL. You write the query that defines what to detect and what data each alert carries. Notification policies control routing, grouping, and throttling independently of rules, and alert events are stored as queryable data in standard {{es}} indices.

Choose Kibana alerting v2 if you need flexible detection logic, queryable alert history, centralized notification management, or cross-rule correlation.

[Get started with Kibana alerting v2 →](kibana-alerting-v2.md)

## Watcher

Watcher supports custom alerting logic with Painless scripting, chained inputs, and direct {{es}} API integration. It is the most flexible system for non-standard use cases but does not integrate with the {{kib}} alerting management UI.

Watcher is not available in {{serverless-full}}.

[Get started with Watcher →](watcher.md)

## Using multiple systems together

The alerting systems are independent and can run side by side:

- **Kibana alerting v1 and Kibana alerting v2** share a single **Rules** navigation entry with separate tabs. Each system writes to its own indices.
- **Watcher** operates through its own API and management UI.
- **Kibana alerting v2 rules on alerts** can query alert data produced by any system, enabling cross-system correlation.

There is no forced migration. You can adopt a new system incrementally while your existing rules continue running.
