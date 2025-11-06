1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the home page, find your hosted deployment and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Hosted deployments** page to view all of your deployments.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From the navigation menu, select **Security**.
4. Locate **Remote Connections > Trust management > Connections using API keys** and select **Add API key**.

    1. Fill both fields.

        * For the **Remote cluster name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key.

5. Restart the local deployment to reload the new setting. To do that, go to the deployment's main page (named after your deployment's name), locate the **Actions** menu, and select **Restart {{es}}**.

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::

If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](/deploy-manage/remote-clusters/ec-edit-remove-trusted-environment.md#ec-edit-remove-trusted-environment-api-key).
