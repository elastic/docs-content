---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-user-privileges.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# User roles and privileges [ec-user-privileges]
$$$general-assign-user-roles$$$

Within an {{ecloud}} organization, users can have one or more roles and each role grants specific privileges.

You can assign user roles when you [invite users to join your organization](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-invite-users). You can also edit the roles assigned to a user later.

On this page, you'll learn the following:

* [How to edit a user's roles](#edit-a-users-roles)
* The [types of roles](#types-of-roles) available, the levels where they can be applied, and the [scope](#ec-role-scoping) of each role type
* The predefined roles available for [{{ech}}](#ech-predefined-roles) and [{{serverless-full}}](#general-assign-user-roles-table)

## Edit a user's roles

To edit the roles assigned to a user:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From a deployment or project on the home page, select **Manage**.
3. From the lower navigation menu, select **Organization**.
4. Find the user on the **Members** tab of the **Organization** page. Click the member name to view their roles.
5. Click **Edit roles** to change the user's roles.

## Types of roles

There are two types of roles you can assign to users:

* **Organization-level roles:** These roles apply to the entire organization and are not specific to any serverless project or hosted deployment.
* **Cloud resource access roles:** These roles are specific to each serverless project or hosted deployment.

### Organization-level roles [ec_organization_level_roles]

* **Organization owner**: The role assigned by default to the user who created the organization. Organization owners have all privileges to {{ecloud}} resources including {{ech}} deployments and {{serverless-full}} projects, as well as users, organization-level details and properties, billing details and subscription levels. They are also able to sign on to deployments with superuser privileges.
* **Billing admin**: Can manage an organization’s billing details such as credit card information, subscription and invoice history. Cannot manage other organization or deployment details and properties.

### Cloud resource access roles [ec_instance_access_roles]

You can set cloud resource access roles at two levels:

* **Globally**, for all {{ech}} deployments, or for all {{serverless-full}} projects of the same type ({{es-serverless}}, {{observability}}, or {{elastic-sec}}). In this case, the role will also apply to new deployments, or projects of the specified type type, created later.
* **Individually**, for specific deployments or projects only. To do that, you have to leave the **Role for all hosted deployments** field, or the **Role for all** for the project type, blank.

{{ech}} deployments and {{serverless-full}} projects each have a set of predefined cloud resource access roles available:

* [{{ech}} predefined roles](#ech-predefined-roles)
* [{{serverless-full}} predefined roles](#general-assign-user-roles-table)

If you're using {{serverless-full}}, you can optionally [create custom roles in a project](/deploy-manage/users-roles/serverless-custom-roles.md). All custom roles grant the same access as the `Viewer` cloud resource access role with regards to {{ecloud}} privileges. To grant more {{ecloud}} privileges, assign more roles. Users receive a union of all their roles' privileges. To assign a custom role to users, go to **Cloud resource access** and select it from the list under the specific project it was created in.

## {{ech}} predefined roles [ech-predefined-roles]

For {{ech}} deployments, the following predefined roles are available:

* **Admin**: Can manage deployment details, properties and security privileges, and is able to sign on to the deployment with superuser privileges. This role can be scoped to one or more deployments. In order to prevent scope expansion, only Admins on all deployments can create new deployments.
* **Editor**: Has the same rights as Admin, except from deployment creation and management of security privileges. Editors are able to sign on to the deployment with the “editor” stack role. This role can be scoped to one or more deployments.
* **Viewer**: Can view deployments, and can sign on to the deployment with the viewer Stack role. This role can be scoped to one or more deployments.


### Mapping of {{ecloud}} roles with {{stack}} roles [ec-stack-user-org-member]

There are two ways for a user to access {{kib}} instances of an {{ech}} deployment:

* [Directly with {{es}} credentials](/deploy-manage/users-roles/cluster-or-deployment-auth.md). In this case, users and their roles are managed directly in {{kib}}. Users in this case don’t need to be members of the {{ecloud}} organization to access the deployment. If you have several deployments, you need to manage users for each of them, individually.
* Through your {{ecloud}} organization. In this case, users who are members of your organization log in to {{ecloud}} and can open the deployments they have access to. Their access level is determined by the roles assigned to them from the **Organization** page. {{ecloud}} roles are mapped to [{{stack}} roles](elasticsearch://reference/elasticsearch/roles.md) on a per-deployment level. When logging in to a specific deployment, users get the stack role that maps to their {{ecloud}} role for that particular deployment.

The following table shows the default mapping:

| Cloud role | Cloud API `role_id` | Stack role |
| --- | --- | --- |
| Organization owner | `organization-admin` | superuser |
| Billing admin | `billing-admin` | none |
| Admin | `deployment-admin` | superuser |
| Editor | `deployment-editor` | editor |
| Viewer | `deployment-viewer` | viewer |

## {{serverless-full}} predefined roles [general-assign-user-roles-table]

You can apply the following predefined roles to {{serverless-full}} projects. Some roles are only available to certain project types.

In the following table, the privileges outlined in **Project access** require [**Cloud, {{es}} and {{kib}} API** access](#api-access) to be granted for the relevant projects.

:::{tip}
You can optionally [create custom roles in a project](/deploy-manage/users-roles/cloud-organization/user-roles.md) and apply them to your organization users.
:::

| Name | {{ecloud}} access | Project access | Availability |
| --- | --- | --- | --- |
| Admin | Has full access to project management, properties, and security privileges. | Superuser role privileges | [![{{es}}](/deploy-manage/images/serverless-es-badge.svg "")](../../../solutions/search.md)[![{{observability}}](/deploy-manage/images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Developer | Viewer | Creates API keys, indices, data streams, adds connectors, and builds visualizations. | [![{{es}}](/deploy-manage/images/serverless-es-badge.svg "")](../../../solutions/search.md) |
| Viewer | Has read-only access to project details, data, and features. | None | [![{{es}}](/deploy-manage/images/serverless-es-badge.svg "")](../../../solutions/search.md)[![{{observability}}](/deploy-manage/images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Editor | Configures all {{observability}} or Security projects. | Has read-only access to data indices. Has full access to all project features. | [![{{observability}}](/deploy-manage/images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Tier 1 analyst | Viewer | Ideal for initial alert triage. General read access, can create dashboards and visualizations. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Tier 2 analyst | Viewer | Ideal for alert triage and beginning the investigation process. Can create cases. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Tier 3 analyst | Viewer | Deeper investigation capabilities. Access to rules, lists, cases, Osquery, and response actions. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Threat intelligence analyst | Viewer | Access to alerts, investigation tools, and intelligence pages. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Rule author | Viewer | Access to detection engineering and rule creation. Can create rules from available data sources and add exceptions to reduce false positives. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| SOC manager | Viewer | Access to alerts, cases, investigation tools, endpoint policy management, and response actions. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Endpoint operations analyst | Viewer | Access to endpoint response actions. Can manage endpoint policies, {{fleet}}, and integrations. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Platform engineer | Viewer | Access to {{fleet}}, integrations, endpoints, and detection content. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Detections admin | Viewer | All available detection engine permissions to include creating rule actions, such as notifications to third-party systems. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Endpoint policy manager | Viewer | Access to endpoint policy management and related artifacts. Can manage {{fleet}} and integrations. | [![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |

## Role scopes [ec-role-scoping]

Roles are assigned to every member of an organization and can refer (or be scoped) to one or more specific deployments, or all deployments. When a role is scoped to all deployments it grants permissions on all existing and future deployments.

This list describes the scope of the different roles:

* **Organization owner**: This role is always scoped to administer all deployments.
* **Billing admin**: This role does not refer to any deployment.
* **Cloud resource access roles**, including **Admin**: These roles can be scoped to either all deployments or projects, or specific deployments, project types, or projects.

Members are only able to see the role assignments of other members under the organization they belong to, for role assignments they are able to manage. Members with the **Organization owner** role assigned are able to see the role assignments of every member of their organization.

Members with the **Admin** role assigned are able to see role assignments for deployments or projects within their scope. For example, admins of all deployments and projects are able to see role assignments scoped to all and specific deployments and projects in the organization, while admins of specific deployments or projects only see role assignments scoped to those specific deployments or projects. This ensures that members assigned to specific deployments or projects do not try to remove role assignments from other members, and that the existence of other deployments or projects are not revealed to these members.

## API access
```{applies_to}
serverless: ga
```
When you grant **Organization owner** access, or **Cloud resource** access for one or more Serverless projects, you can also select the user's level of API access:

* **Cloud API**: Grants access to only the {{ecloud}} console for the relevant Serverless projects.
* **Cloud, {{es}} and {{kib}} API**: Grants access to the {{ecloud}} console and the relevant Serverless projects ("Project access"). 

The **API access** selection impacts the behavior of the selected role. To take full effect, most roles need **Cloud, {{es}} and {{kib}} API** access to be granted. However, you might choose to only grant **Cloud API** access if the user does not need to interact with the project directly.

When **Cloud, {{es}} and {{kib}} API** access is not granted, roles that are designed to work inside of the project have limited access, and can't open the project in {{kib}}. For example: 

* If you select the **Admin** role, the user won't be able to log into the relevant projects as superuser.
* Several predefined roles that are intended for project users, such as the Security **Tier 1 analyst** role, will only have **Viewer** access to the relevant projects.

To learn about the permissions that require **Cloud, {{es}} and {{kib}} API** access for each predefined role, refer to the **Project access** column in the [predefined roles table](#general-assign-user-roles-table).

If you apply a [custom role](/deploy-manage/users-roles/serverless-custom-roles.md), then you must always select **Cloud, {{es}} and {{kib}} API** access for the role to take full effect. If you don't grant this access, then the user only has the equivalent of **Viewer** access to the project in the {{ecloud}} console, and can't log in to the project.