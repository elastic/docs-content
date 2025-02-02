# Custom roles [custom-roles]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

The built-in [organization-level roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-organization-level-roles) and [instance access roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-instance-access-roles) are great for getting started with {{serverless-full}}, and for system administrators who do not need more restrictive access.

As an administrator, however, can create roles for users with the access they need within specific projects. For example, you might create a marketing_user role, which you then assign to all users in your marketing department. This role would grant access to all of the necessary data and features for this team to be successful, without granting them access they don’t require.

All custom roles grant the same access as the `Viewer` instance access role with regards to {{ecloud}} privileges. To grant more {{ecloud}} privileges, assign more roles. Users receive a union of all their roles' privileges.

You can manage custom roles in **{{project-settings}} → {{manage-app}} →{{custom-roles-app}}**. To create a new custom role, click the **Create role** button. To clone, delete, or edit a role, open the actions menu:

:::{image} ../../../images/serverless-custom-roles-ui.png
:alt: Custom Roles app
:class: screenshot
:::

Roles are a collection of privileges that enable users to access project features and data. For example, when you create a custom role, you can assign {{es}} cluster and index privileges and {{kib}} privileges.

::::{note}
You cannot assign [run as privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#_run_as_privilege) in {{serverless-full}} custom roles.

::::



## {{es}} cluster privileges [custom-roles-es-cluster-privileges]

Cluster privileges grant access to monitoring and management features in {{es}}. They also enable some {{stack-manage-app}} capabilities in your project.

:::{image} ../../../images/serverless-custom-roles-cluster-privileges.png
:alt: Create a custom role and define {{es}} cluster privileges
:class: screenshot
:::

Refer to [cluster privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster) for a complete description of available options.


## {{es}} index privileges [custom-roles-es-index-privileges]

Each role can grant access to multiple data indices, and each index can have a different set of privileges. Typically, you will grant the `read` and `view_index_metadata` privileges to each index that you expect your users to work with. For example, grant access to indices that match an `acme-marketing-*` pattern:

:::{image} ../../../images/serverless-custom-roles-index-privileges.png
:alt: Create a custom role and define {{es}} index privileges
:class: screenshot
:::

Refer to [index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) for a complete description of available options.

Document-level and field-level security affords you even more granularity when it comes to granting access to your data. With document-level security (DLS), you can write an {{es}} query to describe which documents this role grants access to. With field-level security (FLS), you can instruct {{es}} to grant or deny access to specific fields within each document.


## {{kib}} privileges [custom-roles-kib-privileges]

When you create a custom role, click **Add Kibana privilege** to grant access to specific features. The features that are available vary depending on the project type. For example, in {{es-serverless}}:

:::{image} ../../../images/serverless-custom-roles-kibana-privileges.png
:alt: Create a custom role and define {{kib}} privileges
:class: screenshot
:::

Open the **Spaces** selection control to specify whether to grant the role access to all spaces or one or more individual spaces. When using the **Customize by feature*** option, you can choose either ***All***, ***Read** or **None** for access to each feature.

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


After your roles are set up, the next step to securing access is to assign roles to your users. Click the **Assign roles** link to go to the **Members** tab of the **Organization** page. Learn more in [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
