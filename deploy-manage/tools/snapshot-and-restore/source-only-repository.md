---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-source-only-repository.html
applies_to:
  deployment:
    self:
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
%  TEST[setup:setup-repository]
%  TEST[s/my_backup_repository/my_repository/]

## Repository settings [source-only-repository-settings]

`chunk_size`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum size of files in snapshots. In snapshots, files larger than this are broken down into chunks of this size or smaller. Defaults to `null` (unlimited file size).

`compress`
:   (Optional, Boolean) If `true`, metadata files, such as index mappings and settings, are compressed in snapshots. Data files are not compressed. Defaults to `true`.

`delegate_type`
:   (Optional, string) Delegated repository type. For valid values, see the [`type` parameter](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository#put-snapshot-repo-api-request-type).

    `source` repositories can use `settings` properties for its delegated repository type.


`max_number_of_snapshots`
:   (Optional, integer) Maximum number of snapshots the repository can contain. Defaults to `Integer.MAX_VALUE`, which is `2^31-1` or `2147483647`.

`max_restore_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`max_snapshot_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md#recovery-settings-for-managed-services) are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`readonly`
:   (Optional, Boolean) If `true`, the repository is read-only. The cluster can retrieve and restore snapshots from the repository but not write to the repository or create snapshots in it.

    Only a cluster with write access can create snapshots in the repository. All other clusters connected to the repository should have the `readonly` parameter set to `true`.

    If `false`, the cluster can write to the repository and create snapshots in it. Defaults to `false`.

    ::::{important}
    If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. Having multiple clusters write to the repository at the same time risks corrupting the contents of the repository.

    ::::



