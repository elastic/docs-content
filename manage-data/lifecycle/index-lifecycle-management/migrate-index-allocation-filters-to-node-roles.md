---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/migrate-index-allocation-filters.html
applies_to:
  stack: ga
  serverless: ga
---

# Migrate index allocation filters to node roles [migrate-index-allocation-filters]

If you currently use [custom node attributes](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#custom-node-attributes) and [attribute-based allocation filters](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) to move indices through [data tiers](../data-tiers.md) in a [hot-warm-cold architecture](https://www.elastic.co/blog/implementing-hot-warm-cold-in-elasticsearch-with-index-lifecycle-management), we recommend that you switch to using the built-in node roles and automatic [data tier allocation](../data-tiers.md#data-tier-allocation). Using node roles enables {{ilm-init}} to automatically move indices between data tiers.

::::{note} 
While we recommend relying on automatic data tier allocation to manage your data in a hot-warm-cold architecture, you can still use attribute-based allocation filters to control shard allocation for other purposes.
::::


{{ech}} and {{ece}} can perform the migration automatically. For self-managed deployments, you need to manually update your configuration, ILM policies, and indices to switch to node roles.


## Automatically migrate to node roles on {{ech}} or {{ece}} [cloud-migrate-to-node-roles] 

If you are using node attributes from the default deployment template in {{ech}} or {{ece}}, you will be prompted to switch to node roles when you:

* Upgrade to {{es}} 7.10 or higher
* Deploy a warm, cold, or frozen data tier
* [Enable autoscaling](../../../deploy-manage/autoscaling.md)

These actions automatically update your cluster configuration and {{ilm-init}} policies to use node roles. Additionally, upgrading to version 7.14 or higher automatically update {{ilm-init}} policies whenever any configuration change is applied to your deployment.

If you use custom index templates, check them after the automatic migration completes and remove any [attribute-based allocation filters](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md).

::::{note} 
You do not need to take any further action after the automatic migration. The following manual steps are only necessary if you do not allow the automatic migration or have a self-managed deployment.
::::



## Migrate to node roles on self-managed deployments [on-prem-migrate-to-node-roles] 

To switch to using node roles:

1. [Assign data nodes](#assign-data-tier) to the appropriate data tier.
2. [Remove the attribute-based allocation settings](#remove-custom-allocation-settings) from your {{ilm}} policy.
3. [Stop setting the custom hot attribute](#stop-setting-custom-hot-attribute) on new indices.
4. Update existing indices to [set a tier preference](#set-tier-preference).


### Assign data nodes to a data tier [assign-data-tier] 

Configure the appropriate roles for each data node to assign it to one or more data tiers: `data_hot`, `data_content`, `data_warm`, `data_cold`, or `data_frozen`. A node can also have other [roles](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md). By default, new nodes are configured with all roles.

When you add a data tier to an {{ech}} deployment, one or more nodes are automatically configured with the corresponding role. To explicitly change the role of a node in an {{ech}} deployment, use the [Update deployment API](../../../deploy-manage/deploy/elastic-cloud/manage-deployments-using-elastic-cloud-api.md#ec_update_a_deployment). Replace the node’s `node_type` configuration with the appropriate `node_roles`. For example, the following configuration adds the node to the hot and content tiers, and enables it to act as an ingest node, remote, and transform node.

```yaml
"node_roles": [
  "data_hot",
  "data_content",
  "ingest",
  "remote_cluster_client",
  "transform"
],
```

If you are directly managing your own cluster, configure the appropriate roles for each node in `elasticsearch.yml`. For example, the following setting configures a node to be a data-only node in the hot and content tiers.

```yaml
node.roles [ data_hot, data_content ]
```


### Remove custom allocation settings from existing {{ilm-init}} policies [remove-custom-allocation-settings] 

Update the allocate action for each lifecycle phase to remove the attribute-based allocation settings. {{ilm-init}} will inject a [migrate](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) action into each phase to automatically transition the indices through the data tiers.

If the allocate action does not set the number of replicas, remove the allocate action entirely. (An empty allocate action is invalid.)

::::{important} 
The policy must specify the corresponding phase for each data tier in your architecture. Each phase must be present so {{ilm-init}} can inject the migrate action to move indices through the data tiers. If you don’t need to perform any other actions, the phase can be empty. For example, if you enable the warm and cold data tiers for a deployment, your policy must include the hot, warm, and cold phases.
::::



### Stop setting the custom hot attribute on new indices [stop-setting-custom-hot-attribute] 

When you create a data stream, its first backing index is now automatically assigned to `data_hot` nodes. Similarly, when you directly create an index, it is automatically assigned to `data_content` nodes.

On {{ech}} deployments, remove the `cloud-hot-warm-allocation-0` index template that set the hot shard allocation attribute on all indices.

```console
DELETE _template/.cloud-hot-warm-allocation-0
```

If you’re using a custom index template, update it to remove the [attribute-based allocation filters](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) you used to assign new indices to the hot tier.

To completely avoid the issues that raise when mixing the tier preference and custom attribute routing setting we also recommend updating all the legacy, composable, and component templates to remove the [attribute-based allocation filters](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) from the settings they configure.


### Set a tier preference for existing indices [set-tier-preference] 

{{ilm-init}} automatically transitions managed indices through the available data tiers by automatically injecting a [migrate action](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) into each phase.

To enable {{ilm-init}} to move an *existing* managed index through the data tiers, update the index settings to:

1. Remove the custom allocation filter by setting it to `null`.
2. Set the [tier preference](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/data-tier-allocation.md#tier-preference-allocation-filter).

For example, if your old template set the `data` attribute to `hot` to allocate shards to the hot tier, set the `data` attribute to `null` and set the `_tier_preference` to `data_hot`.

```console
PUT my-index/_settings
{
  "index.routing.allocation.require.data": null,
  "index.routing.allocation.include._tier_preference": "data_hot"
}
```

For indices that have already transitioned out of the hot phase, the tier preference should include the appropriate fallback tiers to ensure index shards can be allocated if the preferred tier is unavailable. For example, specify the hot tier as the fallback for indices already in the warm phase.

```console
PUT my-index/_settings
{
  "index.routing.allocation.require.data": null,
  "index.routing.allocation.include._tier_preference": "data_warm,data_hot"
}
```

If an index is already in the cold phase, include the cold, warm, and hot tiers.

For indices that have both the `_tier_preference` and `require.data` configured but the `_tier_preference` is outdated (ie. the node attribute configuration is "colder" than the configured `_tier_preference`), the migration needs to remove the `require.data` attribute and update the `_tier_preference` to reflect the correct tiering.

eg. For an index with the following routing configuration:

```JSON
{
  "index.routing.allocation.require.data": "warm",
  "index.routing.allocation.include._tier_preference": "data_hot"
}
```

The routing configuration should be fixed like so:

```console
PUT my-index/_settings
{
  "index.routing.allocation.require.data": null,
  "index.routing.allocation.include._tier_preference": "data_warm,data_hot"
}
```

This situation can occur in a system that defaults to data tiers when, e.g., an ILM policy that uses node attributes is restored and transitions the managed indices from the hot phase into the warm phase. In this case the node attribute configuration indicates the correct tier where the index should be allocated.

