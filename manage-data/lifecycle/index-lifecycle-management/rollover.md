---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-rollover.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Rollover [index-rollover]

In {{es}}, *rollover* replaces your active write index with a new one whenever your index grows too large, too old, or stores too many documents.
This is particularly useful for time-series data, such as logs or metrics, where index growth is continuous and performance can degrade over time.

Without rollover, a single index can grow until searches slow down, shard relocation takes hours, and nodes run low on disk space.

The rollover feature is an important part of how [index lifecycle](../index-lifecycle-management/index-lifecycle.md) and [data stream lifecycles](../data-stream.md) work to keep your indices fast and manageable. By switching the write target of an index, the rollover action provides the following benefits:

* **Automation** - works with ILM to remove manual index rotation tasks and allows for granular control over retention cycles
* **Optimized performance** - keeps shard sizes within recommended limits (10-50 GB)
* **Queries run faster** - improves search performance

::::{tip}
Rolling over to a new index based on size, document count, or age is preferable to time-based rollovers. Rolling over at an arbitrary time often results in many small indices, which can have a negative impact on performance and resource usage.
::::


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

Each data stream requires an [index template](../../data-store/templates.md) that contains the following:

* A name or wildcard (`*`) pattern for the data stream.
* The data stream’s timestamp field. This field must be mapped as a [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) or [`date_nanos`](elasticsearch://reference/elasticsearch/mapping-reference/date_nanos.md) field data type and must be included in every document indexed to the data stream.
* The mappings and settings applied to each backing index when it’s created.



### Rotating your indices with index aliases [rollover-with-aliases]

Data streams are designed for append-only data, where the data stream name can be used as the operations (read, write, rollover, shrink etc.) target. If your use case requires data to be updated in place, you can instead manage your time series data using [index aliases](../../data-store/aliases.md). However, this approach requires additional steps to configure a write alias and templates, such as the following:

* Creating an *index template* that specifies the settings for each new index in the series. You optimize this configuration for ingestion, typically using as many shards as you have hot nodes.
* Creating an *index alias* that references the entire set of indices. 
* Configuring a designated index as the *write index*. This is the active index that handles all write requests. On each rollover, the new index becomes the write index.
* Creating an ILM policy with a rollover action and applying the policy to the index template.

::::{note}
When an index is rolled over, the previous index’s age is updated to reflect the rollover time. This date, rather than the index’s `creation_date`, is used in {{ilm}} `min_age` phase calculations. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::


## How rollover works in ILM

You can define a rollover action in the hot phase of an ILM policy. It will run when any of the configured thresholds are met.

* **Size** - if an index size reaches a set size, for example 50 GB
* **Age** - if an index reaches a certain age, for example 7 days
* **Document count** - if a shards contains 200 million documents or more.


**Special rules:**

* Empty index rollover is blocked unless you set `min_docs: 0` in rollover conditions.
* Forced rollover occurs if any shard reaches 200 M documents.

## Automatic rollover [ilm-automatic-rollover]

{{ilm-init}} and the data stream lifecycle enable you to automatically roll over to a new index based on conditions like the index size, document count, or age. When a rollover is triggered, a new index is created, the write alias is updated to point to the new index, and all subsequent updates are written to the new index.

::::{tip}
Rolling over to a new index based on size, document count, or age is preferable to time-based rollovers. Rolling over at an arbitrary time often results in many small indices, which can have a negative impact on performance and resource usage.
::::


::::{important}
Empty indices will not be rolled over, even if they have an associated `max_age` that would otherwise result in a roll over occurring. A policy can override this behavior, and explicitly opt in to rolling over empty indices, by adding a `"min_docs": 0` condition. This can also be disabled on a cluster-wide basis by setting `indices.lifecycle.rollover.only_if_has_documents` to `false`.
::::


::::{important}
The rollover action implicitly always rolls over a data stream or alias if one or more shards contain 200000000 or more documents. Normally a shard will reach 50GB long before it reaches 200M documents, but this isn’t the case for space efficient data sets. Search performance will very likely suffer if a shard contains more than 200M documents. This is the reason of the builtin limit.
::::


[data streams API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream)