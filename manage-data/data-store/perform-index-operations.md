---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html#view-edit-indices
  - https://www.elastic.co/guide/en/serverless/current/index-management.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Manage and perform operations on indices [manage-indices-operations]

Elastic's Index Management features are an easy, convenient way to manage your cluster’s indices, data streams, templates, and enrich policies. Practicing good index management ensures your data is stored correctly and in the most cost-effective way possible.

You can investigate your indices on the **{{index-manage-app}}** page in {{kib}}. To open the **{{index-manage-app}}** page, use the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Managing indices in {{kib}} [manage-indices]

### Required permissions for {{security-features}} [required-permissions]
:applies_to: {"stack": "ga"}

If you use {{es}} {{security-features}}, the following [security privileges](elasticsearch://reference/elasticsearch/security-privileges.md) are required:

* The `monitor` cluster privilege to access {{kib}}'s **{{index-manage-app}}** features.
* The `view_index_metadata` and `manage` index privileges to view a data stream or index's data.

To add these privileges, go to **{{stack-manage-app}} > Security > Roles** or use the [Create or update roles](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) API.

The **{{index-manage-app}}** page includes the following tabs:

**Indices**
:   View, investigate, and perform operations on your indices. Refer to [Performing operations on indices](#performing-operations-on-indices) on this page.

**Data Streams**
:   View and manage your [data streams](/manage-data/data-store/data-streams.md), including their backing indices and retention settings. Refer to [Manage a data stream](/manage-data/data-store/data-streams/manage-data-stream.md) for details.

**Index Templates** 
:   Create, edit, clone, and delete [index templates](/manage-data/data-store/templates.md) that define how {{es}} configures new indices or data streams.

**Component Templates**
:   Create, edit, clone, and delete [component templates](/manage-data/data-store/templates.md#component-templates), the reusable building blocks used by index templates to define settings, mappings, and aliases.

**Enrich Policies**
:   Create, execute, and delete [enrich policies](/manage-data/ingest/transform-enrich/data-enrichment.md) that add data from existing indices to incoming documents during ingest.



To open the **{{index-manage-app}}** page, use the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).


:::::{applies-switch}

::::{applies-item} serverless:

:::{image} /manage-data/images/serverless-index-management-indices.png
:alt: Index Management indices
:screenshot:
:::

* To access details and perform operations on indices:

    * For a single index, click the index name to drill down into the index overview, [mappings](/manage-data/data-store/mapping.md), and [settings](elasticsearch://reference/elasticsearch/index-settings/index.md). From this view, you can navigate to **Discover** to further explore the documents in the index.

    * For multiple indices, select their checkboxes and then open the **Manage indices** menu. 

* Turn on **Include hidden indices** to view the full set of indices, including backing indices for data streams.

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).
::::

::::{applies-item} stack:
:sync: stack

:::{image} /manage-data/images/elasticsearch-reference-management_index_labels.png
:alt: Index Management UI
:screenshot:
:::

* To access details and perform operations on indices:

    * For a single index, click the index name to drill down into the index overview, [mappings](/manage-data/data-store/mapping.md), [settings](elasticsearch://reference/elasticsearch/index-settings/index.md), and statistics. From this view, you can navigate to **Discover** to further explore the documents in the index, and you can perform operations using the **Manage index** menu.

    * For multiple indices, select their checkboxes and then open the **Manage indices** menu. 

* Turn on **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).
::::
:::::

## Performing operations on indices [performing-operations-on-indices]

You can investigate your indices and perform operations from the **Indices** view on the **{{index-manage-app}}** page in {{kib}}.

To perform index actions:

1. Go to the **Index management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Enable **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).
1. Open the **Indices** view.
1. Click the index name, or to perform operations on multiple indices select their checkboxes and open the **Manage index** menu.


### Available index operations

The following operations are available from the **Manage index** menu. Some operations are unavailable in {{serverless-full}} because data management tasks are handled automatically.

**Show index overview** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   View an overview of the index, including its storage size, status, and aliases, as well as a sample API request to add new documents.

**Show index settings** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   View a list of the currently configured [index settings](elasticsearch://reference/elasticsearch/index-settings/index.md). Turn on **Edit mode** to add or change settings.

**Show index mapping** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   View the [index mappings](/manage-data/data-store/mapping.md). From this page you can set up new mappings for the field types in your index.

**Show index stats** {applies_to}`stack: ga`
:   View statistics for your index. Statistics are compiled by `primaries`, representing values only for primary shards, and by `total`, representing accumulated values for both primary and replica shards. Refer to the [get index statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-stats) API for details.

**Close index** {applies_to}`stack: ga`
:   Close the index so that read or write operations cannot be performed. Refer to the [close index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close) API for details.

**Open index** {applies_to}`stack: ga`
:   Reopen an index that is currently closed to read and write operations. This option is available only for indices that are currently closed. Refer to the [open index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open) API for details.

**Force merge index** {applies_to}`stack: ga`
:   Reduce the number of segments in each shard by merging some of them together and free up the space used by deleted documents. Refer to the [force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) API for details.

**Refresh index** {applies_to}`stack: ga`
:   Refresh the index to make recent operations available for search. Refer to the [refresh index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-refresh) API for details.

**Clear index cache** {applies_to}`stack: ga`
:   Clear all caches for the index. Refer to the [clear cache](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clear-cache) API for details.

**Flush index** {applies_to}`stack: ga`
:   Flush the index to permanently write all data currently in the transaction log to the Lucene index. Refer to the [flush index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-flush) API for details.

**Delete index** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   Delete an index including all of its documents, shards, and metadata. Refer to the [delete index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete) API for details.

**Add lifecycle policy** {applies_to}`stack: ga`
:   Add a lifecycle policy to manage how the index transitions over time. The policy governs how the index moves through phases (`hot`, `warm`, `cold`, `frozen`, and `delete`) and what actions are performed during each phase (for example, shrinking and downsampling). Refer to [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md) for details.

**Convert to lookup index** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview`
:   Convert the index to a lookup mode index that can be used with [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) commands, so that data from the index can be added to {{esql}} query results. This option is available only for single shard indices with fewer than two billion documents. Refer to the {{es}} [`index.mode`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting) index setting for details.
