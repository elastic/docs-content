---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-feature-roles.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-feature-roles.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Grant users access to secured resources [observability-synthetics-feature-roles]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

Typically you need to create the following separate roles:

* [Setup role](/solutions/observability/synthetics/setup-role.md) for enabling Monitor Management.
* [Writer role](/solutions/observability/synthetics/writer-role.md)  for creating, modifying, and deleting monitors.
* [Reader role](/solutions/observability/synthetics/reader-role.md) for {{kib}} users who need to view and create visualizations that access Synthetics data.

{{es-security-features}} provides [built-in roles](elasticsearch://reference/elasticsearch/roles.md) that grant a subset of the privileges needed by Synthetics users. When possible, assign users the built-in roles to minimize the affect of future changes on your security strategy. If no built-in role is available, you can assign users the privileges needed to accomplish a specific task.

In general, you'll work with the following privilege types:

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

Read more about user roles in [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).

:::

::::

### Allow users to view global parameter values [observability-synthetics-view-global-params]

```{applies_to}
stack: ga 9.1
serverless: ga
```

By default, users with custom roles do not have access to global parameter values. Administrators can grant read access to global parameters by adding the Synthetics **Can read global parameter values** {{kib}} privilege to a role. When added, users can view a global parameter value using the [**Get parameters** API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-parameters).