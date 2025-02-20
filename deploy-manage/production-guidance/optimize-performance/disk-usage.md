---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-disk-usage.html
---

# Disk usage [tune-for-disk-usage]


## Disable the features you do not need [_disable_the_features_you_do_not_need]

By default, {{es}} indexes and adds doc values to most fields so that they can be searched and aggregated out of the box. For instance, if you have a numeric field called `foo` that you need to run histograms on but that you never need to filter on, you can safely disable indexing on this field in your [mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create):

```console
PUT index
{
  "mappings": {
    "properties": {
      "foo": {
        "type": "integer",
        "index": false
      }
    }
  }
}
```

[`text`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/text.md) fields store normalization factors in the index to facilitate document scoring. If you only need matching capabilities on a `text` field but do not care about the produced scores, you can use the [`match_only_text`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/text.md#match-only-text-field-type) type instead. This field type saves significant space by dropping scoring and positional information.


## Don’t use default dynamic string mappings [default-dynamic-string-mapping]

The default [dynamic string mappings](../../../manage-data/data-store/mapping/dynamic-mapping.md) will index string fields both as [`text`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/text.md) and [`keyword`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/keyword.md). This is wasteful if you only need one of them. Typically an `id` field will only need to be indexed as a `keyword` while a `body` field will only need to be indexed as a `text` field.

This can be disabled by either configuring explicit mappings on string fields or setting up dynamic templates that will map string fields as either `text` or `keyword`.

For instance, here is a template that can be used in order to only map string fields as `keyword`:

```console
PUT index
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}
```


## Watch your shard size [_watch_your_shard_size]

Larger shards are going to be more efficient at storing data. To increase the size of your shards, you can decrease the number of primary shards in an index by [creating indices](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) with fewer primary shards, creating fewer indices (e.g. by leveraging the [Rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover)), or modifying an existing index using the [Shrink API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink).

Keep in mind that large shard sizes come with drawbacks, such as long full recovery times.


## Disable `_source` [disable-source]

The [`_source`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/mapping-source-field.md) field stores the original JSON body of the document. If you don’t need access to it you can disable it. However, APIs that needs access to `_source` such as update, highlight and reindex won’t work.


## Use `best_compression` [best-compression]

The `_source` and stored fields can easily take a non negligible amount of disk space. They can be compressed more aggressively by using the `best_compression` [codec](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index.md#index-codec).


## Force merge [_force_merge]

Indices in Elasticsearch are stored in one or more shards. Each shard is a Lucene index and made up of one or more segments - the actual files on disk. Larger segments are more efficient for storing data.

The [force merge API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) can be used to reduce the number of segments per shard. In many cases, the number of segments can be reduced to one per shard by setting `max_num_segments=1`.

::::{warning}
**We recommend only force merging a read-only index (meaning the index is no longer receiving writes).**  When documents are updated or deleted, the old version is not immediately removed, but instead soft-deleted and marked with a "tombstone". These soft-deleted documents are automatically cleaned up during regular segment merges. But force merge can cause very large (> 5GB) segments to be produced, which are not eligible for regular merges. So the number of soft-deleted documents can then grow rapidly, resulting in higher disk usage and worse search performance. If you regularly force merge an index receiving writes, this can also make snapshots more expensive, since the new documents can’t be backed up incrementally.
::::



## Shrink index [_shrink_index]

The [shrink API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink) allows you to reduce the number of shards in an index. Together with the force merge API above, this can significantly reduce the number of shards and segments of an index.


## Use the smallest numeric type that is sufficient [_use_the_smallest_numeric_type_that_is_sufficient]

The type that you pick for [numeric data](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/number.md) can have a significant impact on disk usage. In particular, integers should be stored using an integer type (`byte`, `short`, `integer` or `long`) and floating points should either be stored in a `scaled_float` if appropriate or in the smallest type that fits the use-case: using `float` over `double`, or `half_float` over `float` will help save storage.


## Use index sorting to colocate similar documents [_use_index_sorting_to_colocate_similar_documents]

When Elasticsearch stores `_source`, it compresses multiple documents at once in order to improve the overall compression ratio. For instance it is very common that documents share the same field names, and quite common that they share some field values, especially on fields that have a low cardinality or a [zipfian](https://en.wikipedia.org/wiki/Zipf%27s_law) distribution.

By default documents are compressed together in the order that they are added to the index. If you enabled [index sorting](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-sorting-settings.md) then instead they are compressed in sorted order. Sorting documents with similar structure, fields, and values together should improve the compression ratio.


## Put fields in the same order in documents [_put_fields_in_the_same_order_in_documents]

Due to the fact that multiple documents are compressed together into blocks, it is more likely to find longer duplicate strings in those `_source` documents if fields always occur in the same order.


## Roll up historical data [roll-up-historical-data]

Keeping older data can be useful for later analysis but is often avoided due to storage costs. You can use downsampling to summarize and store historical data at a fraction of the raw data’s storage cost. See [Downsampling a time series data stream](../../../manage-data/data-store/data-streams/downsampling-time-series-data-stream.md).
