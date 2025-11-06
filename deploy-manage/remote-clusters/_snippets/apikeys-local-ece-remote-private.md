<!--
This snippet is in use in the following locations:
- ece-remote-cluster-self-managed.md
- ece-remote-cluster-other-ece.md

It requires remote_type substitution to be defined
-->
1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Access the **Security** page of the deployment.
4. Select **Remote Connections > Add trusted environment** and choose **{{remote_type}}**. Then click **Next**.
5. Select **API keys** as authentication mechanism and click **Next**.
6. When asked whether the Certificate Authority (CA) of the remote environment’s proxy or load-balancing infrastructure is public, select **No, it is private**.
7. Add the API key:

    1. Fill both fields.

        * For the **Remote cluster name**, enter the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.
    3. Repeat these steps for each API key you want to add. For example, if you want to use several clusters of the remote environment for CCR or CCS.

8. Add the CA certificate of the remote environment.
9. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment's **Security** page.
10. Select **Create trust** to complete the configuration.
11. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment's main page, locate the **Actions** menu, and select **Restart {{es}}**.

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::

If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](/deploy-manage/remote-clusters/ece-edit-remove-trusted-environment.md#edit-remove-trusted-environment-api-key).

