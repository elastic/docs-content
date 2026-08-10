---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-cert.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Add remote clusters using TLS certificate authentication [remote-clusters-cert]

::::{admonition} Deprecated in 9.0.0.
:class: warning

Certificate based authentication is deprecated. Configure [API key authentication](remote-clusters-api-key.md) instead or follow a guide on how to [migrate remote clusters from certificate to API key authentication](remote-clusters-migrate.md).
::::


To add a remote cluster using TLS certificate authentication:

1. [Review the prerequisites](#remote-clusters-prerequisites-cert)
2. [Establish trust with a remote cluster](#remote-clusters-security-cert)
3. [Connect to a remote cluster](#remote-clusters-connect-cert)
4. [Configure roles and users for remote clusters](#remote-clusters-privileges-cert)

If you run into any issues, refer to [Troubleshooting](/troubleshoot/elasticsearch/remote-clusters.md).

## Prerequisites [remote-clusters-prerequisites-cert]

1. The {{es}} security features need to be enabled on both clusters, on every node. Security is enabled by default. If it’s disabled, set `xpack.security.enabled` to `true` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md). Refer to [General security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings).
2. The local and remote clusters versions must be compatible.

   :::{include} _snippets/remote-cluster-certificate-compatibility.md
   :::

## Establish trust with a remote cluster [remote-clusters-security-cert]

To use {{ccr}} or {{ccs}} safely with remote clusters, enable security on all connected clusters and configure Transport Layer Security (TLS) on every node. Configuring TLS security on the transport interface is minimally required for remote clusters. For additional security, configure TLS on the [HTTP interface](../security/secure-cluster-communications.md) as well.

All connected clusters must trust one another and be mutually authenticated with TLS on the transport interface. This means that the local cluster trusts the certificate authority (CA) of the remote cluster, and the remote cluster trusts the CA of the local cluster. When establishing a connection, all nodes will verify certificates from nodes on the other side. This mutual trust is required to securely connect a remote cluster, because all connected nodes effectively form a single security domain.

User authentication is performed on the local cluster and the user and user’s roles names are passed to the remote clusters. A remote cluster checks the user’s role names against its local role definitions to determine which indices the user is allowed to access.

Before using {{ccr}} or {{ccs}} with secured {{es}} clusters, complete the following configuration task:

1. Configure Transport Layer Security (TLS) on every node to encrypt internode traffic and authenticate nodes in the local cluster with nodes in all remote clusters. Refer to [set up basic security for the {{stack}}](../security/secure-cluster-communications.md) for the required steps to configure security.

    ::::{note}
    This procedure uses the same CA to generate certificates for all nodes. Alternatively, you can add the certificates from the local cluster as a trusted CA in each remote cluster. You must also add the certificates from remote clusters as a trusted CA on the local cluster. Using the same CA to generate certificates for all nodes simplifies this task.
    ::::



## Connect to a remote cluster [remote-clusters-connect-cert]

::::{note}
You must have the `manage` cluster privilege to connect remote clusters.
::::

The local cluster uses the [transport interface](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) to establish communication with remote clusters. The coordinating nodes in the local cluster establish [long-lived](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections) TCP connections with specific nodes in the remote cluster. {{es}} requires these connections to remain open, even if the connections are idle for an extended period.

### Using {{kib}}

To add a remote cluster from Stack Management in {{kib}}:

1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Add a remote cluster**.
3. Select **Certificates** as the connection type.
4. Enter a name (*cluster alias*) for the remote cluster.
5. Specify the {{es}} endpoint URL, or the IP address or host name of the remote cluster followed by the transport port (defaults to `9300`). For example, `cluster.es.eastus2.staging.azure.foundit.no:9300` or `192.0.2.1:9300`.

    Starting with {{kib}} 9.2, you can also specify IPv6 addresses.

### Using the {{es}} API

Alternatively, use the [cluster update settings API]({{es-apis}}operation/operation-cluster-put-settings) to add a remote cluster. You can also use this API to dynamically configure remote clusters for *every* node in the local cluster. To configure remote clusters on individual nodes in the local cluster, define static settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) for each node.

The following request adds a remote cluster with an alias of `cluster_one`. This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish between local and remote indices.

```console
PUT /_cluster/settings
{
  "persistent" : {
    "cluster" : {
      "remote" : {
        "cluster_one" : {    <1>
          "seeds" : [
            "<MY_REMOTE_CLUSTER_ADDRESS>:9300" <2>
          ]
        }
      }
    }
  }
}
```

1. The cluster alias of this remote cluster is `cluster_one`.
2. Specifies the hostname and transport port of at least a seed node in the remote cluster.


You can use the [remote cluster info API]({{es-apis}}operation/operation-cluster-remote-info) to verify that the local cluster is successfully connected to the remote cluster:

```console
GET /_remote/info
```

The API response indicates that the local cluster is connected to the remote cluster with the cluster alias `cluster_one`:

```console-result
{
  "cluster_one" : {
    "seeds" : [
      "<MY_REMOTE_CLUSTER_ADDRESS>:9300"
    ],
    "connected" : true,
    "num_nodes_connected" : 1,  <1>
    "max_connections_per_cluster" : 3,
    "initial_connect_timeout" : "30s",
    "skip_unavailable" : true, <2>
    "mode" : "sniff"
  }
}
```

1. The number of nodes in the remote cluster the local cluster is connected to.
2. Indicates whether to skip the remote cluster if searched through {{ccs}} but no nodes are available.


### Dynamically configure remote clusters [_dynamically_configure_remote_clusters_2]

Use the [cluster update settings API]({{es-apis}}operation/operation-cluster-put-settings) to dynamically configure remote settings on every node in the cluster. The following request adds three remote clusters: `cluster_one`, `cluster_two`, and `cluster_three`.

The `seeds` parameter specifies the hostname and [transport port](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) (default `9300`) of a seed node in the remote cluster.

The `mode` parameter determines the configured connection mode, which defaults to [`sniff`](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-mode). Because `cluster_one` doesn’t specify a `mode`, it uses the default. Both `cluster_two` and `cluster_three` explicitly use different modes.

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "cluster_one": {
          "seeds": [
            "<MY_REMOTE_CLUSTER_ADDRESS>:9300"
          ]
        },
        "cluster_two": {
          "mode": "sniff",
          "seeds": [
            "<MY_SECOND_REMOTE_CLUSTER_ADDRESS>:9300"
          ],
          "transport.compress": true,
          "skip_unavailable": true
        },
        "cluster_three": {
          "mode": "proxy",
          "proxy_address": "<MY_THIRD_REMOTE_CLUSTER_ADDRESS>:9300"
        }
      }
    }
  }
}
```

You can dynamically update settings for a remote cluster after the initial configuration. The following request updates the compression settings for `cluster_two`, and the compression and ping schedule settings for `cluster_three`.

::::{note}
When the compression or ping schedule settings change, all existing node connections must close and re-open, which can cause in-flight requests to fail.
::::


```console
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "cluster_two": {
          "transport.compress": false
        },
        "cluster_three": {
          "transport.compress": true,
          "transport.ping_schedule": "60s"
        }
      }
    }
  }
}
```

You can delete a remote cluster from the cluster settings by passing `null` values for each remote cluster setting. The following request removes `cluster_two` from the cluster settings, leaving `cluster_one` and `cluster_three` intact:

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "cluster_two": {
          "mode": null,
          "seeds": null,
          "skip_unavailable": null,
          "transport.compress": null
        }
      }
    }
  }
}
```


