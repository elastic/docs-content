---
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-cert.html
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

1. The {{es}} security features need to be enabled on both clusters, on every node. Security is enabled by default. If it’s disabled, set `xpack.security.enabled` to `true` in `elasticsearch.yml`. Refer to [General security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings).
2. The local and remote clusters versions must be compatible.

   :::{include} _snippets/remote-cluster-certificate-compatibility.md
   :::

## Establish trust with a remote cluster [remote-clusters-security-cert]

To use {{ccr}} or {{ccs}} safely with remote clusters, enable security on all connected clusters and configure Transport Layer Security (TLS) on every node. Configuring TLS security on the transport interface is minimally required for remote clusters. For additional security, configure TLS on the [HTTP interface](../security/secure-http-communications.md) as well.

All connected clusters must trust one another and be mutually authenticated with TLS on the transport interface. This means that the local cluster trusts the certificate  authority (CA) of the remote cluster, and the remote cluster trusts the CA of the local cluster. When establishing a connection, all nodes will verify certificates from nodes on the other side. This mutual trust is required to securely connect a remote cluster, because all connected nodes effectively form a single security domain.

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

To add a remote cluster from Stack Management in {{kib}}:

1. Select **Remote Clusters** from the side navigation.
2. Enter a name (*cluster alias*) for the remote cluster.
3. Specify the {{es}} endpoint URL, or the IP address or host name of the remote cluster followed by the transport port (defaults to `9300`). For example, `cluster.es.eastus2.staging.azure.foundit.no:9300` or `192.168.1.1:9300`.

Alternatively, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to add a remote cluster. You can also use this API to dynamically configure remote clusters for *every* node in the local cluster. To configure remote clusters on individual nodes in the local cluster, define static settings in `elasticsearch.yml` for each node.

The following request adds a remote cluster with an alias of `cluster_one`. This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish between local and remote indices.

```console
PUT /_cluster/settings
{
  "persistent" : {
    "cluster" : {
      "remote" : {
        "cluster_one" : {    <1>
          "seeds" : [
            "127.0.0.1:9300" <2>
          ]
        }
      }
    }
  }
}
```

1. The cluster alias of this remote cluster is `cluster_one`.
2. Specifies the hostname and transport port of a seed node in the remote cluster.
%  TEST[setup:host]
%  TEST[s/127.0.0.1:{{remote-interface-default-port}}/${transport_host}/]

You can use the [remote cluster info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) to verify that the local cluster is successfully connected to the remote cluster:

```console
GET /_remote/info
```
%  TEST[continued]

The API response indicates that the local cluster is connected to the remote cluster with the cluster alias `cluster_one`:

```console-result
{
  "cluster_one" : {
    "seeds" : [
      "127.0.0.1:9300"
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
%  TESTRESPONSE[s/127.0.0.1:{{remote-interface-default-port}}/$body.cluster_one.seeds.0/]
%  TESTRESPONSE[s/ifeval::(.|\n)*endif::[]//]
%  TEST[s/"connected" : true/"connected" : $body.cluster_one.connected/]
%  TEST[s/"num_nodes_connected" : 1/"num_nodes_connected" : $body.cluster_one.num_nodes_connected/]

### Dynamically configure remote clusters [_dynamically_configure_remote_clusters_2]

Use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to dynamically configure remote settings on every node in the cluster. The following request adds three remote clusters: `cluster_one`, `cluster_two`, and `cluster_three`.

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
            "127.0.0.1:9300"
          ]
        },
        "cluster_two": {
          "mode": "sniff",
          "seeds": [
            "127.0.0.1:9301"
          ],
          "transport.compress": true,
          "skip_unavailable": true
        },
        "cluster_three": {
          "mode": "proxy",
          "proxy_address": "127.0.0.1:9302"
        }
      }
    }
  }
}
```
%  TEST[setup:host]
%  TEST[s/127.0.0.1:{{remote-interface-default-port}}/${transport_host}/]
%  TEST[s/{{remote-interface-default-port-plus1}}/9301/]
%  TEST[s/{{remote-interface-default-port-plus2}}/9302/]

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
%  TEST[continued]

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
%  TEST[continued]


