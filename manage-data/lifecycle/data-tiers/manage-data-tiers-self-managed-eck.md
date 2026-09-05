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

   If an `ElasticsearchAutoscaler` policy manages any of these `nodeSet`s, remove the matching policy before removing the tier or setting its `count` to `0`. Otherwise, autoscaling might change the `nodeSet` count while you complete this procedure. Refer to [Autoscaling in ECK](/deploy-manage/autoscaling/autoscaling-in-eck.md).
   :::

1. Check whether the tier you are removing holds regular indices, [{{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), or both. Use the guidance for the tier you are removing:

   * **Warm tier:** This tier typically holds regular indices. Follow [Remove a tier with regular indices](#remove-regular-indices-self-managed-eck) unless you have manually mounted {{search-snaps}} on the tier.
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

   * If the tier does not contain any {{search-snap}} indices, follow [Remove a tier with regular indices](#remove-regular-indices-self-managed-eck).
   * If the tier contains {{search-snap}} indices, review [Remove a tier with {{search-snaps}}](#remove-searchable-snapshots-self-managed-eck) and select the appropriate procedure based on how the indices are mounted. If regular indices also remain, restore or move the {{search-snap}} indices first, but do not remove the nodes. Then return to the regular indices procedure.

To learn more about {{ilm-init}} or shard allocation filtering, refer to [Create your index lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md), [Managing the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md), and [Shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md).

### Remove a tier with regular indices [remove-regular-indices-self-managed-eck]

This section covers the removal of a tier that holds regular indices. The goal is to ensure all shard allocation rules allow the data to move to other tiers, and then vacate and remove the nodes. You also need to temporarily stop {{ilm-init}} to prevent new indices from being routed to the tier while you work.

:::{note}
If the tier also holds [fully mounted](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) {{search-snaps}}, you have two options:

* **To keep them as {{search-snaps}} on another tier**: apply the same steps in this section. Fully mounted {{search-snaps}} follow the same shard placement rules as regular indices and can be moved by updating their allocation settings.
* **To restore them to regular indices on another tier**: follow [Remove a tier with {{search-snaps}}](#remove-searchable-snapshots-self-managed-eck) to restore the indices and delete the original {{search-snap}} indices and source snapshots, but do not remove the nodes yet. Then return to this section to move any regular indices and remove the nodes.
:::

1. Stop {{ilm-init}} to prevent new indices from being routed to the tier while you work.

   ```sh
   POST /_ilm/stop
   GET /_ilm/status
   ```

   Wait until `operation_mode` is `STOPPED` before proceeding.

1. Determine which shards are allocated to the nodes you want to remove.

   ```sh
   GET /_cat/shards?v&h=index,shard,prirep,state,node
   ```

   Filter the output by the node names you identified in [Before you remove a data tier](#before-remove-data-tier-self-managed-eck).

1. Check and update index allocation rules.

   {{ilm-init}} and manual index configurations use different [index-level shard allocation filters](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) to control shard placement. For every index that has shards on the nodes you are removing, check its allocation settings and apply the relevant substeps:

   ```sh
   GET /my-index/_settings
   ```

   1. $$$update-tier-allocation-rules-self-managed$$$ `_tier_preference` based rules.

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

      Before manually vacating the nodes, update `_tier_preference` so that the tier where you want the data to move is the first available tier in the list. This allows {{es}} to begin relocating the shards to that tier before the nodes are removed.

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
      Do not use the frozen tier as a fallback for regular indices. It is reserved for partially mounted {{search-snaps}}.
      :::

   1. Update node attribute allocation requirement rules.

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

      Unlike `_tier_preference`, a `require` rule is a hard constraint: if the required nodes are gone, the shard becomes unassigned and {{es}} cannot move it automatically. You must remove or redirect these rules before vacating the nodes. To remove the attribute requirement:

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

      If you remove the `require` rule, {{es}} does not re-allocate shards immediately. They move when you vacate the nodes in the next step. If you redirect `require` to a different attribute value, re-allocation starts immediately.

   1. Review other custom allocation rules.

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

1. Vacate the nodes.

   ::::{note}
   On {{eck}}, removing a `nodeSet` from the {{es}} manifest causes {{eck}} to migrate data away from its nodes before removing the underlying StatefulSet, as described in [Cluster upgrade patterns](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md#k8s-upgrade-patterns). If the allocation rules in the previous step are correctly updated, you can skip the manual vacate and proceed directly to removing the `nodeSet`. However, we recommend completing the manual vacate first because it gives you more control and visibility over the relocation process.
   ::::

   To vacate the nodes manually, exclude them from shard allocation by name. {{es}} then relocates their remaining shards to other eligible nodes:

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
   Wait until `GET /_cat/allocation?v=true&s=node` shows that no shards remain on those nodes before proceeding. Updating settings starts the relocation process, but you must wait until [shard allocation and recovery](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery.md) finish. If shards stay on the original tier, use the [cluster allocation explain]({{es-apis}}operation/operation-cluster-allocation-explain) API to determine the cause. Common causes include [disk watermarks](/troubleshoot/elasticsearch/fix-watermark-errors.md) or [`index.routing.allocation.total_shards_per_node`](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#total-shards-per-node) limit reached on the destination nodes.
   :::

1. Remove the nodes.

   After confirming that no shards remain on the nodes, remove them using the instructions for your deployment type.

   :::::{applies-switch}

   ::::{applies-item} self:
   Stop the {{es}} service on each node to be removed and decommission the host. For step-by-step instructions, refer to [Add or remove {{es}} nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md).
   ::::

   ::::{applies-item} eck:
   Remove the `nodeSet` from your {{es}} manifest, or set its `count` to `0`. If you skipped the manual vacate, {{eck}} migrates the remaining data before safely stopping the pods.
   ::::

   :::::

1. Wait until `GET /_cat/nodes?v` shows no nodes from the removed tier remaining in the cluster.

   If you ran the manual vacate, remove the deleted node names from the exclusion rule only after the nodes have left the cluster. Restore any `_name` exclusions that existed before the vacate. If none existed, clear the setting:

   ```sh
   PUT /_cluster/settings
   {
     "persistent": {
       "cluster.routing.allocation.exclude._name": null
     }
   }
   ```

   Confirm that `GET /_cluster/health` reports `green`.

1. Review your {{ilm-init}} policies and consider removing references to the deleted tier to keep them consistent with the cluster topology. This is especially important in older clusters where {{ilm-init}} uses node-attribute-based allocation, as those policies cannot run phases that target nodes that no longer exist.

   For guidance on updating policies, refer to [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

1. Re-enable {{ilm-init}}:

   ```sh
   POST /_ilm/start
   ```

1. Verify that {{ilm-init}} is running and that no indices report errors related to the removed tier:

   ```sh
   GET /_ilm/status
   GET /_all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true
   ```

   Confirm that `operation_mode` is `RUNNING`. Investigate any reported errors and verify that no policy still attempts to allocate data to the removed tier.

### Remove a tier with {{search-snaps}} [remove-searchable-snapshots-self-managed-eck]

This section explains how to remove a data tier that contains [{{search-snap}} indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). Your options for preserving the data depend on how the indices are mounted:

* **[Partially mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) on the frozen tier:** The only way to keep the data available as indices when removing the frozen tier is to restore all partially mounted indices as regular indices on another tier. Follow the steps in this section to restore the indices and remove the original {{search-snap}} indices and source snapshots.
* **[Fully mounted {{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) on the cold tier:** To keep the indices as {{search-snaps}}, move them to another tier by following [Remove a tier with regular indices](#remove-regular-indices-self-managed-eck). This works because fully mounted indices follow the same shard allocation rules as regular indices. Alternatively, follow the steps in this section to restore them as regular indices on another tier.

If you do not need to preserve the data, delete the {{search-snap}} indices before removing the tier.

The following procedure captures the snapshot metadata, restores the indices as regular indices, removes the original {{search-snap}} indices and source snapshots, and then removes the tier's nodes.

:::{note}
The [{{ilm-init}} `searchable_snapshot` action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) typically prefixes the resulting index with `restored-*` for fully mounted indices in the hot or cold phase and `partial-*` for partially mounted indices in the frozen phase. Manually mounted {{search-snaps}} might not use these prefixes. In the following steps, adapt the index names and patterns to match the indices on the tier you are removing.
:::

% TODO: Cover data stream lifecycle `frozen_after` transitions and `dlm-frozen-*` indices. Stopping {{ilm-init}} does not stop these transitions.

1. Stop {{ilm-init}} to prevent data from migrating to the phase you intend to remove while you work.

   ```sh
   POST /_ilm/stop
   GET /_ilm/status
   ```

   Wait until `operation_mode` is `STOPPED` before proceeding.

1. Using the {{search-snap}} indices identified in [Before you remove a data tier](#before-remove-data-tier-self-managed-eck), create an inventory of the indices to restore. For standard {{ilm-init}} configurations, you can use `restored-*` for the cold tier and `partial-*` for the frozen tier. For custom configurations, use individual index names or a pattern that matches the relevant indices. For each index, record the index name, source snapshot name, and snapshot repository.

   ```sh
   GET /<searchable-snapshot-index-name-or-pattern>/_settings?filter_path=**.index.store.snapshot.snapshot_name,**.index.store.snapshot.repository_name&expand_wildcards=all
   ```

1. For each index in the inventory, remove any aliases that were applied to the {{search-snap}} index.

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

1. Restore each index in the inventory from its source snapshot.

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
   3. Specify an ordered list of remaining tiers where the restored index can be allocated. Refer to [Update `_tier_preference`-based rules](#update-tier-allocation-rules-self-managed).
   4. Adjust `index.number_of_replicas` to match your resiliency needs.

   To manage the restored index with a different {{ilm-init}} policy, apply the policy after the restore and configure its rollover alias if required. Refer to [Switch lifecycle policies](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md#switch-lifecycle-policies).

1. Once all snapshots are restored, use `GET /_cat/indices/<index-pattern>?v=true` to check that the restored indices are `green` and are correctly reflecting the expected `docs.count` and `store.size` values.

   If you are using a data stream, you might need to use `GET /_data_stream/<data-stream-name>` to get the list of the backing indices, and then specify them by using `GET /_cat/indices/<backing-index-name>?v=true` to check. When you restore the backing indices of a data stream, some [considerations](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#considerations) apply, and you might need to manually add the restored indices into your data stream or re-create your data stream.

   % TODO: Document how to replace a {{search-snap}} backing index with the restored regular index before deleting the mounted index.

1. After verifying each restored index, delete the corresponding original {{search-snap}} index from the inventory.

   ```sh
   DELETE /<searchable-snapshot-index-name>
   ```

1. Delete the source snapshots recorded in the inventory:

   :::{warning}
   A snapshot created by the {{ilm-init}} `searchable_snapshot` action contains only the managed index, so deleting it after successfully restoring and verifying that index does not affect other indices. This guarantee does not apply to manually created snapshots, which can contain multiple indices or support other mounted {{search-snap}} indices. Before deleting a manually created snapshot, verify that it contains no other data you need and supports no other mounted indices.
   :::

   ```sh
   DELETE /_snapshot/<snapshot_repository_name>/<searchable_snapshot_name>
   ```

   :::{tip}
   You can also delete multiple snapshots at once in {{kib}}. Find **Snapshot and Restore** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), select the **Snapshots** tab, select the snapshots you want to delete, and click **Delete**.
   :::

1. Confirm that no shards remain on the data nodes you wish to remove using `GET /_cat/allocation?v=true&s=node`.

1. Remove the nodes.

   After confirming that no shards remain on the nodes, remove them using the instructions for your deployment type.

   :::::{applies-switch}

   ::::{applies-item} self:
   Stop the {{es}} service on each node to be removed and decommission the host. For step-by-step instructions, refer to [Add or remove {{es}} nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md).
   ::::

   ::::{applies-item} eck:
   Remove the `nodeSet` from your {{es}} manifest, or set its `count` to `0`. {{eck}} safely drains and stops the pods.
   ::::

   :::::

1. Confirm that `GET /_cluster/health` reports `green` and that `GET /_cat/nodes?v` shows no nodes from the removed tier remaining in the cluster.

1. Review your {{ilm-init}} policies and update any phases that target the removed tier. For example, when removing the frozen tier, remove the `frozen` phase. If you want future indices to continue using {{search-snaps}}, configure the `searchable_snapshot` action in an appropriate remaining phase. Also update any allocation rules that reference the removed tier.

    For guidance on updating policies, refer to [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

1. Re-enable {{ilm-init}}:

   ```sh
   POST /_ilm/start
   ```

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
