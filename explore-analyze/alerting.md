---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/alerting-getting-started.html#alerting-concepts-differences
  - https://www.elastic.co/guide/en/serverless/current/project-settings-alerts.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: elasticsearch
  - id: cloud-hosted
navigation_title: Alerting
description: "Elastic alerting overview: Kibana alerting, the {{alerting-v2-system}} (ES|QL, action policies, alert history), and Watcher; where each runs and how to get started."
---

# Alerting [alerting-overview]

Elastic alerting helps you watch your data and respond when something needs attention, whether that is a metric crossing a limit, an asset leaving an area on a map, or an unusual pattern in your time series. You set the conditions and how people should be notified. Elastic runs the checks for you.

Elastic offers three alerting systems, summarized below. Each has a **Get started** link to the full guide for that option.

## {{kib}} alerting

```{applies_to}
stack: ga
serverless: ga
```

{{kib}} alerting gives you ready-made rule types that work with applications such as APM, metrics, security, and uptime monitoring. You set conditions on a schedule you choose and send notifications through common channels (email, chat apps, webhooks, on-call tools, and more). Setup uses forms and clear steps, so you do not need to learn a query language first. It is a strong fit when you want broad coverage out of the box.

[Get started with {{kib}} alerting →](alerting/alerts.md)

## {{alerting-v2-system-cap}} overview

```{applies_to}
serverless: preview
stack: unavailable
```

The {{alerting-v2-system}} is built on {{esql}}. You write the query that defines what to watch for, choose how alert episodes are tracked per series, and control notifications through action policies (shared objects that handle routing, frequency, and notification batching across many rules at once). The {{alerting-v2-system}} also adds alert episode lifecycle tracking, per-series snooze, and rules on alert episodes for correlation and escalation. It is a strong fit when you want full control over what data travels with each alert episode and how your team is notified.

:::{note}
The {{alerting-v2-system}} runs next to {{kib}} alerting on supported deployments. You do not have to move everything at once. Teams can copy or rebuild rules when they are ready. {{kib}} alerting will remain available.
:::

[Get started with the {{alerting-v2-system}} →](alerting/kibana-alerting-experimental.md)

## Watcher

```{applies_to}
stack: ga
serverless: unavailable
```

Watcher is for unusual or highly tailored setups where you need scripts, chained steps, or close control over {{es}} APIs. It does not use the main {{kib}} rules UI used by {{kib}} alerting. It is available on the {{stack}} only, not in {{serverless-full}}.

:::{tip}
For most teams, {{kib}} alerting or the {{alerting-v2-system}} is easier to adopt than Watcher: both work within {{kib}}'s rules UI and don't require writing {{es}} watch definitions.
:::

[Get started with Watcher →](alerting/watcher.md)
