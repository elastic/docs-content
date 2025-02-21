---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-allocation.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-filtering.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/recovery-prioritization.html
---

# Index-level shard allocation

% What needs to be done: Refine

% Scope notes: also reference https://www.elastic.co/guide/en/elasticsearch/reference/current/allocation-total-shards.html and https://www.elastic.co/guide/en/elasticsearch/reference/current/data-tier-shard-filtering.html

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/index-modules-allocation.md
%      Notes: conceptual content
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/shard-allocation-filtering.md
%      Notes: conceptual content
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/recovery-prioritization.md
%      Notes: conceptual content

⚠️ **This page is a work in progress.** ⚠️

The documentation team is working to combine content pulled from the following pages:

* [/raw-migrated-files/elasticsearch/elasticsearch-reference/index-modules-allocation.md](../../../raw-migrated-files/elasticsearch/elasticsearch-reference/index-modules-allocation.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/shard-allocation-filtering.md](../../../raw-migrated-files/elasticsearch/elasticsearch-reference/shard-allocation-filtering.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/recovery-prioritization.md](../../../raw-migrated-files/elasticsearch/elasticsearch-reference/recovery-prioritization.md)

In Elasticsearch, per-index settings allow you to control the allocation of shards to nodes through index-level shard allocation settings. These settings enable you to specify preferences or constraints for where shards of a particular index should reside. This includes allocating shards to nodes with specific attributes or avoiding certain nodes. This level of control helps optimize resource utilization, balance load, and ensure data redundancy and availability according to your deployment's specific requirements. In addition to the content in this article, there are additional resources:

* [Shard allocation filtering](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md): Controlling which shards are allocated to which nodes.
* [Delayed allocation](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/delaying-allocation-when-node-leaves.md): Delaying allocation of unassigned shards caused by a node leaving.
* [Total shards per node](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/total-shards-per-node.md): A hard limit on the number of shards from the same index per node.
* [Data tier allocation](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/data-tier-allocation-settings.md): Controls the allocation of indices to [data tiers](../../../manage-data/lifecycle/data-tiers.md).

## Index-level shard allocation filtering [shard-allocation-filtering]

You can use shard allocation filters to control where {{es}} allocates shards of a particular index. These per-index filters are applied in conjunction with [cluster-wide allocation filtering](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-shard-allocation-filtering) and [allocation awareness](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md).

Shard allocation filters can be based on [custom node attributes](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#custom-node-attributes) or the built-in `_name`, `_host_ip`, `_publish_ip`, `_ip`, `_host`, `_id`, `_tier` and `_tier_preference` attributes. [Index lifecycle management](../../../manage-data/lifecycle/index-lifecycle-management.md) uses filters based on custom node attributes to determine how to reallocate shards when moving between phases.

The `cluster.routing.allocation` settings are dynamic, enabling existing indices to be moved immediately from one set of nodes to another. Shards are only relocated if it is possible to do so without breaking another routing constraint, such as never allocating a primary and replica shard on the same node.

For example, you could use a custom node attribute to indicate a node’s performance characteristics and use shard allocation filtering to route shards for a particular index to the most appropriate class of hardware.


### Enabling index-level shard allocation filtering [index-allocation-filters] 

To filter based on a custom node attribute:

1. Specify the filter characteristics with a custom node attribute in each node’s `elasticsearch.yml` configuration file. For example, if you have `small`, `medium`, and `big` nodes, you could add a `size` attribute to filter based on node size.

    ```yaml
    node.attr.size: medium
    ```

    You can also set custom attributes when you start a node:

    ```sh
    ./bin/elasticsearch -Enode.attr.size=medium
    ```

2. Add a routing allocation filter to the index. The `index.routing.allocation` settings support three types of filters: `include`, `exclude`, and `require`. For example, to tell {{es}} to allocate shards from the `test` index to either `big` or `medium` nodes, use `index.routing.allocation.include`:

    ```console
    PUT test/_settings
    {
      "index.routing.allocation.include.size": "big,medium"
    }
    ```

    If you specify multiple filters the following conditions must be satisfied simultaneously by a node in order for shards to be relocated to it:

    * If any `require` type conditions are specified, all of them must be satisfied
    * If any `exclude` type conditions are specified, none of them may be satisfied
    * If any `include` type conditions are specified, at least one of them must be satisfied

    For example, to move the `test` index to `big` nodes in `rack1`, you could specify:

    ```console
    PUT test/_settings
    {
      "index.routing.allocation.require.size": "big",
      "index.routing.allocation.require.rack": "rack1"
    }
    ```

### Index allocation filter settings [index-allocation-settings]

`index.routing.allocation.include.{{attribute}}`
:   Assign the index to a node whose `{{attribute}}` has at least one of the comma-separated values.

`index.routing.allocation.require.{{attribute}}`
:   Assign the index to a node whose `{{attribute}}` has *all* of the comma-separated values.

`index.routing.allocation.exclude.{{attribute}}`
:   Assign the index to a node whose `{{attribute}}` has *none* of the comma-separated values.

The index allocation settings support the following built-in attributes:

`_name`
:   Match nodes by node name

`_host_ip`
:   Match nodes by host IP address (IP associated with hostname)

`_publish_ip`
:   Match nodes by publish IP address

`_ip`
:   Match either `_host_ip` or `_publish_ip`

`_host`
:   Match nodes by hostname

`_id`
:   Match nodes by node id

`_tier`
:   Match nodes by the node’s [data tier](../../../manage-data/lifecycle/data-tiers.md) role. For more details see [data tier allocation filtering](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/data-tier-allocation-settings.md)

::::{note} 
`_tier` filtering is based on [node](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md) roles. Only a subset of roles are [data tier](../../../manage-data/lifecycle/data-tiers.md) roles, and the generic [data role](../../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role) will match any tier filtering.
::::

You can use wildcards when specifying attribute values, for example:

```console
PUT test/_settings
{
  "index.routing.allocation.include._ip": "192.168.2.*"
}
```

## Index recovery prioritization [recovery-prioritization]

Unallocated shards are recovered in order of priority, whenever possible. Indices are sorted into priority order as follows:

* the optional `index.priority` setting (higher before lower)
* the index creation date (higher before lower)
* the index name (higher before lower)

This means that, by default, newer indices will be recovered before older indices.

Use the per-index dynamically updatable `index.priority` setting to customise the index prioritization order. For instance:

```console
PUT index_1

PUT index_2

PUT index_3
{
  "settings": {
    "index.priority": 10
  }
}

PUT index_4
{
  "settings": {
    "index.priority": 5
  }
}
```

In the above example:

* `index_3` will be recovered first because it has the highest `index.priority`.
* `index_4` will be recovered next because it has the next highest priority.
* `index_2` will be recovered next because it was created more recently.
* `index_1` will be recovered last.

This setting accepts an integer, and can be updated on a live index with the [update index settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings):

```console
PUT index_4/_settings
{
  "index.priority": 1
}
```