# Reset the `elastic` user password [ec-password-reset]

You might need to reset the password for the `elastic` superuser if you cannot authenticate with the `elastic` user ID and are effectively locked out from an Elasticsearch cluster or Kibana.

::::{note}
Elastic does not manage the `elastic` user and does not have access to the account or its credentials. If you lose the password, you have to reset it.
::::


::::{note}
Resetting the `elastic` user password does not interfere with Marketplace integrations.
::::


::::{note}
The `elastic` user should be not be used unless you have no other way to access your deployment. [Create API keys for ingesting data](asciidocalypse://docs/beats/docs/reference/filebeat/beats-api-keys.md), and create user accounts with [appropriate roles for user access](../../../deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md).
::::


To reset the password:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to **Security**.
4. Select **Reset password**.
5. Copy down the auto-generated a password for the `elastic` user:

    ![The password for the elastic user after resetting](../../../images/cloud-reset-password.png "")

6. Close the window.

The password is not accessible after you close the window, so if you lose it, you need to reset the password again.

