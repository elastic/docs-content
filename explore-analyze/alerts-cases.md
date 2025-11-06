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

# Alerts and cases

Alerting tools in Elasticsearch and Kibana provide functionality to monitor data and notify you about significant changes or events in real time. This page provides an overview of how the key components work.

## Alerts

Alerts are notifications generated when specific conditions are met. These notifications are sent to you through channels that you previously set such as email, Slack, webhooks, PagerDuty, and so on. Alerts are created based on rules, which define the criteria for triggering them. Rules monitor the data indexed in Elasticsearch and evaluate conditions on a defined schedule to identify matches. For example, a threshold rule can generate an alert when a value crosses a specific threshold, while a machine learning rule activates an alert when an anomaly detection job identifies an anomaly.

## Cases

Cases are a collaboration and tracking tool, which is particularly useful for incidents or issues that arise from alerts. You can group related alerts into a case for easier management, add notes and comments to provide context, track investigation progress, and assign cases to team members or link them to external systems. Cases ensure that teams have a central place to track and resolve alerts efficiently.

## Maintenance windows

If you have a planned outage, maintenance windows prevent rules from generating notifications in that period. Alerts still occur but their notifications are suppressed.

### Workflow Example

1. **Rule Creation**: You set up a rule to monitor server logs for failed login attempts exceeding 5 within a 10-minute window.
1. **Alert Generation**: When the rule's condition is met, an alert is created.
1. **Notification**: The alert runs an action, such as sending a Slack message or an email, unless a maintenance window is active.
1. **Case Management**: If the alert is part of an ongoing investigation, it's added to a case for further analysis and resolution.

By combining these tools, Elasticsearch and Kibana enable incident response workflows, helping teams to detect, investigate, and resolve issues efficiently.

## Watcher
```{applies_to}
serverless: unavailable
```

You can use Watcher for alerting and monitoring specific conditions in your data. It enables you to define rules and take automated actions when certain criteria are met. Watcher is a powerful alerting tool for custom use cases and more complex alerting logic. It allows advanced scripting using Painless to define complex conditions and transformations.
