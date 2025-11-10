---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/custom-roles.html
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
---

# Serverless project custom roles [custom-roles]

Built-in [organization-level roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_organization_level_roles) and [cloud resource access roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_instance_access_roles) are great for getting started with {{serverless-full}}, and for system administrators who do not need more restrictive access.

As an administrator, you can also create roles for users with the access they need within specific projects. For example, you might create a `marketing_user` role, which you then assign to all users in your marketing department. This role would grant access to all of the necessary data and features for this team to be successful, without granting them access they don’t require.

All custom roles grant the same access as the `Viewer` cloud resource access role with regards to {{ecloud}} privileges. To grant more {{ecloud}} privileges, assign more roles. Users receive a union of all their roles' privileges.

Roles are a collection of privileges that enable users to access project features and data. When you create a custom role, you can assign {{es}} [cluster](#custom-roles-es-cluster-privileges) and [index](#custom-roles-es-index-privileges) privileges and [{{kib}}](#custom-roles-kib-privileges) privileges.

On this page, you'll learn about how to [manage custom roles in your project](#manage-custom-roles), the types of privileges you can assign, and how to [assign the roles](#assign-custom-roles) that you create.

::::{note}
You cannot assign [run as privileges](elasticsearch://reference/elasticsearch/security-privileges.md#_run_as_privilege) in {{serverless-full}} custom roles.
::::

:::{{admonition}} Custom roles in {{stack}}
This topic explains how to create custom roles in {{serverless-full}}. You can also create custom roles for {{stack}} clusters and deployments.

[Learn more](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
:::

## Manage custom roles

You can manage custom roles from within your project, in **{{project-settings}} > {{manage-app}} > {{custom-roles-app}}**. To create a new custom role, click the **Create role** button. To clone, delete, or edit a role, open the actions menu `⋯`.

## {{es}} cluster privileges [custom-roles-es-cluster-privileges]

Cluster privileges grant access to monitoring and management features in {{es}}. They also enable some stack management capabilities in your project.

:::{image} /deploy-manage/images/serverless-custom-roles-cluster-privileges.png
:alt: Create a custom role and define {{es}} cluster privileges
:screenshot:
:::

Refer to [cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) for a complete description of available options.


## {{es}} index privileges [custom-roles-es-index-privileges]

Each role can grant access to multiple data indices, and each index can have a different set of privileges. Typically, you will grant the `read` and `view_index_metadata` privileges to each index that you expect your users to work with. For example, grant access to indices that match an `acme-marketing-*` pattern:

:::{image} /deploy-manage/images/serverless-custom-roles-index-privileges.png
:alt: Create a custom role and define {{es}} index privileges
:screenshot:
:::

Refer to [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) for a complete description of available options.

### Document level and field level security

Document-level and field-level security affords you even more granularity when it comes to granting access to your data:

* With document-level security (DLS), you can write an {{es}} query to describe which documents this role grants access to. Add your query in the **Granted documents query** field using [QueryDSL](/explore-analyze/query-filter/languages/querydsl.md) syntax.

  For example, the following query grants read access only to the documents whose `department_id` equals `12`:

  ```json
  {
    "term" : { "department_id" : 12 }
  }
  ```

* With field-level security (FLS), you can instruct {{es}} to grant or deny access to specific fields within each document. List these fields in the **Granted fields** field.

:::{{tip}}
{{serverless-full}} and {{stack}} both use queries to specify the documents that a role can access. For additional query examples, refer to [Controlling access at the document and field level](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#document-level-security).
:::


## {{kib}} privileges [custom-roles-kib-privileges]

When you create a custom role, click **Add {{kib}} privilege** to grant access to specific features. The features that are available vary depending on the project type. For example, in {{es-serverless}}:

:::{image} /deploy-manage/images/serverless-custom-roles-kibana-privileges.png
:alt: Create a custom role and define {{kib}} privileges
:screenshot:
:::

Open the **Spaces** selection control to specify whether to grant the role access to all spaces or one or more individual spaces. When using the **Customize by feature** option, you can choose either **All**, **Read** or **None** for access to each feature.

All
:   Grants full read-write access.

Read
:   Grants read-only access.

None
:   Does not grant any access.

Some features have finer access control and you can optionally enable sub-feature privileges.

::::{admonition} New features
:class: note

As new features are added to {{serverless-full}}, roles that use the custom option do not automatically get access to the new features. You must manually update the roles.

::::

## Assign custom roles

After your roles are set up, the next step to securing access is to assign roles to your users. Click the **Assign roles** link to go to the **Members** tab of the **Organization** page. Learn more in [](/deploy-manage/users-roles/cloud-organization/user-roles.md).
