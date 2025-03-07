---
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-api-key.html
---

# Add remote clusters using API key authentication [remote-clusters-api-key]

API key authentication enables a local cluster to authenticate itself with a remote cluster via a [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key). The API key needs to be created by an administrator of the remote cluster. The local cluster is configured to provide this API key on each request to the remote cluster. The remote cluster verifies the API key and grants access, based on the API key’s privileges.

All cross-cluster requests from the local cluster are bound by the API key’s privileges, regardless of local users associated with the requests. For example, if the API key only allows read access to `my-index` on the remote cluster, even a superuser from the local cluster is limited by this constraint. This mechanism enables the remote cluster’s administrator to have full control over who can access what data with cross-cluster search and/or cross-cluster replication. The remote cluster’s administrator can be confident that no access is possible beyond what is explicitly assigned to the API key.

On the local cluster side, not every local user needs to access every piece of data allowed by the API key. An administrator of the local cluster can further configure additional permission constraints on local users so each user only gets access to the necessary remote data. Note it is only possible to further reduce the permissions allowed by the API key for individual local users. It is impossible to increase the permissions to go beyond what is allowed by the API key.

In this model, cross-cluster operations use [a dedicated server port](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote_cluster.port) (remote cluster interface) for communication between clusters. A remote cluster must enable this port for local clusters to connect. Configure Transport Layer Security (TLS) for this port to maximize security (as explained in [Establish trust with a remote cluster](#remote-clusters-security-api-key)).

The local cluster must trust the remote cluster on the remote cluster interface. This means that the local cluster trusts the remote cluster’s certificate authority (CA) that signs the server certificate used by the remote cluster interface. When establishing a connection, all nodes from the local cluster that participate in cross-cluster communication verify certificates from nodes on the other side, based on the TLS trust configuration.

To add a remote cluster using API key authentication:

1. [Review the prerequisites](#remote-clusters-prerequisites-api-key)
2. [Establish trust with a remote cluster](#remote-clusters-security-api-key)
3. [Connect to a remote cluster](#remote-clusters-connect-api-key)
4. [Configure roles and users](#remote-clusters-privileges-api-key)

If you run into any issues, refer to [Troubleshooting](/troubleshoot/elasticsearch/remote-clusters.md).

## Prerequisites [remote-clusters-prerequisites-api-key]

* The {{es}} security features need to be enabled on both clusters, on every node. Security is enabled by default. If it’s disabled, set `xpack.security.enabled` to `true` in `elasticsearch.yml`. Refer to [General security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings).
* The nodes of the local and remote clusters must be on {{stack}} 8.14 or later.
* The local and remote clusters must have an appropriate license. For more information, refer to [https://www.elastic.co/subscriptions](https://www.elastic.co/subscriptions).


## Establish trust with a remote cluster [remote-clusters-security-api-key]

::::{note}
If a remote cluster is part of an {{ech}} deployment, it has a valid certificate by default. You can therefore skip steps related to certificates in these instructions.
::::


### On the remote cluster [remote-clusters-security-api-key-remote-action]

1. Enable the remote cluster server on every node of the remote cluster. In `elasticsearch.yml`:

    1. Set [`remote_cluster_server.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote-cluster-network-settings) to `true`.
    2. Configure the bind and publish address for remote cluster server traffic, for example using [`remote_cluster.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote-cluster-network-settings). Without configuring the address, remote cluster traffic may be bound to the local interface, and remote clusters running on other machines can’t connect.
    3. Optionally, configure the remote server port using [`remote_cluster.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote_cluster.port) (defaults to `9443`).

2. Next, generate a certificate authority (CA) and a server certificate/key pair. On one of the nodes of the remote cluster, from the directory where {{es}} has been installed:

    1. Create a CA, if you don’t have a CA already:

        ```sh
        ./bin/elasticsearch-certutil ca --pem --out=cross-cluster-ca.zip --pass CA_PASSWORD
        ```

        Replace `CA_PASSWORD` with the password you want to use for the CA. You can remove the `--pass` option and its argument if you are not deploying to a production environment.

    2. Unzip the generated `cross-cluster-ca.zip` file. This compressed file contains the following content:

        ```txt
        /ca
        |_ ca.crt
        |_ ca.key
        ```

    3. Generate a certificate and private key pair for the nodes in the remote cluster:

        ```sh
        ./bin/elasticsearch-certutil cert --out=cross-cluster.p12 --pass=CERT_PASSWORD --ca-cert=ca/ca.crt --ca-key=ca/ca.key --ca-pass=CA_PASSWORD --dns=example.com --ip=127.0.0.1
        ```

        * Replace `CA_PASSWORD` with the CA password from the previous step.
        * Replace `CERT_PASSWORD` with the password you want to use for the generated private key.
        * Use the `--dns` option to specify the relevant DNS name for the certificate. You can specify it multiple times for multiple DNS.
        * Use the `--ip` option to specify the relevant IP address for the certificate. You can specify it multiple times for multiple IP addresses.

    4. If the remote cluster has multiple nodes, you can either:

        * create a single wildcard certificate for all nodes;
        * or, create separate certificates for each node either manually or in batch with the [silent mode](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-silent).

3. On every node of the remote cluster:

    1. Copy the `cross-cluster.p12` file from the earlier step to the `config` directory. If you didn’t create a wildcard certificate, make sure you copy the correct node-specific p12 file.
    2. Add following configuration to `elasticsearch.yml`:

        ```yaml
        xpack.security.remote_cluster_server.ssl.enabled: true
        xpack.security.remote_cluster_server.ssl.keystore.path: cross-cluster.p12
        ```

    3. Add the SSL keystore password to the {{es}} keystore:

        ```sh
        ./bin/elasticsearch-keystore add xpack.security.remote_cluster_server.ssl.keystore.secure_password
        ```

        When prompted, enter the `CERT_PASSWORD` from the earlier step.

4. Restart the remote cluster.
5. On the remote cluster, generate a cross-cluster API key that provides access to the indices you want to use for {{ccs}} or {{ccr}}. You can use the [Create Cross-Cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) API or [{{kib}}](../api-keys/elasticsearch-api-keys.md).
6. Copy the encoded key (`encoded` in the response) to a safe location. You will need it to connect to the remote cluster later.


### On the local cluster [remote-clusters-security-api-key-local-actions]

1. On every node of the local cluster:

    1. Copy the `ca.crt` file generated on the remote cluster earlier into the `config` directory, renaming the file `remote-cluster-ca.crt`.
    2. Add following configuration to `elasticsearch.yml`:

        ```yaml
        xpack.security.remote_cluster_client.ssl.enabled: true
        xpack.security.remote_cluster_client.ssl.certificate_authorities: [ "remote-cluster-ca.crt" ]
        ```

    3. Add the cross-cluster API key, created on the remote cluster earlier, to the keystore:

        ```sh
        ./bin/elasticsearch-keystore add cluster.remote.ALIAS.credentials
        ```

        Replace `ALIAS` with the same name that you will use to create the remote cluster entry later. When prompted, enter the encoded cross-cluster API key created on the remote cluster earlier.

2. Restart the local cluster to load changes to the keystore and settings.

**Note:** If you are configuring only the cross-cluster API key, you can call the [Nodes reload secure settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API, instead of restarting the cluster. Configuring the `remote_cluster_client` settings in `elasticsearch.yml` still requires a restart.



## Connect to a remote cluster [remote-clusters-connect-api-key]

::::{note}
You must have the `manage` cluster privilege to connect remote clusters.
::::


The local cluster uses the [remote cluster interface](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) to establish communication with remote clusters. The coordinating nodes in the local cluster establish [long-lived](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections) TCP connections with specific nodes in the remote cluster. {{es}} requires these connections to remain open, even if the connections are idle for an extended period.

To add a remote cluster from Stack Management in {{kib}}:

1. Select **Remote Clusters** from the side navigation.
2. Enter a name (*cluster alias*) for the remote cluster.
3. Specify the {{es}} endpoint URL, or the IP address or host name of the remote cluster followed by the remote cluster port (defaults to `9443`). For example, `cluster.es.eastus2.staging.azure.foundit.no:9443` or `192.168.1.1:9443`.

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
            "127.0.0.1:9443" <2>
          ]
        }
      }
    }
  }
}
```

1. The cluster alias of this remote cluster is `cluster_one`.
2. Specifies the hostname and remote cluster port of a seed node in the remote cluster.
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
      "127.0.0.1:9443"
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
%  TESTRESPONSE[s/127.0.0.1:{{remote-interface-default-port}}/$body.cluster_one.seeds.0/]
%  TESTRESPONSE[s/ifeval::(.|\n)*endif::[]//]
%  TEST[s/"connected" : true/"connected" : $body.cluster_one.connected/]
%  TEST[s/"num_nodes_connected" : 1/"num_nodes_connected" : $body.cluster_one.num_nodes_connected/]

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
            "127.0.0.1:9443"
          ]
        },
        "cluster_two": {
          "mode": "sniff",
          "seeds": [
            "127.0.0.1:9444"
          ],
          "transport.compress": true,
          "skip_unavailable": true
        },
        "cluster_three": {
          "mode": "proxy",
          "proxy_address": "127.0.0.1:9445"
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


### Statically configure remote clusters [_statically_configure_remote_clusters]

If you specify settings in `elasticsearch.yml`, only the nodes with those settings can connect to the remote cluster and serve remote cluster requests.

::::{note}
Remote cluster settings that are specified using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) take precedence over settings that you specify in `elasticsearch.yml` for individual nodes.
::::


In the following example, `cluster_one`, `cluster_two`, and `cluster_three` are arbitrary cluster aliases representing the connection to each cluster. These names are subsequently used to distinguish between local and remote indices.

```yaml
cluster:
    remote:
        cluster_one:
            seeds: 127.0.0.1:9443
        cluster_two:
            mode: sniff
            seeds: 127.0.0.1:9444
            transport.compress: true      <1>
            skip_unavailable: true        <2>
        cluster_three:
            mode: proxy
            proxy_address: 127.0.0.1:9445 <3>
```

1. Compression is explicitly enabled for requests to `cluster_two`.
2. Disconnected remote clusters are optional for `cluster_two`.
3. The address for the proxy endpoint used to connect to `cluster_three`.




## Configure roles and users [remote-clusters-privileges-api-key]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) or [remote cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-cluster-priv) on the local cluster.

You can manage users and roles from Stack Management in {{kib}} by selecting **Security > Roles** from the side navigation. You can also use the [role management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) to add, update, remove, and retrieve roles dynamically.

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
%  TEST[skip:TODO]

After creating the local `remote-replication` role, use the [Create or update users](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) API to create a user on the local cluster cluster and assign the `remote-replication` role. For example, the following request assigns the `remote-replication` role to a user named `cross-cluster-user`:

```console
POST /_security/user/cross-cluster-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-replication" ]
}
```
%  TEST[skip:TODO]

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
%  TEST[skip:TODO]

After creating the `remote-search` role, use the [Create or update users](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) API to create a user on the local cluster and assign the `remote-search` role. For example, the following request assigns the `remote-search` role to a user named `cross-search-user`:

```console
POST /_security/user/cross-search-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-search" ]
}
```
%  TEST[skip:TODO]

Note that you only need to create this user on the local cluster.
