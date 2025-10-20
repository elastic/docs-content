<!--
This snippet is in use in the following locations:
- ece-remote-cluster-self-managed.md
- ec-remote-cluster-self-managed.md
-->
To configure a self-managed cluster as a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* `Remote cluster alias`: When using API key authentication, the cluster alias must match the one you configured when adding the API key in the Cloud UI as **Remote cluster name**.
* `mode`: `proxy`
* `proxy_address`: Enter the endpoint of the remote self-managed cluster, including the hostname, FQDN, or IP address, and the port. Both IPv4 and IPv6 addresses are supported.

  Make sure you use the correct port for your authentication method:
  * **API keys**: Use the port configured in the remote cluster interface of the remote cluster (defaults to `9443`).  
  * **TLS Certificates**: Use the {{es}} transport port (defaults to `9300`).

  When using an IPv6 address, enclose it in square brackets followed by the port number. For example: `[2001:db8::1]:9443`.

* `server_name`: Specify a value if the certificate presented by the remote cluster is signed for a different name than the proxy_address.

This is an example of the API call to add or update a remote cluster:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "alias-for-my-remote-cluster": { // Align the alias with the remote cluster name used when adding the API key.
          "mode":"proxy",
          "proxy_address": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io:9400",
          "server_name": "a542184a7a7d45b88b83f95392f450ab.192.168.44.10.ip.es.io"
        }
      }
    }
  }
}
```

For a full list of available client connection settings in proxy mode, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-proxy-settings).
