---
description: Index pattern syntax for pointing a Kibana data view at rolled up data, another cluster, or another project.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Data view search syntax [data-view-search-syntax]

When you [create a data view](create-data-view.md), the index pattern can use the following syntax to reach rolled up data, or data in other clusters or projects.

## Rolled up data [rollup-data-view]
```{applies_to}
serverless: unavailable
stack: deprecated
```

::::{admonition}
:class: warning

Rollups are deprecated. Use [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) instead.
::::

A {{data-source}} can match one rollup index. For a combination rollup {{data-source}} with both raw and rolled up data, use the standard notation:

```ts
rollup_logstash,kibana_sample_data_logs
```

For an example, refer to [Create and visualize rolled up data](/manage-data/lifecycle/rollup/getting-started-kibana.md#rollup-data-tutorial).

## {{ccs-cap}} [management-cross-cluster-search]
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

## {{cps-cap}} [management-cross-project-search]
```{applies_to}
serverless: preview
stack: unavailable
```

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), the {{data-source}} creation form previews matching indices from linked projects based on the current [{{cps}} scope](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana). The {{data-source}} itself doesn't store the scope. When you query the {{data-source}}, results come from whichever linked projects the active {{cps}} scope includes at that time.

To restrict a {{data-source}} to specific projects regardless of the active scope, you can:

* Use [qualified expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) in the index pattern to target specific projects, for example `project_alpha:logs-*,project_beta:logs-*`. To search only the origin project, use `_origin:logs-*`.
* Use [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) in your queries to narrow scope at query time.

## Related pages

* [Create a data view](create-data-view.md)
* [Data views](../data-views.md)
