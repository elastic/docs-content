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

Every workflow run is authorized by:

* A specific user's privileges, by default.
* {applies_to}`stack: ga 9.6+` {applies_to}`serverless: unavailable` The privileges of an assigned user-managed service account.

Use this page to configure who runs your workflows, diagnose privileges errors, and keep your workflows' access current.

## Whose privileges authorize a run [workflows-authorization-user]

When a workflow doesn't run as a service account, the trigger type determines which user's privileges authorize a run.

| Trigger type | Whose privileges are used |
|---|---|
| Manual (UI or API) | The user who starts the run. Manual runs never use a stored API key. |
| Scheduled | The user who last saved the workflow. |
| Alert or detection rule | The user who last saved the rule. |
| Event-based | The user whose action produced the event. For example, a `cases.commentsAdded` event uses the privileges of the user who added the comment. |
| `workflows.failed` (error handler trigger) | The same privileges the failed workflow ran with. |

### Workflows that run as a service account [workflows-authorization-service-account]
```{applies_to}
stack: ga 9.6+
serverless: unavailable
```

When you [assign a service account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md) with `settings.run_as`, every run uses that account's roles. The trigger type and the user who last saved or started the workflow don't change its privileges.

The workflow stores a reference to the account. When a run starts, {{kib}} obtains a short-lived credential and renews it as needed. {{es}} resolves the account's roles whenever it authenticates, so changes to an assigned role apply to later credential requests without saving the workflow again.

If the account is deleted, turned off, or lacks a required privilege, the run fails without falling back to a user.

## How {{kib}} records execution identity [workflows-authorization-audit]

When a workflow run starts, {{kib}} records the execution identity so you can audit which privileges it used. Refer to [](/explore-analyze/workflows/reference/context-variables.md#workflows-ctx-execution) for execution context variables.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: unavailable` For workflows assigned to service accounts, **Triggered by** identifies the user who starts the workflow or last saved it, depending on the trigger. **Run as** shows the service account used for authorization.

The **Created By** filter on the **Workflows** page reflects who last saved the workflow, not necessarily who originally created it.

### Execution identity in child workflows [workflows-authorization-child-identity]

For workflows composed with [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute), the execution identity depends on service account support:

::::{applies-switch}
:::{applies-item} stack: ga 9.6+
Each saved workflow uses its own service account assignment. A child doesn't automatically inherit its parent's assignment. If the child isn't assigned a service account, it uses the original caller's identity. When neither workflow is assigned a service account, the child uses the same execution identity as the parent.
:::
:::{applies-item} { stack: 'ga 9.4-9.5, preview =9.3', serverless: ga }
The child execution runs with the same execution identity as the parent. The **Executions** tab doesn't visually indicate this inheritance.
:::
::::

## How steps use the execution identity [workflows-authorization-scope]

All `kibana.*` and `elasticsearch.*` steps in a workflow share the same execution identity. There's no separate identity per step type. A step fails with a privileges error if the user or service account lacks the required privilege for that step. For example, a `createCase` step fails if the execution identity doesn't have Cases privileges.

For a workflow that isn't assigned a service account, credentials belong to the user identified in [Whose privileges authorize a run](#workflows-authorization-user). For a workflow assigned to a service account, refer to [Workflows assigned a service account](#workflows-authorization-service-account).

_Connector steps are an exception._ The connector authenticates to the third-party system using its own stored credentials, not the workflow's credential. However, {{kib}} still records the connector step as having executed under the workflow's execution identity for auditability. Refer to [Connector-based actions](/explore-analyze/workflows/steps/external-systems-apps.md#connector-based-actions) for details.

## How to keep a user's privileges current [workflows-authorization-updates]

For a workflow that isn't assigned a service account, the following actions refresh the stored API key for future runs:

* Saving the workflow again with the desired user.
* Toggling the workflow's **Enabled** setting off, then back on.

:::{important}
Deactivating a user or changing their role doesn't automatically update the stored key. The key remains active and continues to run with the privileges it captured. To pick up new privileges or to remove an outgoing user's access from future runs, save the workflow again with a different user, or toggle **Enabled** off and back on.
:::

## Check and fix errors [workflows-authorization-troubleshoot]

The following authorization errors can cause a workflow step to fail:

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Step-level privileges error | The execution identity lacks a required privilege for the step. | On the failing step in the run's **Executions** tab. | For a user identity, update the user's role and save the workflow again. For a service account, update one of its assigned roles. |
| Stale or not-valid API key | The stored key is no longer valid, for example because an administrator deleted a role it depended on. There's no dedicated status or list-level indicator for this condition. | As an API key error on the individual `elasticsearch` or `kibana` step in the run's **Executions** tab. | Refresh the API key by saving the workflow again or toggling **Enabled** off and back on. |
| Service account identity error {applies_to}`stack: ga 9.6+` {applies_to}`serverless: unavailable` | The assigned account has `enabled: false`, is deleted, or no longer matches the saved assignment. | In the run's execution details. | Set `enabled: true` or assign an available account, then start a new run. |

<!-- TODO: Workflows currently uses {{es}} API keys on both {{stack}} and {{serverless-short}} with no deployment-specific key type. When {{serverless-short}} enables UIAM API keys, Task Manager will use UIAM-issued keys for Serverless workflow runs. Add a "How the API key differs by deployment type" section when that ships. -->
