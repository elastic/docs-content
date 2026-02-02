---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-role-write.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Writer role [synthetics-role-write]

::::{important}
To minimize the privileges required by the writer role, use the [setup role](/solutions/observability/synthetics/setup-role.md) to enable Monitor Management. This section assumes another user has already enabled Monitor Management.
::::

For users who need to create, modify, and delete monitors, provide write access. Two types of write access are outlined below:

* **General write access**: For most users, you can use [General write access](#synthetics-write-privileges-general), which grants write access to all {{kib}} apps and requires little configuration.
* **Limited write access**: If you want to limit write access to the {{synthetics-app}} only, you can use [Limited write access](#synthetics-write-privileges-limited), which requires additional configuration.

## General write access [synthetics-write-privileges-general]

Create a **writer role**, called something like `synthetics_writer`:

1. Start with the `editor` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-editor). This role grants full access to all features in {{kib}} (including the {{observability}} solution) and read-only access to data indices.

    ::::{note}
    The `editor` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-editor) will grant write access to *all* {{kib}} apps. If you want to limit write access to the {{synthetics-app}} only, refer to [Limited write access](#synthetics-write-privileges-limited).
    ::::

2. *If the user should have permission to create, modify, and delete project monitors*, they will need an API key that can be used to `push` monitors. To create API keys, the user will also need *at least one* of the following privileges in addition to the privileges included in the `editor` built-in role:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | [Cluster](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) | `manage_own_api_key` | Allows access to all security-related operations on {{es}} API keys that are owned by the current authenticated user. |
    | [Cluster](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) | `manage_security` | Allows access to all security-related operations such as CRUD operations on users and roles and cache clearing. |
    | [Cluster](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) | `manage_api_key` | Allows access to all security-related operations on {{es}} API keys. |

## Limited write access [synthetics-write-privileges-limited]

If you want to limit write access to the {{synthetics-app}} only, do *not* use the `editor` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-editor).

Instead to you can create a writer role, called something like `synthetics_writer_limited`, and start by granting the following privileges:

| Type | Privilege | Purpose |
| --- | --- | --- |
| [Index](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) | `synthetics-*`: `read` | Read-only access to synthetics indices. |
| [Index](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) | `.alerts-observability.uptime.alerts-*`: `read` | Read-only access to synthetics alert indices. |
| [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) | `Synthetics and Uptime`: `All` | Access to the {{synthetics-app}} in {{kib}}. |

Additional privileges will depend on the factors below.

### To restrict using Elastic’s global managed infrastructure [disable-managed-locations]

To restrict users assigned this role from using monitors hosted on Elastic’s global managed infrastructure:

1. Expand `Synthetics and Uptime` in the list of [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) privileges.
2. Toggle *Customize sub-feature privileges*.
3. Uncheck *Elastic managed locations enabled*.

### If using Private Locations [synthetics-role-write-private-locations]

The user who initially sets up a new Private Location needs additional privileges. Users who create or update monitors hosted on that Private Location do not need any additional permissions.

The user who is setting up a new Private Location will need the following privileges when creating the agent policy in {{fleet}}:

| Type | Privilege | Purpose |
| --- | --- | --- |
| [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) | `Fleet`: `All` | Access to Fleet in {{kib}}. |
| [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) | `Integrations`: `read` | Access to Integrations in {{kib}}. |

### If using projects [_if_using_projects]

If the user should be able to create and update monitors using [projects](/solutions/observability/synthetics/get-started.md#observability-synthetics-get-started-synthetics-project), add *at least one* of following privileges:

| Type | Privilege | Purpose |
| --- | --- | --- |
| [Cluster](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) | `manage_own_api_key` | Allows access to all security-related operations on {{es}} API keys that are owned by the current authenticated user. |
| [Cluster](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) | `manage_security` | Allows access to all security-related operations such as CRUD operations on users and roles and cache clearing. |
| [Cluster](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) | `manage_api_key` | Allows access to all security-related operations on {{es}} API keys. |