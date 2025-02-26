---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-tiers.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-disable-data-tier.html
  - https://www.elastic.co/guide/en/cloud/current/ec-disable-data-tier.html
applies_to:
  stack: ga
  serverless: ga
---

# Data tiers

A *data tier* is a collection of [nodes](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md) within a cluster that share the same [data node role](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#node-roles), and a hardware profile that’s appropriately sized for the role. Elastic recommends that nodes in the same tier share the same hardware profile to avoid [hot spotting](/troubleshoot/elasticsearch/hotspotting.md).

## Available data tiers [available-tier]

The data tiers that you use, and the way that you use them, depends on the data’s [category](/manage-data/lifecycle.md). The following data tiers are can be used with each data category:

**Content data**:

* [Content tier](/manage-data/lifecycle/data-tiers.md#content-tier) nodes handle the indexing and query load for non-timeseries indices, such as a product catalog.

**Time series data**:

* [Hot tier](/manage-data/lifecycle/data-tiers.md#hot-tier) nodes handle the indexing load for time series data, such as logs or metrics. They hold your most recent, most-frequently-accessed data.
* [Warm tier](/manage-data/lifecycle/data-tiers.md#warm-tier) nodes hold time series data that is accessed less-frequently and rarely needs to be updated.
* [Cold tier](/manage-data/lifecycle/data-tiers.md#cold-tier) nodes hold time series data that is accessed infrequently and not normally updated. To save space, you can keep [fully mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) on the cold tier. These fully mounted indices eliminate the need for replicas, reducing required disk space by approximately 50% compared to the regular indices.
* [Frozen tier](/manage-data/lifecycle/data-tiers.md#frozen-tier) nodes hold time series data that is accessed rarely and never updated. The frozen tier stores [partially mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) of [{{search-snaps}}](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) exclusively. This extends the storage capacity even further — by up to 20 times compared to the warm tier.

::::{tip}
The performance of an {{es}} node is often limited by the performance of the underlying storage and hardware profile. For example hardware profiles, refer to Elastic Cloud’s [instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/hardware.md). Review our recommendations for optimizing your storage for [indexing](/deploy-manage/production-guidance/optimize-performance/indexing-speed.md#indexing-use-faster-hardware) and [search](/deploy-manage/production-guidance/optimize-performance/search-speed.md#search-use-faster-hardware).
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

Content tier nodes are usually optimized for query performance—​they prioritize processing power over IO throughput so they can process complex searches and aggregations and return results quickly. While they are also responsible for indexing, content data is generally not ingested at as high a rate as time series data such as logs and metrics. From a resiliency perspective the indices in this tier should be configured to use one or more replicas.

The content tier is required and is often deployed within the same node grouping as the hot tier. System indices and other indices that aren’t part of a data stream are automatically allocated to the content tier.


### Hot tier [hot-tier]

The hot tier is the {{es}} entry point for time series data and holds your most-recent, most-frequently-searched time series data. Nodes in the hot tier need to be fast for both reads and writes, which requires more hardware resources and faster storage (SSDs). For resiliency, indices in the hot tier should be configured to use one or more replicas.

The hot tier is required. New indices that are part of a [data stream](/manage-data/data-store/data-streams.md) are automatically allocated to the hot tier.


### Warm tier [warm-tier]

Time series data can move to the warm tier once it is being queried less frequently than the recently-indexed data in the hot tier. The warm tier typically holds data from recent weeks. Updates are still allowed, but likely infrequent. Nodes in the warm tier generally don’t need to be as fast as those in the hot tier. For resiliency, indices in the warm tier should be configured to use one or more replicas.


### Cold tier [cold-tier]

When you no longer need to search time series data regularly, it can move from the warm tier to the cold tier. While still searchable, this tier is typically optimized for lower storage costs rather than search speed.

For better storage savings, you can keep [fully mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) on the cold tier. Unlike regular indices, these fully mounted indices don’t require replicas for reliability. In the event of a failure, they can recover data from the underlying snapshot instead. This potentially halves the local storage needed for the data. A snapshot repository is required to use fully mounted indices in the cold tier. Fully mounted indices are read-only.

Alternatively, you can use the cold tier to store regular indices with replicas instead of using {{search-snaps}}. This lets you store older data on less expensive hardware but doesn’t reduce required disk space compared to the warm tier.


### Frozen tier [frozen-tier]

Once data is no longer being queried, or being queried rarely, it may move from the cold tier to the frozen tier where it stays for the rest of its life.

The frozen tier requires a snapshot repository. The frozen tier uses [partially mounted indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) to store and load data from a snapshot repository. This reduces local storage and operating costs while still letting you search frozen data. Because {{es}} must sometimes fetch frozen data from the snapshot repository, searches on the frozen tier are typically slower than on the cold tier.

## Configure data tiers [configure-data-tiers]

Follow the instructions for your deployment type to configure data tiers.

### {{ech}} or {{ece}} [configure-data-tiers-cloud]

The default configuration for an {{ecloud}} deployment includes a shared tier for hot and content data. This tier is required and can’t be removed.

#### Add a data tier

To add a warm, cold, or frozen tier when you create a deployment:

1. On the **Create deployment** page, click **Advanced Settings**.
2. Click **+ Add capacity** for any data tiers to add.
3. Click **Create deployment** at the bottom of the page to save your changes.

:::{image} ../../images/elasticsearch-reference-ess-advanced-config-data-tiers.png
:alt: {{ecloud}}'s deployment Advanced configuration page
:class: screenshot
:::

To add a data tier to an existing deployment:

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body) or the {{ece}} admin console.
2. On the **Deployments** page, select your deployment.
3. In your deployment menu, select **Edit**.
4. Click **+ Add capacity** for any data tiers to add.
5. Click **Save** at the bottom of the page to save your changes.

#### Disable a data tier [disable-a-data-tier]

The process of disabling a data tier depends on whether we are dealing with [searchable snapshots](#ece-disable-searchable-snapshot-data-tier) or [regular indices](#ece-disable-non-searchable-snapshot-data-tier).

The hot and warm tiers store regular indices, while the frozen tier stores searchable snapshots. However, the cold tier can store either regular indices or searchable snapshots. To check if a cold tier contains searchable snapshots perform the following request:

```sh
GET /_cat/indices/restored-*
```

##### Non-searchable snapshot data tier [ece-disable-non-searchable-snapshot-data-tier]

{{ech}} and {{ece}} try to move all data from the nodes that are removed during plan changes. To disable a non-searchable snapshot data tier (e.g., hot, warm, or cold tier), make sure that all data on that tier can be re-allocated by reconfiguring the relevant shard allocation filters. You’ll also need to temporarily stop your index lifecycle management (ILM) policies to prevent new indices from being moved to the data tier you want to disable.

To learn more about ILM, or shard allocation filtering, check the following documentation:

* [Create your index lifecyle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md)
* [Managing the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md)
* [Shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md)

To make sure that all data can be migrated from the data tier you want to disable, follow these steps:

1. Determine which nodes will be removed from the cluster.

    :::::{tab-set}

    ::::{tab-item} {{ech}}

    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. From the **Deployments** page, select your deployment.

        On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

    3. Filter the list of instances by the Data tier you want to disable.

        :::{image} ../../images/cloud-ec-ce-remove-tier-filter-instances.png
        :alt: A screenshot showing a filtered instance list
        :::

        Note the listed instance IDs. In this example, it would be Instance 2 and Instance 3.

    ::::

    ::::{tab-item} Elastic Cloud Enterprise
    1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
    2. From the **Deployments** page, select your deployment.

        Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

    3. Filter the list of instances by the Data tier you want to disable.

        :::{image} ../../images/cloud-enterprise-ec-ce-remove-tier-filter-instances.png
        :alt: A screenshot showing a filtered instance list
        :::

        Note the listed instance IDs. In this example, it would be Instance 2 and Instance 3.
    ::::

    :::::

2. Stop ILM.

    ```sh
    POST /_ilm/stop
    ```

3. Determine which shards need to be moved.

    ```sh
    GET /_cat/shards
    ```

    Parse the output, looking for shards allocated to the nodes to be removed from the cluster. Note that `Instance #2` is shown as `instance-0000000002` in the output.

    :::{image} ../../images/cloud-enterprise-ec-ce-remove-tier-filtered-cat-shards.png
    :alt: A screenshot showing a filtered shard list
    :::

4. Move shards off the nodes to be removed from the cluster.

    You must remove any [index-level shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) from the indices on the nodes to be removed. ILM uses different rules depending on the policy and version of Elasticsearch. Check the index settings to determine which rule to use:

    ```sh
    GET /my-index/_settings
    ```

    1. $$$update-data-tier-allocation-rules$$$ Updating data tier based allocation inclusion rules.

        Data tier based ILM policies use `index.routing.allocation.include` to allocate shards to the appropriate tier. The indices that use this method have index routing settings similar to the following example:

        ```sh
        {
        ...
            "routing": {
                "allocation": {
                    "include": {
                        "_tier_preference": "data_warm,data_hot"
                    }
                }
            }
        ...
        }
        ```

        You must remove the relevant tier from the inclusion rules. For example, to disable the warm tier, the `data_warm` tier preference should be removed:

        ```sh
        PUT /my-index/_settings
        {
            "routing": {
              "allocation": {
                "include": {
                    "_tier_preference": "data_hot"
                }
              }
            }
        }
        ```

        Updating allocation inclusion rules will trigger a shard re-allocation, moving the shards from the nodes to be removed.

    2. Updating node attribute allocation requirement rules.

        Node attribute based ILM policies uses `index.routing.allocation.require` to allocate shards to the appropriate nodes. The indices that use this method have index routing settings that are similar to the following example:

        ```sh
        {
        ...
            "routing": {
                "allocation": {
                    "require": {
                        "data": "warm"
                    }
                }
            }
        ...
        }
        ```

        You must either remove or redefine the routing requirements. To remove the attribute requirements, use the following code:

        ```sh
        PUT /my-index/_settings
        {
            "routing": {
              "allocation": {
                "require": {
                    "data": null
                }
              }
            }
        }
        ```

        Removing required attributes does not trigger a shard reallocation. These shards are moved when applying the plan to disable the data tier. Alternatively, you can use the [cluster re-route API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-reroute) to manually re-allocate the shards before removing the nodes, or explicitly re-allocate shards to hot nodes by using the following code:

        ```sh
        PUT /my-index/_settings
        {
            "routing": {
              "allocation": {
                "require": {
                    "data": "hot"
                }
              }
            }
        }
        ```

    3. Removing custom allocation rules.

        If indices on nodes to be removed have shard allocation rules of other forms, they must be removed as shown in the following example:

        ```sh
        PUT /my-index/_settings
        {
            "routing": {
              "allocation": {
                "require": null,
                "include": null,
                "exclude": null
              }
            }
        }
        ```

5. Edit the deployment, disabling the data tier.

    If autoscaling is enabled, set the maximum size to 0 for the data tier to ensure autoscaling does not re-enable the data tier.

    Any remaining shards on the tier being disabled are re-allocated across the remaining cluster nodes while applying the plan to disable the data tier. Monitor shard allocation during the data migration phase to ensure all allocation rules have been correctly updated. If the plan fails to migrate data away from the data tier, then re-examine the allocation rules for the indices remaining on that data tier.

6. Once the plan change completes, confirm that there are no remaining nodes associated with the disabled tier and that `GET _cluster/health` reports `green`. If this is the case, re-enable ILM.

    ```sh
    POST _ilm/start
    ```

##### Searchable snapshot data tier [ece-disable-searchable-snapshot-data-tier]

When data reaches the `cold` or `frozen` phases, it is automatically converted to a [searchable snapshot](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) by ILM. If you do not intend to delete this data, you should manually restore each of the searchable snapshot indices to a regular index before disabling the data tier, by following these steps:

1. Stop ILM and check ILM status is `STOPPED` to prevent data from migrating to the phase you intend to disable while you are working through the next steps.

    ```sh
    # stop ILM
    POST _ilm/stop

    # check status
    GET _ilm/status
    ```

2. Capture a comprehensive list of index and searchable snapshot names.

    1. The index name of the searchable snapshots may differ based on the data tier. If you intend to disable the cold tier, then perform the following request with the `restored-*` prefix. If the frozen tier is the one to be disabled, use the `partial-*` prefix.

        ```sh
        GET <searchable-snapshot-index-prefix>/_settings?filter_path=**.index.store.snapshot.snapshot_name&expand_wildcards=all
        ```

        In the example we have a list of 4 indices, which need to be moved away from the frozen tier.

        :::{image} ../../images/cloud-enterprise-ec-ce-remove-tier-filter-snapshot-indices.png
        :alt: A screenshot showing a snapshot indices list
        :::

3. (Optional) Save the list of index and snapshot names in a text file, so you can access it throughout the rest of the process.
4. Remove the aliases that were applied to searchable snapshots indices. Use the index prefix from step 2.

    ```sh
    POST _aliases
    {
      "actions": [
        {
          "remove": {
            "index": "<searchable-snapshot-index-prefix>-<index_name>",
            "alias": "<index_name>"
          }
        }
      ]
    }
    ```

    ::::{note}
    If you use data stream, you can skip this step.
    ::::


    In the example we are removing the alias for the `frozen-index-1` index.

    :::{image} ../../images/cloud-enterprise-ec-ce-remove-tier-remove-alias.png
    :alt: A screenshot showing the process of removing a searchable snapshot indice alias
    :::

5. Restore indices from the searchable snapshots.

    1. Follow the steps to [specify the data tier based allocation inclusion rules](/manage-data/lifecycle/data-tiers.md#update-data-tier-allocation-rules).
    2. Remove the associated ILM policy (set it to `null`). If you want to apply a different ILM policy, follow the steps to [Switch lifecycle policies](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md#switch-lifecycle-policies).
    3. If needed, specify the alias for rollover, otherwise set it to `null`.
    4. Optionally, specify the desired number of replica shards.

        ```sh
        POST _snapshot/found-snapshots/<searchable_snapshot_name>/_restore
        {
          "indices": "*",
          "index_settings": {
            "index.routing.allocation.include._tier_preference": "<data_tiers>",
            "number_of_replicas": X,
            "index.lifecycle.name": "<new-policy-name>",
            "index.lifecycle.rollover_alias": "<alias-for-rollover>"
          }
        }
        ```

        The  `<searchable_snapshot_name>` refers to the above-mentioned step: "Capture a comprehensive list of index and searchable snapshot names".

        In the example we are restoring `frozen-index-1` from the snapshot in `found-snapshots` (default snapshot repository) and placing it in the warm tier.

        :::{image} ../../images/cloud-enterprise-ec-ce-remove-tier-restore-snapshot.png
        :alt: A screenshot showing the process of restoring a searchable snapshot to a regular index
        :::

6. Repeat steps 4 and 5 until all snapshots are restored to regular indices.
7. Once all snapshots are restored, use `GET _cat/indices/<index-pattern>?v=true` to check that the restored indices are `green` and are correctly reflecting the expected `doc` and `store.size` counts.

    If you are using data stream, you may need to use `GET _data_stream/<data-stream-name>` to get the list of the backing indices, and then specify them by using `GET _cat/indices/<backing-index-name>?v=true` to check.

8. Once your data has completed restoration from searchable snapshots to the target data tier, `DELETE` searchable snapshot indices using the prefix from step 2.

    ```sh
    DELETE <searchable-snapshot-index-prefix>-<index_name>
    ```

9. Delete the searchable snapshots by following these steps:

    1. Open Kibana and navigate to Management > Data > Snapshot and Restore > Snapshots (or go to `<kibana-endpoint>/app/management/data/snapshot_restore/snapshots`)
    2. Search for `*<ilm-policy-name>*`
    3. Bulk select the snapshots and delete them

        In the example we are deleting the snapshots associated with the `policy_with_frozen_phase`.

        :::{image} ../../images/cloud-enterprise-ec-ce-remove-tier-remove-snapshots.png
        :alt: A screenshot showing the process of deleting snapshots
        :::

10. Confirm that no shards remain on the data nodes you wish to remove using `GET _cat/allocation?v=true&s=node`.
11. Edit your cluster from the console to disable the data tier.
12. Once the plan change completes, confirm that there are no remaining nodes associated with the disabled tier and that `GET _cluster/health` reports `green`. If this is the case, re-enable ILM.

    ```sh
    POST _ilm/start
    ```

### Self-managed deployments [configure-data-tiers-on-premise]

For self-managed deployments, each node’s [data role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role) is configured in `elasticsearch.yml`. For example, the highest-performance nodes in a cluster might be assigned to both the hot and content tiers:

```yaml
node.roles: ["data_hot", "data_content"]
```

::::{note}
We recommend you use [dedicated nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) in the frozen tier.
::::

## Data tier index allocation [data-tier-allocation]

The [`index.routing.allocation.include._tier_preference`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/data-tier-allocation.md#tier-preference-allocation-filter) setting determines which tier the index should be allocated to.

When you create an index, by default {{es}} sets the `_tier_preference` to `data_content` to automatically allocate the index shards to the content tier.

When {{es}} creates an index as part of a [data stream](/manage-data/data-store/data-streams.md), by default {{es}} sets the `_tier_preference` to `data_hot` to automatically allocate the index shards to the hot tier.

At the time of index creation, you can override the default setting by explicitly setting the preferred value in one of two ways:

* Using an [index template](/manage-data/data-store/templates.md). Refer to [Automate rollover with ILM](/manage-data/lifecycle/index-lifecycle-management.md) for details.
* Within the [create index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request body.

You can override this setting after index creation by [updating the index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) to the preferred value.

This setting also accepts multiple tiers in order of preference. This prevents indices from remaining unallocated if no nodes are available in the preferred tier. For example, when {{ilm}} migrates an index to the cold phase, it sets the index `_tier_preference` to `data_cold,data_warm,data_hot`.

To remove the data tier preference setting, set the `_tier_preference` value to `null`. This allows the index to allocate to any data node within the cluster. Setting the `_tier_preference` to `null` does not restore the default value. Note that, in the case of managed indices, a [migrate](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) action might apply a new value in its place.

### Determine the current data tier preference [data-tier-allocation-value]

You can check an existing index’s data tier preference by [polling its settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) for `index.routing.allocation.include._tier_preference`:

```console
GET /my-index-000001/_settings?filter_path=*.settings.index.routing.allocation.include._tier_preference
```

### Troubleshooting [data-tier-allocation-troubleshooting]

The `_tier_preference` setting might conflict with other allocation settings. This conflict might prevent the shard from allocating. A conflict might occur when a cluster has not yet been completely [migrated to data tiers](/troubleshoot/elasticsearch/troubleshoot-migrate-to-tiers.md).

This setting will not unallocate a currently allocated shard, but might prevent it from migrating from its current location to its designated data tier. To troubleshoot, call the [cluster allocation explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain) and specify the suspected problematic shard.


### Automatic data tier migration [data-tier-migration]

{{ilm-init}} automatically transitions managed indices through the available data tiers using the [migrate](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) action. By default, this action is automatically injected in every phase. You can explicitly specify the migrate action with `"enabled": false` to [disable automatic migration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md#ilm-disable-migrate-ex), for example, if you’re using the [allocate action](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md) to manually specify allocation rules.
