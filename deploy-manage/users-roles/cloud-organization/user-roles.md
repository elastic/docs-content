---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-user-privileges.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
applies_to:
  deployment:
    ess: all
    serverless: all
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

1. Go to the user icon on the header bar and select **Organization**.
2. Find the user on the **Members** tab of the **Organization** page. Click the member name to view their roles. 
3. Click **Edit** to change the user's roles.

## Types of roles

There are two types of roles you can assign to users:

* **Oranization-level roles:** These roles apply to the entire organization and are not specific to any serverless project or hosted deployment.
* **Instance access roles:** These roles are specific to each serverless project or hosted deployment.

### Organization-level roles [ec_organization_level_roles]

* **Organization owner**: The role assigned by default to the user who created the organization. Organization owners have all privileges to instances ({{ech}} deployments and {{serverless-full}} projects), users, organization-level details and properties, billing details and subscription levels. They are also able to sign on to deployments with superuser privileges.
* **Billing admin**: Can manage an organization’s billing details such as credit card information, subscription and invoice history. Cannot manage other organization or deployment details and properties.

### Instance access roles [ec_instance_access_roles]

You can set instance access roles at two levels:

* **Globally**, for all {{ech}} deployments, or for all {{serverless-full}} projects of the time type ({{es-serverless}}, {{observability}}, or {{elastic-sec}}). In this case, the role will also apply to new deployments, or projects of the specified type type, created later.
* **Individually**, for specific deployments or projects only. To do that, you have to leave the **Role for all hosted deployments** field, or the **Role for all** for the project type, blank.

{{ech}} deployments and {{serverless-full}} projects each have a set of predefined instance access roles available: 

* [{{ech}} predefined roles](#ech-predefined-roles)
* [{{serverless-full}} predefined roles](#general-assign-user-roles-table)

If you're using {{serverless-full}}, you can optionally [create custom roles in a project](/deploy-manage/users-roles/cloud-organization/user-roles.md). All custom roles grant the same access as the `Viewer` instance access role with regards to {{ecloud}} privileges. To grant more {{ecloud}} privileges, assign more roles. Users receive a union of all their roles' privileges.To assign a custom role to users, go to **Instance access roles** and select it from the list under the specific project it was created in.

## {{ech}} predefined roles [ech-predefined-roles]

For {{ech}} deployments, the following predefined roles are available:

* **Admin**: Can manage deployment details, properties and security privileges, and is able to sign on to the deployment with superuser privileges. This role can be scoped to one or more deployments. In order to prevent scope expansion, only Admins on all deployments can create new deployments.
* **Editor**: Has the same rights as Admin, except from deployment creation and management of security privileges. Editors are able to sign on to the deployment with the “editor” stack role. This role can be scoped to one or more deployments.
* **Viewer**: Can view deployments, and can sign on to the deployment with the viewer Stack role. This role can be scoped to one or more deployments.


### Mapping of {{ecloud}} roles with {{stack}} roles [ec-stack-user-org-member]

There are two ways for a user to access {{kib}} instances of an {{ech}} deployment:

* [Directly with {{es}} credentials](/deploy-manage/users-roles/cluster-or-deployment-auth.md). In this case, users and their roles are managed directly in {{kib}}. Users in this case don’t need to be members of the {{ecloud}} organization to access the deployment. Note that if you have several deployments, you need to manage users for each of them, individually.
* Through your {{ecloud}} organization. In this case, users who are members of your organization log in to {{ecloud}} and can open the deployments they have access to. Their access level is determined by the roles assigned to them from the **Organization** page. {{ecloud}} roles are mapped to [Stack roles](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md#built-in-roles) on a per-deployment level. When logging in to a specific deployment, users get the stack role that maps to their {{ecloud}} role for that particular deployment.

The following table shows the default mapping:

|  Cloud role  |  Cloud API `role_id`  |  Stack role   |
| --- | --- | --- |
| Organization owner | `organization-admin` | superuser |
| Billing admin | `billing-admin` | none |
| Admin | `deployment-admin` | superuser |
| Editor | `deployment-editor` | editor |
| Viewer | `deployment-viewer` | viewer |

## {{serverless-full}} predefined roles [general-assign-user-roles-table]

You can apply the following predefined roles to {{serverless-full}} projects. Some roles are only available to certain project types.

:::{tip}
You can optionally [create custom roles in a project](/deploy-manage/users-roles/cloud-organization/user-roles.md) and apply them to your organization users.
:::

| Name | Description | Available |
| --- | --- | --- |
| Admin | Has full access to project management, properties, and security privileges. Admins log into projects with superuser role privileges. | [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md)[![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Developer | Creates API keys, indices, data streams, adds connectors, and builds visualizations. | [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) |
| Viewer | Has read-only access to project details, data, and features. | [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md)[![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Editor | Configures all Observability or Security projects. Has read-only access to data indices. Has full access to all project features. | [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md)[![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Tier 1 analyst | Ideal for initial alert triage. General read access, can create dashboards and visualizations. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Tier 2 analyst | Ideal for alert triage and beginning the investigation process. Can create cases. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Tier 3 analyst | Deeper investigation capabilities. Access to rules, lists, cases, Osquery, and response actions. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Threat intelligence analyst | Access to alerts, investigation tools, and intelligence pages. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Rule author | Access to detection engineering and rule creation. Can create rules from available data sources and add exceptions to reduce false positives. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| SOC manager | Access to alerts, cases, investigation tools, endpoint policy management, and response actions. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Endpoint operations analyst | Access to endpoint response actions. Can manage endpoint policies, {{fleet}}, and integrations. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Platform engineer | Access to {{fleet}}, integrations, endpoints, and detection content. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Detections admin | All available detection engine permissions to include creating rule actions, such as notifications to third-party systems. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |
| Endpoint policy manager | Access to endpoint policy management and related artifacts. Can manage {{fleet}} and integrations. | [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md) |

## Role scopes [ec-role-scoping]

Roles are assigned to every member of an organization and can refer (or be scoped) to one or more specific deployments, or all deployments. When a role is scoped to all deployments it grants permissions on all existing and future deployments.

This list describes the scope of the different roles:

* **Organization owner**: This role is always scoped to administer all deployments.
* **Billing admin**: This role does not refer to any deployment.
* **Instance access roles**, including **Admin**: These roles can be scoped to either all deployments or projects, or specific deployments, project types, or projects.

Members are only able to see the role assignments of other members under the organization they belong to, for role assignments they are able to manage. Members with the **Organization owner** role assigned are able to see the role assignments of every member of their organization.

Members with the **Admin** role assigned are able to see role assignments for deployments or projects within their scope. For example, admins of all deployments and projects are able to see role assignments scoped to all and specific deployments and projects in the organization, while admins of specific deployments or projects only see role assignments scoped to those specific deployments or projects. This ensures that members assigned to specific deployments or projects do not try to remove role assignments from other members, and that the existence of other deployments or projects are not revealed to these members.