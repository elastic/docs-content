<!--
This snippet is in use in the following locations:
- ece-remote-cluster-self-managed.md
- ece-remote-cluster-same-ece.md
- ece-remote-cluster-other-ece.md
- ece-remote-cluster-ece-ess.md
- ece-enable-ccs-for-eck.md
-->
1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From the navigation menu, select **Security**.
4. Locate **Remote Connections > Trust management > Connections using API keys** and select **Add API key**.

    1. Fill both fields.

        * For the **Remote cluster name**, enter the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key.

5. Restart the local deployment to reload the new setting. To do that, go to the deployment's main page, locate the **Actions** menu, and select **Restart {{es}}**.

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::

If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](/deploy-manage/remote-clusters/ece-edit-remove-trusted-environment.md#edit-remove-trusted-environment-api-key).