### Statically configure remote clusters [_statically_configure_remote_clusters_2]

If you specify settings in `elasticsearch.yml`, only the nodes with those settings can connect to the remote cluster and serve remote cluster requests.

::::{note}
Remote cluster settings that are specified using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) take precedence over settings that you specify in `elasticsearch.yml` for individual nodes.
::::


In the following example, `cluster_one`, `cluster_two`, and `cluster_three` are arbitrary cluster aliases representing the connection to each cluster. These names are subsequently used to distinguish between local and remote indices.

```yaml
cluster:
    remote:
        cluster_one:
            seeds: 127.0.0.1:9300
        cluster_two:
            mode: sniff
            seeds: 127.0.0.1:9301
            transport.compress: true      <1>
            skip_unavailable: true        <2>
        cluster_three:
            mode: proxy
            proxy_address: 127.0.0.1:9302 <3>
```

1. Compression is explicitly enabled for requests to `cluster_two`.
2. Disconnected remote clusters are optional for `cluster_two`.
3. The address for the proxy endpoint used to connect to `cluster_three`.




## Configure roles and users for remote clusters [remote-clusters-privileges-cert]

After [connecting remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md), you create a user role on both the local and remote clusters and assign necessary privileges. These roles are required to use {{ccr}} and {{ccs}}.

::::{important}
You must use the same role names on both the local and remote clusters. For example, the following configuration for {{ccr}} uses the `remote-replication` role name on both the local and remote clusters. However, you can specify different role definitions on each cluster.
::::


You can manage users and roles from Stack Management in {{kib}} by selecting **Security > Roles** from the side navigation. You can also use the [role management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) to add, update, remove, and retrieve roles dynamically. When you use the APIs to manage roles in the `native` realm, the roles are stored in an internal {{es}} index.

The following requests use the [create or update roles API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role). You must have at least the `manage_security` cluster privilege to use this API.

### Configure privileges for {{ccr}} [remote-clusters-privileges-ccr]

The {{ccr}} user requires different cluster and index privileges on the remote cluster and local cluster. Use the following requests to create separate roles on the local and remote clusters, and then create a user with the required roles.


#### Remote cluster [_remote_cluster]

On the remote cluster that contains the leader index, the {{ccr}} role requires the `read_ccr` cluster privilege, and `monitor` and `read` privileges on the leader index.

::::{note}
If requests are authenticated with an [API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key), the API key requires the above privileges on the **local** cluster, instead of the remote.
::::


::::{note}
If requests are issued [on behalf of other users](../users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md), then the authenticating user must have the `run_as` privilege on the remote cluster.
::::


The following request creates a `remote-replication` role on the remote cluster:

```console
POST /_security/role/remote-replication
{
  "cluster": [
    "read_ccr"
  ],
  "indices": [
    {
      "names": [
        "leader-index-name"
      ],
      "privileges": [
        "monitor",
        "read"
      ]
    }
  ]
}
```


#### Local cluster [_local_cluster]

On the local cluster that contains the follower index, the `remote-replication` role requires the `manage_ccr` cluster privilege, and `monitor`, `read`, `write`, and `manage_follow_index` privileges on the follower index.

The following request creates a `remote-replication` role on the local cluster:

```console
POST /_security/role/remote-replication
{
  "cluster": [
    "manage_ccr"
  ],
  "indices": [
    {
      "names": [
        "follower-index-name"
      ],
      "privileges": [
        "monitor",
        "read",
        "write",
        "manage_follow_index"
      ]
    }
  ]
}
```

After creating the `remote-replication` role on each cluster, use the [create or update users API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) to create a user on the local cluster cluster and assign the `remote-replication` role. For example, the following request assigns the `remote-replication` role to a user named `cross-cluster-user`:

```console
POST /_security/user/cross-cluster-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-replication" ]
}
```
%  TEST[continued]

::::{note}
You only need to create this user on the **local** cluster.
::::


You can then [configure {{ccr}}](../tools/cross-cluster-replication/set-up-cross-cluster-replication.md) to replicate your data across datacenters.


