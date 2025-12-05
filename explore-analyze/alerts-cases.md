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
description: Overview of alerting and case management tools for monitoring data and managing incident response.
---

# Alerts and cases [alerts-cases]

Alerting and case management in {{product.elasticsearch}} and {{product.kibana}} enable you to monitor data continuously, receive real-time notifications when specific conditions are met, and track incident investigations collaboratively. These tools help you detect issues early, respond quickly, and maintain visibility throughout the resolution process.

## Alerts [alerts-overview]

Alerts are notifications generated when specific conditions are met. These notifications are sent to you through channels that you previously set such as email, Slack, webhooks, PagerDuty, and so on. Alerts are created based on rules, which define the criteria for triggering them. {{rules-ui}} monitor the data indexed in {{product.elasticsearch}} and evaluate conditions on a defined schedule to identify matches. For example, a threshold rule can generate an alert when a value crosses a specific threshold, while a {{ml}} rule activates an alert when an {{anomaly-job}} identifies an anomaly.

## Cases [cases-overview]

Cases are a collaboration and tracking tool, which is particularly useful for incidents or issues that arise from alerts. You can group related alerts into a case for easier management, add notes and comments to provide context, track investigation progress, and assign cases to team members or link them to external systems. Cases ensure that teams have a central place to track and resolve alerts efficiently.

## Maintenance windows [maintenance-windows-overview]

If you have a planned outage, maintenance windows prevent rules from generating notifications in that period. Alerts still occur but their notifications are suppressed.

### Workflow example [workflow-example]

1. **Rule Creation**: You set up a rule to monitor server logs for failed login attempts exceeding 5 within a 10-minute window.
1. **Alert Generation**: When the rule's condition is met, an alert is created.
1. **Notification**: The alert runs an action, such as sending a Slack message or an email, unless a maintenance window is active.
1. **Case Management**: If the alert is part of an ongoing investigation, it's added to a case for further analysis and resolution.

By combining these tools, {{product.elasticsearch}} and {{product.kibana}} enable incident response workflows, helping teams to detect, investigate, and resolve issues efficiently.

## {{watcher}} [watcher-overview]
```{applies_to}
serverless: unavailable
```

You can use Watcher for alerting and monitoring specific conditions in your data. It enables you to define rules and take automated actions when certain criteria are met. Watcher is a powerful alerting tool for custom use cases and more complex alerting logic. It allows advanced scripting using Painless to define complex conditions and transformations.

:::{tip}
For most use cases, you should use Kibana Alerts instead of Watcher. Kibana Alerts allows rich integrations across use cases like APM, metrics, security, and uptime. Prepackaged rule types simplify setup and hide the details of complex, domain-specific detections, while providing a consistent interface across Kibana.

Watcher is not available in {{serverless-full}}.
:::
