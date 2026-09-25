---
navigation_title: Manage data tiers in self-managed and ECK
description: "Assign or remove Elasticsearch data tier roles on self-managed hosts (elasticsearch.yml) or on Elastic Cloud on Kubernetes (ECK node set config)."
applies_to:
  deployment:
    self: ga
    eck: ga
products:
  - id: elasticsearch
  - id: cloud-kubernetes
---

# Configure data tiers for self-managed and {{eck}} deployments

Whether you operate {{es}} on your own infrastructure or on {{k8s}} with {{eck}}, data tiers are expressed through each node’s [data role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role). You choose which tiers the cluster offers by assigning the corresponding `data_*` roles to nodes or to ECK node sets.

## Before you begin

- Review [{{es}} data tiers](/manage-data/lifecycle/data-tiers.md) so you match tiers to your workload.
- Understand how [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) map to hardware and allocation for each tier.

## Assign data tier roles on self-managed hosts [configure-data-tier-self-managed]
```{applies_to}
deployment:
  self: ga
```

1. For each node, decide which data tier or tiers it should participate in (for example `data_hot`, `data_warm`, `data_cold`, `data_frozen`, or `data_content`).
2. Set `node.roles` in that node’s [`elasticsearch.yml`](/deploy-manage/stack-settings.md) to include the corresponding `data_*` roles (and any other roles the node should have, such as `ingest` or `master`).
3. Restart the node or apply your configuration rollout process so the new roles take effect.

For example, the highest-performance nodes in a cluster might be assigned to both the hot and content tiers:

```yaml
node.roles: ["data_hot", "data_content"]
```

::::{note}
We recommend you use [dedicated nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) in the frozen tier.
::::

## Assign data tier roles in {{eck}}
```{applies_to}
deployment:
  eck: ga
```

{{es}} settings that you normally put in `elasticsearch.yml` are set for each `nodeSet` under `spec.nodeSets[?].config` in the {{es}} resource manifest. Assign `node.roles` there to define each group of pods’ tiers. For example, you can assign the following tiers:

```yaml
spec:
  nodeSets:
  - name: hot-content
    count: 3
    config:
      node.roles: ["data_hot", "data_content", "ingest"]
```

Some settings are [managed by {{eck}}](/deploy-manage/deploy/cloud-on-k8s/settings-managed-by-eck.md); avoid overriding those. For the full mapping between manifest structure and {{es}} configuration, see [Node configuration](/deploy-manage/deploy/cloud-on-k8s/node-configuration.md).


:::{note}
 On {{eck}}, node set and scaling changes try to relocate shards from nodes that are removed, subject to allocation rules, capacity, and [disk watermarks](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) on the destination nodes. For more information, refer to the [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md) documentation.
:::

## Remove a data tier [remove-data-tier-self-managed-eck]

Follow this section when you need to remove the warm, cold, or frozen tier from a self-managed or {{eck}} deployment. The hot and content tiers are required and cannot be removed. If you remove nodes assigned the `data_hot` or `data_content` role, ensure that the corresponding role remains assigned to other nodes.

