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

1. From your deployment page, filter the instance list by the data tier you want to disable and note the instance IDs.

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

1. Check whether the tier you are removing holds regular indices, [{{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), or both:

   * **Warm tier:** This tier typically holds regular indices unless you have manually mounted {{search-snaps}} on it.
   * **Cold tier:** This tier can hold regular indices or [fully mounted](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) {{search-snaps}}. Check for standard {{ilm-init}}-managed {{search-snap}} indices:

       ```sh
       GET /_cat/indices/restored-*?expand_wildcards=all
       ```

       For each returned index, check its [current data tier preference](/manage-data/lifecycle/data-tiers.md#data-tier-allocation-value) to determine whether it is on the tier you are removing.

       Exclude any fully mounted indices associated with the hot tier from the removal inventory. The hot tier is required and is not removed by this procedure.

   * **Frozen tier:** This tier only holds [partially mounted](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) {{search-snaps}}. Check for standard lifecycle-managed indices:

       ```sh
       GET /_cat/indices/partial-*,dlm-frozen-*?expand_wildcards=all
       ```

   :::{note}
   Manually mounted {{search-snaps}} might not use the standard `restored-*` or `partial-*` prefixes. If you mounted snapshots manually, adapt the index names or patterns in these requests to match your configuration.
   :::

1. Review the {{ilm-init}} policies and index templates that can send data to the tier you are removing, and plan the changes required so that they no longer use the tier. This prevents newly created indices and future lifecycle transitions from targeting a tier that is no longer available.

   Depending on your configuration, plan to:

   * Remove or update {{ilm-init}} phases and actions that move indices to the tier.
   * Remove or move any `searchable_snapshot` action that mounts indices on the tier.
   * If you use custom allocation filters in policies or templates, remove or update those that target the tier.

   Before proceeding, make sure that you have identified every affected policy and template.

   To learn more about {{ilm-init}} or shard allocation filtering, refer to [Create your index lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md), [Managing the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md), and [Shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md).

After completing this preparation:

* If the tier contains {{search-snaps}}, start with [Vacate tier instances containing {{search-snaps}}](#searchable-snapshot-data-tier).
* If the tier contains regular indices, or fully mounted {{search-snaps}} that you want to move while keeping them mounted, continue with [Prepare regular indices for tier removal](#non-searchable-snapshot-data-tier).
* After completing every applicable procedure, [disable the data tier](#disable-data-tier-ech-ece).

### Vacate tier instances containing {{search-snaps}} [searchable-snapshot-data-tier]

This section explains how to vacate instances in a data tier that contains [{{search-snap}} indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). Choose how to handle the data before disabling the tier:

* **[Partially mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) on the frozen tier:** These indices cannot remain mounted outside the frozen tier.
    * To preserve the data as regular indices, select another tier with sufficient capacity and follow [Restore {{search-snap}} data to a regular index](/deploy-manage/tools/snapshot-and-restore/restore-searchable-snapshot-to-regular-index.md).
    * If you no longer need the data, delete the mounted indices and any source snapshots you no longer need.
* **[Fully mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) on the cold tier:**
    * To keep them as {{search-snaps}}, use [Prepare regular indices for tier removal](#non-searchable-snapshot-data-tier) before disabling the tier. Fully mounted {{search-snaps}} follow the same shard allocation rules as regular indices.
    * To preserve the data as regular indices, select another tier with sufficient capacity and follow [Restore {{search-snap}} data to a regular index](/deploy-manage/tools/snapshot-and-restore/restore-searchable-snapshot-to-regular-index.md).
    * If you no longer need the data, delete the mounted indices and any source snapshots you no longer need.

:::{note}
:applies_to: {"stack": "ga 9.5+"}

If you are disabling the frozen tier and [{{dlm-init}}](/manage-data/lifecycle/data-stream.md) manages partially mounted indices on it, remove `frozen_after` from the affected data streams and index templates before proceeding.
:::

1. Apply the changes to {{ilm-init}} policies and index templates that you planned in [Before you remove a data tier](#before-you-remove-a-data-tier) so that they no longer create or route {{search-snap}} indices to the tier you want to disable. These changes prevent new {{search-snaps}} from appearing while you process the existing ones.

1. For each mounted {{search-snap}} whose data you want to preserve as a regular index, follow [Restore {{search-snap}} data to a regular index](/deploy-manage/tools/snapshot-and-restore/restore-searchable-snapshot-to-regular-index.md). Complete the restore, validation, alias or data stream update, and mounted index cleanup for one index before proceeding to the next.

1. For each mounted {{search-snap}} whose data you do not want to preserve, record its source snapshot details before deleting the index:

   ```sh
   GET /<searchable-snapshot-index-name>/_settings?filter_path=**.index.store.snapshot.snapshot_name,**.index.store.snapshot.repository_name&expand_wildcards=all
   DELETE /<searchable-snapshot-index-name>
   ```

   If you no longer need the source snapshot, delete it after confirming that it contains no other data you need and that no other mounted index in this or another cluster depends on it:

   ```sh
   DELETE /_snapshot/<snapshot_repository_name>/<searchable_snapshot_name>
   ```

After processing all {{search-snaps}}, continue based on what remains on the tier:

* If the tier also contains regular indices, or fully mounted {{search-snaps}} that you want to move to another tier while keeping them mounted, continue to [Prepare regular indices for tier removal](#non-searchable-snapshot-data-tier).
* Otherwise, continue to [Disable the data tier](#disable-data-tier-ech-ece).

### Prepare regular indices for tier removal [non-searchable-snapshot-data-tier]

This section prepares regular indices to move safely when you disable the tier. It also applies to fully mounted {{search-snaps}} that you want to keep mounted, because they follow the same shard allocation rules as regular indices.

When you update the deployment, {{ech}} and {{ece}} try to move all data from the instances that are removed. Before applying this change, make sure that the relevant shard allocation filters allow the data to move.

1. If you have not already done so, apply the changes to {{ilm-init}} policies and index templates that you planned in [Before you remove a data tier](#before-you-remove-a-data-tier). These changes prevent newly created indices and future lifecycle transitions from targeting the tier. They do not move indices already allocated there. The remaining steps update those indices and start relocating their shards.

   :::{warning}
   Temporarily [stopping {{ilm-init}}](/manage-data/lifecycle/index-lifecycle-management/start-stop-index-lifecycle-management.md) can prevent lifecycle transitions while you update the cluster configuration, but it affects every {{ilm-init}}-managed index in the cluster. It pauses actions such as rollover, migration, and deletion. On clusters with sustained ingestion, a long pause can cause indices on the hot tier to grow until the tier runs out of disk space.

   Keep {{ilm-init}} running unless you understand the effect on your workload. If you stop it, monitor the hot tier and restart {{ilm-init}} as soon as possible. Stopping {{ilm-init}} does not replace updating policies, templates, and index allocation settings.
   :::

1. Determine which shards are allocated to the instances you want to remove.

   ```sh
   GET /_cat/shards?v&h=index,shard,prirep,state,node
   ```

   Parse the output, looking for shards allocated to the instances you identified in [Before you remove a data tier](#before-you-remove-a-data-tier). `Instance #2` is shown as `instance-0000000002` in the output.

   :::{image} /manage-data/images/cloud-enterprise-ec-ce-remove-tier-filtered-cat-shards.png
   :alt: A screenshot showing a filtered shard list
   :::

1. Check and update index allocation rules.

   {{ilm-init}} and manual index configurations can use different [index-level shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) to control shard placement. For every index that has shards on the instances you are removing, check its allocation settings and complete the applicable steps:

   ```sh
   GET /my-index/_settings
   ```

   1. $$$update-data-tier-allocation-rules$$$ Update `_tier_preference`-based rules.

      Data tier-based {{ilm-init}} policies use `index.routing.allocation.include._tier_preference` to express shard placement as an ordered list of preferred tiers. {{es}} allocates shards to the first tier in the list that has nodes in the cluster and considers later tiers only when none of the preceding tiers have any nodes.

      Indices using this method have settings similar to the following example:

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

      Before disabling the tier, update `_tier_preference` so that the tier where you want the data to move is the first available tier in the list. This change makes the destination tier preferred and starts relocating the shards before the deployment plan removes the tier.

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
      Do not use the frozen tier as a fallback for regular indices or fully mounted {{search-snaps}}. It is reserved for partially mounted {{search-snaps}}.
      :::

   1. Review custom allocation rules.

      Some custom configurations use [index-level shard allocation filters](elasticsearch://reference/elasticsearch/index-settings/shard-allocation.md#index-allocation-settings) in addition to or instead of `_tier_preference`. These filters use `require`, `include`, or `exclude` rules with built-in or custom node attributes to control shard placement.

      For example, the following settings use a custom `data` node attribute to require warm nodes:

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

      A `require` rule is a hard constraint. If no nodes match it, the shard remains unassigned. To remove this requirement:

      ```sh
      PUT /my-index/_settings
      {
        "index.routing.allocation.require.data": null <1>
      }
      ```
      1. You can update the rule to target the destination nodes instead of removing it.

      For each affected index, update or remove the custom filters that prevent allocation to the destination tier.

      The following example removes all `_name`-based allocation filters from an index:

      ```sh
      PUT /my-index/_settings
      {
        "index.routing.allocation.require._name": null,
        "index.routing.allocation.include._name": null,
        "index.routing.allocation.exclude._name": null
      }
      ```

   :::{important}
   If your allocation setting changes start relocation, wait until [shard allocation and recovery](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery.md) finish. Use `GET /_cat/allocation?v=true&s=node` to monitor the instances that the plan will remove. Shards might remain if you only removed a `require` rule because that change does not force them to move. The deployment plan relocates them when it disables the tier.

   If shards that you expect to move remain on the original tier, use the [cluster allocation explain]({{es-apis}}operation/operation-cluster-allocation-explain) API to determine the cause. Refer to [Using the cluster allocation API for troubleshooting](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md) for common examples. Common causes include [disk watermarks](/troubleshoot/elasticsearch/fix-watermark-errors.md) or the [`index.routing.allocation.total_shards_per_node`](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#total-shards-per-node) limit on the destination nodes.
   :::

After updating the allocation rules, continue to [Disable the data tier](#disable-data-tier-ech-ece).

### Disable the data tier [disable-data-tier-ech-ece]

After completing every applicable vacate procedure, disable the data tier from the deployment editor.

1. Edit the deployment and disable the data tier.

   If autoscaling is enabled, set the maximum size to `0` for the data tier to ensure autoscaling does not re-enable it.

   Any remaining shards on the tier being disabled are re-allocated across the remaining cluster nodes while applying the deployment plan. Monitor shard allocation during the data migration phase to ensure all allocation rules have been correctly updated. If the plan fails to migrate data away from the tier, re-examine the allocation rules for the indices that remain on it.

1. Once the plan change completes, confirm that `GET /_cat/nodes?v` shows no nodes associated with the disabled tier and that `GET /_cluster/health` reports `green`.

1. Verify that {{ilm-init}} is running and that no indices report errors related to the disabled tier:

   ```sh
   GET /_ilm/status
   GET /_all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true
   ```

   Confirm that `operation_mode` is `RUNNING`. Investigate any reported errors and verify that no policy still attempts to allocate data to the disabled tier.

## Related pages

- [Configure data tiers](/manage-data/lifecycle/data-tiers.md#configure-data-tiers)
- [Data tier index allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation)
- [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md)
