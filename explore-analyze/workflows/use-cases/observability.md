---
navigation_title: Observability
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Use workflows to respond to anomaly detection alerts, correlate signals across data sources, and automate scheduled data operations in Elastic Observability.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Observability workflows [workflows-automate-observability]

Observability signals (infrastructure metrics, application logs, traces, and anomaly detection results) generate the same kind of "observe a problem, do something about it" loop that security does. Use workflows to close that loop: correlate signals across sources, route to the right team, and run scheduled maintenance or reporting tasks.

## What you can automate [workflows-observability-patterns]

The following patterns use existing workflow capabilities:

- **Respond to anomaly detection alerts.** Configure an [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) on an anomaly detection rule. The workflow runs with the alert's context, and can query log data in a window around the anomaly, enrich with host or service metadata, and open a case or post a notification.
- **Correlate signals across data sources.** Use [{{es}} search actions](/explore-analyze/workflows/steps/elasticsearch.md) to query metrics, logs, and traces in the same workflow, then combine results with [`if` steps](/explore-analyze/workflows/steps/if.md) to decide on next actions. Use [data action steps](/explore-analyze/workflows/steps/data.md) to filter, group, and deduplicate results before acting on them.
- **Automate scheduled data operations.** Use a [scheduled trigger](/explore-analyze/workflows/triggers/scheduled-triggers.md) to run periodic health checks, index rollover tasks, or data quality audits.
- **Analyze signals with AI.** Use [AI steps](/explore-analyze/workflows/steps/ai-steps.md) to summarize a multi-signal investigation with `ai.summarize`, classify anomaly shapes with `ai.classify`, or invoke an {{agent-builder}} agent with `ai.agent` before the workflow takes action.
- **Operate on Observability Streams.** Use [Streams action steps](/explore-analyze/workflows/steps/streams.md) to list available streams and pull significant events into a workflow for further processing.

## Example flow [workflows-observability-example-flow]

An anomaly response workflow has the shape:

1. **Alert trigger** fires when an anomaly detection rule surfaces an anomaly.
2. **Elasticsearch step** queries log data in a window around `event.alerts[0].kibana.alert.start`.
3. **AI step** calls an {{agent-builder}} agent to interpret the pattern.
4. **Kibana step** creates a case with the anomaly details and the agent's interpretation.
5. **Connector step** posts a summary to the on-call channel.

## Learn more

- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): Use anomaly detection or alerting rules to invoke a workflow.
- [Scheduled triggers](/explore-analyze/workflows/triggers/scheduled-triggers.md): Run a workflow on a fixed schedule.
- [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md): React when another workflow fails.
- [{{es}} action steps](/explore-analyze/workflows/steps/elasticsearch.md): Reference for search, index, and request actions.
- [Streams action steps](/explore-analyze/workflows/steps/streams.md): Observability Streams operations (technical preview).
- [Data action steps](/explore-analyze/workflows/steps/data.md): Filter, aggregate, and transform signal data inside a workflow.
- [{{agent-builder}} for Observability](/solutions/observability/ai/agent-builder-observability.md): How Agent Builder integrates with observability workflows.

% Ben Ironside Goldstein, 2026-04-16: Planned child pages per Vision doc Section 4.4 and observability section of Section 6:
% - Respond to anomaly detection alerts (tutorial)
% - Correlate signals across data sources (how-to)
% - Automate scheduled data operations (how-to)
% Pending Observability team engagement confirmation (Vision §9 open question).
