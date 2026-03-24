---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: >
  Share reports, set up alerts to detect important changes, automate responses
  with workflows, and track incidents with cases.
type: overview
---

# Share, alert, and automate

The {{es}} platform provides tools to share insights, get notified about important changes, automate responses, and track incidents. These tools work together across every Elastic solution and project type.

## Distribute insights with reporting and sharing

[Reporting and sharing](report-and-share.md) lets you export and distribute dashboards, Discover sessions, and visualizations, including to people who don't log into {{kib}}.

- Generate reports on demand or [schedule them automatically](report-and-share/automating-report-generation.md)
- Export as PDF, PNG snapshots, or CSV files
- Share direct links to live dashboards with real-time, filtered views

[Learn more about reporting and sharing →](report-and-share.md)

## Get notified when it matters with alerting

[Alerting](alerting.md) monitors your {{es}} data continuously and notifies you when specific conditions are met, so you don't have to watch dashboards around the clock.

:::{image} /explore-analyze/images/kibana-create-threshold-alert-created.png
:alt: Creating a threshold alert rule in Kibana
:screenshot:
:::

Define rules that evaluate your data on a schedule and trigger actions when criteria are met:

- **Threshold rules**: notify you when error rates spike
- **Machine learning rules**: alert on anomalies
- **Geo-containment rules**: track assets leaving a defined area

Notifications go where your team already works: email, Slack, PagerDuty, Microsoft Teams, webhooks, and more.

Elastic solutions extend this foundation with domain-specific rules. Security detection rules match threat patterns, while Observability rules monitor SLOs, infrastructure metrics, and log error rates. All rules share the same interface, action framework, and notification channels.

[Learn more about alerting →](alerting.md)

## Automate multi-step responses with workflows

[Workflows](workflows.md) turn manual, repetitive processes into automated sequences that run reliably every time.

:::{image} /explore-analyze/images/workflows-editor.png
:alt: The workflow editor showing a sequence of automated steps
:screenshot:
:::

A workflow is a sequence of steps triggered by an alert, a schedule, or a manual action. Each step can:

- Query {{es}} or call external APIs
- Branch on conditions or loop over collections
- Create cases, send notifications, or isolate hosts

For example, when a security alert fires, a workflow can enrich it with threat intelligence, create a case, notify the on-call analyst, and isolate the affected host, all without human intervention.

[Learn more about workflows →](workflows.md)

## Track and coordinate response with cases

[Cases](cases.md) provide a central place to track incidents, document findings, and coordinate response efforts across your team.

:::{image} /explore-analyze/images/kibana-cases-create.png
:alt: Creating a case in Kibana
:screenshot:
:::

- Attach alerts, files, and visualizations to build a record of your investigation
- Assign team members and add comments
- Push updates to external systems like Jira or ServiceNow

Cases are available in {{elastic-sec}}, Observability, and Stack Management.

[Learn more about cases →](cases.md)

## How these tools work together

These capabilities chain together into complete operational workflows:

1. A **dashboard** reveals a pattern, such as error rates climbing for a specific service.
2. An **alert rule** detects the threshold breach and triggers a notification.
3. A **workflow** automatically enriches the alert, checks if the service is in a maintenance window, and creates a case if it isn't.
4. A **case** tracks the investigation, collecting related alerts, team comments, and resolution steps.
5. A **scheduled report** captures the post-incident dashboard state and distributes it to stakeholders.

Together, these tools close the loop from data to action to resolution without requiring you to leave the Elastic platform.

## Next steps

- **[Automatically generate reports](report-and-share/automating-report-generation.md)**: Set up recurring report delivery for your dashboards.
- **[Getting started with alerting](alerting/alerts/alerting-getting-started.md)**: Create your first alert rule and configure notification channels.
- **[Get started with workflows](workflows/get-started.md)**: Build your first automated workflow to respond to alerts.
- **[Create a case](cases/create-cases.md)**: Start tracking an incident and attach relevant alerts and evidence.
