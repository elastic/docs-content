---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-rollover.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Rollover [index-rollover]

In {{es}}, the [rollover action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) replaces your active write index with a new one whenever your index grows too large, too old, or stores too many documents.
This is particularly useful for time-series data, such as logs or metrics, where index growth is continuous and performance can degrade over time.

Without rollover, a single index can grow until searches slow down, shard relocation takes hours, and nodes run low on disk space.

The rollover feature is an important part of how [index lifecycle](../index-lifecycle-management/index-lifecycle.md) and [data stream lifecycles](../data-stream.md) work to keep your indices fast and manageable. By switching the write target of an index, the rollover action provides the following benefits:

* **Automation** - works with ILM to remove manual index rotation tasks and allows for granular control over retention cycles
* **Optimized performance** - keeps shard sizes within recommended limits (10-50 GB)
* **Queries run faster** - improves search performance


## Recommended approaches

Decide your approach to index rotation based on your use case and requirements.

| Use case               | Recommended approach                                      | Benefits                              |
| ---------------------- | --------------------------------------------------------- | ------------------------------------- |
| Logs, metrics          | [Data streams](rollover.md#rollover-data-stream)          | Automatic rollover, minimal setup     |
| Legacy indexing setup  | [Alias-based rollover](rollover.md#rollover-with-aliases) | Granular control over rollover timing |
| Small, static datasets | No rollover                                               | Simpler management                    |

:::{tip}
For new projects, use data streams. They're simple to manage and handle rollover automatically.
:::


### Rotating your indices with data streams [rollover-data-stream]

We recommend using [data streams](../../data-store/data-streams.md) to manage time series data. Data streams automatically track the write index while keeping configuration to a minimum.
When targeting a data stream, the new index becomes the data stream's writing index and it's generation is incremented.

Each data stream requires an [index template](../../data-store/templates.md) that contains the following:

* A name or wildcard (`*`) pattern for the data stream.
* The data stream’s timestamp field. This field must be mapped as a [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) or [`date_nanos`](elasticsearch://reference/elasticsearch/mapping-reference/date_nanos.md) field data type and must be included in every document indexed to the data stream.
* The mappings and settings applied to each backing index when it’s created.



### Rotating your indices with aliases [rollover-with-aliases]

Data streams are designed for append-only data, where the data stream name can be used as the operations (read, write, rollover, shrink etc.) target. If your use case requires data to be updated in place, you can instead manage your time series data using [index aliases](../../data-store/aliases.md). However, this approach requires additional configuration steps.

To roll over an index alias, the alias and its [write index](../../data-store/aliases.md#write-index) must meet the following conditions:

* The index name must match the pattern `^.-\d+$*`, for example `my-index-000001`.
* The `index.lifecycle.rollover_alias` must be configured as the alias to roll over.
* The index must be the write index for the alias.


::::{note}
When an index is rolled over, the previous index’s age is updated to reflect the rollover time. This date, rather than the index’s `creation_date`, is used in {{ilm}} `min_age` phase calculations. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::


## How rollover works in ILM

You define a rollover action in the hot phase of an ILM policy. It will run when any of the configured thresholds are met.
You can configure the following rollover conditions:

* **Size** - an index will rollover when it reaches a set size, for example 50 GB.
* **Age** - an index will rollover when an index reaches a certain age, for example 7 days.
* **Document count** - an index will rollover when a shard contains a certain number of documents, for example 2 million.

::::{tip}
Rolling over to a new index based on size, document count, or age is preferable to time-based rollovers. Rolling over at an arbitrary time often results in many small indices, which can have a negative impact on performance and resource usage.
::::

**Special rules:**

* Empty indices rollover is blocked even if they have an associated `max_age` that would otherwise result in a roll over occurring. A policy can override this behavior if you set `min_docs: 0` in the rollover conditions. This can also be disabled on a cluster-wide basis if you set `indices.lifecycle.rollover.only_if_has_documents` to `false`.
* Forced rollover occurs if any shard reaches 200 million documents. Usually, a shard will reach 50 GB long before it reaches 200 million documents, but this isn’t the case for space efficient data sets.




??? link to [data streams API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream)