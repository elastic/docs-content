---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-source-only-repository.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Source-only repository [snapshots-source-only-repository]

You can use a source-only repository to take minimal, source-only snapshots that use up to 50% less disk space than regular snapshots.

Unlike other repository types, a source-only repository doesn’t directly store snapshots. It delegates storage to another registered snapshot repository.

When you take a snapshot using a source-only repository, {{es}} creates a source-only snapshot in the delegated storage repository. This snapshot only contains stored fields and metadata. It doesn’t include index or doc values structures and isn’t immediately searchable when restored. To search the restored data, you first have to [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) it into a new data stream or index.

::::{important}
Source-only snapshots are only supported if the `_source` field is enabled and no source-filtering is applied. As a result, indices adopting synthetic source cannot be restored. When you restore a source-only snapshot:

* The restored index is read-only and can only serve `match_all` search or scroll requests to enable reindexing.
* Queries other than `match_all` and `_get` requests are not supported.
* The mapping of the restored index is empty, but the original mapping is available from the types top level `meta` element.
* Information such as document count, deleted document count and store size are not available for such indices since these indices do not contain the relevant data structures to retrieve this information from. Therefore, this information is not shown for such indices in APIs such as the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

::::


Before registering a source-only repository, use {{kib}} or the [create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository) to register a snapshot repository of another type to use for storage. Then register the source-only repository and specify the delegated storage repository in the request.

```console
PUT _snapshot/my_src_only_repository
{
  "type": "source",
  "settings": {
    "delegate_type": "fs",
    "location": "my_backup_repository"
  }
}
```

## Repository settings [source-only-repository-settings]

The `source` repository type supports a number of settings to customize how data is stored, which may be specified when creating the repository.

Repository settings cover delegation to another repository type, snapshot data layout and compression, throughput limits, read-only mode, and the maximum number of snapshots.
For a complete list of all source-only repository settings, refer to [Source-only repository settings](elasticsearch://reference/elasticsearch/configuration-reference/source-repository-settings.md#repository-source-repository-settings).


