---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/archive-indices.html
---

# Reading indices from older Elasticsearch versions [archive-indices]

{{es}} has full query and write support for indices created in the previous major version. If you have indices created in {{es}} versions 5 or 6, you can now use the archive functionality to import them into newer {{es}} versions as well.

The archive functionality provides slower read-only access to older {{es}} data, for compliance or regulatory reasons, the occasional lookback or investigation, or to rehydrate parts of it. Access to the data is expected to be infrequent, and can therefore happen with limited performance and query capabilities.

For this, {{es}} has the ability to access older snapshot repositories (going back to version 5). The legacy indices in the [snapshot repository](../../tools/snapshot-and-restore.md) can either be [restored](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore), or can be directly accessed via [searchable snapshots](../../tools/snapshot-and-restore/searchable-snapshots.md) so that the archived data won’t even need to fully reside on local disks for access.


## Supported field types [archive-indices-supported-field-types]

Old mappings are imported as much "as-is" as possible into {{es}} 8, but only provide regular query capabilities on a select subset of fields:

* [Numeric types](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`boolean` type](elasticsearch://reference/elasticsearch/mapping-reference/boolean.md)
* [`ip` type](elasticsearch://reference/elasticsearch/mapping-reference/ip.md)
* [`geo_point` type](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md)
* [`date` types](elasticsearch://reference/elasticsearch/mapping-reference/date.md): the date `format` setting on date fields is supported as long as it behaves similarly across these versions. In case it is not, for example [when using custom date formats](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/migrate-to-java-time.html), this field can be updated on legacy indices so that it can be changed by a user if need be.
* [`keyword` type](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type): the `normalizer` setting on keyword fields is supported as long as it behaves similarly across these versions. In case it is not, this field can be updated on legacy indices if need be.
* [`text` type](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type): scoring capabilities are limited, and all queries return constant scores that are equal to 1.0. The `analyzer` settings on text fields are supported as long as they behave similarly across these versions. In case they do not, they can be updated on legacy indices if need be.
* [Multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md)
* [Field aliases](elasticsearch://reference/elasticsearch/mapping-reference/field-alias.md)
* [`object`](elasticsearch://reference/elasticsearch/mapping-reference/object.md) fields
* some basic metadata fields, e.g. `_type` for querying {{es}} 5 indices
* [runtime fields](../../../manage-data/data-store/mapping/map-runtime-field.md)
* [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md)

{{es}} 5 indices with mappings that have [multiple mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/removal-of-types.html) are collapsed together on a best-effort basis before they are imported.

In case the auto-import of mappings does not work, or the new {{es}} version can’t make sense of the mapping, it falls back to importing the index without the mapping, but stores the original mapping in the [_meta](elasticsearch://reference/elasticsearch/mapping-reference/mapping-meta-field.md) section of the imported index. The legacy mapping can then be introspected using the [GET mapping](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping) API and an updated mapping can be manually put in place using the [update mapping](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) API, copying and adapting relevant sections of the legacy mapping to work with the current {{es}} version. While auto-import is expected to work in most cases, failures of doing so should be [raised](https://github.com/elastic/elasticsearch/issues/new/choose) with the Elastic team for future improvements.


## Supported APIs [_supported_apis]

Archive indices are read-only, and provide data access via the [search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) and [field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps) APIs. They do not support the [Get API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get) nor any write APIs.

Archive indices allow running queries as well as aggregations in so far as they are [supported by the given field type](#archive-indices-supported-field-types).

Due to `_source` access the data can also be [reindexed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) to a new index that has full compatibility with the current {{es}} version.


## How to upgrade older {{es}} 5 or 6 clusters? [_how_to_upgrade_older_es_5_or_6_clusters]

Take a snapshot of the indices in the old cluster, delete indices that are not directly supported by ES 8 (i.e. indices older than 7.0), upgrade the cluster without the old indices, and then [restore](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) the legacy indices from the snapshot or [mount](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-searchable-snapshots-mount) them via searchable snapshots.

In the future, we plan on streamlining the upgrade process going forward, making it easier to take legacy indices along when going to future major {{es}} versions.

