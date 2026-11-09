---
navigation_title: Manage service accounts
applies_to:
  stack: ga 9.6+
  serverless: ga
description: Create, review, take out of service, and delete user-managed service accounts for Kibana workloads.
products:
  - id: kibana
  - id: elasticsearch
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Create and manage service accounts in {{kib}} [manage-service-accounts-kibana]

Create user-managed service accounts and assign roles to control programmatic access to {{es}} and {{kib}} APIs. Accounts created in {{kib}} are ready to use with {{kib}} applications such as [Workflows](/explore-analyze/workflows.md). On {{stack}} deployments, you can also use them with your own applications by [creating a service token](authenticate-kibana-api-with-service-account.md#create-service-account-api-token).

:::{note}
:applies_to: serverless: ga
On {{serverless-short}}, user-managed service accounts can only be used within {{kib}} applications. For programmatic access from external applications, use [API keys](/deploy-manage/api-keys.md).
:::

{applies_to}`serverless: unavailable` You can also create service accounts for external applications through the [{{es}} API]({{es-apis}}operation/operation-security-put-user-managed-service-account), although accounts created this way can't be assigned to workloads in {{kib}} applications.

## Before you begin [manage-service-accounts-before-you-begin]

Before you create or manage service accounts, check these requirements:

- Sign in to {{kib}} as a user with the `manage_security` cluster privilege. Without it, the **Service accounts** page isn't available.
- {applies_to}`self: ga` Set [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-encryptedsavedobjects-encryptionkey) in `kibana.yml`. {{kib}} uses this key to encrypt the stored credential.
- On {{stack}} deployments, service accounts must be enabled in {{kib}}. This is the default. If your deployment turns them off, set [`xpack.security.serviceAccounts.enabled`](kibana://reference/configuration-reference/security-settings.md#service-account-settings) to `true` to re-enable them.

## Create a service account [create-service-account-kibana]

Create a service account with the roles your workloads need:

1. Find **Service accounts** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create account**.
3. In the **Name** field, enter a unique name of up to 128 characters. The name must start with a letter or number and can contain letters, numbers, hyphens, and underscores.
4. Optional: In the **Description** field, describe what the account is used for.
5. Under **Set privileges**, select one or more predefined or custom roles that grant the privileges the account needs. To create a role, click **Create new role**.

    For details on predefined roles and how to create custom roles, refer to:

    - {{stack}} deployments: [Built-in roles](elasticsearch://reference/elasticsearch/roles.md) and [role management in {{kib}}](kibana-role-management.md).
    - {{serverless-short}} projects: [Predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) and [custom roles](/deploy-manage/users-roles/serverless-custom-roles.md). Before you assign roles, review the [role limits in {{serverless-short}}](#service-account-serverless-roles).

6. Review the selected roles, and click **Create account**.
7. Confirm that the account appears in the **Service accounts** table with the roles you selected. On {{stack}} deployments, the account uses the principal `kibana/<name>`.

Your service account is now ready to use in {{kib}} applications such as [Workflows](/explore-analyze/workflows.md). {{kib}} manages the credential for you. You don't need to copy a secret, and no token is displayed.

{applies_to}`serverless: unavailable` To use the account from an external API client, [create a separate named service token](authenticate-kibana-api-with-service-account.md#create-service-account-api-token).

## Roles and privileges in {{serverless-short}} [service-account-serverless-roles]
```{applies_to}
serverless: ga
```

A service account can have up to 50 roles. Its privileges come from its assigned roles and cannot exceed the access its creator had when the account was created.

When a workload uses [cross-project search](/explore-analyze/cross-project-search.md), its service account's predefined roles apply across linked projects. For a custom role to grant access to a linked project, that project must define a role with the same name. Custom roles aren't copied between projects.


## Review service accounts [review-service-accounts-kibana]

The **Service accounts** table shows each account's name, description, roles, creator, and number of bound workloads. A **Disabled** badge identifies accounts that can't authenticate. Use the **Role** filter to find accounts assigned to specific roles.

When an account has bound workloads, click **View** in the **Workloads** column to review them.

## Update a service account [update-service-account-kibana]

You can't update service accounts in the {{kib}} UI. On {{serverless-short}}, to change an account's assigned roles or description, [delete the account](#delete-service-account-kibana) and [create a new one](#create-service-account-kibana). On {{stack}} deployments, you can update accounts through the {{es}} API.

:::{tip}
To change a service account's effective privileges, you can edit a role already assigned to it without changing the account's role assignments. Changes to a role also affect other users and service accounts assigned that role.
:::

### Update or deactivate an account through the {{es}} API [disable-service-account]
```{applies_to}
serverless: unavailable
```

Use the [create or replace user-managed service account API]({{es-apis}}operation/operation-security-put-user-managed-service-account) to update an account's roles or description, or to deactivate it by setting `enabled` to `false`.

The PUT request replaces the complete account definition. Send the full definition, including every role, the description, and the `enabled` value you want to preserve. A role left out of the `roles` list is no longer assigned, and an omitted `description` is cleared. If you omit `enabled`, it defaults to `true`. The `roles` field itself is required.

For example, this request deactivates an account by sending its full definition with `enabled` set to `false`:

```console
PUT /_security/service/kibana/workflow-runner
{
  "roles": [ "workflow_runner" ],
  "description": "Runs incident response workflows",
  "enabled": false
}
```

Setting `enabled: false` prevents authentication with the account's service tokens without deleting the account. It doesn't invalidate [short-lived access tokens](token-based-authentication-services.md#token-authentication-access-token) already issued to run workloads as the account. API keys already issued to the account also remain valid.

To reactivate the account, send the complete definition again with `enabled` set to `true`.

[Workflows assigned to an account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md#assign-workflow-service-account) that has `enabled: false` fail the next time they run. They don't fall back to the user who starts or edits the workflow.

## Delete a service account [delete-service-account-kibana]

Deleting a service account is permanent. On {{stack}} deployments, if you only need to temporarily prevent the account from authenticating, [deactivate it](#disable-service-account) instead.

To delete a service account:

1. On the **Service accounts** page, find the account.
2. From the **Actions** column, click **Delete**.
3. Review the confirmation:
    - If no workloads are bound, click **Delete account**.
    - If workloads are bound, review the list. To delete the account without removing the bindings, click **Force delete account**.

If you force delete an account, workloads assigned to it fail on their next run. To restore access, assign each affected workload a valid service account. This reassignment is required even if you recreate the deleted account with the same name. For Workflows, [assign a service account to each affected workflow](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md#assign-workflow-service-account).


### Credentials after deletion in {{stack}} deployments [delete-service-account-stack-credentials]
```{applies_to}
serverless: unavailable
```

Deleting an account through {{kib}} attempts to remove every service token, including the credential it stores for workloads and tokens created outside {{kib}}. It also attempts to invalidate any short-lived access tokens used to run workloads as the account. If any credential cleanup fails, {{kib}} completes the deletion and reports a warning.

A service token left behind after deletion can't authenticate, but it prevents you from creating another account with the same name until you delete the token.

:::{important}
API keys owned by the account aren't invalidated when you delete the account. {{rules-ui}} and tasks that obtained an API key while authenticated as the account can continue to run with that key. To revoke this access, [invalidate the API keys]({{es-apis}}operation/operation-security-invalidate-api-key) explicitly.
:::

## Next steps [manage-service-accounts-next-steps]

Use these guides to work with service accounts and learn more about their credentials:

- [Run a workflow as a service account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md).
- {applies_to}`serverless: unavailable` [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).
- Learn more about [service account types and credentials](service-accounts.md).
