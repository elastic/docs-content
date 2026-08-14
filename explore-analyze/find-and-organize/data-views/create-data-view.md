---
description: Create a Kibana data view so Discover, Lens, and other analytics features can access your Elasticsearch indices, data streams, or aliases.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create a data view

Create a {{data-source}} to make your own {{es}} data available in **Discover**, **Lens**, and other analytics features.

## Before you begin [create-data-view-prereqs]

* You need a role with the **Data View Management** {{kib}} privilege and the `view_index_metadata` {{es}} privilege. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
* If a **Read only** badge appears, you don't have sufficient privileges to create or save {{data-sources}}. The create control is unavailable.
* You need data already indexed into {{es}}. Some workflows create a {{data-source}} for you automatically instead. Refer to [How data views are created](../data-views.md#data-views-how-you-get-one).

## Create the data view [create-data-view-steps]

1. Open the create form:

   * In **Discover** or **Lens**, open the data view menu, then select **Create a {{data-source}}**.
   * Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create data view**.

   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: Data view menu in Discover, with the current data view selected
   :screenshot:
   :width: 50%
   :::

2. In the **Name** field, enter a name for the {{data-source}}.
3. In the **Index pattern** field, enter a pattern. {{kib}} looks for the names of indices, data streams, and aliases that match your input. You can view all available sources or only the sources that the data view targets.

   ![Create data view](/explore-analyze/images/kibana-create-data-view.png "")

    * To match multiple sources, use a wildcard (`*`). `filebeat-*` matches `filebeat-apache-a`, `filebeat-apache-b`, and so on.
    * To match several individual sources, enter their names, separated by a comma, with no space after the comma. `filebeat-a,filebeat-b` matches two indices.
    * To exclude a source, use a minus sign (`-`), for example `-test3`.

   For data on another cluster, another project, or a rollup index, refer to [What the index pattern matches](#what-the-index-pattern-matches).

4. Open the **Timestamp field** menu, then select the default field for filtering your data by time.

    * If you don't set a default time field, you can't use global time filters on your dashboards. Skip a default time field when you have multiple time fields and want to combine visualizations that use different timestamps.
    * If your index doesn't have time-based data, select **I don't want to use the time filter**.

5. Select **Show advanced settings** to:

    * Allow hidden and system indices.
    * Set a **Custom data view ID**. By default, {{kib}} assigns a randomly generated ID to the {{data-source}} saved object. A custom, human-readable ID (for example, `logs-prod`) makes the {{data-source}} easier to recreate with the same ID across spaces, deployments, or environments. Dashboards and visualizations that reference that ID keep working. Refer to [Manage dashboards as code](/explore-analyze/dashboards/manage-dashboards-as-code.md).

6. $$$reload-fields$$$ Select **Save {{data-source}} to {{kib}}**.

You can now select your new {{data-source}} from the data view menu in **Discover**, **Lens**, and other analytics features. Manage it from the **Data Views** management page.

## What the index pattern matches [what-the-index-pattern-matches]

The **Index pattern** field tells the {{data-source}} which names to query. What you enter depends on where the data lives:

* [Data in this cluster or project](#index-pattern-local): wildcards, comma-separated names, or a minus sign to exclude
* {applies_to}`stack: ga` {applies_to}`serverless: unavailable` [Data on another cluster](#management-cross-cluster-search): `cluster:index` syntax for {{ccs}}
* {applies_to}`serverless: preview` {applies_to}`stack: unavailable` [Data in another project](#management-cross-project-search): qualified expressions for {{cps}}
* {applies_to}`stack: deprecated` {applies_to}`serverless: unavailable` [Rolled-up data](#rollup-data-view): one rollup index, or rollup and raw data together

### Data in this cluster or project [index-pattern-local]

* To match multiple sources, use a wildcard (`*`). `filebeat-*` matches `filebeat-apache-a`, `filebeat-apache-b`, and so on.
* To match several individual sources, enter their names, separated by a comma, with no space after the comma. `filebeat-a,filebeat-b` matches two indices.
* To exclude a source, use a minus sign (`-`), for example `-test3`.

### Data on another cluster [management-cross-cluster-search]
```{applies_to}
serverless: unavailable
stack: ga
```

If your {{es}} clusters are configured for [{{ccs}}](/explore-analyze/cross-cluster-search.md), you can create a {{data-source}} to search across the clusters of your choosing. Specify data streams, indices, and aliases in a remote cluster using the following syntax:

```ts
<remote_cluster_name>:<target>
```

To query {{ls}} indices across two {{es}} clusters that you set up for {{ccs}}, named `cluster_one` and `cluster_two`:

```ts
cluster_one:logstash-*,cluster_two:logstash-*
```

Use wildcards in your cluster names to match any number of clusters. To search {{ls}} indices across clusters named `cluster_foo`, `cluster_bar`, and so on:

```ts
cluster_*:logstash-*
```

To query across all {{es}} clusters that have been configured for {{ccs}}, use a standalone wildcard for your cluster name:

```ts
*:logstash-*
```

To match indices starting with `logstash-`, but exclude those starting with `logstash-old`, from all clusters having a name starting with `cluster_`:

```ts
cluster_*:logstash-*,cluster_*:-logstash-old*
```

Excluding a cluster avoids sending any network calls to that cluster. To exclude a cluster with the name `cluster_one`:

```ts
cluster_*:logstash-*,-cluster_one:*
```

After you configure a {{data-source}} to use the {{ccs}} syntax, all searches and aggregations using that {{data-source}} in {{kib}} take advantage of {{ccs}}.

For more information, refer to [Excluding clusters or indices from cross-cluster search](/explore-analyze/cross-cluster-search.md#exclude-problematic-clusters).

### Data in another project [management-cross-project-search]
```{applies_to}
serverless: preview
stack: unavailable
```

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), the {{data-source}} creation form previews matching indices from linked projects based on the current [{{cps}} scope](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana). The {{data-source}} itself doesn't store the scope. When you query the {{data-source}}, results come from whichever linked projects the active {{cps}} scope includes at that time.

To restrict a {{data-source}} to specific projects regardless of the active scope, you can:

* Use [qualified expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) in the index pattern to target specific projects, for example `project_alpha:logs-*,project_beta:logs-*`. To search only the origin project, use `_origin:logs-*`.
* Use [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) in your queries to narrow scope at query time.

### Rolled-up data [rollup-data-view]
```{applies_to}
serverless: unavailable
stack: deprecated
```

:::{warning}
Rollups are deprecated. Use [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) instead.
:::

A {{data-source}} can match one rollup index. For a combination rollup {{data-source}} with both raw and rolled up data, use the standard notation:

```ts
rollup_logstash,kibana_sample_data_logs
```

For an example, refer to [Create and visualize rolled up data](/manage-data/lifecycle/rollup/getting-started-kibana.md#rollup-data-tutorial).

## Create a temporary {{data-source}} [_create_a_temporary_data_source]

To explore data or build a visualization without saving a {{data-source}}, select **Use without saving** in the **Create {{data-source}}** form in **Discover** or **Lens**. With a temporary {{data-source}}, you can add fields and create an {{es}} query alert, the same way you would with a saved {{data-source}}. Your work isn't visible to others in your space.

A temporary {{data-source}} remains in your space until you change apps, or until you save it.

:::{image} /explore-analyze/images/ad-hoc-data-view.gif
:alt: Create a temporary data view in Discover using Use without saving
:screenshot:
:::

::::{note}
Temporary {{data-sources}} aren't available on the **Data Views** management page. **Use without saving** appears only in **Discover** and **Lens**.
::::

## Related pages

* [Data views](../data-views.md)
* [Delete a data view](delete-data-view.md)
* [Duplicate a data view](duplicate-data-view.md)
