---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: elasticsearch
  - id: cloud-hosted
description: Short guide to select Kibana alerting v1, v2, or Watcher by use case, deployment, and how much control you need, with links to detailed docs.
---

# Choose an alerting system [choose-an-alerting-system]

Check out [Alerting overview](../alerting-overview.md) for an introduction to each system, where they run, and **Get started** links. Return here to select a system by goal if you are still deciding. If you already know which system you need, open [Kibana alerting v1](kibana-alerting-v1.md), [{{alerting-v2}}](kibana-alerting-v2.md), or [Watcher](watcher.md).

:::{note}
You do not need to stand up {{kib}} alerting v1, v2, and {{watcher}} together. Pick the single option that fits your deployment and the goals in the tables below.
:::

## Select by use case

| Goal | Suggested system | Where it runs |
|---|---|---|
| Monitor metrics, logs, or uptime with ready-made rules and minimal setup | [Kibana alerting v1](kibana-alerting-v1.md) | {{stack}} and {{serverless-full}} |
| Use rules tailored to Security, Observability, APM, or Maps | [Kibana alerting v1](kibana-alerting-v1.md) | {{stack}} and {{serverless-full}} |
| Define what to watch using ES\|QL and specify exactly what data goes with each alert | [{{alerting-v2}}](kibana-alerting-v2.md) | {{stack}} 9.4+ and {{serverless-full}} |
| Search alert history over time, explore it in Discover, or build dashboards from it | [{{alerting-v2}}](kibana-alerting-v2.md) | {{stack}} 9.4+ and {{serverless-full}} |
| Set who gets notified and how often in one place, then reuse that across many rules | [{{alerting-v2}}](kibana-alerting-v2.md) | {{stack}} 9.4+ and {{serverless-full}} |
| Tie several rules together or limit notifications for one host or service without silencing the entire rule | [{{alerting-v2}}](kibana-alerting-v2.md) | {{stack}} 9.4+ and {{serverless-full}} |
| Build highly custom logic with scripting and chained inputs | [Watcher](watcher.md) | {{stack}} only |

## Compare at a glance

| | Kibana alerting v1 | {{alerting-v2}} | Watcher |
|---|---|---|---|
| **Best for** | Teams using built-in rule types with form-based setup | Teams that need full control over detection and notification routing | Custom alerting logic requiring scripting |
| **Rule definition** | Select a rule type and fill in parameters | Write an ES\|QL query | Write a JSON watch definition |
| **Alert data** | Updated in place; limited queryability | Immutable, append-only events queryable with ES\|QL in Discover | Watch history index |
| **Notifications** | Configured per action on each rule | Centralized action policies, reusable across rules | Action-level throttling and conditions |
| **Noise reduction** | Snooze per rule, maintenance windows | Per-series snooze, per-episode acknowledgment, activation thresholds, matcher-based routing, rules on alerts | Action conditions and throttling |
| **Availability** | All deployments | {{stack}} 9.4+ | Self-managed and {{ech}} only |

## Kibana alerting v1

Kibana alerting v1 provides prepackaged rule types integrated with Elastic solutions. Rules are configured through forms — no query language is required. Actions are triggered through built-in connectors such as email, Slack, PagerDuty, and webhooks.

Choose Kibana alerting v1 if you want broad rule type coverage out of the box and are working within Observability, Security, APM, Uptime, or Maps.

[Get started with Kibana alerting v1 →](kibana-alerting-v1.md)

## {{alerting-v2}}

{{alerting-v2}} is built on ES|QL. You write the query that defines what to detect and what data each alert carries. Action policies control routing, grouping, and throttling independently of rules, and alert events are stored as queryable data in standard {{es}} indices.

Choose {{alerting-v2}} if you need flexible detection logic, queryable alert history, centralized notification management, or cross-rule correlation.

[Get started with {{alerting-v2}} →](kibana-alerting-v2.md)

## Watcher

Watcher supports custom alerting logic with Painless scripting, chained inputs, and direct {{es}} API integration. It is the most flexible system for non-standard use cases but does not integrate with the {{kib}} alerting management UI.

Watcher is not available in {{serverless-full}}.

[Get started with Watcher →](watcher.md)

## Using multiple systems together

The alerting systems are independent and can run side by side:

- **Kibana alerting v1 and {{alerting-v2}}** share a single **Rules** navigation entry with separate tabs. Each system writes to its own indices.
- **Watcher** operates through its own API and management UI.
- **{{alerting-v2}} rules on alerts** can query alert data produced by any system, enabling cross-system correlation.

There is no forced migration. You can adopt a new system incrementally while your existing rules continue running.
