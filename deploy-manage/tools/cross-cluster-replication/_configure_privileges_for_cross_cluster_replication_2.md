---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_configure_privileges_for_cross_cluster_replication_2.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Configure privileges for cross-cluster replication [_configure_privileges_for_ccr_2]

The {{ccr}} user requires different cluster and index privileges on the remote cluster and local cluster. Use the following requests to create separate roles on the local and remote clusters, and then create a user with the required roles.


## Remote cluster [_remote_cluster_4]

On the remote cluster that contains the leader index, the {{ccr}} role requires the `read_ccr` cluster privilege, and `monitor` and `read` privileges on the leader index.

::::{note}
If requests are authenticated with an [API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key), the API key requires the above privileges on the **local** cluster, instead of the remote.
::::


::::{note}
If requests are issued [on behalf of other users](../../users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md), then the authenticating user must have the `run_as` privilege on the remote cluster.
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


## Local cluster [_local_cluster_4]

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

After creating the `remote-replication` role on each cluster, use the [create or update users API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) to create a user on the local cluster and assign the `remote-replication` role. For example, the following request assigns the `remote-replication` role to a user named `cross-cluster-user`:

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
