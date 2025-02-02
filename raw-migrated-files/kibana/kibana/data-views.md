# Create a {{data-source}} [data-views]

{{kib}} requires a {{data-source}} to access the {{es}} data that you want to explore. A {{data-source}} can point to one or more indices, [data streams](../../../manage-data/data-store/index-types/data-streams.md), or [index aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html). For example, a {{data-source}} can point to your log data from yesterday, or all indices that contain your data.


## Required permissions [data-views-read-only-access]

* Access to **Data Views** requires the [{{kib}} privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) `Data View Management`.
* To create a {{data-source}}, you must have the [{{es}} privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) `view_index_metadata`.
* If a read-only indicator appears in {{kib}}, you have insufficient privileges to create or save {{data-sources}}. In addition, the buttons to create {{data-sources}} or save existing {{data-sources}} are not visible. For more information, refer to [Granting access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md).


## Create a data view [settings-create-pattern]

If you collected data using one of the {{kib}} [ingest options](../../../manage-data/ingest.md), uploaded a file, or added sample data, you get a {{data-source}} for free, and can start exploring your data. If you loaded your own data, follow these steps to create a {{data-source}}.

1. Open **Lens** or **Discover**, and then open the data view menu.

    :::{image} ../../../images/kibana-discover-data-view.png
    :alt: How to set the {{data-source}} in Discover
    :class: screenshot
    :::

2. Click **Create a {{data-source}}**.
3. Give your {{data-source}} a name.
4. Start typing in the **Index pattern** field, and {{kib}} looks for the names of indices, data streams, and aliases that match your input. You can view all available sources or only the sources that the data view targets.

    ![Create data view](../../../images/kibana-create-data-view.png "")

    * To match multiple sources, use a wildcard (*). `filebeat-*` matches `filebeat-apache-a`, `filebeat-apache-b`, and so on.
    * To match multiple single sources, enter their names, separated by a comma.  Do not include a space after the comma. `filebeat-a,filebeat-b` matches two indices.
    * To exclude a source, use a minus sign (-), for example, `-test3`.

5. Open the **Timestamp field** dropdown, and then select the default field for filtering your data by time.

    * If you don’t set a default time field, you can’t use global time filters on your dashboards. This is useful if you have multiple time fields and want to create dashboards that combine visualizations based on different timestamps.
    * If your index doesn’t have time-based data, choose **I don’t want to use the time filter**.

6. Click **Show advanced settings** to:

    * Display hidden and system indices.
    * Specify your own {{data-source}} name. For example, enter your {{es}} index alias name.

7. $$$reload-fields$$$ Click **Save {{data-source}} to {{kib}}**.

    You can manage your data view from **Stack Management**.



### Create a temporary {{data-source}} [_create_a_temporary_data_source]

Want to explore your data or create a visualization without saving it as a data view? Select **Use without saving** in the **Create {{data-source}}** form in **Discover** or **Lens**. With a temporary {{data-source}}, you can add fields and create an {{es}} query alert, just like you would a regular {{data-source}}.  Your work won’t be visible to others in your space.

A temporary {{data-source}} remains in your space until you change apps, or until you save it.

:::{image} https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte3a4f3994c44c0cc/637eb0c95834861044c21a25/ad-hoc-data-view.gif
:alt: how to create an ad-hoc data view
:class: screenshot
:::

::::{note}
Temporary {{data-sources}} are not available in **Stack Management.**
::::



### Use {{data-sources}} with rolled up data [rollup-data-view]

::::{admonition} Deprecated in 8.11.0.
:class: warning

Rollups are deprecated and will be removed in a future version. Use [downsampling](../../../manage-data/data-store/index-types/downsampling-time-series-data-stream.md) instead.
::::


A {{data-source}} can match one rollup index.  For a combination rollup {{data-source}} with both raw and rolled up data, use the standard notation:

```ts
rollup_logstash,kibana_sample_data_logs
```

For an example, refer to [Create and visualize rolled up data](../../../manage-data/lifecycle/rollup.md#rollup-data-tutorial).


### Use {{data-sources}} with {{ccs}} [management-cross-cluster-search]

If your {{es}} clusters are configured for [{{ccs}}](../../../solutions/search/cross-cluster-search.md), you can create a {{data-source}} to search across the clusters of your choosing. Specify data streams, indices, and aliases in a remote cluster using the following syntax:

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

Once you configure a {{data-source}} to use the {{ccs}} syntax, all searches and aggregations using that {{data-source}} in {{kib}} take advantage of {{ccs}}.

For more information, refer to [Excluding clusters or indicies from cross-cluster search](../../../solutions/search/cross-cluster-search.md#exclude-problematic-clusters).


## Delete a {{data-source}} [delete-data-view]

When you delete a {{data-source}}, you cannot recover the associated field formatters, runtime fields, source filters, and field popularity data. Deleting a {{data-source}} does not remove any indices or data documents from {{es}}.

::::{warning}
Deleting a {{data-source}} breaks all visualizations, saved Discover sessions, and other saved objects that reference the data view.
::::


1. Go to the **Data Views** management page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. Find the {{data-source}} that you want to delete, and then click ![Delete icon](../../../images/kibana-delete.png "") in the **Actions** column.


## {{data-source}} field cache [data-view-field-cache]

The browser caches {{data-source}} field lists for increased performance. This is particularly impactful for {{data-sources}} with a high field count that span a large number of indices and clusters. The field list is updated every couple of minutes in typical {{kib}} usage. Alternatively, use the refresh button on the {{data-source}} management detail page to get an updated field list. A force reload of {{kib}} has the same effect.

The field list may be impacted by changes in indices and user permissions.
