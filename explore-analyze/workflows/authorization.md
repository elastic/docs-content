---
navigation_title: Authorization
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn whose privileges authorize each type of workflow run, what those privileges grant access to, how to keep them current, and how to troubleshoot privileges errors.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Workflow authorization [workflows-authorization]

Every workflow run is authorized by a specific user's privileges. Use this page to configure who runs your workflows, diagnose privileges errors, and keep your workflows' access current.

## Whose privileges authorize a run [workflows-authorization-user]

The trigger type determines which user's privileges authorize a run.

| Trigger type | Whose privileges are used |
|---|---|
| Manual (UI or API) | The user who starts the run. Manual runs never use a stored API key. |
| Scheduled | The user who last saved the workflow. |
| Alert or detection rule | The user who last saved the rule. |
| Event-based | The user whose action produced the event. For example, a `cases.commentsAdded` event uses the privileges of the user who added the comment. |
| `workflows.failed` (error handler trigger) | The same privileges the failed workflow ran with. |

## How {{kib}} records execution identity [workflows-authorization-audit]

When a workflow run starts, {{kib}} records the execution identity so you can audit which privileges a run used. For a composed workflow ([`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute)), the child execution runs with the same execution identity as the parent, though the **Executions** tab doesn't visually indicate this inheritance. Refer to [](/explore-analyze/workflows/reference/context-variables.md#workflows-ctx-execution) for more information about execution context variables.

:::{note}
The **Created By** filter on the **Workflows** page reflects who last saved the workflow, not necessarily who originally created it.
:::

## How steps use the API key [workflows-authorization-scope]

All `kibana.*` and `elasticsearch.*` steps in a workflow share a single API key. There's no separate credential per step type. The key's privileges determine what each step can do. A step fails with a privileges error if the executing user lacks the required privilege for that step. For example, a `createCase` step fails if the user doesn't have Cases privileges.

_Connector steps are an exception._ The connector authenticates to the third-party system using its own stored credentials, not the workflow's API key. However, {{kib}} still records the connector step as having executed under the workflow's API key for auditability. Refer to [Connector-based actions](/explore-analyze/workflows/steps/external-systems-apps.md#connector-based-actions) for details.

## How to keep a workflow's privileges current [workflows-authorization-updates]

The following actions refresh the stored API key for future runs:

* Saving the workflow again with the desired user.
* Toggling the workflow's **Enabled** setting off, then back on.

:::{important}
Deactivating a user or changing their role doesn't automatically update the stored key. The key remains active and continues to run with the privileges it captured. To pick up new privileges or to remove an outgoing user's access from future runs, save the workflow again with a different user, or toggle **Enabled** off and back on.
:::

## Check and fix errors [workflows-authorization-troubleshoot]

Two types of authorization errors can cause a workflow step to fail:

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Step-level privileges error | The executing user lacks a required privilege for the step. | On the failing step in the run's **Executions** tab. | Save the workflow as a user who has the required privilege, or update the user's role and save again. |
| Stale or not-valid API key | The stored key is no longer valid, for example because an administrator deleted a role it depended on. There's no dedicated status or list-level indicator for this condition. | As an API key error on the individual `elasticsearch` or `kibana` step in the run's **Executions** tab. | Refresh the API key by saving the workflow again or toggling **Enabled** off and back on. |

<!-- TODO: Workflows currently uses {{es}} API keys on both {{stack}} and {{serverless-short}} with no deployment-specific key type. When {{serverless-short}} enables UIAM API keys, Task Manager will use UIAM-issued keys for Serverless workflow runs. Add a "How the API key differs by deployment type" section when that ships. -->
