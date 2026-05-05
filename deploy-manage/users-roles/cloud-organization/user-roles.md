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

1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the navigation menu, select **Organization** > **Members**.
3. Select the user on the **Members** tab of the **Organization** page.
4. Click **Edit** to change the user's roles.

:::{note}
The ability to view and manage role assignments depends on your roles and scope. **Organization owners** can manage role assignments for all members, while members with the **Admin** role can only manage assignments for deployments or projects within their scope.

Role assignments and resources outside your scope are not visible.
:::

## Types of roles

There are three categories of roles you can assign to users:

* **Organization-level roles:** These roles apply to the entire organization and are not specific to any resource.
* **Cloud resource access roles:** These roles are specific to each serverless project or hosted deployment.
* **Connected cluster access roles:** Grant access to {{ecloud}} services for clusters you connect through [Cloud Connect](/deploy-manage/cloud-connect.md).

### Organization-level roles [ec_organization_level_roles]

* **Organization owner**: This role is assigned by default to the user who created the organization.

    Organization owners have full access to {{ecloud}} for the organization. They can manage {{ech}} deployments, {{serverless-full}} projects, and clusters linked through [Cloud Connect](/deploy-manage/cloud-connect.md). They can also manage members, organization settings, billing, and subscription details.

* **Billing admin**: Can manage an organization’s billing details such as credit card information, subscription and invoice history. Cannot manage other organization or deployment details and properties.

### Cloud resource access roles [ec_instance_access_roles]

You can set cloud resource access roles at two levels:

* **Globally**, for all {{ech}} deployments, or for all {{serverless-full}} projects of the same type ({{es-serverless}}, {{observability}}, or {{elastic-sec}}). In this case, the role will also apply to new deployments, or projects of the specified type, created later.
* **Individually**, for specific deployments or projects only. To do that, you have to leave the **Role for all hosted deployments** field, or the **Role for all** for the project type, blank.

{{ech}} deployments and {{serverless-full}} projects each have a set of predefined cloud resource access roles available:

