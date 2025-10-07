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

* `mode`: `proxy`
* `proxy_address`: This value can be found on the **Security** page of the {{remote_type}} you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters** section. Also, using the API, this value can be obtained from the {{es}} resource info, concatenating the field `metadata.endpoint` and port `9400` using a semicolon.

  ::::{note}
  If you’re using API keys as security model, change the port into `9443`.
  ::::

* `server_name`: This value can be found on the **Security** page of the {{remote_type}} you want to use as a remote. Copy the **Server name** from the **Remote cluster parameters** section. Also, using the API, this can be obtained from the {{es}} resource info field `metadata.endpoint`.

This is an example of the API call to `_cluster/settings`:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "alias-for-my-remote-cluster": {
          "mode":"proxy",
          "proxy_address": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io:9400",
          "server_name": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io"
        }
      }
    }
  }
}
```

::::{note}
When using API key authentication, the cluster alias must match the one you configured when adding the API key in the Cloud UI.
::::
