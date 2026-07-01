---
navigation_title: Execution permissions
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn which user context workflow runs use.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Workflow execution permissions [workflows-execution-permissions]

Workflows run with a {{kib}} user context. That context determines which {{kib}} and {{es}} resources the workflow can access during the run. [Connector-based action steps](/explore-analyze/workflows/steps/external-systems-apps.md#connector-based-actions) authenticate to the external system with the credentials stored in the connector.

## Which user context is used [workflows-execution-user-context]

The user context depends on how the workflow is triggered:

* Manual runs from the {{kib}} UI or API use the permissions of the authenticated user who starts the run.
* Scheduled workflows use the permissions of the user who last saved the workflow. When an enabled scheduled workflow is edited, {{kib}} refreshes the stored execution credentials for future runs.
* Alert and detection rule triggers use the permissions of the user who last saved the rule.
* Event-based triggers use the permissions of the user whose action produced the event. For example, a `cases.commentsAdded` event runs the workflow with the permissions of the user who added the comment.
* For `workflows.failed`, the handler runs with the permissions the failed workflow ran with.

## Stored credentials [workflows-stored-execution-credentials]

For runs that happen later, such as scheduled workflows and workflows triggered by rules, {{kib}} stores execution credentials for the relevant user context. These credentials control access to {{kib}} and {{es}} resources during the workflow run.

Stored credentials continue to work if the user who created them is later deactivated or their role changes. To update the stored credentials for future runs, save the workflow or rule again with the user context you want future runs to use.

## Execution metadata [workflows-execution-metadata]

When a workflow run starts, {{kib}} records the execution identity so you can audit which permissions a run used.

Refer to [](/explore-analyze/workflows/reference/context-variables.md#workflows-ctx-execution) for the full execution metadata reference.
