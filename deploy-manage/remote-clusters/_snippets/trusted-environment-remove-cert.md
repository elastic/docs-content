By removing a trusted environment, this deployment will no longer be able to establish remote connections using certificate trust to clusters of that environment. The remote environment will also no longer be able to connect to this deployment using certificate trust.

::::{note}
With this method, you can only remove trusted environments relying exclusively on certificates. To remove remote connections that use API keys for authentication, refer to [Change a cross-cluster API key used for a remote connection](#edit-remove-trusted-environment-api-key).
::::

1. Go to the deployment's **Security** page.
2. In the list of trusted environments, locate the one you want to remove.
3. Remove it using the corresponding `delete` icon.

   :::{image} /deploy-manage/images/cloud-delete-trust-environment.png
   :alt: button for deleting a trusted environment
   :::

1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the list of existing remote clusters, delete the ones corresponding to the trusted environment you removed earlier.

