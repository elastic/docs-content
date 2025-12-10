---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-api-key.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Add remote clusters using API key authentication [remote-clusters-api-key]

API key authentication enables a local cluster to authenticate itself with a remote cluster via a [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key). The API key needs to be created by an administrator of the remote cluster. The local cluster is configured to provide this API key on each request to the remote cluster. The remote cluster verifies the API key and grants access, based on the API key’s privileges.

All cross-cluster requests from the local cluster are bound by the API key’s privileges, regardless of local users associated with the requests. For example, if the API key only allows read access to `my-index` on the remote cluster, even a superuser from the local cluster is limited by this constraint. This mechanism enables the remote cluster’s administrator to have full control over who can access what data with cross-cluster search and/or cross-cluster replication. The remote cluster’s administrator can be confident that no access is possible beyond what is explicitly assigned to the API key.

On the local cluster side, not every local user needs to access every piece of data allowed by the API key. An administrator of the local cluster can further configure additional permission constraints on local users so each user only gets access to the necessary remote data. Note it is only possible to further reduce the permissions allowed by the API key for individual local users. It is impossible to increase the permissions to go beyond what is allowed by the API key.

In this model, cross-cluster operations use [a dedicated server port](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote_cluster.port) (remote cluster interface) for communication between clusters, which defaults to port `9443`. A remote cluster must enable this port for local clusters to connect. Configure Transport Layer Security (TLS) for this port to maximize security (as explained in [Establish trust with a remote cluster](#remote-clusters-security-api-key)).

The local cluster must trust the remote cluster on the remote cluster interface. This means that the local cluster trusts the remote cluster’s certificate authority (CA) that signs the server certificate used by the remote cluster interface. When establishing a connection, all nodes from the local cluster that participate in cross-cluster communication verify certificates from nodes on the other side, based on the TLS trust configuration.

To add a remote cluster using API key authentication:

1. [Review the prerequisites](#remote-clusters-prerequisites-api-key)
2. [Establish trust with a remote cluster](#remote-clusters-security-api-key)
3. [Connect to a remote cluster](#remote-clusters-connect-api-key)
4. (Optional) [Configure strong identity verification](#remote-cluster-strong-verification)
5. [Configure roles and users](#remote-clusters-privileges-api-key)


If you run into any issues, refer to [Troubleshooting](/troubleshoot/elasticsearch/remote-clusters.md).

## Prerequisites [remote-clusters-prerequisites-api-key]

* The {{es}} security features need to be enabled on both clusters, on every node. Security is enabled by default. If it’s disabled, set `xpack.security.enabled` to `true` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md). Refer to [General security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings).
* The nodes of the local and remote clusters must be on {{stack}} 8.14 or later.
* The local and remote clusters must have an appropriate license. For more information, refer to [https://www.elastic.co/subscriptions](https://www.elastic.co/subscriptions).


## Establish trust with a remote cluster [remote-clusters-security-api-key]

::::{note}
If a remote cluster is part of an {{ech}} (ECH) deployment, the remote cluster server is enabled by default and it uses a publicly trusted certificate provided by the platform proxies. Therefore, you can skip the following steps in these instructions:

**On the remote (ECH) cluster:** Skip steps 1-4 (enabling the service, generating certificates, configuring SSL settings, and restarting the cluster), and go directly to [create an API key](#create-api-key).

**On the local (self-managed) cluster:** Do not add the `xpack.security.remote_cluster_client.ssl.certificate_authorities` setting to the configuration file because ECH uses publicly trusted certificates that don't require custom CA configuration.
::::


### On the remote cluster [remote-clusters-security-api-key-remote-action]

By default, the remote cluster server interface is not enabled on self-managed clusters. Follow the steps below to enable the interface and create an API key on the remote cluster.

#### Enable and secure the remote cluster server interface

:::{include} _snippets/self_rcs_enable.md
:::

#### Create an API key [create-api-key]

:::{include} _snippets/apikeys-create-key.md
:::


### On the local cluster [remote-clusters-security-api-key-local-actions]

:::{include} _snippets/self_rcs_local_config.md
:::



## Connect to a remote cluster [remote-clusters-connect-api-key]

::::{note}
You must have the `manage` cluster privilege to connect remote clusters.
::::

The local cluster uses the [remote cluster interface](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) to establish communication with remote clusters. The coordinating nodes in the local cluster establish [long-lived](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections) TCP connections with specific nodes in the remote cluster. {{es}} requires these connections to remain open, even if the connections are idle for an extended period.

### Using {{kib}}

To add a remote cluster from Stack Management in {{kib}}:

1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Add a remote cluster**.
3. Select **API keys** as the connection type.
4. Enter a name (*cluster alias*) for the remote cluster.
5. Specify the {{es}} endpoint URL, or the IP address or host name of the remote cluster followed by the remote cluster port (defaults to `9443`). For example, `cluster.es.eastus2.staging.azure.foundit.no:9443` or `192.0.2.1:9443`.

    Starting with {{kib}} 9.2, you can also specify IPv6 addresses.

### Using the {{es}} API

Alternatively, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to add a remote cluster. You can also use this API to dynamically configure remote clusters for *every* node in the local cluster. To configure remote clusters on individual nodes in the local cluster, define static settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) for each node.

::::{note}
If the remote cluster is part of an {{ech}}, {{ece}}, or {{eck}} deployment, configure the connection to use `proxy`. The default `sniff` mode doesn't work in these environments. Refer to the [connection modes](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-proxy-modes) description for more information.
::::

The following request adds a remote cluster with an alias of `cluster_one`. This *cluster alias* is a unique identifier that represents the connection to the remote cluster and is used to distinguish between local and remote indices.

```console
PUT /_cluster/settings
{
  "persistent" : {
    "cluster" : {
      "remote" : {
        "cluster_one" : {    <1>
          "seeds" : [
            "<MY_REMOTE_CLUSTER_ADDRESS>:9443" <2>
          ]
        }
      }
    }
  }
}
```

1. The cluster alias of this remote cluster is `cluster_one`.
2. Specifies the hostname and remote cluster port of a seed node in the remote cluster.


You can use the [remote cluster info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) to verify that the local cluster is successfully connected to the remote cluster:

```console
GET /_remote/info
```

The API response indicates that the local cluster is connected to the remote cluster with the cluster alias `cluster_one`:

```console-result
{
  "cluster_one" : {
    "seeds" : [
      "<MY_REMOTE_CLUSTER_ADDRESS>:9443"
    ],
    "connected" : true,
    "num_nodes_connected" : 1,  <1>
    "max_connections_per_cluster" : 3,
    "initial_connect_timeout" : "30s",
    "skip_unavailable" : true, <2>
    "cluster_credentials": "::es_redacted::", <3>
    "mode" : "sniff"
  }
}
```

1. The number of nodes in the remote cluster the local cluster is connected to.
2. Indicates whether to skip the remote cluster if searched through {{ccs}} but no nodes are available.
3. If present, indicates the remote cluster has connected using API key authentication.


### Dynamically configure remote clusters [_dynamically_configure_remote_clusters]

Use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to dynamically configure remote settings on every node in the cluster. The following request adds three remote clusters: `cluster_one`, `cluster_two`, and `cluster_three`.

The `seeds` parameter specifies the hostname and [remote cluster port](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) (default `9443`) of a seed node in the remote cluster.

The `mode` parameter determines the configured connection mode, which defaults to [`sniff`](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#sniff-mode). Because `cluster_one` doesn’t specify a `mode`, it uses the default. Both `cluster_two` and `cluster_three` explicitly use different modes.

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "cluster_one": {
          "seeds": [
            "<MY_REMOTE_CLUSTER_ADDRESS>:9443"
          ]
        },
        "cluster_two": {
          "mode": "sniff",
          "seeds": [
            "<MY_SECOND_REMOTE_CLUSTER_ADDRESS>:9443"
          ],
          "transport.compress": true,
          "skip_unavailable": true
        },
        "cluster_three": {
          "mode": "proxy",
          "proxy_address": "<MY_THIRD_REMOTE_CLUSTER_ADDRESS>:9443"
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


### Statically configure remote clusters [_statically_configure_remote_clusters]

If you specify settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md), only the nodes with those settings can connect to the remote cluster and serve remote cluster requests.

::::{note}
Remote cluster settings that are specified using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) take precedence over settings that you specify in `elasticsearch.yml` for individual nodes.
::::


In the following example, `cluster_one`, `cluster_two`, and `cluster_three` are arbitrary cluster aliases representing the connection to each cluster. These names are subsequently used to distinguish between local and remote indices.

```yaml
cluster:
    remote:
        cluster_one:
            seeds: <MY_REMOTE_CLUSTER_ADDRESS>:9443
        cluster_two:
            mode: sniff
            seeds: <MY_SECOND_REMOTE_CLUSTER_ADDRESS>:9443
            transport.compress: true      <1>
            skip_unavailable: true        <2>
        cluster_three:
            mode: proxy
            proxy_address: <MY_THIRD_REMOTE_CLUSTER_ADDRESS>:9443 <3>
```

1. Compression is explicitly enabled for requests to `cluster_two`.
2. Disconnected remote clusters are optional for `cluster_two`.
3. The address for the proxy endpoint used to connect to `cluster_three`.


## Strong identity verification [remote-cluster-strong-verification]
```{applies_to}
deployment:
  stack: preview 9.3
```

Cross-cluster API keys can be configured with strong identity verification to provide an additional layer of security. To enable this feature, a
cross-cluster API key is created on the remote cluster with a certificate identity pattern that specifies which certificates are allowed
to use it. The local cluster must then sign each request with its private key and include a certificate whose subject Distinguished Name
(DN) matches the pattern. The remote cluster validates both that the certificate is trusted by its configured certificate authorities
and that the certificate's subject matches the API key's identity pattern.

Each remote cluster alias on the local cluster can have different remote signing configurations.

### How strong identity verification works [_how_strong_verification_works]

When a local cluster makes a request to a remote cluster using a cross-cluster API key:

1. The local cluster signs the request headers with its configured private key and sends the signature and certificate chain as header
   in the request to the remote cluster.
2. The remote cluster verifies that the API key is valid.
3. If the API key has a certificate identity pattern configured, the remote cluster extracts the Distinguished Name (DN) from the
   certificate chain's leaf certificate and matches it against the certificate identity pattern.
4. The remote cluster validates that the provided certificate chain is trusted.
5. The remote cluster validates the signature and checks that the certificate is not expired.

If any of these validation steps fail, the request is rejected.

### Configure strong identity verification [_configure_strong_verification]

To use strong identity verification, the local and remote clusters must be configured to sign request headers and to verify request
headers. This can be done through the cluster settings API or `elasticsearch.yaml`.

#### On the local cluster [_certificate_identity_local_cluster]

When [adding the remote cluster](#using-the-es-api) to the local cluster, you must configure it to sign cross-cluster requests with a certificate–private key pair. You can generate a signing certificate using [elasticsearch-certutil](#remote-clusters-security-api-key-remote-action) or use an existing certificate. The private key can be encrypted and the password must be stored securely as a secure setting in Elasticsearch keystore. Refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-signing-settings) for details.

```yaml
cluster.remote.my_remote_cluster.signing.certificate: "path/to/signing/certificate.crt"
cluster.remote.my_remote_cluster.signing.key: "path/to/signing/key.key"
```

::::{note}
Replace `my_remote_cluster` with your remote cluster alias, and the paths with the paths to your certificate and key files.
::::

#### On the remote cluster [_certificate_identity_remote_cluster]

The remote cluster must be configured with a certificate authority that trusts the certificate that was used to sign the request headers.

```yaml
cluster.remote.signing.certificate_authorities: "path/to/signing/certificate_authorities.crt"
```

When creating a cross-cluster API key on the remote cluster, specify a `certificate_identity` pattern that matches the Distinguished
Name (DN) of the local cluster's certificate. Use the [Create Cross-Cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) API:

```console
POST /_security/cross_cluster/api_key
{
  "name": "my-cross-cluster-api-key",
  "access": {
    "search": [
      {
        "names": ["logs-*"]
      }
    ]
  },
  "certificate_identity": "CN=local-cluster.example.com,O=Example Corp,C=US"
}
```

The `certificate_identity` field supports regular expressions. For example:

* `"CN=.*.example.com,O=Example Corp,C=US"` matches any certificate with a CN ending in "example.com"
* `"CN=local-cluster.*,O=Example Corp,C=US"` matches any certificate with a CN starting with "local-cluster"
* `"CN=.*"` matches any certificate (not recommended for production)

For a full list of available strong identity verification settings for remote clusters, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-signing-settings).


## Configure roles and users [remote-clusters-privileges-api-key]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) or [remote cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-cluster-priv) on the local cluster.

To manage users and roles in {{kib}}, go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). You can also use the [role management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) to add, update, remove, and retrieve roles dynamically.

The following examples use the [Create or update roles](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) API. You must have at least the `manage_security` cluster privilege to use this API.

::::{note}
The cross-cluster API key used by the local cluster to connect the remote cluster must have sufficient privileges to cover all remote indices privileges required by individual users.
::::


### Configure privileges for {{ccr}} [_configure_privileges_for_ccr]

Assuming the remote cluster is connected under the name of `my_remote_cluster`, the following request creates a role called `remote-replication` on the local cluster that allows replicating the remote `leader-index` index:

```console
POST /_security/role/remote-replication
{
  "cluster": [
    "manage_ccr"
  ],
  "remote_indices": [
    {
      "clusters": [ "my_remote_cluster" ],
      "names": [
        "leader-index"
      ],
      "privileges": [
        "cross_cluster_replication"
      ]
    }
  ]
}
```

After creating the local `remote-replication` role, use the [Create or update users](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) API to create a user on the local cluster cluster and assign the `remote-replication` role. For example, the following request assigns the `remote-replication` role to a user named `cross-cluster-user`:

```console
POST /_security/user/cross-cluster-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-replication" ]
}
```

Note that you only need to create this user on the local cluster.


### Configure privileges for {{ccs}} [_configure_privileges_for_ccs]

Assuming the remote cluster is connected under the name of `my_remote_cluster`, the following request creates a `remote-search` role on the local cluster that allows searching the remote `target-index` index:

```console
POST /_security/role/remote-search
{
  "remote_indices": [
    {
      "clusters": [ "my_remote_cluster" ],
      "names": [
        "target-index"
      ],
      "privileges": [
        "read",
        "read_cross_cluster",
        "view_index_metadata"
      ]
    }
  ]
}
```

After creating the `remote-search` role, use the [Create or update users](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) API to create a user on the local cluster and assign the `remote-search` role. For example, the following request assigns the `remote-search` role to a user named `cross-search-user`:

```console
POST /_security/user/cross-search-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-search" ]
}
```

Note that you only need to create this user on the local cluster.
