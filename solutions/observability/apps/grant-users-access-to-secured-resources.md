---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-feature-roles.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-feature-roles.html
---

# Grant users access to secured resources [observability-synthetics-feature-roles]

You can use role-based access control to grant users access to secured resources. The roles that you set up depend on your organization’s security requirements and the minimum privileges required to use specific features.

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

Typically you need the create the following separate roles:

* [Setup role](../../../solutions/observability/apps/setup-role.md) for enabling Monitor Management.
* [Writer role](../../../solutions/observability/apps/writer-role.md)  for creating, modifying, and deleting monitors.
* [Reader role](../../../solutions/observability/apps/reader-role.md) for {{kib}} users who need to view and create visualizations that access Synthetics data.

{{es-security-features}} provides [built-in roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) that grant a subset of the privileges needed by Synthetics users. When possible, assign users the built-in roles to minimize the affect of future changes on your security strategy. If no built-in role is available, you can assign users the privileges needed to accomplish a specific task.

In general, these are types of privileges you’ll work with:

* **{{es}} cluster privileges**: Manage the actions a user can perform against your cluster.
* **{{es}} index privileges**: Control access to the data in specific indices your cluster.
* **{{kib}} space privileges**: Grant users write or read access to features and apps within {{kib}}.

:::

:::{tab-item} Serverless
:sync: serverless

* **Viewer**:

    * View and create visualizations that access Synthetics data.

* **Editor**:

    * Create, modify, and delete monitors.
    * View and create visualizations that access Synthetics data.

* **Admin**:

    * Full access to project management, properties, and security privileges.
    * Create, modify, and delete monitors.
    * View and create visualizations that access Synthetics data.


Read more about user roles in [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md).

:::

::::