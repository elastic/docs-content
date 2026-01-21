---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/archive-indices.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Reading indices from older {{es}} versions [archive-indices]

{{es}} has full query and write support for indices created in the previous major version. If you have indices created in {{es}} versions 5, 6, or 7, you can use the archive functionality to import them into newer {{es}} versions as well.

The archive functionality provides slower read-only access to older {{es}} data, for compliance or regulatory reasons, the occasional lookback or investigation, or to rehydrate parts of it. Access to the data is expected to be infrequent, and can therefore happen with limited performance and query capabilities.

For this, {{es}} can access older snapshot repositories going back to version 5. The legacy indices in the [snapshot repository](../../tools/snapshot-and-restore.md) can either be [restored](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) or directly accessed through [searchable snapshots](../../tools/snapshot-and-restore/searchable-snapshots.md) so that the archived data won’t need to fully reside on local disks for access.


## Supported field types [archive-indices-supported-field-types]

Old mappings are imported as close as possible into {{es}} 9, but only provide regular query capabilities on a select subset of fields:

* [Numeric types](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`boolean` type](elasticsearch://reference/elasticsearch/mapping-reference/boolean.md)
* [`ip` type](elasticsearch://reference/elasticsearch/mapping-reference/ip.md)
* [`geo_point` type](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md)
* [`date` types](elasticsearch://reference/elasticsearch/mapping-reference/date.md): the date `format` setting on date fields is supported as long as it behaves similarly across these versions. If it is not, for example, [when using custom date formats](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/migrate-to-java-time.html), this field can be updated on legacy indices so a user can change it if needed.
* [`keyword` type](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type): The `normalizer` setting on keyword fields is supported as long as it behaves similarly across these versions. If they do not, they can be updated on legacy indices if necessary.
* [`text` type](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type): Scoring capabilities are limited, and all queries return constant scores equal to 1.0. The `analyzer` settings on text fields are supported as long as they behave similarly across these versions. If they don't, they can be updated on legacy indices.
* [Multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md)
* [Field aliases](elasticsearch://reference/elasticsearch/mapping-reference/field-alias.md)
* [`object`](elasticsearch://reference/elasticsearch/mapping-reference/object.md) fields
* some basic metadata fields, such as `_type` for querying {{es}} 5 indices
* [runtime fields](../../../manage-data/data-store/mapping/map-runtime-field.md)
* [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md)

{{es}} 5 indices with mappings that have [multiple mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/removal-of-types.html) are collapsed together on a best-effort basis before being imported.

If auto-importing mappings does not work, or the new {{es}} version doesn't understand the mapping, it falls back to importing the index without the mapping, but stores the original mapping in the [_meta](elasticsearch://reference/elasticsearch/mapping-reference/mapping-meta-field.md) section of the imported index. Users can then examine the legacy mapping using the [GET mapping](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping) API, and manually update the mapping using the [update mapping](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) API, copying and adapting relevant sections of the legacy mapping to work with the current {{es}} version. While auto-import is expected to work in most cases, any failures should be [raised](https://github.com/elastic/elasticsearch/issues/new/choose) with the Elastic team for future improvements.


## Supported APIs [_supported_apis]

Archive indices are read-only and provide data access through the [search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) and [field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps) APIs. They do not support the [Get API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get) or any write APIs.

Archive indices allow running queries and aggregations if the [field type](#archive-indices-supported-field-types) supports them.

Due to `_source` access, the data can also be [reindexed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) to a new index that's fully compatible with the current {{es}} version.


## Upgrade older {{es}} clusters [_how_to_upgrade_older_es_clusters]

To upgrade older {{es}} 5, 6, or 7 clusters: 

1. Take a snapshot of the indices in the old cluster. 
2. Delete any indices created before 8.0.0. 
3. Upgrade the cluster without the old indices, then [restore](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) the legacy indices from the snapshot or [mount](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-searchable-snapshots-mount) them using searchable snapshots.

% In the future, we plan on streamlining the upgrade process going forward, making it easier to take legacy indices along when going to future major {{es}} versions.

