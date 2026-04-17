---
navigation_title: Automate security operations
applies_to:
  stack: preview 9.3
  serverless: preview
description: Use workflows to automate security alert response, case creation, enrichment, and notification routing in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Automate security operations [workflows-automate-security]

Use workflows to close the loop between detection and response. When a detection or alerting rule fires, a workflow can enrich the alert with additional context, create or update a case, notify the right channel, and take follow-up actions, all without leaving Elastic.

This section describes common security automation patterns you can build with workflows today. Each pattern uses capabilities that already exist in the workflow engine: [alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md), [{{es}} action steps](/explore-analyze/workflows/steps/elasticsearch.md), [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md), [AI steps](/explore-analyze/workflows/steps/ai-steps.md), and [external system connectors](/explore-analyze/workflows/steps/external-systems-apps.md).

## What you can automate [workflows-security-patterns]

The following patterns map directly to workflow building blocks:

- **Respond to alerts automatically.** An [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) starts the workflow when a detection rule or alerting rule fires. The full alert context is available as `event.alerts[*]`, so later steps can query additional data, build case content, and route notifications based on alert fields.
- **Create and populate cases.** The `kibana.createCaseDefaultSpace` action opens an {{elastic-sec}} case with fields populated from the alert. Refer to [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md) for the full list of named case actions.
- **Route by severity or entity.** Use [`if` steps](/explore-analyze/workflows/steps/if.md) to branch on alert severity, host, user, or rule name, and send notifications to different Slack channels, PagerDuty services, or Jira projects.
- **Enrich alerts with external context.** Use [HTTP actions](/explore-analyze/workflows/steps/external-systems-apps.md) to pull data from threat intelligence APIs, CMDBs, or identity providers, then write the enriched record back to {{es}} or into the case body.
- **Investigate with AI assistance.** An [AI step](/explore-analyze/workflows/steps/ai-steps.md) can call an {{agent-builder}} agent to summarize an alert, classify severity, or draft a triage note for the workflow to attach to the case.

## Example flow [workflows-security-example-flow]

A typical automated alert response workflow has the shape:

1. **Alert trigger** fires when a detection rule matches.
2. **Elasticsearch step** queries surrounding host and user context.
3. **If step** evaluates severity.
4. **Kibana step** creates a case with pre-populated fields.
5. **AI step** calls an {{agent-builder}} agent for a triage summary and appends it to the case.
6. **Connector step** posts a notification to Slack or PagerDuty.

For a complete YAML example that creates a case from a step output, refer to the [Chain steps to move output data](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md#workflows-chain-steps-example) example.

## Learn more

- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): Configure a detection or alerting rule to invoke a workflow.
- [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md): Reference for case, alert, and other Kibana API actions.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Reference for `ai.prompt` and `ai.agent` steps.
- [{{agent-builder}} for Elastic Security](/solutions/security/ai/agent-builder/agent-builder.md): How Agent Builder integrates with Security workflows.
- [Call {{agent-builder}} agents from Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md): Detailed patterns for invoking AI agents from workflow steps.
- [`elastic/workflows` GitHub repo](https://github.com/elastic/workflows): Security-focused example workflows you can adapt.

% Ben Ironside Goldstein, 2026-04-16: Planned child pages per Vision doc Section 4.1:
% - Automatically respond to alerts (end-to-end tutorial)
% - Route alerts by severity (how-to)
% - Enrich alerts with external context (how-to)
% - Investigate with AI assistance (how-to, also anchors AI-augmented section)
% Also deferred: Alert and event fields reference under Reference > Triggers > Alert triggers.
