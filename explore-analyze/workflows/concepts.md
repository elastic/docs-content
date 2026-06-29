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

Workflows execute with a {{kib}} user context. That context determines which {{kib}} and {{es}} resources the workflow can access during the run. Connector steps use credentials stored in the connector to authenticate to the external system.

The execution identity depends on how the workflow is triggered:

* Manual runs from the {{kib}} UI or API use the permissions of the logged-in user who starts the run.
* Scheduled workflows use the permissions of the user who last modified the workflow. When an enabled scheduled workflow is edited, {{kib}} refreshes the stored execution credentials for future runs.
* Alert and detection rule triggers use the permissions of the user who last modified the rule. If the rule has not been modified, they use the permissions of the user who created the rule.
* Event-based triggers use the permissions of the user whose action produced the event. For example, a `cases.addComment` event runs the workflow with the permissions of the user who added the comment.

When a workflow run starts, {{kib}} records execution metadata:

* `execution.executedBy`: the user whose permissions are used for the workflow run.
* `execution.triggeredBy`: the trigger that started the workflow, such as `manual` or `scheduled`.
