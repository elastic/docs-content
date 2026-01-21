---
navigation_title: Configure SLO access
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/slo-privileges.html
products:
  - id: observability
---



# Configure service-level objective (SLO) access [slo-privileges]


::::{important}
To create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions) and an {{es}} cluster with both `transform` and `ingest` [node roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) present.
::::


You can enable access to SLOs in two different ways:

* Creating the following roles, depending on the type of access needed:

    * [**SLO Editor**](#slo-all-access) — Create, edit, and manage SLOs and their historical summaries.
    * [**SLO Viewer**](#slo-read-access) — Check SLOs and their historical summaries.

* Using the `editor` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-editor). This role grants full access to all features in {{kib}} (including the {{observability}} solution) and read-only access to data indices. Users assigned to this role can create, edit, and manage SLOs.

    ::::{note}
    The `editor` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-editor) grants write access to *all* {{kib}} apps. If you want to limit access to the SLOs only, you have to manually create and assign the mentioned roles.

    ::::


To create a role:

1. Open the **Roles** management page by finding it in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Roles** page, click **Create role**.


## Create an SLO Editor role [slo-all-access]

Set the following privileges for the SLO Editor role:

1. Under **Index privileges** in the **Elasticsearch** section, add `.slo-observability.*` to the **Indices** field and `read`, `view_index_metadata`, `write`, and `manage` to the **Privileges** field.
2. Click **Add index privilege**.
3. In the **Indices** field, add the indices for which you plan to create SLOs. Then, add `read` and `view_index_metadata` to the **Privileges** field. The following example shows `logs-*`, but you can specify any indices.

    :::{image} /solutions/images/observability-slo-es-priv-editor.png
    :alt: Cluster and index privileges for SLO Editor role
    :screenshot:
    :::

4. In the **Kibana** section, click **Add Kibana privilege**.
5. From the **Spaces** dropdown, either select any specific spaces you want the role to apply to, or select **All Spaces**.
6. Set **Observability → SLOs** to `All`.

    :::{image} /solutions/images/observability-slo-kibana-priv-all.png
    :alt: SLO Kibana all privileges
    :screenshot:
    :::

7. Click **Create Role** at the bottom of the page and assign the role to the relevant users.


## Create an SLO Viewer role [slo-read-access]

Set the following privileges for the SLO Read role:

1. Under **Index privileges** in the **Elasticsearch** section, add `.slo-observability.*` to the **Indices** field and `read` and `view_index_metadata` to the **Privileges** field.

    :::{image} /solutions/images/observability-slo-es-priv-viewer.png
    :alt: Index privileges for SLO Viewer role
    :screenshot:
    :::

2. In the **Kibana** section, click **Add Kibana privilege**.
3. From the **Spaces** dropdown, either select any specific spaces you want the role to apply to, or select **All Spaces**.
4. Set **Observability → SLOs** to `Read`.

    :::{image} /solutions/images/observability-slo-kibana-priv-read.png
    :alt: SLO Kibana read privileges
    :screenshot:
    :::

5. Click **Create Role** at the bottom of the page and assign the role to the relevant users.
