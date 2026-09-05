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

Follow this section when you need to remove the warm, cold, or frozen tier from an {{ech}} or {{ece}} deployment. The shared hot and content tier is required and cannot be removed.

The steps differ depending on whether the tier holds [regular indices](#non-searchable-snapshot-data-tier) or [{{search-snap}}](#searchable-snapshot-data-tier) indices (typical for cold or frozen when using {{ilm}} ({{ilm-init}})).

### Before you remove a data tier [before-you-remove-a-data-tier]

:::{important}
Disabling a data tier, attempting to scale nodes down in size, reducing availability zones, or reverting an [autoscaling](/deploy-manage/autoscaling.md) change can all result in cluster instability, cluster inaccessibility, and even data corruption or loss in extreme cases.

To avoid this, especially for [production environments](/deploy-manage/production-guidance.md), and in addition to making configuration changes to your indices and {{ilm-init}} as described in this guide:

* Review the disk size, CPU, JVM memory pressure, and other [performance metrics](/deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md) of your deployment **before** attempting to perform the scaling down action.
* Make sure that you have enough resources and [availability zones](/deploy-manage/production-guidance/availability-and-resilience.md) to handle your workloads after scaling down.
* Check that your [deployment hardware profile](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) (for {{ech}}) or [deployment template](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md) (for {{ece}}) is correct for your business use case. For example, if you need to scale due to CPU pressure increases and are using a *Storage Optimized* hardware profile, consider switching to a *CPU Optimized* configuration instead.
* Review [disk watermarks](/troubleshoot/elasticsearch/fix-watermark-errors.md) and ensure the remaining nodes are not close to their limits.

Read [https://www.elastic.co/cloud/shared-responsibility](https://www.elastic.co/cloud/shared-responsibility) for additional details.
If in doubt, reach out to Support.
:::

Check whether the tier you are removing holds regular indices, [{{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), or both. Use the guidance for the tier you are removing:

* **Warm tier:** This tier typically holds regular indices. Follow [Remove a tier with regular indices](#non-searchable-snapshot-data-tier) unless you have manually mounted {{search-snaps}} on the tier.
* **Cold tier:** This tier can hold regular indices or [fully mounted](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) {{search-snaps}}. Check for standard {{ilm-init}}-managed {{search-snap}} indices:

    ```sh
    GET /_cat/indices/restored-*?expand_wildcards=all
    ```

    For each returned index, check its [current data tier preference](/manage-data/lifecycle/data-tiers.md#data-tier-allocation-value) to determine whether it is on the tier you are removing.

    Exclude any fully mounted indices associated with the hot tier from the removal inventory. The hot tier is required and is not removed by this procedure.

* **Frozen tier:** This tier only holds [partially mounted](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) {{search-snaps}}. Check for standard {{ilm-init}}-managed indices:

    ```sh
    GET /_cat/indices/partial-*?expand_wildcards=all
    ```

:::{note}
Manually mounted {{search-snaps}} might not use the standard `restored-*` or `partial-*` prefixes. If you mounted snapshots manually, adapt the index names or patterns in these requests to match your configuration.
:::

* If the tier does not contain any {{search-snap}} indices, follow [Remove a tier with regular indices](#non-searchable-snapshot-data-tier).
* If the tier contains {{search-snap}} indices, review [Remove a tier with {{search-snaps}}](#searchable-snapshot-data-tier) and select the appropriate procedure based on how the indices are mounted. If regular indices also remain, restore or move the {{search-snap}} indices first, but do not disable the tier yet. Then return to the regular indices procedure.

To learn more about {{ilm-init}} or shard allocation filtering, refer to [Create your index lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md), [Managing the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md), and [Shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md).

### Remove a tier with regular indices [non-searchable-snapshot-data-tier]

This section covers the removal of a tier that holds regular indices. The goal is to ensure all shard allocation rules allow the data to move to other tiers before you disable the tier. You also need to temporarily stop {{ilm-init}} to prevent new indices from being routed to the tier while you work.

:::{note}
If the tier also holds [fully mounted](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) {{search-snaps}}, you have two options:

* **To keep them as {{search-snaps}} on another tier**: apply the same steps in this section. Fully mounted {{search-snaps}} follow the same shard placement rules as regular indices and can be moved by updating their allocation settings.
* **To restore them to regular indices on another tier**: follow [Remove a tier with {{search-snaps}}](#searchable-snapshot-data-tier) to restore the indices and delete the original {{search-snap}} indices, but do not disable the tier yet. Then return to this section to move any regular indices and disable the tier. You can optionally delete source snapshots that you no longer need.
:::

When you update the deployment, {{ech}} and {{ece}} try to move all data from the nodes that are removed. Before applying this change, make sure that the relevant shard allocation filters allow the data to move.

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

2. Stop {{ilm-init}} to prevent new indices from being routed to the tier while you work.

    ```sh
    POST /_ilm/stop
    GET /_ilm/status
    ```

    Wait until `operation_mode` is `STOPPED` before proceeding.

3. Determine which shards are allocated to the nodes you want to remove.

    ```sh
    GET /_cat/shards?v&h=index,shard,prirep,state,node
    ```

    Parse the output, looking for shards allocated to the nodes to be removed from the cluster. `Instance #2` is shown as `instance-0000000002` in the output.

    :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-filtered-cat-shards.png
    :alt: A screenshot showing a filtered shard list
    :::

4. Check and update index allocation rules.

    {{ilm-init}} and manual index configurations use different [index-level shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) to control shard placement. For every index that has shards on the nodes you are removing, check its allocation settings and apply the relevant substeps:

    ```sh
    GET /my-index/_settings
    ```

    1. $$$update-data-tier-allocation-rules$$$ Update `_tier_preference`-based rules.

        Data tier-based {{ilm-init}} policies use `index.routing.allocation.include._tier_preference` to express shard placement as an ordered list of preferred tiers. Indices using this method have settings similar to the following example:

        ```sh
        {
        ...
            "routing": {
                "allocation": {
                    "include": {
                        "_tier_preference": "data_warm,data_hot" <1>
                    }
                }
            }
        ...
        }
        ```
        1. The example represents an index in the `warm` tier.

        Before disabling the tier, update `_tier_preference` so that the tier where you want the data to move is the first available tier in the list. This allows {{es}} to begin relocating the shards before the deployment plan removes the tier.

        Update the setting based on where you want to move the data:

        * To move the data to an existing fallback tier, remove the tier being disabled from the list. For example, when disabling the warm tier, change `data_warm,data_hot` to `data_hot`.
        * To move the data to a later lifecycle tier, add that tier before the tier being disabled. For example, when disabling the warm tier, change `data_warm,data_hot` to `data_cold,data_warm,data_hot`.

        The following example moves data from warm to cold:

        ```sh
        PUT /my-index/_settings
        {
            "routing": {
              "allocation": {
                "include": {
                    "_tier_preference": "data_cold,data_warm,data_hot" <1>
                }
              }
            }
        }
        ```

        1. You can also use `data_cold,data_hot`. Both values move the data to cold, but omitting `data_warm` removes that tier from the fallback sequence.

        :::{note}
        Do not use the frozen tier as a fallback for regular indices. It is reserved for partially mounted {{search-snaps}}.
        :::

    2. Update node attribute allocation requirement rules.

        Older {{ilm-init}} policies and some custom configurations use `index.routing.allocation.require` to pin shards to nodes with a specific attribute. Indices using this method have settings similar to the following example:

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

        Unlike `_tier_preference`, a `require` rule is a hard constraint: if the required nodes are gone, the shard becomes unassigned and {{es}} cannot move it automatically. You must remove or redirect these rules before disabling the tier. To remove the attribute requirement:

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

        Alternatively, redirect the index to a different tier by setting `require` to the desired attribute value. For example, to move an index to nodes with `data` attribute of `cold`:

        ```sh
        PUT /my-index/_settings
        {
            "routing": {
              "allocation": {
                "require": {
                    "data": "cold"
                }
              }
            }
        }
        ```

        Adjust the `data` value to match the [custom node attributes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#custom-node-attributes) and [index-level shard allocation filters](elasticsearch://reference/elasticsearch/index-settings/shard-allocation.md) your indices already use. You cannot send regular indices to the frozen tier.

        If you remove the `require` rule, {{es}} does not re-allocate shards immediately. They move when the deployment plan disables the tier. You can instead use the [cluster reroute API]({{es-apis}}operation/operation-cluster-reroute) or redirect `require` to a different attribute value to start re-allocation before applying the plan.

    3. Review other custom allocation rules.

        If indices on the nodes being removed use other [index-level shard allocation filters](elasticsearch://reference/elasticsearch/index-settings/shard-allocation.md#index-allocation-settings), such as `include`, `exclude`, or `require` configurations not covered earlier, update or remove any rules that would prevent shards from moving to the intended nodes. You can preserve rules unrelated to the tier removal.

        The following example removes all `_name`-based custom allocation filters from an index:

        ```sh
        PUT /my-index/_settings
        {
          "index.routing.allocation.require._name": null,
          "index.routing.allocation.include._name": null,
          "index.routing.allocation.exclude._name": null
        }
        ```

    :::{important}
    If your allocation setting changes start relocation, wait until [shard allocation and recovery](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery.md) finish. Use `GET /_cat/allocation?v=true&s=node` to monitor the nodes that the plan will remove. Shards might remain if you only removed a `require` rule because that change does not force them to move. The deployment plan relocates them when it disables the tier.

    If shards that you expect to move remain on the original tier, use the [cluster allocation explain]({{es-apis}}operation/operation-cluster-allocation-explain) API to determine the cause. Common causes include [disk watermarks](/troubleshoot/elasticsearch/fix-watermark-errors.md) or the [`index.routing.allocation.total_shards_per_node`](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#total-shards-per-node) limit on the destination nodes.
    :::

5. Edit the deployment, disabling the data tier.

    If autoscaling is enabled, set the maximum size to 0 for the data tier to ensure autoscaling does not re-enable the data tier.

    Any remaining shards on the tier being disabled are re-allocated across the remaining cluster nodes while applying the plan to disable the data tier. Monitor shard allocation during the data migration phase to ensure all allocation rules have been correctly updated. If the plan fails to migrate data away from the data tier, then re-examine the allocation rules for the indices remaining on that data tier.

6. Once the plan change completes, confirm that `GET /_cat/nodes?v` shows no nodes associated with the disabled tier and that `GET /_cluster/health` reports `green`.

7. Review your {{ilm-init}} policies and consider removing references to the disabled tier to keep them consistent with the deployment topology. This is especially important in older deployments where {{ilm-init}} uses node-attribute-based allocation, as those policies cannot run phases that target nodes that no longer exist.

    For guidance on updating policies, refer to [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

8. Re-enable {{ilm-init}}:

    ```sh
    POST /_ilm/start
    ```

9. Verify that {{ilm-init}} is running and that no indices report errors related to the disabled tier:

    ```sh
    GET /_ilm/status
    GET /_all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true
    ```

    Confirm that `operation_mode` is `RUNNING`. Investigate any reported errors and verify that no policy still attempts to allocate data to the disabled tier.

### Remove a tier with {{search-snaps}} [searchable-snapshot-data-tier]

This section explains how to remove a data tier that contains [{{search-snap}} indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). Your options for preserving the data depend on how the indices are mounted:

* **[Partially mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) on the frozen tier:** The only way to keep the data available as indices when removing the frozen tier is to restore all partially mounted indices as regular indices on another tier. Follow the steps in this section to restore the indices and remove the original {{search-snap}} indices.
* **[Fully mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) on the cold tier:** To keep the indices as {{search-snaps}}, move them to another tier by following [Remove a tier with regular indices](#non-searchable-snapshot-data-tier). This works because fully mounted indices follow the same shard placement rules as regular indices. Alternatively, follow the steps in this section to restore them as regular indices on another tier.

If you do not need to preserve the data, delete the {{search-snap}} indices and continue from the shard verification before disabling the tier.

The following procedure captures the snapshot metadata, restores the indices as regular indices, removes the original {{search-snap}} indices, optionally deletes the source snapshots, and then disables the tier.

:::{note}
The [{{ilm-init}} `searchable_snapshot` action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) typically prefixes the resulting index with `restored-*` for fully mounted indices in the hot or cold phase and `partial-*` for partially mounted indices in the frozen phase. Manually mounted {{search-snaps}} might not use these prefixes. In the following steps, adapt the index names and patterns to match the indices on the tier you are removing.
:::

% TODO: Cover data stream lifecycle `frozen_after` transitions and `dlm-frozen-*` indices. Stopping {{ilm-init}} does not stop these transitions.

1. From your deployment page, filter the instance list by the data tier you want to disable and note the instance IDs.

2. Stop {{ilm-init}} to prevent data from migrating to the phase you intend to remove while you work.

    ```sh
    POST /_ilm/stop
    GET /_ilm/status
    ```

    Wait until `operation_mode` is `STOPPED` before proceeding.

3. Using the {{search-snap}} indices identified in [Before you remove a data tier](#before-you-remove-a-data-tier), create an inventory of the indices to restore. For standard {{ilm-init}} configurations, you can use `restored-*` for the cold tier and `partial-*` for the frozen tier. For custom configurations, use individual index names or a pattern that matches the relevant indices. For each index, record the index name, source snapshot name, and snapshot repository.

    ```sh
    GET /<searchable-snapshot-index-name-or-pattern>/_settings?filter_path=**.index.store.snapshot.snapshot_name,**.index.store.snapshot.repository_name&expand_wildcards=all
    ```

    :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-filter-snapshot-indices.png
    :alt: A screenshot showing a snapshot indices list
    :::

4. For each index in the inventory, remove any aliases that were applied to the {{search-snap}} index.

    ```sh
    POST /_aliases
    {
      "actions": [
        {
          "remove": {
            "index": "<searchable-snapshot-index-name>",
            "alias": "<alias-name>"
          }
        }
      ]
    }
    ```

    ::::{note}
    If you use a data stream, you can skip this step.
    ::::

    :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-remove-alias.png
    :alt: A screenshot showing the process of removing a {{search-snap}} index alias
    :::

5. Restore each index in the inventory from its source snapshot.

    The restore request creates a regular index on the remaining tiers and prevents it from inheriting the previous {{ilm-init}} policy and rollover alias:

    ```sh
    POST /_snapshot/<snapshot_repository_name>/<searchable_snapshot_name>/_restore <1>
    {
      "indices": "*", <2>
      "index_settings": {
        "index.routing.allocation.include._tier_preference": "<data_tiers>", <3>
        "index.number_of_replicas": 1, <4>
        "index.lifecycle.name": null,
        "index.lifecycle.rollover_alias": null
      }
    }
    ```
    1. Use the corresponding snapshot repository and snapshot name from the inventory.
    2. The `*` value restores every index in the snapshot. Snapshots created by the {{ilm-init}} `searchable_snapshot` action contain only the managed index. For a manually created snapshot that contains multiple indices, replace `*` with the name of the original index you want to restore.
    3. Specify an ordered list of remaining tiers where the restored index can be allocated. Refer to [Update `_tier_preference`-based rules](#update-data-tier-allocation-rules).
    4. Adjust `index.number_of_replicas` to match your resiliency needs.

    To manage the restored index with a different {{ilm-init}} policy, apply the policy after the restore and configure its rollover alias if required. Refer to [Switch lifecycle policies](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md#switch-lifecycle-policies).

    :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-restore-snapshot.png
    :alt: A screenshot showing the process of restoring a {{search-snap}} to a regular index
    :::

6. Once all snapshots are restored, use `GET /_cat/indices/<index-pattern>?v=true` to check that the restored indices are `green` and reflect the expected `docs.count` and `store.size` values.

    If you are using a data stream, you might need to use `GET /_data_stream/<data-stream-name>` to get the list of the backing indices, and then specify them by using `GET /_cat/indices/<backing-index-name>?v=true` to check. When you restore the backing indices of a data stream, some [considerations](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#considerations) apply, and you might need to manually add the restored indices into your data stream or re-create your data stream.

    % TODO: Document how to replace a {{search-snap}} backing index with the restored regular index before deleting the mounted index.

7. After verifying each restored index, delete the corresponding original {{search-snap}} index from the inventory.

    ```sh
    DELETE /<searchable-snapshot-index-name>
    ```

8. If you no longer need the source snapshots, delete them from {{kib}}:

    :::{warning}
    Deleting the source snapshots is not required to disable the tier. Before deleting a snapshot, verify that no mounted index in this or another cluster still depends on it and that it contains no other data you need. The underlying snapshot is the sole full copy of the data for every {{search-snap}} index mounted from it.
    :::

    1. Find **Snapshot and Restore** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. Select the **Snapshots** tab.
    3. Search for the snapshot names recorded in the inventory. If the snapshots were created by the same {{ilm-init}} policy, you can search for the policy name instead.
    4. Select the snapshots you want to delete, and click **Delete**.

       :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-remove-snapshots.png
       :alt: A screenshot showing the process of deleting snapshots
       :::

9. Confirm that no shards remain on the data nodes you want to remove using `GET /_cat/allocation?v=true&s=node`.

10. Edit your deployment from the console to disable the data tier.

    If autoscaling is enabled, set the maximum size to `0` for the data tier to ensure autoscaling does not re-enable it.

11. Once the plan change completes, confirm that `GET /_cat/nodes?v` shows no nodes associated with the disabled tier and that `GET /_cluster/health` reports `green`.

12. Review your {{ilm-init}} policies and update any phases that target the disabled tier. For example, when disabling the frozen tier, remove the `frozen` phase. If you want future indices to continue using {{search-snaps}}, configure the `searchable_snapshot` action in an appropriate remaining phase. Also update any allocation rules that reference the disabled tier.

    For guidance on updating policies, refer to [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

13. Re-enable {{ilm-init}}:

    ```sh
    POST /_ilm/start
    ```

14. Verify that {{ilm-init}} is running and that no indices report errors related to the disabled tier:

    ```sh
    GET /_ilm/status
    GET /_all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true
    ```

    Confirm that `operation_mode` is `RUNNING`. Investigate any reported errors and verify that no policy still attempts to allocate data to the disabled tier.

## Related pages

- [Configure data tiers](/manage-data/lifecycle/data-tiers.md#configure-data-tiers)
- [Data tier index allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation)
- [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md)
