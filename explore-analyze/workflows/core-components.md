---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about the core components that make up Elastic workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Core components

Workflows are composed of three core elements that make workflow automation possible: triggers, steps, and connectors. Together, these components define when workflows run, what they do, and what external systems they connect to.

## Triggers

Triggers define _when_ a workflow runs. A trigger is an event or condition that initiates a workflow, such as an alert firing or a scheduled time occurring. Every workflow begins with a trigger.

Examples of triggers include:

* A user runs a workflow manually
* A specific time or interval is reached
* A detection alert is generated

For more information, refer to [](/explore-analyze/workflows/triggers.md).

## Steps

Steps define _what_ a workflow does. A step is an individual unit of logic or action within a workflow. Steps control how data moves, how decisions are made, and what results are produced. Workflows can contain one or more steps, executed in sequence.

For more information, refer to [](/explore-analyze/workflows/steps.md).

## {{connectors-ui}}

{{connectors-ui}} define _where_ workflows can reach. A connector is the interface between {{kib}} and an external system, allowing workflows to act on or respond to events and services outside of {{kib}}.

For more information, refer to [](/explore-analyze/workflows/steps/external-systems-apps.md#connector-based-actions).