The steps differ depending on whether the tier holds [regular indices](#remove-regular-indices-self-managed-eck) or [{{search-snap}}](#remove-searchable-snapshots-self-managed-eck) indices (typical for cold or frozen when using {{ilm}} ({{ilm-init}})).

### Before you remove a data tier [before-remove-data-tier-self-managed-eck]

:::{important}
Removing a data tier reduces the cluster's capacity. This can cause cluster instability, inaccessibility, or data loss if the remaining nodes cannot absorb the data from the removed tier.

Before proceeding:

* Confirm that the remaining tiers have enough disk space, CPU, and memory to absorb the data and workload from the tier you are removing.
* Review [disk watermarks](/troubleshoot/elasticsearch/fix-watermark-errors.md) and ensure the remaining nodes are not close to their limits.
:::

1. Identify which nodes belong to the data tier you want to remove:

   ```sh
   GET /_nodes?filter_path=nodes.*.name,nodes.*.ip,nodes.*.roles
   ```

   Note the names of the nodes with the corresponding `data_*` role.

   :::{tip}
   For {{eck}}, also identify every `nodeSet` in your {{es}} manifest that has the `data_*` role associated with the tier you want to remove.
   :::

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

* If the tier contains {{search-snaps}}, start with [Vacate tier nodes containing {{search-snaps}}](#remove-searchable-snapshots-self-managed-eck).
* If the tier contains regular indices, or fully mounted {{search-snaps}} that you want to move while keeping them mounted, continue with [Vacate tier nodes containing regular indices](#remove-regular-indices-self-managed-eck).
* After completing every applicable vacate procedure, [remove the tier nodes](#remove-empty-tier-nodes-self-managed-eck).

### Vacate tier nodes containing {{search-snaps}} [remove-searchable-snapshots-self-managed-eck]

This section explains how to vacate nodes in a data tier that contains [{{search-snap}} indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). Choose how to handle the data before vacating the nodes:

* **[Partially mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) on the frozen tier:** These indices cannot remain mounted outside the frozen tier.
    * To preserve the data as regular indices, select another tier with sufficient capacity and follow [Restore {{search-snap}} data to a regular index](/deploy-manage/tools/snapshot-and-restore/restore-searchable-snapshot-to-regular-index.md).
    * If you no longer need the data, delete the mounted indices and any source snapshots you no longer need.
* **[Fully mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) on the cold tier:**
    * To keep them as {{search-snaps}}, use the [regular index vacate procedure](#remove-regular-indices-self-managed-eck) to move their shards to another tier. Fully mounted {{search-snaps}} follow the same shard allocation rules as regular indices.
    * To preserve the data as regular indices, select another tier with sufficient capacity and follow [Restore {{search-snap}} data to a regular index](/deploy-manage/tools/snapshot-and-restore/restore-searchable-snapshot-to-regular-index.md).
    * If you no longer need the data, delete the mounted indices and any source snapshots you no longer need.

:::{note}
:applies_to: {"stack": "ga 9.5+"}

If you are removing the frozen tier and [{{dlm-init}}](/manage-data/lifecycle/data-stream.md) manages partially mounted indices on it, remove `frozen_after` from the affected data streams and index templates before proceeding.
:::

1. Apply the changes to {{ilm-init}} policies and index templates that you planned in [Before you remove a data tier](#before-remove-data-tier-self-managed-eck) so that they no longer create or route {{search-snap}} indices to the tier you want to remove. These changes prevent new {{search-snaps}} from appearing while you process the existing ones.

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

* If the tier also contains regular indices, or fully mounted {{search-snaps}} that you want to move to another tier while keeping them mounted, continue to [Vacate tier nodes containing regular indices](#remove-regular-indices-self-managed-eck).
* Otherwise, continue to [Remove the tier nodes](#remove-empty-tier-nodes-self-managed-eck).

### Vacate tier nodes containing regular indices [remove-regular-indices-self-managed-eck]

This section covers vacating tier nodes that hold regular indices. It also applies to fully mounted {{search-snaps}} that you want to keep mounted, because they follow the same shard allocation rules as regular indices.

1. If you have not already done so, apply the changes to {{ilm-init}} policies and index templates that you planned in [Before you remove a data tier](#before-remove-data-tier-self-managed-eck). These changes prevent newly created indices and future lifecycle transitions from targeting the tier. They do not move indices already allocated there. The remaining steps update those indices and relocate their shards.

   :::{warning}
   Temporarily [stopping {{ilm-init}}](/manage-data/lifecycle/index-lifecycle-management/start-stop-index-lifecycle-management.md) can prevent lifecycle transitions while you update the cluster configuration, but it affects every {{ilm-init}}-managed index in the cluster. It pauses actions such as rollover, migration, and deletion. On clusters with sustained ingestion, a long pause can cause indices on the hot tier to grow until the tier runs out of disk space.

   Keep {{ilm-init}} running unless you understand the effect on your workload. If you stop it, monitor the hot tier and restart {{ilm-init}} as soon as possible. Stopping {{ilm-init}} does not replace updating policies, templates, and index allocation settings.
   :::

1. Determine which shards are allocated to the nodes you want to remove.

   ```sh
   GET /_cat/shards?v&h=index,shard,prirep,state,node
   ```

   Filter the output by the node names you identified in [Before you remove a data tier](#before-remove-data-tier-self-managed-eck).

1. Check and update index allocation rules.

   {{ilm-init}} and manual index configurations can use different [index-level shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) to control shard placement. For every index that has shards on the nodes you are removing, check its allocation settings and complete the applicable steps:

   ```sh
   GET /my-index/_settings
   ```

   1. $$$update-tier-allocation-rules-self-managed$$$ Update `_tier_preference`-based rules.

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

      Before manually vacating the nodes, update `_tier_preference` so that the tier where you want the data to move is the first available tier in the list. This change makes the destination tier preferred and starts relocating the shards before the nodes are removed.

      Update the setting based on where you want to move the data:

      * To move the data to an existing fallback tier, remove the tier being removed from the list. For example, when removing the warm tier, change `data_warm,data_hot` to `data_hot`.
      * To move the data to a later lifecycle tier, add that tier before the tier being removed. For example, when removing the warm tier, change `data_warm,data_hot` to `data_cold,data_warm,data_hot`.

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

      Removing a custom filter does not necessarily start relocation if the current nodes remain eligible. The manual vacate in the following step forces any remaining shards to move.

1. Vacate the nodes manually.

   :::{note}
   On {{eck}}, removing a `nodeSet` from the {{es}} manifest can migrate data away from its nodes before removing the underlying StatefulSet, as described in [Cluster upgrade patterns](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md#k8s-upgrade-patterns). This procedure uses a manual vacate so that you can verify the nodes are empty before removing the `nodeSet`.
   :::

   Exclude the nodes from shard allocation by name. {{es}} then relocates their remaining shards to other eligible nodes:

   ```sh
   PUT /_cluster/settings
   {
     "persistent": {
       "cluster.routing.allocation.exclude._name": "<node-name-1>,<node-name-2>" <1>
     }
   }
   ```
   1. If `_name` exclusions are already configured, include their existing values in the comma-separated list to preserve them.

   :::{important}
   Wait until `GET /_cat/allocation?v=true&s=node` shows that no shards remain on those nodes before proceeding. Updating settings starts the relocation process, but you must wait until [shard allocation and recovery](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery.md) finish. If shards stay on the original tier, use the [cluster allocation explain]({{es-apis}}operation/operation-cluster-allocation-explain) API to determine the cause. Refer to [Using the cluster allocation API for troubleshooting](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md) for common examples. Common causes include [disk watermarks](/troubleshoot/elasticsearch/fix-watermark-errors.md) or [`index.routing.allocation.total_shards_per_node`](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#total-shards-per-node) limit reached on the destination nodes.
   :::

After the nodes are empty, continue to [Remove the tier nodes](#remove-empty-tier-nodes-self-managed-eck).

### Remove the tier nodes [remove-empty-tier-nodes-self-managed-eck]

After completing every applicable vacate procedure, follow these steps to remove the empty nodes from the tier.

1. Confirm that no shards remain on the nodes you want to remove:

   ```sh
   GET /_cat/allocation?v=true&s=node
   ```

   Do not continue until the nodes report no shards. If shards remain, complete the applicable vacate procedure and use the [cluster allocation explain]({{es-apis}}operation/operation-cluster-allocation-explain) API to identify any allocation constraints.

1. Remove the nodes.

   :::::{applies-switch}

   ::::{applies-item} self:
   Stop the {{es}} service on each node to be removed and decommission the host. For step-by-step instructions, refer to [Add or remove {{es}} nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md).
   ::::

   ::::{applies-item} eck:
   Remove every `nodeSet` associated with the tier from your {{es}} manifest, or set each `count` to `0`. If an `ElasticsearchAutoscaler` policy manages any of these `nodeSet`s, remove the matching policy before applying this change. Otherwise, autoscaling might change the `nodeSet` counts while you complete this procedure. Refer to [Autoscaling in ECK](/deploy-manage/autoscaling/autoscaling-in-eck.md).

   {{eck}} safely stops the pods after you have vacated their shards.
   ::::

   :::::

1. Wait until `GET /_cat/nodes?v` shows no nodes from the removed tier remaining in the cluster.

1. If you used the manual vacate, remove the deleted node names from the exclusion rule only after the nodes have left the cluster. Restore any `_name` exclusions that existed before the vacate. If none existed, clear the setting:

   ```sh
   PUT /_cluster/settings
   {
     "persistent": {
       "cluster.routing.allocation.exclude._name": null
     }
   }
   ```

1. Confirm that `GET /_cluster/health` reports `green`.

1. Verify that {{ilm-init}} is running and that no indices report errors related to the removed tier:

   ```sh
   GET /_ilm/status
   GET /_all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true
   ```

   Confirm that `operation_mode` is `RUNNING`. Investigate any reported errors and verify that no policy still attempts to allocate data to the removed tier.


## Related pages

* [Configure data tiers](/manage-data/lifecycle/data-tiers.md#configure-data-tiers)
* [Data tier index allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation)
* [Add or remove {{es}} nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md)
