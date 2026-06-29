---
navigation_title: Concepts
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Concepts and reference material for the components that make up a workflow definition.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Workflow concepts [workflows-concepts]

Concept and reference material for the components that make up a workflow definition. Use this section when you need to know what a specific trigger or step accepts, what its output looks like, or how templating expressions are evaluated.

- [Triggers](/explore-analyze/workflows/triggers.md): Manual, scheduled, alert, and event-driven triggers.
- [Steps](/explore-analyze/workflows/steps.md): Action, flow control, AI, data, and composition steps.
- [Templating engine](/explore-analyze/workflows/templating.md): Liquid templating syntax and custom filters.
- [Reference](/explore-analyze/workflows/reference.md): Quick-reference pages for the workflow YAML surface. Cheat sheet, A-Z step type index, context variables, and the Liquid filter catalog.

## Execution permissions [workflows-execution-permissions]

Workflows execute with a {{kib}} user context. The user context determines which {{kib}} and {{es}} resources the workflow can access. Connector steps use credentials stored in the connector to authenticate to the external system.

When a workflow run starts, {{kib}} records execution metadata:

* `execution.executedBy`: the user whose permissions are used for the workflow run.
* `execution.triggeredBy`: the trigger that started the workflow, such as `manual` or `scheduled`.

For manually run workflows, the workflow uses the permissions of the user who starts the run.

For scheduled workflows, {{kib}} stores execution credentials with the scheduled Task Manager task. Future scheduled runs use those stored credentials. When an enabled scheduled workflow is edited, {{kib}} refreshes the stored execution credentials so future scheduled runs use the permissions from the latest edit context.
