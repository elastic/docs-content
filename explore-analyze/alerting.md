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
---

# Alerting

Alerting tools in Elasticsearch and Kibana provide functionality to monitor data and notify you about significant changes or events in real time. This page provides an overview of how the key components work.

## {{kib}} alerts

Alerts are notifications generated when specific conditions are met. These notifications are sent to you through channels that you previously set such as email, Slack, webhooks, PagerDuty, and so on. 

Alerts are created based on rules, which define the criteria for triggering them. Rules monitor the data indexed in Elasticsearch and evaluate conditions on a defined schedule to identify matches. For example, a threshold rule can generate an alert when a value crosses a specific threshold, while a machine learning rule activates an alert when an anomaly detection job identifies an anomaly.

## Watcher
```{applies_to}
serverless: unavailable
```

You can use Watcher for alerting and monitoring specific conditions in your data. It enables you to define rules and take automated actions when certain criteria are met. Watcher is a powerful alerting tool for custom use cases and more complex alerting logic. It allows advanced scripting using Painless to define complex conditions and transformations.

:::{tip}
For most use cases, you should use Kibana Alerts instead of Watcher. Kibana Alerts allows rich integrations across use cases like APM, metrics, security, and uptime. Prepackaged rule types simplify setup and hide the details of complex, domain-specific detections, while providing a consistent interface across Kibana.

Watcher is not available in {{serverless-full}}.
:::
