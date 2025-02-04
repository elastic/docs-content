# User roles and privileges [ec-user-privileges]

Within an {{ecloud}} organization, users can have one or more roles and each role grants specific privileges.

::::{note}
This page focuses on roles for hosted deployments. Roles for serverless projects are detailed in the [serverless documentation](https://docs.elastic.co/serverless/general/assign-user-roles).
::::



## Organization-level roles [ec_organization_level_roles]

* **Organization owner** - The role assigned by default to the user who created the organization. Organization owners have all privileges to instances (hosted deployments and serverless projects), users, organization-level details and properties, billing details and subscription levels. They are also able to sign on to deployments with superuser privileges.
* **Billing admin** - Can manage an organization’s billing details such as credit card information, subscription and invoice history. Cannot manage other organization or deployment details and properties.


## Instance access roles [ec_instance_access_roles]

You can set instance access roles:

* globally, for all hosted deployments. In this case, the role will also apply to new deployments created later.
* individually, for specific deployments only. To do that, you have to leave the **Role for all hosted deployments** field blank.

For hosted deployments, the predefined roles available are the following:

* **Admin** - Can manage deployment details, properties and security privileges, and is able to sign on to the deployment with superuser privileges. This role can be scoped to one or more deployments. In order to prevent scope expansion, only Admins on all deployments can create new deployments.
* **Editor** - Has the same rights as Admin, except from deployment creation and management of security privileges. Editors are able to sign on to the deployment with the “editor” stack role. This role can be scoped to one or more deployments.
* **Viewer** - Can view deployments, and can sign on to the deployment with the viewer Stack role. This role can be scoped to one or more deployments.

Within the same organization, all members share the same set of default permissions. From the Elasticsearch Service main page you can:

* See the organization details.
* Modify your **Profile** under your avatar in the upper right corner.
* [Leave](../../../deploy-manage/users-roles/cloud-organization/manage-users.md#ec-leave-organization) the organization.

::::{note}
The {{ecloud}} UI navigation and access to components is based on user privileges.
::::



## Role scoping [ec-role-scoping]

Roles are assigned to every member of an organization and can refer (or be scoped) to one or more specific deployments, or all deployments. When a role is scoped to all deployments it grants permissions on all existing and future deployments.

This list describes the scope of the different roles:

* **Organization owner** - This role is always scoped to administer all deployments.
* **Billing admin** - This role does not refer to any deployment.
* **Admin**, **Editor**, and **Viewer** - These roles can be scoped to either all deployments, or specific deployments.

Members are only able to see the role assignments of other members under the organization they belong to, for role assignments they are able to manage. Members with the Organization owner role assigned are able to see the role assignments of every member of their organization.

Members with the Admin role assigned are able to see role assignments for deployments within their scope. For example, Admins of all deployments are able to see role assignments scoped to all and specific deployments in the organization, while Admins of specific deployments only see role assignments scoped to those specific deployments. This ensures that members assigned to specific deployments do not try to remove role assignments from other members, and that the existence of other deployments are not revealed to these members.


## Mapping of {{ecloud}} roles with {{stack}} roles [ec-stack-user-org-member]

There are two ways for a user to access {{kib}} instances of an {{ecloud}} deployment:

* Directly with {{es}} credentials. In this case, users and their roles are managed directly in [{{kib}}](https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html). Users in this case don’t need to be members of the {{ecloud}} organization to access the deployment. Note that if you have several deployments, you need to manage users for each of them, individually.
* Through your {{ecloud}} organization. In this case, users who are members of your organization log in to {{ecloud}} and can open the deployments they have access to. Their access level is determined by the roles assigned to them from the Organization page. {{ecloud}} roles are mapped to [Stack roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md#built-in-roles) on a per-deployment level. When logging in to a specific deployment, users get the Stack role that maps to their Cloud role for that particular deployment.

The following table shows the default mapping:

|     |     |     |
| --- | --- | --- |
| **Cloud role** | **Cloud API `role_id`** | **Stack role** |
| Organization owner | `organization-admin` | superuser |
| Billing admin | `billing-admin` | none |
| Admin | `deployment-admin` | superuser |
| Editor | `deployment-editor` | editor |
| Viewer | `deployment-viewer` | viewer |

::::{note}
This table applies to deployments running on version 7.13 onwards. For earlier versions, only the superuser role mapping applies.
::::
