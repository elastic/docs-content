<!--
Used in:
- explore-analyze/cross-cluster-search.md
_configure_privileges_for_cross_cluster_replication_2.md
-->

You can manage roles in {{kib}} on the **Roles** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). You can also use the [role management]({{es-apis}}group/endpoint-security) APIs to add, update, remove, and retrieve roles dynamically. When you use the UI or APIs to manage roles, the roles are stored in an internal {{es}} index. When you use local files, the roles are only stored in those files. For more information, refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

The following examples use the [create or update roles]({{es-apis}}operation/operation-security-put-role) API and the [create or update users]({{es-apis}}operation/operation-security-put-user) API. You must have at least the `manage_security` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) to use these APIs.
