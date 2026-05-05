---
navigation_title: Automate security operations
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
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

This section describes common security automation patterns you can build with workflows today. Each pattern uses capabilities that already exist in the workflow engine: [alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md), [{{es}} action steps](/explore-analyze/workflows/steps/elasticsearch.md), [Cases action steps](/explore-analyze/workflows/steps/cases.md), [AI steps](/explore-analyze/workflows/steps/ai-steps.md), and [external system connectors](/explore-analyze/workflows/steps/external-systems-apps.md).

## What you can automate [workflows-security-patterns]

The following patterns map directly to workflow building blocks:

- **Respond to alerts automatically.** An [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) starts the workflow when a detection rule or alerting rule fires. The full alert context is available as `event.alerts[*]`, so later steps can query additional data, build case content, and route notifications based on alert fields.
- **Create and populate cases.** [Cases action steps](/explore-analyze/workflows/steps/cases.md) give you 27 step types to create cases, attach alerts and observables, assign on-call reviewers, and manage the case lifecycle. Use `cases.createCase` to open a case from the alert payload, then `cases.addAlerts` and `cases.addObservables` to attach supporting evidence.
- **Route by severity or entity.** Use [`if`](/explore-analyze/workflows/steps/if.md) or [`switch`](/explore-analyze/workflows/steps/switch.md) steps to branch on alert severity, host, user, or rule name, and send notifications to different Slack channels, PagerDuty services, or Jira projects.
- **Enrich alerts with external context.** Use [HTTP actions](/explore-analyze/workflows/steps/external-systems-apps.md) to pull data from threat intelligence APIs, CMDBs, or identity providers, then write the enriched record back to {{es}} or into the case body.
- **Investigate with AI assistance.** [AI steps](/explore-analyze/workflows/steps/ai-steps.md) let a workflow classify alerts with `ai.classify`, summarize evidence with `ai.summarize`, or invoke an {{agent-builder}} agent with `ai.agent`.
- **Gate destructive actions on human approval.** Use [human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md) with the `waitForInput` step to pause for analyst confirmation before the workflow isolates a host or blocks a user.

## How-to guides [workflows-security-how-tos]

Step-by-step guides for building the most common security automation workflows:

- [Triage a security alert into a case](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-triage-with-case.md): The full SOC triage loop. Enrich the alert, open a case, attach alerts and observables, isolate the host, and notify Slack.
- [Triage alerts with an AI agent](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md): Run an {{agent-builder}} agent on Attack Discovery alerts, populate a case with the analysis, and post a summary to Slack.
- [Enrich an alert with threat intelligence](/explore-analyze/workflows/use-cases/security/automate-security-operations/enrich-alert-with-threat-intel.md): A focused enrichment recipe you can run standalone or compose into a larger triage workflow.

## Learn more

- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): Configure a detection or alerting rule to invoke a workflow.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): 27 step types for working with {{elastic-sec}} cases.
- [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md): Reference for alert-management and other {{kib}} API actions.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Reference for `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent` steps.
- [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Pause for reviewer approval before destructive actions.
- [{{agent-builder}} for Elastic Security](/solutions/security/ai/agent-builder/agent-builder.md): How Agent Builder integrates with Security workflows.
- [Call {{agent-builder}} agents from Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md): Detailed patterns for invoking AI agents from workflow steps.
- [`elastic/workflows` GitHub repo](https://github.com/elastic/workflows): More security example workflows you can adapt.
