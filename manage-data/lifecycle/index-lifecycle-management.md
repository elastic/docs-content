---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/overview-index-lifecycle-management.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-concepts.html
---

# Index lifecycle management

{{ilm-cap}} ({{ilm-init}}) provides an integrated and streamlined way to manage time-based data such as logs and metrics, making it easier to follow best practices for managing your indices.

You can configure {{ilm-init}} policies to automatically manage indices according to your performance, resiliency, and retention requirements. For example, you could use {{ilm-init}} to:

* Spin up a new index when an index reaches a certain size or number of documents
* Create a new index each day, week, or month and archive previous ones
* Delete stale indices to enforce data retention standards

::::{tip}
{{ilm-init}} is not available on {{es-serverless}}.

:::{dropdown} Why?
In an {{ecloud}} or self-managed environment, ILM lets you automatically transition indices through data tiers according to your performance needs and retention requirements. This allows you to balance hardware costs with performance. {{es-serverless}} eliminates this complexity by optimizing your cluster performance for you.

Data stream lifecycle is an optimized lifecycle tool that lets you focus on the most common lifecycle management needs, without unnecessary hardware-centric concepts like data tiers.
:::
::::

::::{important}
To use {{ilm-init}}, all nodes in a cluster must run the same version. Although it might be possible to create and apply policies in a mixed-version cluster, there is no guarantee they will work as intended. Attempting to use a policy that contains actions that aren’t supported on all nodes in a cluster will cause errors.
::::

## Actions

{{ilm-init}} policies can trigger actions like:

* **Rollover**: Creates a new write index when the current one reaches a certain size, number of docs, or age.
* **Shrink**: Reduces the number of primary shards in an index.
* **Force merge**: Triggers a [force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) to reduce the number of segments in an index’s shards.
* **Delete**: Permanently remove an index, including all of its data and metadata.
* [And more](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/index.md)

Each action has options you can use to specify index behavior and characteristics like:

* The maximum shard size, number of documents, or age at which you want to roll over to a new index.
* The point at which the index is no longer being updated and the number of primary shards can be reduced.
* When to force a merge to permanently remove documents marked for deletion.
* The point at which the index can be moved to less performant hardware.
* The point at which the availability is not as critical and the number of replicas can be reduced.
* When the index can be safely deleted.

For example, if you are indexing metrics data from a fleet of ATMs into Elasticsearch, you might define a policy that says:

1. When the total size of the index’s primary shards reaches 50GB, roll over to a new index.
2. Move the old index into the warm phase, mark it read only, and shrink it down to a single shard.
3. After 7 days, move the index into the cold phase and move it to less expensive hardware.
4. Delete the index once the required 30 day retention period is reached.

**Learn about all available actions in [Index lifecycle actions](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/index.md).**

## Create and manage {{ilm-init}} policies

You can create and manage index lifecycle policies through [{{kib}} Management](/manage-data/lifecycle/index-lifecycle-management/index-management-in-kibana.md) or the [{{ilm-init}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-ilm). For more details on creating and managing index lifecycle policies refer to:

* [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md)
* [Update a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md)
* [Start and stop index lifecycle management](/manage-data/lifecycle/index-lifecycle-management/start-stop-index-lifecycle-management.md)
* [Restore a managed data stream or index](/manage-data/lifecycle/index-lifecycle-management/restore-managed-data-stream-index.md)
* [Customize built-in policies](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md)

Default {{ilm}} policies are created automatically when you use {{agent}}, {{beats}}, or the {{ls}} {{es}} output plugin to send data to the {{stack}}.

![index lifecycle policies](../../images/elasticsearch-reference-index-lifecycle-policies.png)

::::{tip}
To automatically back up your indices and manage snapshots, use [snapshot lifecycle policies](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm).
::::

## Migrate to {{ilm-init}}

For existing hot-warm deployments that are currently using index curation, migrating to ILM gives you more fine-grained control over the lifecycle of each index. Read more in:

* [Manage existing indices](/manage-data/lifecycle/index-lifecycle-management/manage-existing-indices.md)
* [Migrate to index lifecycle management](/manage-data/lifecycle/index-lifecycle-management/migrate-index-management.md)
* [Migrate index allocation filters to node roles](/manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md)