### Configure privileges for {{ccs}} [remote-clusters-privileges-ccs]

The {{ccs}} user requires different cluster and index privileges on the remote cluster and local cluster. The following requests create separate roles on the local and remote clusters, and then create a user with the required roles.


#### Remote cluster [_remote_cluster_2]

On the remote cluster, the {{ccs}} role requires the `read` and `read_cross_cluster` privileges for the target indices.

::::{note}
If requests are authenticated with an [API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key), the API key requires the above privileges on the **local** cluster, instead of the remote.
::::


::::{note}
If requests are issued [on behalf of other users](../users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md), then the authenticating user must have the `run_as` privilege on the remote cluster.
::::


The following request creates a `remote-search` role on the remote cluster:

```console
POST /_security/role/remote-search
{
  "indices": [
    {
      "names": [
        "target-indices"
      ],
      "privileges": [
        "read",
        "read_cross_cluster"
      ]
    }
  ]
}
```


#### Local cluster [_local_cluster_2]

On the local cluster, which is the cluster used to initiate cross cluster search, a user only needs the `remote-search` role. The role privileges can be empty.

The following request creates a `remote-search` role on the local cluster:

```console
POST /_security/role/remote-search
{}
```

After creating the `remote-search` role on each cluster, use the [create or update users API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) to create a user on the local cluster and assign the `remote-search` role. For example, the following request assigns the `remote-search` role to a user named `cross-search-user`:

```console
POST /_security/user/cross-search-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-search" ]
}
```
%  TEST[continued]

::::{note}
You only need to create this user on the **local** cluster.
::::


Users with the `remote-search` role can then [search across clusters](../../solutions/search/cross-cluster-search.md).


### Configure privileges for {{ccs}} and {{kib}} [clusters-privileges-ccs-kibana-cert]

When using {{kib}} to search across multiple clusters, a two-step authorization process determines whether or not the user can access data streams and indices on a remote cluster:

* First, the local cluster determines if the user is authorized to access remote clusters. The local cluster is the cluster that {{kib}} is connected to.
* If the user is authorized, the remote cluster then determines if the user has access to the specified data streams and indices.

To grant {{kib}} users access to remote clusters, assign them a local role with read privileges to indices on the remote clusters. You specify data streams and indices in a remote cluster as `<remote_cluster_name>:<target>`.

To grant users read access on the remote data streams and indices, you must create a matching role on the remote clusters that grants the `read_cross_cluster` privilege with access to the appropriate data streams and indices.

For example, you might be actively indexing {{ls}} data on a local cluster and and periodically offload older time-based indices to an archive on your remote cluster. You want to search across both clusters, so you must enable {{kib}} users on both clusters.


#### Local cluster [_local_cluster_3]

On the local cluster, create a `logstash-reader` role that grants `read` and `view_index_metadata` privileges on the local `logstash-*` indices.

::::{note}
If you configure the local cluster as another remote in {{es}}, the `logstash-reader` role on your local cluster also needs to grant the `read_cross_cluster` privilege.
::::


```console
POST /_security/role/logstash-reader
{
  "indices": [
    {
      "names": [
        "logstash-*"
        ],
        "privileges": [
          "read",
          "view_index_metadata"
          ]
    }
  ]
}
```

Assign your {{kib}} users a role that grants [access to {{kib}}](../users-roles/cluster-or-deployment-auth/built-in-roles.md), as well as your `logstash_reader` role. For example, the following request creates the `cross-cluster-kibana` user and assigns the `kibana-access` and `logstash-reader` roles.

```console
PUT /_security/user/cross-cluster-kibana
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [
    "logstash-reader",
    "kibana-access"
    ]
}
```


#### Remote cluster [_remote_cluster_3]

On the remote cluster, create a `logstash-reader` role that grants the `read_cross_cluster` privilege and `read` and `view_index_metadata` privileges for the `logstash-*` indices.

```console
POST /_security/role/logstash-reader
{
  "indices": [
    {
      "names": [
        "logstash-*"
        ],
        "privileges": [
          "read_cross_cluster",
          "read",
          "view_index_metadata"
          ]
    }
  ]
}
```
