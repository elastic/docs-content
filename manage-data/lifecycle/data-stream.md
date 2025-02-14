---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-stream-lifecycle.html
---

# Data stream lifecycle [data-stream-lifecycle]

A data stream lifecycle is the built-in mechanism data streams use to manage their lifecycle. It enables you to easily automate the management of your data streams according to your retention requirements. For example, you could configure the lifecycle to:

* Ensure that data indexed in the data stream will be kept at least for the retention time you defined.
* Ensure that data older than the retention period will be deleted automatically by {{es}} at a later time.

To achieve that, it supports:

* Automatic [rollover](index-lifecycle-management/rollover.md), which chunks your incoming data in smaller pieces to facilitate better performance and backwards incompatible mapping changes.
* Configurable retention, which allows you to configure the time period for which your data is guaranteed to be stored. {{es}} is allowed at a later time to delete data older than this time period. Retention can be configured on the data stream level or on a global level. Read more about the different options in this [tutorial](data-stream/tutorial-data-stream-retention.md).

A data stream lifecycle also supports downsampling the data stream backing indices. See [the downsampling example](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) for more details.


## How does it work? [data-streams-lifecycle-how-it-works] 

In intervals configured by [`data_streams.lifecycle.poll_interval`](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-stream-lifecycle-settings.html#data-streams-lifecycle-poll-interval), {{es}} goes over each data stream and performs the following steps:

1. Checks if the data stream has a data stream lifecycle configured, skipping any indices not part of a managed data stream.
2. Rolls over the write index of the data stream, if it fulfills the conditions defined by [`cluster.lifecycle.default.rollover`](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-stream-lifecycle-settings.html#cluster-lifecycle-default-rollover).
3. After an index is not the write index anymore (i.e. the data stream has been rolled over), automatically tail merges the index. Data stream lifecycle executes a merge operation that only targets the long tail of small segments instead of the whole shard. As the segments are organised into tiers of exponential sizes, merging the long tail of small segments is only a fraction of the cost of force merging to a single segment. The small segments would usually hold the most recent data so tail merging will focus the merging resources on the higher-value data that is most likely to keep being queried.
4. If [downsampling](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) is configured it will execute all the configured downsampling rounds.
5. Applies retention to the remaining backing indices. This means deleting the backing indices whose `generation_time` is longer than the effective retention period (read more about the [effective retention calculation](data-stream/tutorial-data-stream-retention.md#effective-retention-calculation)). The `generation_time` is only applicable to rolled over backing indices and it is either the time since the backing index got rolled over, or the time optionally configured in the [`index.lifecycle.origination_date`](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-stream-lifecycle-settings.html#index-data-stream-lifecycle-origination-date) setting.

::::{important} 
We use the `generation_time` instead of the creation time because this ensures that all data in the backing index have passed the retention period. As a result, the retention period is not the exact time data gets deleted, but the minimum time data will be stored.
::::


::::{note} 
Steps `2-4` apply only to backing indices that are not already managed by {{ilm-init}}, meaning that these indices either do not have an {{ilm-init}} policy defined, or if they do, they have [`index.lifecycle.prefer_ilm`](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-stream-lifecycle-settings.html#index-lifecycle-prefer-ilm) set to `false`.
::::



## Configuring data stream lifecycle [data-stream-lifecycle-configuration] 

Since the lifecycle is configured on the data stream level, the process to configure a lifecycle on a new data stream and on an existing one differ.

In the following sections, we will go through the following tutorials:

* To create a new data stream with a lifecycle, you need to add the data stream lifecycle as part of the index template that matches the name of your data stream (see [Tutorial: Create a data stream with a lifecycle](data-stream/tutorial-create-data-stream-with-lifecycle.md)). When a write operation with the name of your data stream reaches {{es}} then the data stream will be created with the respective data stream lifecycle.
* To update the lifecycle of an existing data stream you need to use the [data stream lifecycle APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-data-stream) to edit the lifecycle on the data stream itself (see [Tutorial: Update existing data stream](data-stream/tutorial-update-existing-data-stream.md)).
* Migrate an existing {{ilm-init}} managed data stream to Data stream lifecycle using [Tutorial: Migrate ILM managed data stream to data stream lifecycle](data-stream/tutorial-migrate-ilm-managed-data-stream-to-data-stream-lifecycle.md).

::::{note} 
Updating the data stream lifecycle of an existing data stream is different from updating the settings or the mapping, because it is applied on the data stream level and not on the individual backing indices.
::::






