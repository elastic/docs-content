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

Seeing something in your data is only the first step. What matters is what happens next: sharing a report with stakeholders, getting notified when a critical threshold is crossed, automatically triaging an alert, or coordinating a response across your team. The {{es}} platform provides a progression of tools that take you from insight to action, and they work together across every Elastic solution and project type.

## Distribute insights with reporting and sharing

[Reporting and sharing](report-and-share.md) lets you export and distribute dashboards, Discover sessions, and visualizations so that insights reach the people who need them — even those who don't log into {{kib}}.

Generate reports on demand or [schedule them automatically](report-and-share/automating-report-generation.md) for recurring delivery. Export dashboards as PDF or PNG snapshots for executive reviews, or generate CSV files for teams that work in spreadsheets. You can also share direct links to live dashboards, giving collaborators real-time access to filtered views of the data.

[Learn more about reporting and sharing →](report-and-share.md)

## Get notified when it matters with alerting

[Alerting](alerting.md) monitors your {{es}} data continuously and notifies you when specific conditions are met — so you don't have to watch dashboards around the clock.

:::{image} /explore-analyze/images/kibana-create-threshold-alert-created.png
:alt: Creating a threshold alert rule in Kibana
:screenshot:
:::

Define rules that evaluate your data on a schedule and trigger actions when criteria are met. A threshold rule can notify you when error rates spike, a machine learning rule can alert on anomalies, and a geo-containment rule can track assets leaving a defined area. Notifications go where your team already works: email, Slack, PagerDuty, Microsoft Teams, webhooks, and more.

Elastic solutions extend this foundation with domain-specific rules. Security detection rules match threat patterns across your data. Observability rules monitor SLOs, infrastructure metrics, and log error rates. But all rules share the same interface, action framework, and notification channels.

[Learn more about alerting →](alerting.md)

## Automate multi-step responses with workflows

[Workflows](workflows.md) turn manual, repetitive processes into automated sequences that run reliably every time. They bridge the gap between detecting a problem and resolving it.

A workflow is a defined sequence of steps — triggered by an alert, a schedule, or a manual action — that can query {{es}}, call external APIs, branch on conditions, and loop over collections. For example, when a security alert fires, a workflow can enrich it with threat intelligence, create a case, notify the on-call analyst, and isolate the affected host — all without human intervention.

Workflows address common operational challenges: alert fatigue from too many notifications, understaffed teams that can't keep up with manual triage, and tool fragmentation that forces context-switching between systems.

[Learn more about workflows →](workflows.md)

## Track and coordinate response with cases

[Cases](cases.md) provide a central place to track incidents, document findings, and coordinate response efforts. Whether you're a security analyst triaging threats or an SRE responding to an outage, cases bring together alerts, evidence, and team communication in one place.

:::{image} /explore-analyze/images/kibana-cases-create.png
:alt: Creating a case in Kibana
:screenshot:
:::

Attach alerts, files, and visualizations to a case to build a record of your investigation. Assign team members, add comments, and push updates to external systems like Jira or ServiceNow to keep your existing workflows intact. Cases are available in {{elastic-sec}}, Observability, and Stack Management.

[Learn more about cases →](cases.md)

## How these tools work together

These capabilities are designed to chain together into complete operational workflows:

1. A **dashboard** reveals a pattern — error rates climbing for a specific service.
2. An **alert rule** detects the threshold breach and triggers a notification.
3. A **workflow** automatically enriches the alert, checks if the service is in a maintenance window, and creates a case if it isn't.
4. A **case** tracks the investigation, collecting related alerts, team comments, and resolution steps.
5. A **scheduled report** captures the post-incident dashboard state and distributes it to stakeholders.

Each tool handles one part of the chain, but together they close the loop from data to insight to action to resolution — without requiring you to leave the Elastic platform or stitch together external tools.

## Next steps

- **[Automatically generate reports](report-and-share/automating-report-generation.md)**: Set up recurring report delivery for your dashboards.
- **[Getting started with alerting](alerting/alerts/alerting-getting-started.md)**: Create your first alert rule and configure notification channels.
- **[Get started with workflows](workflows/get-started.md)**: Build your first automated workflow to respond to alerts.
- **[Create a case](cases/create-cases.md)**: Start tracking an incident and attach relevant alerts and evidence.