* [{{ech}} predefined roles](#ech-predefined-roles)
* [{{serverless-full}} predefined roles](#general-assign-user-roles-table)

If you're using {{serverless-full}}, you can optionally [create custom roles in a project](/deploy-manage/users-roles/serverless-custom-roles.md). All custom roles grant the same access as the `Viewer` cloud resource access role with regards to {{ecloud}} privileges. To grant more {{ecloud}} privileges, assign more roles. Users receive a union of all their roles' privileges. To assign a custom role to users, go to **Cloud resource access** and select it from the list under the specific project it was created in.

### Connected cluster access roles [ec_connected_cluster_access_roles]

These roles apply when your organization uses [Cloud Connect](/deploy-manage/cloud-connect.md) to link self-managed, {{ece}}, or {{eck}} clusters to {{ecloud}} services. Role assignments can be scoped to all connected clusters in the organization or to specific clusters.

The predefined roles for connected clusters are:

* **Admin**: Members assigned this role for all connected clusters can connect new clusters to the organization or disconnect existing ones.

* **Viewer**: Provides read-only access to {{ecloud}} services that interact with connected clusters.

The exact permissions granted by **Admin** and **Viewer** depend on the {{ecloud}} service used with Cloud Connect. For [AutoOps](/deploy-manage/monitor/autoops.md), refer to [{{ecloud}} roles for AutoOps](/deploy-manage/monitor/autoops/cc-manage-users.md#assign-roles).

:::{note}
As more services become available for use with [Cloud Connect](/deploy-manage/cloud-connect.md), refer to each service’s documentation for role-specific permissions. The role names in {{ecloud}} remain consistent.
:::

## {{ech}} predefined roles [ech-predefined-roles]

For {{ech}} deployments, the following predefined roles are available. Each role defines what users can do in the {{ecloud}} console for deployment management and within the deployment for access to {{kib}} and data.

Roles can be scoped to specific deployments or to all deployments.

| Role name | {{ecloud}} access | Deployment access | Notes |
|---|---|---|---|
| **Admin** | Manage deployment details, properties, and security privileges within their scope | [`superuser` built-in {{es}} role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-superuser), which grants full access to {{kib}}, cluster management, and all data indices | Only Admins scoped to all deployments can create new deployments |
| **Editor** | Manage deployment details and properties within their scope, but cannot create new deployments or manage security | [`editor` built-in {{es}} role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-editor), which grants full access to {{kib}} features and read-only access to user data indices | Some {{es}} HTTP APIs are not available due to limited cluster privileges, such as `GET _cat/indices` |
| **Viewer** | Read-only access to deployments within their scope | [`viewer` built-in {{es}} role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-viewer), which grants read-only access to {{kib}} features and user data indices | |

### Mapping of {{ecloud}} roles with {{stack}} roles [ec-stack-user-org-member]

There are two ways for a user to access {{kib}} instances of an {{ech}} deployment:

* **[Directly with {{es}} credentials](/deploy-manage/users-roles/cluster-or-deployment-auth.md)**. In this case, users and their roles are managed directly in {{kib}}. Users in this case don’t need to be members of the {{ecloud}} organization to access the deployment. If you have several deployments, you need to manage users for each of them, individually.
* **Through your {{ecloud}} organization**. In this case, users who are members of your organization log in to {{ecloud}} and can open the deployments they have access to. Their access level is determined by the roles assigned to them from the **Organization** page. {{ecloud}} roles are mapped to [{{stack}} roles](elasticsearch://reference/elasticsearch/roles.md) on a per-deployment level. When logging in to a specific deployment, users get the stack role that maps to their {{ecloud}} role for that particular deployment.

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

In the following table, the privileges outlined in **Project access** require [**Cloud Console, {{es}}, and {{kib}}** access](#access) to be granted for the relevant projects.

:::{tip}
You can optionally [create custom roles in a project](/deploy-manage/users-roles/serverless-custom-roles.md) and apply them to your organization users.
:::

| Role name | {{ecloud}} access | Project access | Availability |
| --- | --- | --- | --- |
| Admin | Has full access to project management, properties, and security privileges. | Superuser role privileges | [![{{es}}](/deploy-manage/images/serverless-es-badge.svg "")](../../../solutions/search.md)[![{{observability}}](/deploy-manage/images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
| Developer | Manage project settings. | Creates API keys, indices, data streams, adds connectors, and builds visualizations. | [![{{es}}](/deploy-manage/images/serverless-es-badge.svg "")](../../../solutions/search.md) |
| Viewer | Has read-only access to project details. | Has read-only access to project data and features. | [![{{es}}](/deploy-manage/images/serverless-es-badge.svg "")](../../../solutions/search.md)[![{{observability}}](/deploy-manage/images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](/deploy-manage/images/serverless-sec-badge.svg "")](../../../solutions/security.md) |
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

Roles are assigned to every member of an organization. Depending on the role type, assignments can be scoped to specific {{ech}} deployments or {{serverless-short}} projects, connected clusters, or to all resources of a given type. When a role is scoped to all resources, it grants permissions on all existing and future resources of that type.

This list describes the scope of the different roles:

* **Organization owner**: This role is always scoped to administer all deployments, projects and connected clusters.
* **Billing admin**: This role does not refer to any deployment, project, or connected cluster.
* **Cloud resource access roles**, including **Admin**: These roles can be scoped to either all deployments or projects, or specific deployments, project types, or projects.
* **Connected cluster access roles**: These roles can be scoped to either all connected clusters or selected clusters.

## Access options [access]
```{applies_to}
serverless: ga
```
When you grant **Organization owner** access, or **Cloud resource** access for one or more {{serverless-short}} projects, you can select the surfaces the user can access:

| Access | Grants |
| --- | --- |
| **Cloud Console, {{es}}, and {{kib}}** (default) | Grants access to the {{ecloud}} Console, plus the {{kib}} interface and {{es}} service for the applicable projects. |
| **Cloud Console** | Grants access to only the {{ecloud}} Console for the applicable {{serverless-short}} projects. |

### Considerations

The **Access** selection impacts the behavior of the selected role. Most roles require **Cloud Console, {{es}}, and {{kib}}** access to take full effect. However, you might choose to only grant **Cloud Console** access if the user does not need to interact with the project directly.

When **Cloud Console, {{es}}, and {{kib}}** access is not granted, roles that are designed to work inside of the project have limited access, and can't open the project in {{kib}}. For example: 

* If you select the **Admin** role, the user is able configure project settings and network security in {{ecloud}}, but can't log in to the relevant projects as superuser.
* Several predefined roles that are intended for project users, such as the Security **Tier 1 analyst** role, can view the relevant projects on the {{ecloud}} Console home page, but can't open the project to view their dashboards and visualizations.
* [Custom roles](/deploy-manage/users-roles/serverless-custom-roles.md) always require **Cloud Console, {{es}}, and {{kib}}** access. Without it, users have only **Viewer** access in the {{ecloud}} Console, and can't log in to the project.

{applies_to}`serverless: preview` If your organization uses [{{cps}}](/deploy-manage/cross-project-search-config.md), the roles assigned to a user determine what data they can access across linked projects. Users can only see data from a linked project if their role on that project grants the necessary privileges. Refer to [Manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-and-api-key-access).

For details on the permissions granted for each role, refer to the [predefined roles table](#general-assign-user-roles-table).

:::{tip}
When inviting a user to your organization with the {{ecloud}} API, you can set their access surfaces in the invitation request. To grant {{ecloud}} Console-only access, pass an empty `application_id` array in the role assignment. For an example, refer to [Manage users](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-api-organizations).
:::
