---
navigation_title: Manage trusted environments
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-edit-remove-trusted-environment.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---

# Manage trusted environments for remote connections in {{ece}} [ece-edit-remove-trusted-environment]

From a deployment’s **Security** page, you can manage trusted environments that were created previously. This can happen when:

* You no longer need a trusted environment and want to remove it.
* You want to refresh the certificate, or add or remove trusted deployments of an existing trusted environment relying on certificates as a security model.
* You want to remove or update the access level granted by a cross-cluster API key.


## Remove a certificate-based trusted environment [ece_remove_a_trusted_environment]

By removing a trusted environment, this deployment will no longer be able to establish remote connections using certificate trust to clusters of that environment. The remote environment will also no longer be able to connect to this deployment using certificate trust.

::::{note}
With this method, you can only remove trusted environments relying exclusively on certificates. To remove remote connections that use API keys for authentication, refer to [Update the access level of a remote cluster connection relying on a cross-cluster API key](#ece-edit-remove-trusted-environment-api-key).
::::


1. Go to the deployment’s **Security** page.
2. In the list of trusted environments, locate the one you want to remove.
3. Remove it using the corresponding `delete` icon.

   :::{image} /deploy-manage/images/cloud-enterprise-delete-trust-environment.png
   :alt: button for deleting a trusted environment
   :::

1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the list of existing remote clusters, delete the ones corresponding to the trusted environment you removed earlier.


## Update a certificate-based trusted environment [ece_update_a_certificate_based_trusted_environment]

1. Go to the deployment’s **Security** page.
2. In the list of trusted environments, locate the one you want to edit.
3. Open its details by selecting the `Edit` icon.

   :::{image} /deploy-manage/images/cloud-enterprise-edit-trust-environment.png
   :alt: button for editing a trusted environment
   :::

4. Edit the trust configuration for that environment:

   * From the **Trust level** tab, you can add or remove trusted deployments.
   * From the **Environment settings** tab, you can manage the certificates and the label of the environment.

5. Save your changes.


## Change a cross-cluster API key used for a remote connection [ece-edit-remove-trusted-environment-api-key]

This section describes the steps to change the API key used for an existing remote connection. For example, if the previous key expired and you need to rotate it with a new one.

::::{note}
If you need to update the permissions granted by a cross-cluster API key for a remote connection, you only need to update the privileges granted by the API key directly in {{kib}}.
::::


1. On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key with the appropriate permissions. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
2. Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next steps.
3. From the navigation menu, select **Security** and locate the **Remote connections** section.
4. Locate the API key currently used for connecting to the remote cluster, copy its current alias, and delete it.
5. Add the new API key by selecting **Add API key**.

    * For the **Remote cluster name**, enter the same alias that was used for the previous key.

      ::::{note}
      If you use a different alias, you also need to re-create the remote cluster in {{kib}} with a **Name** that matches the new alias.
      ::::

    * For the **Cross-cluster API key**, paste the encoded cross-cluster API key, then click **Add** to save the API key to the keystore.

6. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

   ::::{note}
   If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
   ::::
