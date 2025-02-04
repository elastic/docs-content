---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-role-setup.html
---

# Setup role [synthetics-role-setup]

Administrators who set up Synthetics typically need to enable Monitor Management.

Monitor Management will be enabled automatically when a user with the required permissions loads the Synthetics UI. This must be completed just once by an admin before any users with the [Writer role](writer-role.md) can create synthetic monitors. This applies to monitors created via both [projects](create-monitors-with-project-monitors.md) and [the UI](create-monitors-in-synthetics-app.md).

As a best practice, **grant the setup role to administrators only**, and use a more restrictive role for event publishing.

Create a **setup role**, called something like `synthetics_setup`:

1. Start with the `editor` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md). This role grants full access to all features in {{kib}} (including the {{observability}} solution) and read-only access to data indices.

    ::::{note} 
    The `editor` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) will grant write access to *all* {{kib}} apps. If you want to limit write access to the {{synthetics-app}} only, refer to [Limited write access](writer-role.md#synthetics-write-privileges-limited).

    If you choose this approach, you will still need to grant the privileges in the next step.

    ::::

2. Grant the role additional privileges that are required to enable Monitor Management:

    1. Grant all of the following privileges:

        | Type | Privilege | Purpose |
        | --- | --- | --- |
        | [Cluster](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster) | `monitor` | Allows the user to retrieve cluster details. |
        | [Cluster](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster) | `manage_ilm` | Allows the user access to all index lifecycle management operations related to managing policies. |
        | [Cluster](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster) | `read_pipeline` | Gives the user read-only access to the ingest pipline. |
        | [Index](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) | `synthetics-*`: `view_index_metadata` | Gives the user read-only access to index and data stream metadata. |
        | [Index](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) | `synthetics-*`: `create_doc` | Allows the user to index documents. |
        | [Index](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) | `synthetics-*`: `auto_configure` | Permits auto-creation of indices and data streams. |
        | [Index](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) | `synthetics-*`: `monitor` | Gives access to all actions that are required for monitoring (recovery, segments info, index stats, and status). |


::::{note} 
If users with the setup role also need to create, modify, and delete monitors, add the privileges defined in the [writer role](writer-role.md).
::::


