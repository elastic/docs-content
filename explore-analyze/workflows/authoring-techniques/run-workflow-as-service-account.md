---
navigation_title: Run as a service account
applies_to:
  stack: ga 9.6+
  serverless: ga
description: Assign a user-managed service account to a workflow, verify its execution identity, and troubleshoot permission errors.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Run a workflow as a service account [run-workflow-as-service-account]

By default, workflows run with a user's privileges. As an alternative, you can run a workflow as a [user-managed service account](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.md#user-managed-service-accounts).

The workflow then uses the account's privileges for every run, regardless of who starts or last edits it. This gives shared workflows a stable identity, even if their creator leaves your organization. You can also give the account only the privileges the workflow needs, even if the people who manage it have broader access.

This guide shows you how to assign a service account to a workflow and verify its execution identity.

## Before you begin [run-workflow-as-service-account-prerequisites]

Before you assign a service account to a workflow, make sure you meet these requirements:

- You need the **Update** [Workflows privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-workflows-subfeatures) to assign an account. To run the workflow and review its execution, you also need **Execute** and **Read Workflow Execution**.
- You need the `manage_security` cluster privilege to add, change, or remove the workflow's service account assignment. Editing or deleting a workflow assigned to a service account also requires this privilege, in addition to the corresponding Workflows privilege.

## Assign a service account [assign-workflow-service-account]

The `settings.run_as` field specifies the ID of the account that runs the workflow. On {{stack}} deployments, this is the account's principal, such as `kibana/incident-response`. On {{serverless-short}}, it is a generated identifier independent of the account's name.

You can assign an existing account or create one without leaving the workflow editor. The account must have the privileges required by the workflow steps.

1. Open the workflow in the {{kib}} workflow editor.
2. In the `settings` block, add `run_as`:

    - To use an existing account, select it from the picker or enter its ID.
    - To create and assign an account, select **Create account** and configure its roles.

    For example:

    ```yaml
    settings:
      run_as: "<service-account-id>"
    ```

    Replace `<service-account-id>` with the account's ID.

3. Save the workflow.

The saved assignment applies to manual, scheduled, alert, and event-driven runs. Users who have permission to run the workflow don't need `manage_security` to start it.

## Verify the execution identity [verify-workflow-execution-identity]

[Test the complete workflow](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md#workflows-supply-test-input). The test uses the saved definition and the service account's privileges. You can't test individual steps or unsaved definitions when `run_as` is set.

After the test completes, open its execution details. The overview identifies both identities:

- **Triggered by** shows the identity associated with the start of the run, which can be a user or a service account.
- **Run as** shows the assigned service account whose privileges authorize the workflow's actions.

Steps that call {{es}} or {{kib}} (`elasticsearch.*` and `kibana.*`) use the service account's privileges. {{connectors-ui}} use their own stored credentials to authenticate to external systems. For details about credentials and child workflows, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md).

% TBD: Confirm agent credential propagation with Workflows and Agent Builder after https://github.com/elastic/kibana/issues/293019 is resolved before adding a claim about agents invoked by a workflow assigned to a service account.

## Handle permission and identity failures [handle-workflow-service-account-failures]

A workflow assigned to a service account never falls back to the triggering user's privileges. If a run fails, check the account and its roles:

- If the account is deactivated or deleted, the next run fails.
- If the account lacks a privilege required by a step, that step fails with a privileges error.
- If the account was deleted and recreated with the same name, the old assignment no longer matches it. Remove the assignment, save the workflow, then assign the recreated account.

[Update the account or its roles](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-service-accounts-in-kibana.md#update-service-account-kibana), or assign a different account, then run the workflow again.

## Remove the assignment [remove-workflow-service-account]

To remove the service account assignment from a workflow, remove `run_as` from the workflow's `settings` block and save the workflow. Future runs return to the default [workflow authorization model](/explore-analyze/workflows/authorization.md), in which the trigger type determines whose privileges are used.

Changing or removing the assignment doesn't switch the identity of a run already in progress. That run fails if it needs to renew its credential or resumes after a pause.
