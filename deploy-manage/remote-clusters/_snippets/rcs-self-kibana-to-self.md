<!--
This snippet is in use in the following locations:
- eck-remote-clusters-to-other-eck.md
- self-remote-cluster-eck.md
-->
% ECK and self-managed clusters present a different Kibana UI when adding remote clusters than ECE/ECH deployments
To add a remote cluster in {{kib}}:

1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Add a remote cluster**.
2. In **Select connection type**, choose the authentication mechanism you prepared earlier (**API keys** or **Certificates**), and click **Next**.
4. Set the **Remote cluster name**: This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish local and remote indices.

    When using API key authentication, this alias must match the **Remote cluster name** you configured when [adding the API key](#configure-local-cluster).

5. In **Connection mode**, select **Manually enter proxy address and server name** to enable the proxy mode and fill in the following fields:

    * **Proxy address**: Enter the endpoint of the remote cluster, including the hostname, FQDN, or IP address, and the port:
        
      Make sure you use the correct port for your authentication method:
      * **API keys**: Use the port configured in the remote cluster interface of the remote cluster (defaults to `9443`).  
      * **TLS certificates**: Use the {{es}} transport port (defaults to `9300`).

      Starting with {{kib}} 9.2, this field also supports IPv6 addresses. When using an IPv6 address, enclose it in square brackets followed by the port number. For example: `[2001:db8::1]:9443`.

    * **Server name (optional)**: Specify a value if the TLS certificate presented by the remote cluster is signed for a different name than the remote address.

5. Click **Next**.
6. In **Confirm setup**, click **Add remote cluster** (you have already established trust in a previous step).
