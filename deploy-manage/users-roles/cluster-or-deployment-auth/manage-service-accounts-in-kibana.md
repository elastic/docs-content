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

Create user-managed service accounts and assign roles to control access to {{es}} and {{kib}} APIs. {{kib}} creates each account in {{es}} and securely stores its credential.

## Before you begin [manage-service-accounts-before-you-begin]

- You need the `manage_security` cluster privilege. Without it, the **Service accounts** page isn't available. The `manage_service_account` privilege applies only to built-in accounts in the `elastic` namespace.
- On self-managed deployments, set [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-encryptedsavedobjects-encryptionkey) in `kibana.yml`. {{kib}} uses this key to encrypt the stored credential.
- Create the roles that you want to assign. Each account requires at least one role.

% Follow-up in elastic/kibana: document xpack.security.serviceAccounts.enabled and xpack.security.serviceAccounts.requestLifetime (default 10m), then add links to the settings reference.

Service accounts are enabled by default on {{ech}}, {{ece}}, {{eck}}, and self-managed deployments. Setting `xpack.security.serviceAccounts.enabled` to `false` turns off the **Service accounts** page and workload integration.

## Create a service account [create-service-account-kibana]

1. Find **Service accounts** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). In the **Classic** solution view, select **Stack Management** → **Security** → **Service accounts**.
2. Click **Create account**.
3. In the **Name** field, enter a unique name of up to 128 characters. The name must start with a letter or number and can contain letters, numbers, hyphens, and underscores.
4. Optional: In the **Description** field, describe what the account is used for.
5. Under **Set privileges**, select one or more predefined or custom roles that grant the privileges the account needs. To create a role, click **Create new role**.
6. Review the privileges granted by the selected roles, and click **Create account**.

The new account appears with the principal `kibana/<name>`. {{kib}} creates and stores its credential. No token is displayed, and you don't need to copy a secret.

{{es}} resolves the assigned roles by name whenever the account authenticates. Editing a role changes the privileges it grants to the account. Deleting a role stops that role from granting privileges.

## Review service accounts [review-service-accounts-kibana]

The **Service accounts** table shows each account's name, description, roles, creator, and number of bound workloads. A **Disabled** badge identifies accounts that can't authenticate. Use the **Role** filter to find accounts assigned to specific roles.

When an account has bound workloads, click **View** in the **Workloads** column to review them.

% TBD: Recheck the creation flyout and role selector after https://github.com/elastic/kibana/pull/296889 merges. The Workloads column and View action are verified in main after #297492.

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

Setting `enabled: false` prevents the account from authenticating without deleting it. To reactivate the account, send the complete definition again with `enabled` set to `true`.

Workloads bound to an account that has `enabled: false` fail the next time they run. They don't fall back to the user who starts or edits the workload.

## Delete a service account [delete-service-account-kibana]

Delete an account when you no longer need its identity:

1. On the **Service accounts** page, find the account.
2. From the **Actions** column, click **Delete**.
3. Review the confirmation:
    - If no workloads are bound, click **Delete account**.
    - If workloads are bound, review the list. To delete the account without removing the bindings, click **Force delete account**.

Deleting an account removes all its service tokens, including tokens created outside {{kib}}, and the credential stored by {{kib}}. It also invalidates access tokens issued to the account. If credential cleanup fails, {{kib}} reports a warning. A service token left behind can't authenticate while the account is absent.

Forced deletion leaves workload bindings in place. Those workloads fail on their next run. Creating another account with the same name doesn't restore an old binding. Bind each workload to the replacement account.

:::{important}
API keys owned by the account aren't invalidated when you delete the account. Rules and tasks that obtained an API key while authenticated as the account can continue to run with that key. To revoke this access, [invalidate the API keys]({{es-apis}}operation/operation-security-invalidate-api-key) explicitly.
:::

## Next steps [manage-service-accounts-next-steps]

- [Run a workflow as a service account](/explore-analyze/workflows/authoring-techniques/run-workflow-as-service-account.md).
- [Authenticate to the {{kib}} API with a service account](authenticate-kibana-api-with-service-account.md).
- Learn more about [service account types and credentials](service-accounts.md).
