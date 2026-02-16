This section describes the steps to change the API key used for an existing remote connection. For example, if the previous key expired and you need to rotate it with a new one.

::::{note}
If you need to update the permissions granted by a cross-cluster API key for a remote connection, you only need to update the privileges granted by the API key directly in {{kib}}.
::::


1. On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](/deploy-manage/api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key with the appropriate permissions. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
2. Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next steps.
3. From the navigation menu of your local deployment, select **Security** and locate the **Remote connections** section.
4. Locate the API key currently used for connecting to the remote cluster, copy its current alias, and delete it.
5. Add the new API key by selecting **Add API key**.

    * For the **Remote cluster name**, enter the same alias that was used for the previous key.

      ::::{note}
      If you use a different alias, you also need to re-create the remote cluster in {{kib}} with a **Remote cluster name** that matches the new alias.
      ::::

    * For the **Cross-cluster API key**, paste the encoded cross-cluster API key, then click **Add** to save the API key to the keystore.

6. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment's main page (named after your deployment's name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

   ::::{note}
   If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
   ::::

