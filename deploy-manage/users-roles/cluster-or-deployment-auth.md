---
navigation_title: Cluster or deployment
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-clusters.html
  - https://www.elastic.co/guide/en/cloud/current/ec-security.html
applies_to:
  stack: all
products:
  - id: cloud-enterprise
  - id: cloud-hosted
---

# Cluster or deployment users

To prevent unauthorized access to your Elastic resources, you need a way to identify users and validate that a user is who they claim to be (*authentication*), and control what data users can access and what tasks they can perform (*authorization*).

In this section, you’ll learn how to set up authentication and authorization at the cluster or deployment level, and learn about the underlying security technologies that {{es}} uses to authenticate and authorize requests internally and across services.

This section only covers direct access to and communications with an {{es}} cluster - sometimes known as a deployment - as well as the related {{kib}} instance. To learn about managing access to your {{ecloud}} organization or {{ece}} orchestrator, or to learn how to use single sign-on to access a cluster using your {{ecloud}} credentials, refer to [](/deploy-manage/users-roles.md).

:::{admonition} Control access to {{serverless-short}} projects
If you use {{serverless-full}}, you can only manage authentication at the [Elastic Cloud organization level](/deploy-manage/users-roles/cloud-organization.md).
:::

## Quickstart

If you plan to use native {{es}} user and role management, then [follow our quickstart](/deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md) to learn how to set up basic authentication and authorization features, including [spaces](/deploy-manage/manage-spaces.md), [roles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md), and [native users](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md).

### User authentication

Set up methods to identify users to the {{es}} cluster.

Key tasks for managing user authentication include:

* [Managing built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md)
* [Managing users natively](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md)
* [Integrating with external authentication providers](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md)

You can also learn the basics of {{es}} authentication, learn about accounts used to communicate within an {{es}} cluster and across services, and perform advanced tasks.

[View all user authentication docs](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md)

:::{admonition} Control access to {{serverless-short}} projects
This topic describes using the native realm at the cluster or deployment level, for the purposes of authenticating with {{es}} and {{kib}}.
You can also manage and authenticate users natively at the [Elastic Cloud organization](/deploy-manage/users-roles/cloud-organization/manage-users.md) level.
:::


### User authorization

After a user is authenticated, use role-based access control to determine whether the user behind an incoming request is allowed to execute the request.

Key tasks for managing user authorization include:

* [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md)
* Assigning [built-in roles](elasticsearch://reference/elasticsearch/roles.md) or your own roles to users
* Creating [mappings of users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) for external authentication providers
* [Setting up field- and document-level security](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) {applies_to}`stack: ga` {applies_to}`serverless: ga` 

You can also learn the basics of {{es}} authorization, and perform advanced tasks.

[View all user authorization docs](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md)

::::{tip}
User roles are also used to control access to [{{kib}} spaces](/deploy-manage/manage-spaces.md).
::::



:::{admonition} Built-in and custom roles in {{serverless-short}}
This topic describes built-in roles in {{stack}} clusters and deployments and explains how to create custom ones. You can also learn about [organization-level](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_organization_level_roles) roles and [cloud resource access roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_instance_access_roles) in {{serverless-full}}.
To create custom roles for {{serverless-full}}, refer to [](/deploy-manage/users-roles/serverless-custom-roles.md).
:::

