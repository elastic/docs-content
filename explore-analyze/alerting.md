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
description: Watch your data and respond to conditions automatically with Elastic alerting. Compare Kibana standard alerting, Kibana ES|QL alerting, and Watcher to find the right fit.
---

# Alerting [alerting-overview]

Elastic alerting helps you watch your data and respond when something needs attention, whether that is a metric crossing a limit, an asset leaving an area on a map, or an unusual pattern in your time series. You set the conditions and how people should be notified. Elastic runs the checks for you.

Elastic offers three alerting systems. If you're not sure which fits your situation, refer to [Compare alerting systems](alerting/compare-alerting-systems.md).

## {{alerting-v2-system-cap}}

```{applies_to}
stack: experimental 9.5+
serverless: ga
```

You write an {{esql}} query that defines what to watch for, decide whether matches are tracked as [alert episodes](alerting/esql/alerts.md) or recorded as rule events for later analysis, and control notifications through action policies that handle routing, frequency, and notification batching. {{alerting-v2-system-cap}} also adds alert episode lifecycle tracking, per-series snooze, queryable rule event history, and rules that can correlate those events for escalation. It is a strong fit when you want full control over what data travels with each detection and how your team is notified.

:::{note}
{{alerting-v2-system-cap}} runs next to {{alerting-v1-system}} on {{serverless-full}} and {{stack}} 9.5 and later. You don't have to move everything at once. You can copy or rebuild rules when you're ready, and your existing {{alerting-v1-system}} rules won't be affected.
:::

[Get started with {{alerting-v2-system}} →](alerting/esql/system-overview.md)

## {{alerting-v1-system-cap}}

```{applies_to}
stack: ga
serverless: ga
```

{{alerting-v1-system-cap}} gives you ready-made rule types that work with applications such as APM, metrics, and uptime monitoring. You set the conditions and how often to check them, and send notifications through common channels (email, chat apps, webhooks, on-call tools, and more). Setup uses forms and clear steps, so you do not need to learn a query language first. It is a strong fit when you want broad coverage out of the box.

[Get started with {{alerting-v1-system}} →](alerting/alerts.md)

## Watcher

```{applies_to}
stack: ga
serverless: unavailable
```

Watcher is for unusual or highly tailored setups where you need scripts, chained steps, or close control over {{es}} APIs. It does not use the main {{kib}} rules UI used by {{alerting-v1-system}}. It is available on the {{stack}} only, not in {{serverless-full}}.

:::{tip}
For most teams, {{alerting-v1-system}} is easier to adopt than Watcher. Both {{alerting-v1-system}} and {{alerting-v2-system}} work within {{kib}}'s rules UI and don't require writing {{es}} watch definitions.
:::

[Get started with Watcher →](alerting/watcher.md)
