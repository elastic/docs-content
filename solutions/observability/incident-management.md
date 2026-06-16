---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/incident-management.html
  - https://www.elastic.co/guide/en/serverless/current/incident-management.html
applies_to:
  stack: ga
  serverless:
products:
  - id: observability
  - id: cloud-serverless
---

# Incident management [incident-management]

Explore the topics in this section to learn how to respond to incidents detected in your {{observability}} data.

|     |     |
| --- | --- |
| [Alerting](/solutions/observability/incident-management/alerting.md) | Trigger alerts when incidents occur, and use built-in connectors to send the alerts to email, slack, or other third-party systems, such as your external incident management application. |
| [Cases](/solutions/observability/incident-management/observability-cases.md) | Collect and share information about {{observability}} issues by opening cases and optionally sending them to your external incident management application. |
| [Service-level objectives (SLOs)](/solutions/observability/incident-management/service-level-objectives-slos.md) | Set clear, measurable targets for your service performance, based on factors like availability, response times, error rates, and other key metrics. |

## Automate incident response with workflows [incident-management-automate]

Use [Elastic Workflows](/explore-analyze/workflows.md) to encode your incident-response runbooks as declarative YAML automations triggered by alerts. The [Automate root cause analysis for an {{observability}} alert](/explore-analyze/workflows/use-cases/observability/root-cause-analysis.md) workflow shows how to invoke an Agent Builder agent on each alert, attach the analysis to a case, and notify the on-call channel.