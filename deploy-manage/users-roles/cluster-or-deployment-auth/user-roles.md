---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/authorization.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# User roles [authorization]


After a user is [authenticated](user-authentication.md), {{stack}} needs to determine whether the user behind an incoming request is allowed to execute the request. The primary method of authorization in a cluster is [role-based access control](#roles) (RBAC), although {{stack}} also supports [Attribute-based access control](#attributes) (ABAC).

:::{tip}
If you use {{ece}} or {{ech}}, then you can also implement RBAC at the level of your [{{ece}} orchestrator](/deploy-manage/users-roles/cloud-enterprise-orchestrator.md) or [{{ecloud}} organization](/deploy-manage/users-roles/cloud-organization.md).

If you use {{serverless-full}}, then you can only manage RBAC at the [{{ecloud}} organization level](/deploy-manage/users-roles/cloud-organization.md).

You must authenticate users at the same level where you implement RBAC. For example, if you want to use organization-level roles, than you must authenticate your users at the organization level.
:::

## How role-based access control works [roles]

Role-based access control (RBAC) enables you to authorize users by assigning privileges to roles and assigning roles to users or groups. This is the primary way of controlling access to resources in {{stack}}.
<br>

:::{image} /deploy-manage/images/elasticsearch-reference-authorization.png
:alt: This image illustrates role-based access control
:::

The authorization process revolves around the following constructs:

*Secured Resource*
:   A resource to which access is restricted. Indices, aliases, documents, fields, users, and the {{es}} cluster itself are all examples of secured objects.

*Privilege*
:   A named group of one or more actions that a user may execute against a secured resource. Each secured resource has its own sets of available privileges. For example, `read` is an index privilege that represents all actions that enable reading the indexed/stored data. For a complete list of available privileges, see [{{es}} privileges](elasticsearch://reference/elasticsearch/security-privileges.md).

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

## Set up user authorization using RBAC

Review these topics to learn how to configure RBAC in your cluster or deployment:

* Learn about [built-in roles](elasticsearch://reference/elasticsearch/roles.md)
* [Define your own roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md)
* Learn about the [{{kib}}](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) and [{{es}}](elasticsearch://reference/elasticsearch/security-privileges.md) privileges you can assign to roles
* Learn how to [control access at the document and field level](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) {applies_to}`stack: ga` {applies_to}`serverless: ga`

:::{tip}
This topic describes built-in roles in {{stack}} clusters and deployments and explains how to create custom ones. You can also learn about [organization-level](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_organization_level_roles) roles and [cloud resource access roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_instance_access_roles) in {{serverless-full}}.
To create custom roles for {{serverless-full}}, refer to [](/deploy-manage/users-roles/serverless-custom-roles.md).
:::

The way that you assign roles to users depends on your authentication realm:

* [Native realm](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md): 
  * Using {{es}} API [`_security` endpoints](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security)
  * [In {{kib}}](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md#managing-native-users), from the **Users** management page. Find the page in the navigation menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* [File realm](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md): 
  * Using a [`user_roles` file](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md#k8s-basic)
  * In ECK: As part of a [basic authentication secret](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md#k8s-basic)
* [External realms](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md): By [mapping users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md)

:::{tip}
This topic describes using the native realm at the cluster or deployment level, for the purposes of authenticating with Elasticsearch and Kibana.

You can also manage authentication and identity integration at the [Elastic Cloud organization](/deploy-manage/users-roles/cloud-organization/manage-users.md) level.
:::

### Advanced topics

* Learn how to [delegate authorization to another realm](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-delegation.md)
* Learn how to [build a custom authorization plugin](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-plugins.md) for unsupported systems or advanced applications
* Learn how to [submit requests on behalf of other users](/deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md)
* Learn about [attribute-based access control](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md#attributes)

::::{tip}
User roles are also used to control access to [{{kib}} spaces](/deploy-manage/manage-spaces.md). 
::::

## Attribute-based access control [attributes]

Attribute-based access control (ABAC) enables you to use attributes to restrict access to documents in search queries and aggregations. For example, you can assign attributes to users and documents, then implement an access policy in a role definition. Users with that role can read a specific document only if they have all the required attributes.

For more information, see [Document-level attribute-based access control with {{es}}](https://www.elastic.co/blog/attribute-based-access-control-elasticsearch).













