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

Use this page to control access to individual workflows, understand whose privileges authorize a run, and diagnose authorization errors.

## Control access to an individual workflow [workflows-access-control]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

Workflow access control is in technical preview. New workflows are **Public** by default. Public workflows use the existing Workflows privileges in their space. Public does not mean anonymous access.

Make a workflow **Private** to restrict it to its owner and selected users. Each user still needs the corresponding Workflows privileges in the space. Sharing a workflow does not grant those privileges or the permissions needed by its steps.

:::{important}
Private access restricts the Workflows UI and APIs. It does not restrict Elasticsearch queries of execution data. Read [Private workflow execution data](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-private-execution-data) before you use private workflows for sensitive work.
:::

### Workflow roles [workflows-access-roles]

These permissions apply to private workflows:

| Action | Owner | Editor | Executor | Viewer |
|---|---|---|---|---|
| View the workflow and its execution history | Yes | Yes | Yes | Yes |
| Run, cancel, or resume an execution | Yes | Yes | Yes | No |
| Edit, turn on or off, or delete the workflow | Yes | Yes | No | No |
| Change visibility or sharing | Yes | No | No | No |
| Permanently delete the workflow and its execution data | Yes | No | No | No |

The matching feature privilege is also required for each action. For example, Editor access does not grant the Workflows **Delete** privilege. Executor access does not grant **Cancel Workflow Execution**, and viewing execution history also requires **Read Workflow Execution**.

Executors can test the saved workflow from the editor, including when it is turned off. Testing unsaved changes or an individual step requires owner or Editor access. Test runs do not enable the workflow. Normal and scheduled runs require an enabled workflow.

### Share a workflow [workflows-share-access]

To change sharing, you must own the workflow and have the Workflows **Update** privilege. For administrator access, refer to [Recover access to a private workflow](#workflows-recover-private-access).

1. Open a saved workflow.
2. Open the actions menu in the header and select **Access**.
3. Set **Visibility** to **Private**.
4. Under **Users with access**, find a user and select **Viewer**, **Executor**, or **Editor**. Repeat for each user you want to add.
5. Select **Save**.

The Workflows list does not show a visibility badge. Use the **Access** dialog to review sharing.

You can add up to 100 users, in addition to the owner. Sharing uses individual user profiles, not Elasticsearch roles or groups. A user must have signed in to Kibana to have a profile that can appear in the picker.

The picker shows users with Workflows **Read** in the current space. Saving a new grant or increasing a user's access also checks these privileges:

| Workflow role | Required Workflows privileges |
|---|---|
| Viewer | **Read** |
| Executor | **Read** and **Execute** |
| Editor | **Read**, **Execute**, and **Update** |

If a recipient later loses these privileges, their entry can remain in the access list, but the entry alone does not let them use Workflows. You can remove the entry or reduce its role without restoring their privileges first. An unchanged entry does not prevent you from changing other users' access.

To stop sharing with a user, remove their entry and save. To return to space-level access, set **Visibility** to **Public** and save. Existing workflows without access settings keep their previous behavior. Manage sharing through this dialog. The public Workflows API does not provide an operation to change access settings.

### Ownership [workflows-access-owner]

When you create a workflow with a Kibana user profile, that profile becomes its owner. Editing or saving the workflow as another user does not transfer ownership. Ownership transfer is not supported.

Workflows created before access control was available can have no recorded owner. Their recorded creator can set the first access settings, which records that user's profile as the owner. Until then, those workflows remain public.

[Managed workflows](/explore-analyze/workflows/managed-workflows.md) use their existing product permissions and do not provide the **Access** dialog.

### Check automated runs before changing access [workflows-private-automated-runs]

Before making a workflow private, verify that its execution identity is the owner or has Executor or Editor access. Use [Whose privileges authorize a run](#workflows-authorization-user) to identify the caller for each trigger. The caller must also have the required feature privileges. A parent workflow does not automatically grant access to a child workflow it calls.

Scheduled runs use saved credentials associated with the user who last saved the workflow. Changing the access list does not refresh those credentials. If that identity no longer has access to the private workflow, the scheduler skips the run before creating an execution record. There is no new entry in the execution history for that skipped attempt. Restore the identity's workflow access, or save the workflow as a user with access and the required privileges.

The engine also checks access when an execution starts. If access is removed after a run is queued, that run can fail when it starts. Changing a user's roles does not revoke an existing saved API key or replace its captured privileges. Follow [How to keep a workflow's privileges current](#workflows-authorization-updates), or invalidate the API key to stop using those credentials.

### Recover access to a private workflow [workflows-recover-private-access]

```{applies_to}
stack: preview 9.6+
serverless: unavailable
```

On Elastic Stack, a user with the exact `superuser` role can view, edit, delete, and change access to another user's private workflow. This lets you recover access when the owner leaves. The dialog shows a notice that you are editing another user's access settings. The existing owner stays unchanged.

To run the private workflow, add yourself as Executor or Editor and save. Testing unsaved changes or individual steps requires Editor access. A superuser who is already the owner can run it without a separate grant. API keys and custom roles with equivalent privileges do not receive this administrator override.

A superuser can also set the first access settings on a workflow without an owner. In that case, the superuser's profile becomes the owner. This recovery mechanism is not available in Serverless.

### Audit access changes [workflows-access-audit]

```{applies_to}
stack: preview 9.6+
serverless: unavailable
```

With [Kibana audit logging enabled](/deploy-manage/security/logging-configuration/enabling-audit-logs.md), use these events to review access changes and decisions:

| Event action | What it records |
|---|---|
| `workflow_access_control_update` | The previous and saved owner, visibility, and user grants after an access update succeeds. |
| `workflow_access_control_denied` | An operation denied by the workflow ACL, including execution checks. |
| `workflow_access_control_admin_override` | An access check that uses the superuser override. This confirms authorization, not completion of the requested operation. |

Request-scoped events include the caller's identity. ACL events exclude workflow YAML and execution inputs and outputs. Audit logs must be enabled to collect these events.

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
