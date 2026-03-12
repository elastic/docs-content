---
navigation_title: Alerting workflows
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Workflows are automated task sequences used as notification policy destinations and direct rule links in Kibana alerting v2."
---

# Kibana alerting v2 workflows [workflows-v2]

Workflows are user-defined automated sequences of tasks for actions, notifications, and external integrations. In Kibana alerting v2, workflows serve as the destinations for notification policies and can also be linked directly to rules.

## How workflows relate to alerting

Workflows are referenced in two ways:

1. **As notification policy destinations** — when a notification policy dispatches an alert, it sends the alert data to the configured workflow. The workflow then executes its task sequence (for example, send a Slack message, create a PagerDuty incident, update a ticket).

2. **As direct rule links** — rules can link to workflows that are triggered on specific rule events (for example, when a rule first activates or when an error occurs during execution).

## Workflow configuration

Workflows are managed in the **Workflows** management area. Each workflow defines:

- **Name** and **description**.
- **Task sequence** — an ordered list of tasks to execute, such as sending a message or making an HTTP request.
- **Destinations** — the external systems the workflow integrates with (Slack, PagerDuty, email, webhooks, and others).

## Workflow destinations in notification policies

When you create a notification policy, you select one or more workflows as destinations. The policy's matching, grouping, and throttling logic determines when and how alerts are sent to those workflows.

For example:

- A "Critical Production Alerts" policy might route to a PagerDuty workflow for immediate incident creation.
- A "Warning Summary" policy might route to a Slack workflow that delivers a digest every 15 minutes.
- A policy can route to multiple workflows simultaneously (for example, both Slack and email).

## Authentication

Workflows use the API key from the notification policy that triggered them. This means the workflow executes with the privileges of the user who created or last updated the notification policy. This design prevents privilege escalation — you need workflow-level permissions to add a workflow as a policy destination.