### Statically configure remote clusters [_statically_configure_remote_clusters_2]

If you specify settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md), only the nodes with those settings can connect to the remote cluster and serve remote cluster requests.

::::{note}
Remote cluster settings that are specified using the [cluster update settings API]({{es-apis}}operation/operation-cluster-put-settings) take precedence over settings that you specify in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) for individual nodes.
::::


In the following example, `cluster_one`, `cluster_two`, and `cluster_three` are arbitrary cluster aliases representing the connection to each cluster. These names are subsequently used to distinguish between local and remote indices.

```yaml
cluster:
    remote:
        cluster_one:
            seeds: <MY_REMOTE_CLUSTER_ADDRESS>:9300
        cluster_two:
            mode: sniff
            seeds: <MY_SECOND_REMOTE_CLUSTER_ADDRESS>:9300
            transport.compress: true      <1>
            skip_unavailable: true        <2>
        cluster_three:
            mode: proxy
            proxy_address: <MY_THIRD_REMOTE_CLUSTER_ADDRESS>:9300 <3>
```

1. Compression is explicitly enabled for requests to `cluster_two`.
2. Disconnected remote clusters are optional for `cluster_two`.
3. The address for the proxy endpoint used to connect to `cluster_three`.




## Configure roles and users for remote clusters [remote-clusters-privileges-cert]

After [connecting remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md), configure privileges so users can use {{ccr}} and {{ccs}}:

* [Configure privileges for {{ccr}}](/deploy-manage/tools/cross-cluster-replication/_configure_privileges_for_cross_cluster_replication_2.md#configure-privileges-for-ccr-cert)
* [Configure privileges for {{ccs}}](/explore-analyze/cross-cluster-search.md#configure-privileges-for-ccs-cert)
