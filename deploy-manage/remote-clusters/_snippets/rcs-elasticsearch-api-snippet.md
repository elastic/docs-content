<!--
This snippet is in use in the following locations:
- ec-remote-cluster-same-ess.md
- ec-remote-cluster-other-ess.md
- ec-remote-cluster-ece.md
- ece-remote-cluster-same-ece.md
- ece-remote-cluster-other-ece.md
- ece-remote-cluster-ece-ess.md

It requires remote_type substitution to be defined
-->
To add a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* **Remote cluster alias**: When using API key authentication, the cluster alias must match the one you configured when [adding the API key](#configure-local-cluster) in the Cloud UI as **Remote cluster name**.
* **mode**: `proxy`
* **proxy_address**: This value can be found on the **Security** page of the {{remote_type}} deployment you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters** section.
   
   Using the API, this value can be obtained from the {{es}} resource info, concatenating the field `metadata.endpoint` and port `9400` using a semicolon.

  ::::{note}
  If you’re using API keys as security model, change the port to `9443`.
  ::::

* **server_name**: This value can be found on the **Security** page of the {{remote_type}} deployment you want to use as a remote. Copy the **Server name** from the **Remote cluster parameters** section.
   
   Using the API, this can be obtained from the {{es}} resource info field `metadata.endpoint`.

This example shows the API call to add or update a remote cluster. The alias `alias-for-my-remote-cluster` must match the remote cluster name used when adding the API key to the deployment:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "alias-for-my-remote-cluster": { // Remote cluster alias
          "mode":"proxy",
          "proxy_address": "<REMOTE_CLUSTER_ADDRESS>:9443",
          "server_name": "<REMOTE_CLUSTER_SERVER_NAME>"
        }
      }
    }
  }
}
```

For a full list of available client connection settings in proxy mode, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-proxy-settings).
