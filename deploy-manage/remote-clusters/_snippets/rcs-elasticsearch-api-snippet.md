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
To configure a deployment as a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* `Remote cluster alias`: When using API key authentication, the cluster alias must match the one you configured when adding the API key in the Cloud UI as **Remote cluster name**.
* `mode`: `proxy`
* `proxy_address`: This value can be found on the **Security** page of the {{remote_type}} you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters** section. 
   
   Using the API, this value can be obtained from the {{es}} resource info, concatenating the field `metadata.endpoint` and port `9400` using a semicolon.

  ::::{note}
  If you’re using API keys as security model, change the port to `9443`.
  ::::

* `server_name`: This value can be found on the **Security** page of the {{remote_type}} you want to use as a remote. Copy the **Server name** from the **Remote cluster parameters** section. 
   
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
          "proxy_address": "a542184a7a7d45b88b83f95392f450ab.192.0.2.10.ip.es.io:9400",
          "server_name": "a542184a7a7d45b88b83f95392f450ab.192.0.2.10.ip.es.io"
        }
      }
    }
  }
}
```

For a full list of available client connection settings in proxy mode, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-proxy-settings).
