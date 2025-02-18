---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/authorization.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

# User roles [authorization]


After a user is authenticated, use role-based access control to determine whether the user behind an incoming request is allowed to execute the request. The primary method of authorization in a cluster is role-based access control (RBAC). Review the following topics to learn about authorization in your Elasticsearch cluster.

### Set up user authorization

* [Define roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md)
* Learn about [built-in roles](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md)
* Learn about the [Elasticsearch](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) and [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) privileges you can assign to roles
* Creating [mappings of users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) for external authentication providers
* Learn how to [control access at the document and field level](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md)

### Advanced topics

* Learn how to [delegate authorization to another realm](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-delegation.md)
* Learn how to [build a custom authorization plugin](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-plugins.md) for unsupported systems or advanced applications
* Learn how to [submit requests on behalf of other users](/deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md)
* Learn about [attribute-based access control](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md#attributes)

::::{tip}
User roles are also used to control access to [{{kib}} spaces](/deploy-manage/manage-spaces.md). 
::::



The {{stack-security-features}} add *authorization*, which is the process of determining whether the user behind an incoming request is allowed to execute the request.

This process takes place after the user is successfully identified and [authenticated](user-authentication.md).


## Role-based access control [roles]

The {{security-features}} provide a role-based access control (RBAC) mechanism, which enables you to authorize users by assigning privileges to roles and assigning roles to users or groups.

:::{image} ../../../images/elasticsearch-reference-authorization.png
:alt: This image illustrates role-based access control
:::

The authorization process revolves around the following constructs:

*Secured Resource*
:   A resource to which access is restricted. Indices, aliases, documents, fields, users, and the {{es}} cluster itself are all examples of secured objects.

*Privilege*
:   A named group of one or more actions that a user may execute against a secured resource. Each secured resource has its own sets of available privileges. For example, `read` is an index privilege that represents all actions that enable reading the indexed/stored data. For a complete list of available privileges see [Security privileges](elasticsearch-privileges.md).

*Permissions*
:   A set of one or more privileges against a secured resource. Permissions can easily be described in words, here are few examples:

    * `read` privilege on the `products` data stream or index
    * `manage` privilege on the cluster
    * `run_as` privilege on `john` user
    * `read` privilege on documents that match query X
    * `read` privilege on `credit_card` field


*Role*
:   A named set of permissions

*User*
:   The authenticated user.

*Group*
:   One or more groups to which a user belongs. Groups are not supported in some realms, such as native, file, or PKI realms.

A role has a unique name and identifies a set of permissions that translate to privileges on resources. You can associate a user or group with an arbitrary number of roles. When you map roles to groups, the roles of a user in that group are the combination of the roles assigned to that group and the roles assigned to that user. Likewise, the total set of permissions that a user has is defined by the union of the permissions in all its roles.

The method for assigning roles to users varies depending on which realms you use to authenticate users. For more information, see [Mapping users and groups to roles](mapping-users-groups-to-roles.md).


## Attribute-based access control [attributes]

The {{security-features}} also provide an attribute-based access control (ABAC) mechanism, which enables you to use attributes to restrict access to documents in search queries and aggregations. For example, you can assign attributes to users and documents, then implement an access policy in a role definition. Users with that role can read a specific document only if they have all the required attributes.

For more information, see [Document-level attribute-based access control with X-Pack 6.1](https://www.elastic.co/blog/attribute-based-access-control-with-xpack).













