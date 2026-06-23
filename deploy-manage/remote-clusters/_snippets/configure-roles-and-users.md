<!--
This snippet is in use in the following locations:
- self-remote-cluster-eck.md
- eck-remote-clusters.md
- eck-remote-clusters-to-other-eck.md
- eck-remote-clusters-to-external.md
- ece-remote-cluster-self-managed.md
- ece-remote-cluster-same-ece.md
- ece-remote-cluster-other-ece.md
- ece-remote-cluster-ece-ess.md
- ece-enable-ccs-for-eck.md
- ec-remote-cluster-self-managed.md
- ec-remote-cluster-same-ess.md
- ec-remote-cluster-other-ess.md
- ec-remote-cluster-ece.md
- ec-enable-ccs-for-eck.md
-->

If you're using the API key–based security model for {{ccr}} or {{ccs}}, the [cross-cluster API key](/deploy-manage/remote-clusters/remote-clusters-api-key.md) used to connect to a remote cluster defines the maximum privileges that any user can exercise on that remote cluster. Define user roles with [remote indices privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) or [remote cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-cluster-priv) on the local cluster to grant remote access to specific users. By default, users have no remote privileges unless they are superusers or are assigned a role that includes remote privileges.

If you're using TLS certificate–based authentication, create roles with the same name on both the local and remote clusters. Each cluster defines its own role privileges, but the names must match so that authorization is enforced on both sides of the connection.

For more details, refer to [Configure privileges for {{ccr}}](/deploy-manage/tools/cross-cluster-replication/_configure_privileges_for_cross_cluster_replication_2.md) and [Configure privileges for {{ccs}}](/explore-analyze/cross-cluster-search.md#configure-privileges-for-ccs).
