<!--
This snippet is in use in the following locations:
- ec-remote-cluster-same-ess.md
- ec-remote-cluster-other-ess.md
- ec-remote-cluster-ece.md
- ece-remote-cluster-same-ece.md
- ece-remote-cluster-other-ece.md
- ece-remote-cluster-ess.md

It requires remote_type substitution to be defined
-->
1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Add a remote cluster**.
2. In **Select connection type**, choose the authentication mechanism you prepared earlier (**API keys** or **Certificates**), and then click **Next**.
3. In **Add connection information**, fill in the following fields:

    * **Remote cluster name**: This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish local and remote indices.

      When using API key authentication, this alias must match the **Remote cluster name** you configured when adding the API key in the Cloud UI.

    * **Remote address**: This value can be found on the **Security** page of the {{remote_type}} you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters** section.

      ::::{note}
      If you’re using API keys as security model, change the port to `9443`.
      ::::

    * **Configure advanced options** (optional): Expand this section if you need to customize additional settings.
      * **TLS server name**: Specify a value if the certificate presented by the remote cluster is signed for a different name than the remote address.

        This value can be found on the **Security** page of the {{remote_type}} you want to use as a remote. Copy the **Server name** from the **Remote cluster parameters** section.

      * **Socket connections**: Define the number of connections to open with the remote cluster.

    For a full list of available client connection settings, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-proxy-settings).

4. Click **Next**.
5. In **Confirm setup**, click **Add remote cluster** (you have already established trust in a previous step).
