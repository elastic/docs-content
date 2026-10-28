---
navigation_title: Manage service accounts
applies_to:
  stack: ga 9.6+
  serverless: unavailable
description: Create, review, take out of service, and delete user-managed service accounts for Kibana workloads.
products:
  - id: kibana
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Create and manage service accounts in {{kib}} [manage-service-accounts-kibana]

Create user-managed service accounts and assign roles to control programmatic access to {{es}} and {{kib}} APIs. {{kib}} creates each account in {{es}} and securely stores its credential.

## Before you begin [manage-service-accounts-before-you-begin]

Before you create or manage service accounts, check these requirements:

- You need the `manage_security` cluster privilege. Without it, the **Service accounts** page isn't available. The `manage_service_account` privilege applies only to built-in accounts in the `elastic` namespace.
- {applies_to}`self: ga` Set [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-encryptedsavedobjects-encryptionkey) in `kibana.yml`. {{kib}} uses this key to encrypt the stored credential.

% TBD: pending to add link to the setting reference as soon as the kibana PR is created and merged
Service accounts are enabled by default on {{ech}}, {{ece}}, {{eck}}, and self-managed deployments. Set the {{kib}} `xpack.security.serviceAccounts.enabled` setting to `false` to turn off the **Service accounts** page and workload integration.

## Create a service account [create-service-account-kibana]

Create a service account with the roles your workloads need:

1. Find **Service accounts** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Click **Create account**.
3. In the **Name** field, enter a unique name of up to 128 characters. The name must start with a letter or number and can contain letters, numbers, hyphens, and underscores.
4. Optional: In the **Description** field, describe what the account is used for.
5. Under **Set privileges**, select one or more predefined or custom roles that grant the privileges the account needs. To [create a role](kibana-role-management.md), click **Create new role**.
6. Review the selected roles, and click **Create account**.

The service account uses the principal `kibana/<name>`. For workloads such as workflows, rules, and scheduled tasks, {{kib}} creates and securely stores the credential for you. You don't need to copy a secret, and no token is displayed. To use the account from an external API client, [create a separate named service token](authenticate-kibana-api-with-service-account.md#create-service-account-api-token).

{{es}} resolves the assigned roles by name whenever the account authenticates. Editing a role changes the privileges it grants to the account. Deleting a role stops that role from granting privileges.

## Review service accounts [review-service-accounts-kibana]

The **Service accounts** table shows each account's name, description, roles, creator, and number of bound workloads. A **Disabled** badge identifies accounts that can't authenticate. Use the **Role** filter to find accounts assigned to specific roles.

When an account has bound workloads, click **View** in the **Workloads** column to review them.

Accounts created directly through the [{{es}} API]({{es-apis}}operation/operation-security-put-user-managed-service-account) also appear in the table.

:::{important}
Don't create service accounts directly through the {{es}} API if you plan to use them with {{kib}} applications such as Workflows. Create them in {{kib}} so it can generate and securely store the credential needed to run workloads as the account.
:::

You can't edit an account on this page. To change its roles or description, [update the account through the {{es}} API](#disable-service-account), or delete the account and create another one.

## Update or deactivate a service account [disable-service-account]

Use the [create or replace user-managed service account API]({{es-apis}}operation/operation-security-put-user-managed-service-account) to update an account's roles or description, or to deactivate it by setting `enabled` to `false`. These actions aren't available in the {{kib}} UI.

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

Workloads bound to an account that has `enabled: false` fail the next time they run. They don't fall back to the user who starts or edits the workload.

## Delete a service account [delete-service-account-kibana]

Deleting a service account is permanent. If you only need to temporarily prevent the account from authenticating, [deactivate it](#disable-service-account) instead.

To delete a service account:

1. On the **Service accounts** page, find the account.
2. From the **Actions** column, click **Delete**.
3. Review the confirmation:
    - If no workloads are bound, click **Delete account**.
    - If workloads are bound, review the list. To delete the account without removing the bindings, click **Force delete account**.

If you force delete an account, its bound workloads fail on their next run. To restore access, assign each affected workload a valid service account. This reassignment is required even if you recreate the deleted account with the same name. For Workflows, [assign a service account to each affected workflow](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md#assign-workflow-service-account).

Deleting an account through {{kib}} attempts to remove every service token, including the credential it stores for workloads and tokens created outside {{kib}}. It also attempts to invalidate any short-lived access tokens used to run workloads as the account. If any credential cleanup fails, {{kib}} completes the deletion and reports a warning.

A service token left behind after deletion can't authenticate, but it prevents you from creating another account with the same name until you delete the token. If you delete an account directly through the {{es}} API, short-lived access tokens already issued to the account remain valid until they expire, 20 minutes after issuance by default.

:::{important}
API keys owned by the account aren't invalidated when you delete the account. {{rules-ui}} and tasks that obtained an API key while authenticated as the account can continue to run with that key. To revoke this access, [invalidate the API keys]({{es-apis}}operation/operation-security-invalidate-api-key) explicitly.
:::

## Next steps [manage-service-accounts-next-steps]

Use these guides to work with service accounts and learn more about their credentials:

- [Run a workflow as a service account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md).
- [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).
- Learn more about [service account types and credentials](service-accounts.md).
