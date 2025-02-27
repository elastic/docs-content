---
navigation_title: "Cross-cluster search"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-cross-cluster-search.html
applies_to:
  stack: all
---



# Cross-cluster search with application data [apm-cross-cluster-search]


Elastic APM utilizes {{es}}'s cross-cluster search functionality. Cross-cluster search lets you run a single search request against one or more [remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md) — making it easy to search APM data across multiple sources. This means you can also have deployments per data type, making sizing and scaling more predictable, and allowing for better performance while managing multiple observability use cases.


## Set up cross-cluster search [apm-set-up-cross-cluster-search]

**Step 1. Set up remote clusters.**

If you’re using the {{ech}}, see [Enable cross-cluster search](../../../deploy-manage/remote-clusters/ec-enable-ccs.md).

To add remote clusters directly in {{kib}}, find `Remote Clusters` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). All you need is a name for the remote cluster and the seed node(s). Remember the names of your remote clusters, you’ll need them in step two. See [managing remote clusters](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md) for detailed information on the setup process.

Alternatively, you can [configure remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md) in {{es}}'s `elasticsearch.yml` file.

**Step 2. Edit the default Applications UI {{data-sources}}.**

Applications UI {{data-sources}} determine which clusters and indices to display data from. {{data-sources-cap}} follow this convention: `<cluster-name>:<index-pattern>`.

To display data from all remote clusters and the local cluster, duplicate and prepend the defaults with `*:`. For example, the default {{data-source}} for Error indices is `logs-apm*,apm*`. To add all remote clusters, change this to `*:logs-apm*,*:apm*,logs-apm*,apm*`

You can also specify certain clusters to display data from, for example, `cluster-one:logs-apm*,cluster-one:apm*,logs-apm*,apm*`.

There are two ways to edit the default {{data-source}}:

* In the Applications UI — Find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Go to **Settings** → **Indices** and change all `xpack.apm.indices.*` values to include remote clusters.
* In `kibana.yml` — Update the [`xpack.apm.indices.*`](asciidocalypse://docs/kibana/docs/reference/configuration-reference/apm-settings.md) configuration values to include remote clusters.

::::{tip}

In a cross-cluster search (CCS) environment, it’s possible for different clusters to serve different data tiers in responses. If one of the requested clusters responds slowly, it can cause a timeout at the proxy after 320 seconds. This results in 502 Bad Gateway server error responses presented as failure toast messages in the UI, and no data loaded.

To prevent this, you can exclude [data tiers](../../../manage-data/lifecycle/data-tiers.md) that might slow down responses from search: the `data_frozen` and `data_cold` tiers. To exclude data tiers from search in the APM UI:

1. To open **Advanced settings**, find **Stack Management** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Observability** section, update the **Excluded data tiers from search** option with a list of data tiers.

::::
