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
navigation_title: Alerting
description: Set up alerting in Elastic to monitor your data and get notified when conditions are met — from threshold-based rules to geofencing and anomaly detection.
---

# Alerting [alerting-overview]

Elastic alerting lets you monitor your data and take action when something needs attention — whether that's a metric crossing a threshold, an asset leaving a geographic boundary, or an anomaly in your time series data. You define the conditions, choose how you want to be notified, and Elastic handles the rest.

Elastic provides three alerting systems: [Kibana alerting v1](alerting/kibana-alerting-v1.md), [Kibana alerting v2](alerting/kibana-alerting-v2.md), and [Watcher](alerting/watcher.md).

## Kibana alerting v1

```{applies_to}
stack: ga
serverless: ga
```

Kibana alerting v1 provides a set of built-in rule types integrated with applications like APM, Metrics, Security, and Uptime. Rules evaluate conditions on a defined schedule and trigger actions through connectors — email, Slack, webhooks, PagerDuty, and more. Prepackaged rule types simplify setup for common use cases.

Refer to [Kibana alerting v1](alerting/kibana-alerting-v1.md) to get started.

## Kibana alerting v2

```{applies_to}
stack: preview 9.4
serverless: preview
```

Kibana alerting v2 is a redesigned alerting framework built on ES|QL. You write the query that defines what to detect and what data each alert carries. V2 introduces notification policies for centralized notification control, per-series snooze, alert lifecycle tracking with episodes, and the ability to write rules on alerts for correlation and escalation.

Kibana alerting v2 runs alongside Kibana alerting v1. There is no forced migration.

Refer to [Kibana alerting v2](alerting/kibana-alerting-v2.md) to get started.

## Watcher

```{applies_to}
serverless: unavailable
```

Watcher provides alerting for custom use cases and complex alerting logic. It supports advanced scripting with Painless to define complex conditions and transformations.

:::{tip}
For most use cases, Kibana alerting v1 or Kibana alerting v2 is recommended over Watcher. They offer richer integrations, prepackaged rule types, and a consistent management interface. Watcher is not available in {{serverless-full}}.
:::

Refer to [Watcher](alerting/watcher.md) to get started.
