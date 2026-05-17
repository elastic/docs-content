---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: elasticsearch
  - id: cloud-hosted
description: Short guide to select Kibana alerting, the {{alerting-v2}}, or Watcher by use case, deployment, and how much control you need, with links to detailed docs.
---

# Choose an alerting system [choose-an-alerting-system]

Elastic has three alerting systems. You only need one. Pick the one that fits how you want to define rules and route notifications.

## Select by use case

| Goal | Suggested system | Availability |
|---|---|---|
| Monitor metrics, logs, or uptime with ready-made rules and no query language | [Kibana alerting](alerts.md) | All deployments |
| Use rules built for Security, Observability, APM, or Maps | [Kibana alerting](alerts.md) | All deployments |
| Write {{esql}} to define exactly what to detect and what data each alert carries | [{{alerting-v2}}](kibana-alerting-experimental.md) | {{serverless-full}} |
| Query alert history in Discover or build dashboards from alert data | [{{alerting-v2}}](kibana-alerting-experimental.md) | {{serverless-full}} |
| Manage notification routing, grouping, and throttling in one place, reusable across rules | [{{alerting-v2}}](kibana-alerting-experimental.md) | {{serverless-full}} |
| Build highly custom logic with scripting and chained inputs | [Watcher](watcher.md) | Self-managed and {{ech}} only |

## Compare at a glance

| | Kibana alerting | {{alerting-v2}} | Watcher |
|---|---|---|---|
| **Best for** | Teams using built-in rule types with form-based setup | Teams that need full control over detection and notification routing | Custom alerting logic requiring scripting |
| **Rule definition** | Select a rule type and fill in parameters | Write an {{esql}} query | Write a JSON watch definition |
| **Alert data** | Updated in place; limited query support | Append-only events queryable with {{esql}} in Discover | Watch history index |
| **Notifications** | Configured per action on each rule | Centralized action policies, reusable across rules | Action-level throttling and conditions |
| **Noise reduction** | Snooze per rule, maintenance windows | Per-series snooze, per-episode acknowledgment, activation thresholds, matcher-based routing, rules on alerts | Action conditions and throttling |
| **Availability** | All deployments | {{serverless-full}} | Self-managed and {{ech}} only |
