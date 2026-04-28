---
navigation_title: Manage data tiers in ECH or ECE
description: "Add or remove warm, cold, or frozen data tiers in Elastic Cloud Hosted or Elastic Cloud Enterprise, including safe removal with shard migration."
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-disable-data-tier.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-disable-data-tier.html
applies_to:
  deployment:
    ess: ga
    ece: ga
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Add or remove data tiers in {{ech}} or {{ece}} [manage-data-tiers-ech-ece]

In {{ech}} and {{ece}}, you add **warm**, **cold**, or **frozen** capacity from the deployment editor, and you remove a tier only after data can migrate away safely. The default configuration includes a shared tier for hot and content data; that tier is required and cannot be removed.

## Add a data tier [add-data-tier-ech-ece]

Review [{{es}} data tiers](/manage-data/lifecycle/data-tiers.md) so you choose the right tier for your workload.

### Add capacity when you create a deployment

1. On the **Create deployment** page, click **Advanced Settings**.
2. Click **+ Add capacity** for any data tiers to add.
3. Click **Create deployment** at the bottom of the page to save your changes.

:::{image} /manage-data/images/elasticsearch-reference-ess-advanced-config-data-tiers.png
:alt: {{ecloud}}'s deployment Advanced configuration page
:screenshot:
:::

### Add capacity to an existing deployment

:::{include} /deploy-manage/_snippets/find-manage-deployment-ech-and-ece.md
:::

4. From the navigation menu, select **Edit**.
5. Click **+ Add capacity** for any data tiers to add.
6. Click **Save** at the bottom of the page to save your changes.

## Remove a data tier [remove-data-tier-ech-ece]

