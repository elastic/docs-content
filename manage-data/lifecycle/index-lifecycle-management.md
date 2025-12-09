---
navigation_title: Index lifecycle managment
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/overview-index-lifecycle-management.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-concepts.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-index-management.html
  - https://www.elastic.co/guide/en/cloud/current/ec-configure-index-management.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
---

# {{ilm-cap}} ({{ilm-init}}) in {{es}}

{{ilm}} ({{ilm-init}}) automates the management of time-based indices, such as logs and metrics. Using {{ILM-init}} policies, you can streamline index rollover, retention, and deletion to optimize performance, reliability, and storage costs for your data.

For example, you can use {{ilm-init}} to:

* Spin up a new index when an index reaches a certain size or number of documents
* Create a new index each day, week, or month and archive previous ones
* Delete stale indices to enforce data retention standards

::::{important}
To use {{ilm-init}}, all nodes in a cluster must run the same version. Although it might be possible to create and apply policies in a mixed-version cluster, there is no guarantee they will work as intended. Attempting to use a policy that contains actions that aren’t supported on all nodes in a cluster will cause errors.
::::

## {{ilm-init}} availability

Note the availability of {{ilm-init}} to ensure that it's applicable for your use case.

* You can use {{ilm-init}} to manage indices and data streams:

    * **Indices:** You use {{ilm-init}} to manage a specific index or set of indices by defining a lifecycle policy and applying it to the indices or an index alias. Each index is then evaluated against its policy and transitions through phases (`hot`, `warm`, `cold`, `frozen`, `delete`) based on pre-defined conditions. This approach allows for more granular control over each index but requires considerably more effort compared to using a data stream, which is our recommended option.

    * **Data streams:** A [data stream](/manage-data/data-store/data-streams.md) acts as a layer of abstraction over a set of indices that contain append-only, time series data. You can configure {{ilm-init}} using a data stream as a single named resource, so that rollover and any other configured actions are performed on the data stream's backing indices automatically.

* {{ilm-init}} is available for all deployment types on the versioned {{stack}} but is not available for {{es-serverless}}. In a {{serverless-short}} environment, [data stream lifecycle](/manage-data/lifecycle/data-stream.md) is available as a data lifecycle option.

    :::{admonition} Simpler lifecycle management in Serverless environments
    {{ilm-init}} lets you automatically transition indices through data tiers according to your performance needs and retention requirements. This allows you to balance hardware costs with performance. {{ilm-init}} is not available in {{serverless-short}} because in that environment your cluster performance is optimized for you. Instead, data stream lifecycle is available as a data management option.

    Data stream lifecycle is a simpler lifecycle management tool optimized for the most common lifecycle management needs. It enables you to configure the retention duration for your data and to optimize how the data is stored, without hardware-centric concepts like data tiers. For a detailed comparison of {{ilm-init}} and data stream lifecycle refer to [Data lifecycle](/manage-data/lifecycle.md).
    :::

## Index lifecycle actions

{{ilm-init}} policies can trigger actions like:

* **Rollover**: Creates a new write index when the current one reaches a certain size, number of docs, or age.
* **Shrink**: Reduces the number of primary shards in an index.
* **Force merge**: Triggers a [force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) to reduce the number of segments in an index’s shards.
* **Delete**: Permanently remove an index, including all of its data and metadata.
* [And more](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md)

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

**Learn about all available actions in [Index lifecycle actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md).**

## Create and manage {{ilm-init}} policies

You can create and manage index lifecycle policies through {{kib}}'s [Index Management](/manage-data/data-store/index-basics.md#index-management) UI or the [{{ilm-init}} APIs]({{es-apis}}group/endpoint-ilm). For more details on creating and managing index lifecycle policies refer to:

* [Create an {{ilm}} policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md)
* [Check the {{ilm-init}} status of {{es}} indices and data streams](/manage-data/lifecycle/index-lifecycle-management/policy-view-status.md)
* [Update or switch an {{es}} index lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md)
* [Restore managed indices and manage {{ilm-init}} actions](/manage-data/lifecycle/index-lifecycle-management/restore-managed-data-stream-index.md)
* [](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md)

Default {{ilm}} policies are created automatically when you install an [Elastic Integration](integration-docs://reference/index.md), or when you use {{agent}}, {{beats}}, or the {{ls}} {{es}} output plugin to send data to the {{stack}}.

![index lifecycle policies](/manage-data/images/elasticsearch-reference-index-lifecycle-policies.png)

::::{tip}
To automatically back up your indices and manage snapshots, use [snapshot lifecycle policies](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm).
::::

## Pausing and troubleshooting {{ilm-init}}

In case you want to temporarily pause the {{ilm-init}} service while you perform maintenance, make other changes to your cluster, or do any troubleshooting, refer to [](/manage-data/lifecycle/index-lifecycle-management/start-stop-index-lifecycle-management.md).

In the event of any issues running {{ilm-init}}, refer to [Fix index lifecycle management errors](/troubleshoot/elasticsearch/index-lifecycle-management-errors.md) for detailed troubleshooting guidance. 

## Migrate to {{ilm-init}}

For existing hot-warm deployments that are currently using index curation, migrating to ILM gives you more fine-grained control over the lifecycle of each index. Read more in:

* [](/manage-data/lifecycle/index-lifecycle-management/manage-existing-indices.md)
* [](/manage-data/lifecycle/index-lifecycle-management/migrate-index-management.md)
* [](/manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md)

You can also set up {{ilm-init}} to manage an existing set of indices that do not already have a managed lifecycle. The {{ilm-init}} policy that you apply should not contain a rollover action, because the policy won't be carried forward when the rollover action creates a new index. Refer to [](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md) to learn more.