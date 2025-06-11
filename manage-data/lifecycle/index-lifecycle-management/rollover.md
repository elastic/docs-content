---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-rollover.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Rollover [index-rollover]

When indexing time series data like logs or metrics, you can’t write to a single index indefinitely. To meet your indexing and search performance requirements and manage resource usage, you write to an index until some threshold is met and then create a new index and start writing to it instead. Using rolling indices enables you to:

* Optimize the active index for high ingest rates on high-performance *hot* nodes.
* Optimize for search performance on *warm* nodes.
* Shift older, less frequently accessed data to less expensive *cold* nodes,
* Delete data according to your retention policies by removing entire indices.

We recommend using [data streams](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream) to manage time series data. Data streams automatically track the write index while keeping configuration to a minimum.

Each data stream requires an [index template](../../data-store/templates.md) that contains:

* A name or wildcard (`*`) pattern for the data stream.
* The data stream’s timestamp field. This field must be mapped as a [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) or [`date_nanos`](elasticsearch://reference/elasticsearch/mapping-reference/date_nanos.md) field data type and must be included in every document indexed to the data stream.
* The mappings and settings applied to each backing index when it’s created.

Data streams are designed for append-only data, where the data stream name can be used as the operations (read, write, rollover, shrink etc.) target. If your use case requires data to be updated in place, you can instead manage your time series data using [index aliases](../../data-store/aliases.md). However, there are a few more configuration steps and concepts:

* An *index template* that specifies the settings for each new index in the series. You optimize this configuration for ingestion, typically using as many shards as you have hot nodes.
* An *index alias* that references the entire set of indices.
* A single index designated as the *write index*. This is the active index that handles all write requests. On each rollover, the new index becomes the write index.

::::{note}
When an index is rolled over, the previous index’s age is updated to reflect the rollover time. This date, rather than the index’s `creation_date`, is used in {{ilm}} `min_age` phase calculations. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::



## Automatic rollover [ilm-automatic-rollover]

{{ilm-init}} and the data stream lifecycle (in [preview]]) enable you to automatically roll over to a new index based on conditions like the index size, document count, or age. When a rollover is triggered, a new index is created, the write alias is updated to point to the new index, and all subsequent updates are written to the new index.

::::{tip}
Rolling over to a new index based on size, document count, or age is preferable to time-based rollovers. Rolling over at an arbitrary time often results in many small indices, which can have a negative impact on performance and resource usage.
::::


::::{important}
Empty indices will not be rolled over, even if they have an associated `max_age` that would otherwise result in a roll over occurring. A policy can override this behavior, and explicitly opt in to rolling over empty indices, by adding a `"min_docs": 0` condition. This can also be disabled on a cluster-wide basis by setting `indices.lifecycle.rollover.only_if_has_documents` to `false`.
::::


::::{important}
The rollover action implicitly always rolls over a data stream or alias if one or more shards contain 200000000 or more documents. Normally a shard will reach 50GB long before it reaches 200M documents, but this isn’t the case for space efficient data sets. Search performance will very likely suffer if a shard contains more than 200M documents. This is the reason of the builtin limit.
::::


