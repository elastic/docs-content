---
navigation_title: Run as a service account
applies_to:
  stack: ga 9.6+
  serverless: unavailable
description: Assign a user-managed service account to a workflow, verify its execution identity, and troubleshoot permission errors.
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Run a workflow as a service account [run-workflow-as-service-account]

Starting with {{stack}} 9.6, you can run a workflow as a [user-managed service account](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.md#user-managed-service-accounts).

Each run uses the account's roles, regardless of who starts or last edits the workflow. This is useful for shared workflows: their identity remains stable even if the person who created them leaves your organization. You can also give the account only the privileges the workflow needs, even if the people who manage it have broader access.

This guide shows you how to assign a service account to a workflow and verify which identity its runs use.

## Before you begin [run-workflow-as-service-account-prerequisites]

Before you assign a service account to a workflow, make sure you meet these requirements:

- You need the **Update** [Workflows privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-workflows-subfeatures) to assign an account. To run the workflow and review its execution, you also need **Execute** and **Read Workflow Execution**.
- You need the `manage_security` cluster privilege to add, change, or remove the workflow's service account assignment. Editing or deleting a workflow assigned to a service account also requires this privilege, in addition to the corresponding Workflows privilege.

## Assign a service account [assign-workflow-service-account]

The `settings.run_as` field specifies the account that runs the workflow. Set it to the account's full principal, such as `kibana/incident-response`.

You can assign an existing account or create one without leaving the workflow editor. In both cases, the account must be [created in {{kib}}](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-service-accounts-in-kibana.md) and have the roles required by the workflow steps. Accounts created directly through the {{es}} API can't be used for workflow execution, even if they use the `kibana` namespace.

1. Open the workflow in the {{kib}} workflow editor.
2. In the `settings` block, add `run_as`:

    - To use an existing account, select it from the picker or enter its principal.
    - To create and assign an account, select **Create account** and configure its roles.

    For example:

    ```yaml
    settings:
      run_as: kibana/incident-response
    ```

3. Save the workflow.

The saved assignment applies to manual, scheduled, alert, and event-driven runs. Users who have permission to run the workflow don't need `manage_security` to start it.

## Verify the execution identity [verify-workflow-execution-identity]

Run the saved workflow, then open its execution details. The overview identifies both identities:

- **Triggered by** identifies the user who starts the workflow or last saved it, depending on the trigger.
- **Run as** is the service account whose privileges authorized the workflow's actions.

Steps that call {{es}} or {{kib}} (`elasticsearch.*` and `kibana.*`) use the service account's privileges. Connectors use their own stored credentials to authenticate to external systems. For details about credentials and child workflows, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md).

% TBD: Confirm agent credential propagation with Workflows and Agent Builder after https://github.com/elastic/kibana/issues/293019 is resolved before adding a claim about agents invoked by a bound workflow.

## Test the workflow [test-bound-workflow]

Save your changes before you [test the complete workflow](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md#workflows-supply-test-input). The test uses the saved definition and the service account's privileges. You can't test individual steps or unsaved definitions when `run_as` is set.

## Handle permission and identity failures [handle-workflow-service-account-failures]

A workflow assigned to a service account never falls back to the triggering user's privileges. If a run fails, check the account and its roles:

- If the account is deactivated or deleted, the next run fails.
- If the account lacks a privilege required by a step, that step fails with a privileges error.
- If the account was deleted and recreated with the same principal, the old assignment no longer matches it. Remove the assignment, save the workflow, then assign the recreated account.

[Update the account or its roles](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-service-accounts-in-kibana.md#disable-service-account), or assign a different account, then run the workflow again.

## Remove the assignment [remove-workflow-service-account]

Remove `run_as` from the workflow's `settings` block and save the workflow. Future runs return to the default [workflow authorization model](/explore-analyze/workflows/authorization.md), in which the trigger type determines whose privileges are used.

Changing or removing the assignment doesn't switch the identity of a run already in progress. That run fails if it needs to renew its credential or resumes after a pause.
