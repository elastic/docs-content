---
navigation_title: ECH and ECE
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-password-reset-elastic.html
  - https://www.elastic.co/guide/en/cloud/current/ec-password-reset.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-password-reset.html
applies_to:
  deployment:
    ece:
    ess:
products:
  - id: cloud-enterprise
  - id: cloud-hosted
---

# Reset the `elastic` user password in {{ech}} and {{ece}} [ec-password-reset]

You might need to reset the password for the `elastic` superuser if you can't authenticate with the `elastic` user ID and are effectively locked out from an {{es}} cluster or {{kib}}.

::::{note}
Elastic does not manage the `elastic` user and does not have access to the account or its credentials. If you lose the password, you have to reset it.
::::

::::{note}
Resetting the `elastic` user password does not interfere with Marketplace integrations.
::::

::::{note}
The `elastic` user should be not be used unless you have no other way to access your deployment. [Create API keys for ingesting data](beats://reference/filebeat/beats-api-keys.md), and create user accounts with [appropriate roles for user access](../../../deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md).
::::

To reset the password:

:::{include} /deploy-manage/_snippets/find-manage-deployment-ech-and-ece.md
:::

3. Under the deployment's name in the navigation menu, select **Security**.
4. Select **Reset password**.
5. Copy down the auto-generated a password for the `elastic` user.

The password is not accessible after you close the window, so if you lose it, you need to reset the password again.

