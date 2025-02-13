# Security [xpack-security]

The {{stack}} {{security-features}} enable you to easily secure a cluster. With security, you can password-protect your data as well as implement more advanced security measures such as encrypting communications, role-based access control, IP filtering, and auditing. For more information, see [Secure a cluster](../../../deploy-manage/security.md) and [Configuring Security in {{kib}}](../../../deploy-manage/security.md).

::::{note} 
There are security limitations that affect {{kib}}. For more information, refer to [Security](../../../deploy-manage/security.md).
::::



## Required permissions [_required_permissions_6] 

The `manage_security` cluster privilege is required to access all Security features.


## Users [_users_2] 

To create and manage users, go to the **Users** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). You can also change their passwords and roles. For more information about authentication and built-in users, see [Setting up user authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).


## Roles [_roles_2] 

To manage roles, go to the **Roles** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), or use the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles). For more information on configuring roles for {{kib}}, see [Granting access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md).

For a more holistic overview of configuring roles for the entire stack, see [User authorization](../../../deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

::::{note} 
Managing roles that grant [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) using the {{es}} [role management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) is not supported. Doing so will likely cause Kibana’s authorization to behave unexpectedly.

::::








