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

Check out [Alerting overview](../alerting-overview.md) for an introduction to each system, where they run, and **Get started** links. Return here to select a system by goal if you are still deciding. If you already know which system you need, open [Kibana alerting v1](kibana-alerting-v1.md), [Kibana alerting v2](kibana-alerting-v2.md), or [Watcher](watcher.md).

:::{note}
You do not need to stand up {{kib}} alerting v1, v2, and {{watcher}} together. Pick the single option that fits your deployment and the goals in the tables below.
:::

## Select by use case

| Goal | Suggested system | Where it runs |
|---|---|---|
| Monitor metrics, logs, or uptime with ready-made rules and minimal setup | [Kibana alerting v1](kibana-alerting-v1.md) | {{stack}} and {{serverless-full}} |
| Use rules tailored to Security, Observability, APM, or Maps | [Kibana alerting v1](kibana-alerting-v1.md) | {{stack}} and {{serverless-full}} |
| Define what to watch using ES\|QL and specify exactly what data goes with each alert | [Kibana alerting v2](kibana-alerting-v2.md) | {{serverless-full}} only |
| Search alert history over time, explore it in Discover, or build dashboards from it | [Kibana alerting v2](kibana-alerting-v2.md) | {{serverless-full}} only |
| Set who gets notified and how often in one place, then reuse that across many rules | [Kibana alerting v2](kibana-alerting-v2.md) | {{serverless-full}} only |
| Tie several rules together or limit notifications for one host or service without silencing the entire rule | [Kibana alerting v2](kibana-alerting-v2.md) | {{serverless-full}} only |
| Build highly custom logic with scripting and chained inputs | [Watcher](watcher.md) | {{stack}} only |

## Compare at a glance

| | Kibana alerting v1 | Kibana alerting v2 | Watcher |
|---|---|---|---|
| **Best for** | Broad coverage with built-in rule types and forms | Full control over detection, history, and notifications in one ES\|QL-centric model | Maximum flexibility for non-standard or scripted workflows |
| **How you define rules** | Select a rule type and fill in fields | Write an ES\|QL query | Author a watch (for example JSON) and optional scripts |
| **Alert records** | Focus on current status; shape depends on rule type | Each run adds to a searchable history you can analyze later | History stored in {{es}} for the watch |
| **Notifications** | Configure connectors and frequency on each rule | Reuse shared notification settings across rules | Throttle and conditions per action |
| **Extra notifications** | Snooze a rule, use maintenance windows | Tune per group, mark items handled, chain follow-up logic | Action conditions and throttling |
| **Where it runs** | {{stack}} and {{serverless-full}} | {{serverless-full}} only | {{stack}} only |