Follow this section when you need to remove a data tier from an {{ech}} or {{ece}} deployment. The steps differ depending on whether the tier holds [regular indices](#non-searchable-snapshot-data-tier) or [{{search-snap}}](#searchable-snapshot-data-tier) indices (typical for cold or frozen when using {{ilm}} ({{ilm-init}})).

### Before you remove a data tier [before-you-remove-a-data-tier]

:::{important}
Disabling a data tier, attempting to scale nodes down in size, reducing availability zones, or reverting an [autoscaling](/deploy-manage/autoscaling.md) change can all result in cluster instability, cluster inaccessibility, and even data corruption or loss in extreme cases.

To avoid this, especially for [production environments](/deploy-manage/production-guidance.md), and in addition to making configuration changes to your indices and {{ilm-init}} as described in this guide:

* Review the disk size, CPU, JVM memory pressure, and other [performance metrics](/deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md) of your deployment **before** attempting to perform the scaling down action.
* Make sure that you have enough resources and [availability zones](/deploy-manage/production-guidance/availability-and-resilience.md) to handle your workloads after scaling down.
* Check that your [deployment hardware profile](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) (for {{ech}}) or [deployment template](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md) (for {{ece}}) is correct for your business use case. For example, if you need to scale due to CPU pressure increases and are using a *Storage Optimized* hardware profile, consider switching to a *CPU Optimized* configuration instead.

Read [https://www.elastic.co/cloud/shared-responsibility](https://www.elastic.co/cloud/shared-responsibility) for additional details.
If in doubt, reach out to Support.
:::

* Know whether you are disabling a tier that stores **regular indices** (for example hot, warm, or cold without {{search-snaps}}) or **{{search-snaps}}** (for example cold or frozen with {{ilm-init}}). The **cold** tier can hold either; use these requests to check for {{search-snap}} indices:

    ```sh
    # cold data tier: {{search-snap}} indices
    GET /_cat/indices/restored-*

    # frozen data tier: {{search-snap}} indices
    GET /_cat/indices/partial-*
    ```

* To learn more about {{ilm-init}} or shard allocation filtering, see [Create your index lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md), [Managing the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md), and [Shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md).

### Remove a tier with regular indices [non-searchable-snapshot-data-tier]

The hot and warm tiers store regular indices, while the frozen tier stores {{search-snaps}}. The cold tier can store either; use the checks in [Before you remove a data tier](#before-you-remove-a-data-tier) if you are unsure.

{{ech}} and {{ece}} try to move all data from the nodes that are removed during plan changes. To disable a tier that holds only regular indices (for example, hot, warm, or cold tier), make sure that all data on that tier can be re-allocated by reconfiguring the relevant shard allocation filters. You’ll also need to temporarily stop your {{ilm-init}} policies to prevent new indices from being moved to the data tier you want to disable.

To make sure that all data can be migrated from the data tier you want to disable, follow these steps:

1. Determine which nodes will be removed from the cluster.

    :::::{applies-switch}

    ::::{applies-item} ess:

    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. From the **Hosted deployments** page, select your deployment.

        On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

    3. Filter the list of instances by the Data tier you want to disable.

        :::{image} /manage-data/images/cloud-ec-ce-remove-tier-filter-instances.png
        :alt: A screenshot showing a filtered instance list
        :::

        Note the listed instance IDs. In this example, it would be Instance 2 and Instance 3.

    ::::

    ::::{applies-item} ece:
    1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
    2. From the **Deployments** page, select your deployment.

        Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

    3. Filter the list of instances by the Data tier you want to disable.

        :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-filter-instances.png
        :alt: A screenshot showing a filtered instance list
        :::

        Note the listed instance IDs. In this example, it would be Instance 2 and Instance 3.
    ::::

    :::::

2. Stop {{ilm-init}}.

    ```sh
    POST /_ilm/stop
    ```

3. Determine which shards need to be moved.

    ```sh
    GET /_cat/shards
    ```

    Parse the output, looking for shards allocated to the nodes to be removed from the cluster. `Instance #2` is shown as `instance-0000000002` in the output.

    :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-filtered-cat-shards.png
    :alt: A screenshot showing a filtered shard list
    :::

4. Move shards off the nodes to be removed from the cluster.

    You must remove any [index-level shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) from the indices on the nodes to be removed. {{ilm-init}} uses different rules depending on the policy and version of {{es}}. Check the index settings to determine which rule to use:

    ```sh
    GET /my-index/_settings
    ```

    1. $$$update-data-tier-allocation-rules$$$ Updating data tier based allocation inclusion rules.

        Data tier based {{ilm-init}} policies use `index.routing.allocation.include` to allocate shards to the appropriate tier. The indices that use this method have index routing settings similar to the following example:

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

        Node attribute based {{ilm-init}} policies use `index.routing.allocation.require` to allocate shards to the appropriate nodes. The indices that use this method have index routing settings that are similar to the following example:

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

6. Once the plan change completes, confirm that there are no remaining nodes associated with the disabled tier and that `GET _cluster/health` reports `green`. If this is the case, re-enable {{ilm-init}}.

    ```sh
    POST _ilm/start
    ```

### Remove a tier with {{search-snaps}} [searchable-snapshot-data-tier]

When data reaches the `cold` or `frozen` phases, it is automatically converted to a [{{search-snap}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) by {{ilm-init}}. If you do not intend to delete this data, you should manually restore each of the {{search-snap}} indices to a regular index before disabling the data tier, by following these steps:

1. Stop {{ilm-init}} and check {{ilm-init}} status is `STOPPED` to prevent data from migrating to the phase you intend to disable while you are working through the next steps.

    ```sh
    # stop {{ilm-init}}
    POST _ilm/stop

    # check status
    GET _ilm/status
    ```

2. Capture a comprehensive list of index and {{search-snap}} names.

    1. The index name of the {{search-snaps}} may differ based on the data tier. If you intend to disable the cold tier, then perform the following request with the `restored-*` prefix. If the frozen tier is the one to be disabled, use the `partial-*` prefix.

        ```sh
        GET <searchable-snapshot-index-prefix>/_settings?filter_path=**.index.store.snapshot.snapshot_name&expand_wildcards=all
        ```

        In the example we have a list of 4 indices, which need to be moved away from the frozen tier.

        :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-filter-snapshot-indices.png
        :alt: A screenshot showing a snapshot indices list
        :::

3. (Optional) Save the list of index and snapshot names in a text file, so you can access it throughout the rest of the process.
4. Remove the aliases that were applied to {{search-snaps}} indices. Use the index prefix from step 2.

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

    :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-remove-alias.png
    :alt: A screenshot showing the process of removing a {{search-snap}} index alias
    :::

5. Restore indices from the {{search-snaps}}.

    1. Follow the steps to [specify the data tier based allocation inclusion rules](/manage-data/lifecycle/data-tiers/manage-data-tiers-ech-ece.md#update-data-tier-allocation-rules).
    2. Remove the associated {{ilm-init}} policy (set it to `null`). If you want to apply a different {{ilm-init}} policy, follow the steps to [Switch lifecycle policies](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md#switch-lifecycle-policies).
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

        The  `<searchable_snapshot_name>` refers to the above-mentioned step: "Capture a comprehensive list of index and {{search-snap}} names".

        In the example we are restoring `frozen-index-1` from the snapshot in `found-snapshots` (default snapshot repository) and placing it in the warm tier.

        :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-restore-snapshot.png
        :alt: A screenshot showing the process of restoring a {{search-snap}} to a regular index
        :::

6. Repeat steps 4 and 5 until all snapshots are restored to regular indices.
7. Once all snapshots are restored, use `GET _cat/indices/<index-pattern>?v=true` to check that the restored indices are `green` and are correctly reflecting the expected `doc` and `store.size` counts.

    If you are using data stream, you may need to use `GET _data_stream/<data-stream-name>` to get the list of the backing indices, and then specify them by using `GET _cat/indices/<backing-index-name>?v=true` to check. When you restore the backing indices of a data stream, some [considerations](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#considerations) apply, and you might need to manually add the restored indices into your data stream or recreate your data stream.

8. Once your data has completed restoration from {{search-snaps}} to the target data tier, `DELETE` {{search-snap}} indices using the prefix from step 2.

    ```sh
    DELETE <searchable-snapshot-index-prefix>-<index_name>
    ```

9. Delete the {{search-snaps}} by following these steps:

    1. Open {{kib}}, go to the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and go to the **Snapshots** tab. (Alternatively, go to `<kibana-endpoint>/app/management/data/snapshot_restore/snapshots`.)
    2. Search for `*<ilm-policy-name>*`
    3. Bulk select the snapshots and delete them

        In the example we are deleting the snapshots associated with the `policy_with_frozen_phase`.

        :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-remove-snapshots.png
        :alt: A screenshot showing the process of deleting snapshots
        :::

10. Confirm that no shards remain on the data nodes you wish to remove using `GET _cat/allocation?v=true&s=node`.
11. Edit your cluster from the console to disable the data tier.
12. Once the plan change completes, confirm that there are no remaining nodes associated with the disabled tier and that `GET _cluster/health` reports `green`. If this is the case, re-enable {{ilm-init}}.

    ```sh
    POST _ilm/start
    ```

## Related pages

- [Configure data tiers](/manage-data/lifecycle/data-tiers.md#configure-data-tiers)
- [Data tier index allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation)
- [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md)
