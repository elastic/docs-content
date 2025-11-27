---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Perform operations on indices

You can perform a number of index operations from the **Index management** page in {{kib}}.

To perform index actions:

1. Go to the **Index management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Enable **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).
1. Open the **Indices** view.
1. Click the index name, or to perform operations on multiple indices select their checkboxes and open the **Manage index** menu.

## Available index operations

Several index operations are available from the **Manage index** menu. Some of the operations listed are unavailable in {{serverless-full}} since in that environment many data management tasks are handled automatically.

**Show index overview** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   View an overview of the index, including its storage size, status, and aliases, as well as a sample API request to add new documents.

**Show index settings** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   View a list of the currently configured [index settings](elasticsearch://reference/elasticsearch/index-settings/index.md). Enable **Edit mode** to add or change settings.

**Show index mapping** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   View the [index mappings](/manage-data/data-store/mapping.md). From this page you can set up new mappings for the field types in your index.

**Show index stats** {applies_to}`stack: ga`
:   View statistics for your index. Statistics are compiled by `primaries`, representing values only for primary shards, and by `total`, representing accumulated values for both primary and replica shards. Refer to the [get index statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-stats) API for details.

**Close index** {applies_to}`stack: ga`
:   Close the index so that read or write operations cannot be performed. Refer to the [close index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close) API for details.

**Open index** {applies_to}`stack: ga`
:   Reopen an index that is currently closed to read and write operations. This option is available only for indices that are currently closed. Refer to the [open index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open) API for details.

**Force merge index** {applies_to}`stack: ga`
:   Perform a force merge operation on the shards of the indices. This reduces the number of segments in each shard by merging some of them together and also frees up the space used by deleted documents. Refer to the [force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) API for details.

**Refresh index** {applies_to}`stack: ga`
:   Refresh the index to make the most recent operations performed on the index available for search. Refer to the [refresh index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-refresh) API for details.

**Clear index cache** {applies_to}`stack: ga`
:   Clear all of the caches for the index. Refer to the [clear cache](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clear-cache) API for details.

**Flush index** {applies_to}`stack: ga`
:   Flush the index to ensure that all data currently stored only in the transaction log is stored permanently in the Lucene index. Refer to the [flush index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-flush) API for details.

**Delete index** {applies_to}`stack: ga` {applies_to}`serverless: ga`
:   Delete an index including all of its documents, shards, and metadata. Refer to the [delete index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete) API for details.

**Add lifecycle policy** {applies_to}`stack: ga`
:   Add a lifecycle policy to the index to manage how it transitions over time. The policy governs how the index moves through different phases (`hot`, `warm`, `cold`, `frozen`, and `delete`) and what actions, such as shrinking and downsampling, are performed on the index during each of these phases. Refer to [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md) to learn more.

**Convert to lookup index** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview`
:   Convert the index to a lookup mode index that can be used with [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) commands, so that data from the index can be added to {{esql}} query results. This option is available only for single shard indices that have less than two billion documents. Refer to the {{es}} [`index.mode`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting) index setting for details.
