---
navigation_title: Data tiers
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-tiers.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
  - id: cloud-enterprise
  - id: cloud-hosted
---

# {{es}} data tiers: hot, warm, cold, and frozen storage explained

{{es}} organizes data into storage tiers to balance performance, cost, and accessibility. Each tier—from hot for frequently accessed data to frozen for rarely queried datasets—has specific hardware and storage characteristics. This guide explains how to configure, manage, and automate data placement across tiers for both time series and general content data.

Each *data tier* is a collection of [nodes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md) in an {{es}} cluster that share the same [data node role](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles), and a hardware profile that’s appropriately sized for the role. Elastic recommends that nodes in the same tier share the same hardware profile to avoid [hot spotting](/troubleshoot/elasticsearch/hotspotting.md).

:::{admonition} Serverless manages data storage for you
By abstracting cluster management tasks, {{serverless-full}} adjusts data storage and scaling based on your workload. Certain [project settings](/deploy-manage/deploy/elastic-cloud/project-settings.md) allow you to customize how your data is stored and calibrate the performance of your data.
:::

## Available data tiers [available-tier]

The data tiers that you use, and the way that you use them, depends on the data’s [category](/manage-data/lifecycle.md). The following data tiers are can be used with each data category:

**Content data**:

* [Content tier](/manage-data/lifecycle/data-tiers.md#content-tier) nodes handle the indexing and query load for non-timeseries indices, such as a product catalog.

**Time series data**:

* [Hot tier](/manage-data/lifecycle/data-tiers.md#hot-tier) nodes handle the indexing load for time series data, such as logs or metrics. They hold your most recent, most-frequently-accessed data.
* [Warm tier](/manage-data/lifecycle/data-tiers.md#warm-tier) nodes hold time series data that is accessed less-frequently and rarely needs to be updated.
* [Cold tier](/manage-data/lifecycle/data-tiers.md#cold-tier) nodes hold time series data that is accessed infrequently and not normally updated. To save space, you can keep [fully mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) on the cold tier. These fully mounted indices eliminate the need for replicas, reducing required disk space by approximately 50% compared to the regular indices.
* [Frozen tier](/manage-data/lifecycle/data-tiers.md#frozen-tier) nodes hold time series data that is accessed rarely and never updated. The frozen tier stores [partially mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) of [{{search-snaps}}](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) exclusively. This extends the storage capacity even further — by up to 20 times compared to the warm tier.

::::{tip}
The performance of an {{es}} node is often limited by the performance of the underlying storage and hardware profile. For example hardware profiles, refer to Elastic Cloud’s [instance configurations](cloud://reference/cloud-hosted/hardware.md). Review our recommendations for optimizing your storage for [indexing](/deploy-manage/production-guidance/optimize-performance/indexing-speed.md#indexing-use-faster-hardware) and [search](/deploy-manage/production-guidance/optimize-performance/search-speed.md#search-use-faster-hardware).
::::

::::{important}
{{es}} assumes nodes within a data tier share the same hardware profile (such as CPU, RAM, disk capacity). Data tiers with unequally resourced nodes have a higher risk of [hot spotting](/troubleshoot/elasticsearch/hotspotting.md).
::::

The way data tiers are used often depends on the data’s category:

* Content data remains on the [content tier](/manage-data/lifecycle/data-tiers.md#content-tier) for its entire data lifecycle.
* Time series data may progress through the descending temperature data tiers (hot, warm, cold, and frozen) according to your performance, resiliency, and data retention requirements.

    You can automate these lifecycle transitions using the [data stream lifecycle](/manage-data/data-store/data-streams.md), or custom [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md).

Learn more about each data tier, including when and how it should be used.

### Content tier [content-tier]

Data stored in the content tier is generally a collection of items such as a product catalog or article archive. Unlike time series data, the value of the content remains relatively constant over time, so it doesn’t make sense to move it to a tier with different performance characteristics as it ages. Content data typically has long data retention requirements, and you want to be able to retrieve items quickly regardless of how old they are.

Content tier nodes are usually optimized for query performance—they prioritize processing power over IO throughput so they can process complex searches and aggregations and return results quickly. While they are also responsible for indexing, content data is generally not ingested at as high a rate as time series data such as logs and metrics. From a resiliency perspective the indices in this tier should be configured to use one or more replicas.

The content tier is required and is often deployed within the same node grouping as the hot tier. System indices and other indices that aren’t part of a data stream are automatically allocated to the content tier.


### Hot tier [hot-tier]

The hot tier is the {{es}} entry point for time series data and holds your most-recent, most-frequently-searched time series data. Nodes in the hot tier need to be fast for both reads and writes, which requires more hardware resources and faster storage (SSDs). For resiliency, indices in the hot tier should be configured to use one or more replicas.

The hot tier is required. New indices that are part of a [data stream](/manage-data/data-store/data-streams.md) are automatically allocated to the hot tier.


### Warm tier [warm-tier]

Time series data can move to the warm tier once it is being queried less frequently than the recently-indexed data in the hot tier. The warm tier typically holds data from recent weeks. Updates are still allowed, but likely infrequent. Nodes in the warm tier generally don’t need to be as fast as those in the hot tier. For resiliency, indices in the warm tier should be configured to use one or more replicas.


### Cold tier [cold-tier]

When you no longer need to search time series data regularly, it can move from the warm tier to the cold tier. While still searchable, this tier is typically optimized for lower storage costs rather than search speed.

For better storage savings, you can keep [fully mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) on the cold tier. Unlike regular indices, these fully mounted indices don’t require replicas for reliability. In the event of a failure, they can recover data from the underlying snapshot instead. This potentially halves the local storage needed for the data. A snapshot repository is required to use fully mounted indices in the cold tier. Fully mounted indices are read-only.

Alternatively, you can use the cold tier to store regular indices with replicas instead of using {{search-snaps}}. This lets you store older data on less expensive hardware but doesn’t reduce required disk space compared to the warm tier.


### Frozen tier [frozen-tier]

Once data is no longer being queried, or being queried rarely, it may move from the cold tier to the frozen tier where it stays for the rest of its life.

We recommend you use [dedicated nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) in the frozen tier. The frozen tier requires a snapshot repository and uses [partially mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) to store and load data from the snapshot repository. This reduces local storage and operating costs while still letting you search frozen data. Because {{es}} must sometimes fetch frozen data from the snapshot repository, searches on the frozen tier are typically slower than on the cold tier.

## Configure data tiers [configure-data-tiers]

How you configure data tiers depends on your cluster's deployment type. Use the guide that matches your deployment:

* For **ECH or ECE**, the default {{ecloud}} deployment includes a shared tier for hot and content data, which is required and can’t be removed. To add or remove warm, cold, or frozen capacity in the Elastic Cloud UI, including safe removal with data migration, refer to [Add or remove data tiers in {{ech}} or {{ece}}](/manage-data/lifecycle/data-tiers/manage-data-tiers-ech-ece.md).
* For **Self-managed or ECK**, assign [data roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role) (`data_*`) so your cluster exposes the tiers you need in `elasticsearch.yml` on each host, or under each node set’s `config` in an {{eck}} {{es}} resource. Refer to [Configure data tiers for self-managed and {{eck}} deployments](/manage-data/lifecycle/data-tiers/manage-data-tiers-self-managed-eck.md).

## Data tier index allocation [data-tier-allocation]

The [`index.routing.allocation.include._tier_preference`](elasticsearch://reference/elasticsearch/index-settings/data-tier-allocation.md#tier-preference-allocation-filter) setting determines which tier the index should be allocated to.

When you create an index, by default {{es}} sets the `_tier_preference` to `data_content` to automatically allocate the index shards to the content tier.

When {{es}} creates an index as part of a [data stream](/manage-data/data-store/data-streams.md), by default {{es}} sets the `_tier_preference` to `data_hot` to automatically allocate the index shards to the hot tier.

At the time of index creation, you can override the default setting by explicitly setting the preferred value in one of two ways:

* Using an [index template](/manage-data/data-store/templates.md). Refer to [](/manage-data/lifecycle/index-lifecycle-management.md) for details.
* Within the [create index]({{es-apis}}operation/operation-indices-create) request body.

You can override this setting after index creation by [updating the index setting]({{es-apis}}operation/operation-indices-put-settings) to the preferred value.

This setting also accepts multiple tiers in order of preference. This prevents indices from remaining unallocated if there are no nodes in the cluster for the preferred tier. For example, when {{ilm}} migrates an index to the cold phase, it sets the index `_tier_preference` to `data_cold,data_warm,data_hot`.

To remove the data tier preference setting, set the `_tier_preference` value to `null`. This allows the index to allocate to any data node within the cluster. Setting the `_tier_preference` to `null` does not restore the default value. In the case of managed indices, a [migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) action might apply a new value in its place.

### Determine the current data tier preference [data-tier-allocation-value]

You can check an existing index’s data tier preference by [polling its settings]({{es-apis}}operation/operation-indices-get-settings) for `index.routing.allocation.include._tier_preference`:

```console
GET /my-index-000001/_settings?filter_path=*.settings.index.routing.allocation.include._tier_preference
```

### Troubleshooting [data-tier-allocation-troubleshooting]

The `_tier_preference` setting might conflict with other allocation settings. This conflict might prevent the shard from allocating. A conflict might occur when a cluster has not yet been completely [migrated to data tiers](/troubleshoot/elasticsearch/troubleshoot-migrate-to-tiers.md).

This setting will not unallocate a currently allocated shard, but might prevent it from migrating from its current location to its designated data tier. To troubleshoot, call the [cluster allocation explain API]({{es-apis}}operation/operation-cluster-allocation-explain) and specify the suspected problematic shard.


### Automatic data tier migration [data-tier-migration]

{{ilm-init}} automatically transitions managed indices through the available data tiers using the [migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) action. By default, this action is automatically injected in every phase.

### Disable data tier allocation [data-tier-allocation]
You can explicitly disable data allocation for  data tier migration in an ILM policy with the following setting:
```sh
    "migrate": {
      "enabled": false
    }
```

For example:

```sh
 "cold": {
        "min_age": "15m",
        "actions": {
          "set_priority": {
            "priority": 0
          },
          "migrate": {
            "enabled": false
          }
        }
      },
```

Defining the `migrate` action with `"enabled": false` for a data tier [disables automatic {{ilm-init}} shard migration](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md#ilm-disable-migrate-ex). This is useful if, for example, you’re using the [allocate action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md) to manually specify allocation rules.

:::{important}
Do not disable automatic {{ilm-init}} migration without manually defining {{ilm-init}} allocation rules. If data migration is disabled without allocation rules defined, this can prevent data from moving to the specified data tier, even though the data has successfully moved through the {{ilm-init}} policy with a status of `complete`.
:::