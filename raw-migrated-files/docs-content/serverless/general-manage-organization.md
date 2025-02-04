# Manage users and roles [general-manage-organization]

In this article, learn how to:

* [Invite your team](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-manage-access-to-organization): Invite users in your organization to access serverless projects and specify their roles.
* [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles): Assign predefined roles to users in your organization.
* [Join an organization from an existing Elastic Cloud account](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-join-organization-from-existing-cloud-account): Join a new organization and bring over your projects.
* [Leave an organization](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-leave-an-organization): Leave an organization.


## Invite your team [general-manage-access-to-organization]

To allow other users to interact with your projects, you must invite them to join your organization and grant them access to your organization resources and instances.

Alternatively, [configure {{ecloud}} SAML SSO](../../../deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) to enable your organization members to join the {{ecloud}} organization automatically. [preview]

1. Go to the user icon on the header bar and select **Organization**.
2. On the **Members** page, click **Invite members**.
3. Enter the email addresses of the users you want to invite in the textbox.

    To add multiple members, enter the member email addresses, separated by a space.

    Grant access to all projects of the same type with a unique role, or select individual roles for specific projects. For more details about roles, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

4. Click **Send invites**.

    Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation before it expires. If the invite has expired, an admin can resend the invitation.


On the **Members** tab of the **Organization** page, view the list of current members, including status and role.

In the **Actions** column, click the three dots to edit a member’s role or revoke the invite.


## Assign user roles and privileges [general-assign-user-roles]

Within an organization, users can have one or more roles and each role grants specific privileges.

You must assign user roles when you [invite users to join your organization](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-manage-access-to-organization). To subsequently edit the roles assigned to a user:

1. Go to the user icon on the header bar and select **Organization**.
2. Find the user on the **Members** tab of the **Organization** page. Click the member name to view and edit its roles.

There are two types of roles you can assign to users:

* **Oranization-level roles:** These roles apply to the entire organization and are not specific to any serverless project or hosted deployment.
* **Instance access roles:** These roles are specific to each serverless project or hosted deployment.


### Organization-level roles [general-assign-user-roles-organization-level-roles]

* **Organization owner**. Can manage all roles under the organization and has full access to all serverless projects, organization-level details, billing details, and subscription levels. This role is assigned by default to the person who created the organization.
* **Billing admin**. Has access to all invoices and payment methods. Can make subscription changes.


### Instance access roles [general-assign-user-roles-instance-access-roles]

Each serverless project type has a set of predefined roles that you can assign to your organization members. To assign the predefined roles:

* globally, for all projects of the same type ({{es-serverless}}, {{observability}}, or {{elastic-sec}}). In this case, the role will also apply to new projects created later.
* individually, for specific projects only. To do that, you have to set the **Role for all** field of that specific project type to **None**.

For example, assign a user the developer role for a specific {{es-serverless}} project:

:::{image} ../../../images/serverless-individual-role.png
:alt: Individual role
:class: screenshot
:::

You can optionally [create custom roles in a project](../../../deploy-manage/users-roles/cloud-organization/user-roles.md). To assign a custom role to users, go to "Instance access roles" and select it from the list under the specific project it was created in.

$$$general-assign-user-roles-table$$$

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


## Leave an organization [general-leave-an-organization]

On the **Organization** page, click **Leave organization**.

If you’re the only user in the organization, you are able to leave only when you have deleted all projects and don’t have any pending bills.


## Join an organization from an existing Elastic Cloud account [general-join-organization-from-existing-cloud-account]

If you already belong to an organization, and you want to join a new one you will need to leave your existing organzation.

If you want to join a new organization, follow these steps:

1. Make sure you do not have active projects or deployments before you leave your current organization.
2. Delete your projects and clear any bills.
3. Leave your current organization.
4. Ask the administrator to invite you to the organization you want to join.
5. Accept the invitation that you will get by email.
