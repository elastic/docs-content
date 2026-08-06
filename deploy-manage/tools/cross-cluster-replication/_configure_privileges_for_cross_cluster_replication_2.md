---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_configure_privileges_for_cross_cluster_replication_2.html
applies_to:
  stack: all

products:
  - id: elasticsearch
---

# Configure privileges for {{ccr}} [_configure_privileges_for_ccr_2]

To use a [remote cluster](/deploy-manage/remote-clusters.md) for {{ccr}}, you need to configure user roles with the correct cluster and index privileges. The steps depend on the [remote cluster security model](/deploy-manage/remote-clusters/security-models.md) in use:

* [API key authentication](#configure-privileges-for-ccr-api-key) (recommended), where you create roles with the required privileges on the local cluster.
* {applies_to}`stack: deprecated 9.0` [TLS certificate authentication](#configure-privileges-for-ccr-cert), where you create matching roles on both the local and remote clusters.

:::{include} /deploy-manage/remote-clusters/_snippets/configure-privileges-role-management.md
:::

## API key authentication [configure-privileges-for-ccr-api-key]

:::{include} /deploy-manage/remote-clusters/_snippets/configure-privileges-api-key-authorization.md
:::

To grant a user {{ccr}} access, you create a role on the local cluster, assign it the `manage_ccr` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) and the `cross_cluster_replication` [index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) for the remote cluster alias and leader index, then assign that role to the user.

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

After creating the local `remote-replication` role, use the [create or update users]({{es-apis}}operation/operation-security-put-user) API to create a user on the local cluster and assign the `remote-replication` role. For example, the following request assigns the `remote-replication` role to a user named `cross-cluster-user`:

```console
POST /_security/user/cross-cluster-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-replication" ]
}
```

Note that you only need to create this user on the local cluster.

You can then [configure {{ccr}}](set-up-cross-cluster-replication.md) to replicate your data across datacenters.

## TLS certificate authentication [configure-privileges-for-ccr-cert]
```{applies_to}
stack: deprecated 9.0
```

:::{warning}

Certificate based authentication is deprecated. Configure [API key authentication](/deploy-manage/remote-clusters/remote-clusters-api-key.md) instead or follow a guide on how to [migrate remote clusters from certificate to API key authentication](/deploy-manage/remote-clusters/remote-clusters-migrate.md).
:::

After [connecting remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md), create matching user roles on both the local and remote clusters and assign the necessary privileges. With TLS-based authentication, the local user's role names are forwarded to the remote cluster, which authorizes the request by evaluating roles with the same names defined locally.

:::{important}
You must use the same role names on both the local and remote clusters. For example, the following configuration uses the `remote-replication` role name on both clusters. However, you can specify different role definitions on each cluster.
:::

### Remote cluster [_remote_cluster_4]

On the remote cluster that contains the leader index, the {{ccr}} role requires the `read_ccr` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster), and `monitor` and `read` [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) on the leader index.

:::{note}
If requests are issued [on behalf of other users](/deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md), then the authenticating user must have the [`run_as` privilege](elasticsearch://reference/elasticsearch/security-privileges.md#_run_as_privilege).
:::

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

### Local cluster [_local_cluster_4]

On the local cluster that contains the follower index, the `remote-replication` role requires the `manage_ccr` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster), and `monitor`, `read`, `write`, and `manage_follow_index` [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) on the follower index.

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

After creating the `remote-replication` role on each cluster, use the [create or update users]({{es-apis}}operation/operation-security-put-user) API to create a user on the local cluster and assign the `remote-replication` role. For example, the following request assigns the `remote-replication` role to a user named `cross-cluster-user`:

```console
POST /_security/user/cross-cluster-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "remote-replication" ]
}
```

::::{note}
You only need to create this user on the **local** cluster.
::::

You can then [configure {{ccr}}](set-up-cross-cluster-replication.md) to replicate your data across datacenters.
