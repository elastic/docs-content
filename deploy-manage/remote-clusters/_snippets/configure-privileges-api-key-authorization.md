<!--
Used in:
- explore-analyze/cross-cluster-search.md (#configure-privileges-for-ccs-api-key)
_configure_privileges_for_cross_cluster_replication_2.md (#configure-privileges-for-ccr-api-key)
-->

Authorization works in two parts:

* The [cross-cluster API key](/deploy-manage/remote-clusters/remote-clusters-api-key.md) used to connect to a remote cluster defines the maximum privileges that any user can exercise on remote clusters. This key is created and configured when you configure the remote cluster.
* Roles on the local cluster with [remote indices privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) or [remote cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-cluster-priv) grant remote access to specific users. 

By default, users have no remote privileges unless they are superusers or are assigned a role that includes remote privileges. A user's effective access is the intersection of their role privileges and the API key privileges.

:::{note}
The cross-cluster API key used by the local cluster to connect the remote cluster must have sufficient privileges to cover all remote indices privileges required by individual users.
:::
