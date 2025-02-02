# Data tiers [data-tiers]

A *data tier* is a collection of [nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html) within a cluster that share the same [data node role](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles), and a hardware profile that’s appropriately sized for the role. Elastic recommends that nodes in the same tier share the same hardware profile to avoid [hot spotting](../../../troubleshoot/elasticsearch/hotspotting.md).

The data tiers that you use, and the way that you use them, depends on the data’s [category](../../../manage-data/lifecycle.md).

The following data tiers are can be used with each data category:

Content data:

* [Content tier](../../../manage-data/lifecycle/data-tiers.md#content-tier) nodes handle the indexing and query load for non-timeseries indices, such as a product catalog.

Time series data:

* [Hot tier](../../../manage-data/lifecycle/data-tiers.md#hot-tier) nodes handle the indexing load for time series data, such as logs or metrics. They hold your most recent, most-frequently-accessed data.
* [Warm tier](../../../manage-data/lifecycle/data-tiers.md#warm-tier) nodes hold time series data that is accessed less-frequently and rarely needs to be updated.
* [Cold tier](../../../manage-data/lifecycle/data-tiers.md#cold-tier) nodes hold time series data that is accessed infrequently and not normally updated. To save space, you can keep [fully mounted indices](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-searchable-snapshot.html) on the cold tier. These fully mounted indices eliminate the need for replicas, reducing required disk space by approximately 50% compared to the regular indices.
* [Frozen tier](../../../manage-data/lifecycle/data-tiers.md#frozen-tier) nodes hold time series data that is accessed rarely and never updated. The frozen tier stores [partially mounted indices](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) of [{{search-snaps}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-searchable-snapshot.html) exclusively. This extends the storage capacity even further — by up to 20 times compared to the warm tier.

::::{tip}
The performance of an {{es}} node is often limited by the performance of the underlying storage and hardware profile. For example hardware profiles, refer to Elastic Cloud’s [instance configurations](https://www.elastic.co/guide/en/cloud/current/ec-reference-hardware.html). Review our recommendations for optimizing your storage for [indexing](../../../deploy-manage/production-guidance/optimize-performance/indexing-speed.md#indexing-use-faster-hardware) and [search](../../../deploy-manage/production-guidance/optimize-performance/search-speed.md#search-use-faster-hardware).
::::


::::{important}
{{es}} assumes nodes within a data tier share the same hardware profile (such as CPU, RAM, disk capacity). Data tiers with unequally resourced nodes have a higher risk of [hot spotting](../../../troubleshoot/elasticsearch/hotspotting.md).
::::


The way data tiers are used often depends on the data’s category:

* Content data remains on the [content tier](../../../manage-data/lifecycle/data-tiers.md#content-tier) for its entire data lifecycle.
* Time series data may progress through the descending temperature data tiers (hot, warm, cold, and frozen) according to your performance, resiliency, and data retention requirements.

    You can automate these lifecycle transitions using the [data stream lifecycle](../../../manage-data/data-store/index-types/data-streams.md), or custom [{{ilm}}](../../../manage-data/lifecycle/index-lifecycle-management.md).



## Available data tiers [available-tier]

Learn more about each data tier, including when and how it should be used.


### Content tier [content-tier]

Data stored in the content tier is generally a collection of items such as a product catalog or article archive. Unlike time series data, the value of the content remains relatively constant over time, so it doesn’t make sense to move it to a tier with different performance characteristics as it ages. Content data typically has long data retention requirements, and you want to be able to retrieve items quickly regardless of how old they are.

Content tier nodes are usually optimized for query performance—​they prioritize processing power over IO throughput so they can process complex searches and aggregations and return results quickly. While they are also responsible for indexing, content data is generally not ingested at as high a rate as time series data such as logs and metrics. From a resiliency perspective the indices in this tier should be configured to use one or more replicas.

The content tier is required and is often deployed within the same node grouping as the hot tier. System indices and other indices that aren’t part of a data stream are automatically allocated to the content tier.


### Hot tier [hot-tier]

The hot tier is the {{es}} entry point for time series data and holds your most-recent, most-frequently-searched time series data. Nodes in the hot tier need to be fast for both reads and writes, which requires more hardware resources and faster storage (SSDs). For resiliency, indices in the hot tier should be configured to use one or more replicas.

The hot tier is required. New indices that are part of a [data stream](../../../manage-data/data-store/index-types/data-streams.md) are automatically allocated to the hot tier.


### Warm tier [warm-tier]

Time series data can move to the warm tier once it is being queried less frequently than the recently-indexed data in the hot tier. The warm tier typically holds data from recent weeks. Updates are still allowed, but likely infrequent. Nodes in the warm tier generally don’t need to be as fast as those in the hot tier. For resiliency, indices in the warm tier should be configured to use one or more replicas.


### Cold tier [cold-tier]

When you no longer need to search time series data regularly, it can move from the warm tier to the cold tier. While still searchable, this tier is typically optimized for lower storage costs rather than search speed.

For better storage savings, you can keep [fully mounted indices](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-searchable-snapshot.html) on the cold tier. Unlike regular indices, these fully mounted indices don’t require replicas for reliability. In the event of a failure, they can recover data from the underlying snapshot instead. This potentially halves the local storage needed for the data. A snapshot repository is required to use fully mounted indices in the cold tier. Fully mounted indices are read-only.

Alternatively, you can use the cold tier to store regular indices with replicas instead of using {{search-snaps}}. This lets you store older data on less expensive hardware but doesn’t reduce required disk space compared to the warm tier.


### Frozen tier [frozen-tier]

Once data is no longer being queried, or being queried rarely, it may move from the cold tier to the frozen tier where it stays for the rest of its life.

The frozen tier requires a snapshot repository. The frozen tier uses [partially mounted indices](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) to store and load data from a snapshot repository. This reduces local storage and operating costs while still letting you search frozen data. Because {{es}} must sometimes fetch frozen data from the snapshot repository, searches on the frozen tier are typically slower than on the cold tier.


## Configure data tiers [configure-data-tiers]

Follow the instructions for your deployment type to configure data tiers.


### {{ess}} or {{ece}} [configure-data-tiers-cloud]

The default configuration for an {{ecloud}} deployment includes a shared tier for hot and content data. This tier is required and can’t be removed.

To add a warm, cold, or frozen tier when you create a deployment:

1. On the **Create deployment** page, click **Advanced Settings**.
2. Click **+ Add capacity** for any data tiers to add.
3. Click **Create deployment** at the bottom of the page to save your changes.

:::{image} ../../../images/elasticsearch-reference-ess-advanced-config-data-tiers.png
:alt: {{ecloud}}'s deployment Advanced configuration page
:class: screenshot
:::

To add a data tier to an existing deployment:

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.
3. In your deployment menu, select **Edit**.
4. Click **+ Add capacity** for any data tiers to add.
5. Click **Save** at the bottom of the page to save your changes.

To remove a data tier, refer to [Disable a data tier](../../../manage-data/lifecycle/index-lifecycle-management.md).


### Self-managed deployments [configure-data-tiers-on-premise]

For self-managed deployments, each node’s [data role](../../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role) is configured in `elasticsearch.yml`. For example, the highest-performance nodes in a cluster might be assigned to both the hot and content tiers:

```yaml
node.roles: ["data_hot", "data_content"]
```

::::{note}
We recommend you use [dedicated nodes](../../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) in the frozen tier.
::::



## Data tier index allocation [data-tier-allocation]

The [`index.routing.allocation.include._tier_preference`](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-tier-shard-filtering.html#tier-preference-allocation-filter) setting determines which tier the index should be allocated to.

When you create an index, by default {{es}} sets the `_tier_preference` to `data_content` to automatically allocate the index shards to the content tier.

When {{es}} creates an index as part of a [data stream](../../../manage-data/data-store/index-types/data-streams.md), by default {{es}} sets the `_tier_preference` to `data_hot` to automatically allocate the index shards to the hot tier.

At the time of index creation, you can override the default setting by explicitly setting the preferred value in one of two ways:

* Using an [index template](../../../manage-data/data-store/templates.md). Refer to [Automate rollover with ILM](../../../manage-data/lifecycle/index-lifecycle-management.md) for details.
* Within the [create index](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) request body.

You can override this setting after index creation by [updating the index setting](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-update-settings.html) to the preferred value.

This setting also accepts multiple tiers in order of preference. This prevents indices from remaining unallocated if no nodes are available in the preferred tier. For example, when {{ilm}} migrates an index to the cold phase, it sets the index `_tier_preference` to `data_cold,data_warm,data_hot`.

To remove the data tier preference setting, set the `_tier_preference` value to `null`. This allows the index to allocate to any data node within the cluster. Setting the `_tier_preference` to `null` does not restore the default value. Note that, in the case of managed indices, a [migrate](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-migrate.html) action might apply a new value in its place.


### Determine the current data tier preference [data-tier-allocation-value]

You can check an existing index’s data tier preference by [polling its settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-settings.html) for `index.routing.allocation.include._tier_preference`:

```console
GET /my-index-000001/_settings?filter_path=*.settings.index.routing.allocation.include._tier_preference
```


### Troubleshooting [data-tier-allocation-troubleshooting]

The `_tier_preference` setting might conflict with other allocation settings. This conflict might prevent the shard from allocating. A conflict might occur when a cluster has not yet been completely [migrated to data tiers](../../../troubleshoot/elasticsearch/troubleshoot-migrate-to-tiers.md).

This setting will not unallocate a currently allocated shard, but might prevent it from migrating from its current location to its designated data tier. To troubleshoot, call the [cluster allocation explain API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-allocation-explain.html) and specify the suspected problematic shard.


### Automatic data tier migration [data-tier-migration]

{{ilm-init}} automatically transitions managed indices through the available data tiers using the [migrate](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-migrate.html) action. By default, this action is automatically injected in every phase. You can explicitly specify the migrate action with `"enabled": false` to [disable automatic migration](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-migrate.html#ilm-disable-migrate-ex), for example, if you’re using the [allocate action](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-allocate.html) to manually specify allocation rules.
