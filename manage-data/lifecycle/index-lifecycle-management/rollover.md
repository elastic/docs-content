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
This is particularly useful for time-series data, such as logs or metrics where index growth is continuous, in order to meet performance and retention requirements.

Without rollover, a single index would continue to grow, causing search performance to drop and having a higher administrative burden on the cluster.

The rollover feature is an important part of how [index lifecycle](../index-lifecycle-management/index-lifecycle.md) (ILM) and [data stream lifecycles](../data-stream.md) (DLM) work to keep your indices fast and manageable. By switching the write target of an index, the rollover action provides the following benefits:

* **Lifecycle** - works with lifecycle management (ILM or DLM) to transition the index through its lifecycle actions and allows for granular control over retention cycles
* **Optimized performance** - keeps shard sizes within recommended limits (10-50 GB)
* **Queries run faster** - improves search performance

Rollover can be triggered via the [API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover), ILM, or DLM.

## How rollover works in ILM

You define a rollover action in the hot phase of an index lifecycle policy. It will run when any of the configured thresholds are met and the write index contains at least one document.
You can configure the following rollover conditions:

* **Size** - an index will rollover when its shards reach a set size, for example 50 GB.
* **Age** - an index will rollover when an index reaches a certain age, for example 7 days.
* **Document count** - an index will rollover when a shard contains a certain number of documents, for example 2 million.

::::{tip}
Rolling over to a new index based on size, document count, or age is preferable to time-based rollovers. Rolling over at an arbitrary time often results in many small indices, which can have a negative impact on performance and resource usage.
::::

After rollover, indices move to other index lifecycle phases like warm, cold, frozen, and delete. Rollover creates a new write index while the old one continues through the lifecycle phases.

**Special rules:**

* Rollover for an empty write index is skipped even if they have an associated `max_age` that would otherwise result in a roll over occurring. A policy can override this behavior if you set `min_docs: 0` in the rollover conditions. This can also be disabled on a cluster-wide basis if you set `indices.lifecycle.rollover.only_if_has_documents` to `false`.
* Forced rollover occurs if any shard reaches 200 million documents. Usually, a shard will reach 50 GB long before it reaches 200 million documents, but this isn’t the case for space efficient data sets.

## Recommended approaches

Decide your approach to index rotation based on your use case and requirements.

| Use case               | Recommended approach                                      | Setup benefits and limitations                                                                  |
| ---------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Logs, metrics          | [Data streams](rollover.md#rollover-data-stream)          | Configure rollover with lifecycle management, *minimal setup*, control over rollover timing ^1^ |
| Legacy indexing setup  | [Alias-based rollover](rollover.md#rollover-with-aliases) | Configure rollover with lifecycle management, *advanced setup*, control over rollover timing    |
| Small, static datasets | No rollover                                               | Simpler management                                                                              |

^1^ Rollover is handled automatically in Serverless projects, therefore configuring rollover timing is abstracted from the user. {applies_to}`serverless: ga`

:::{tip}
For new projects, use data streams. They're simple to manage with lifecycle policies where you define phases and actions that handle rollover automatically.
:::


### Rotating your indices with data streams [rollover-data-stream]

We recommend using [data streams](../../data-store/data-streams.md) to manage time series data. When set up to use ILM policies that include rollover, data streams automatically manage the rotation of your indices. This ensures you can write to the data stream without additional configuration.
When targeting a data stream, the new backing index becomes the data stream's writing index. The generation of new backing indices is incremented automatically when it reaches a specified age or size.

Each data stream requires an [index template](../../data-store/templates.md) that contains the following:

* A name or wildcard (`*`) pattern for the data stream.
* Optional: The mappings and settings applied to each backing index when it’s created.

For more information about this approach, refer to the [Manage time series data with data streams](../index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-with-data-streams) tutorial.

:::{tip}
Data streams are designed for append-only data, where the data stream name can be used as the operations (read, write, rollover, shrink etc.) target. If your use case requires data to be updated in place, you can perform [update or delete operations directly on the backing indices](../../data-store/data-streams/use-data-stream.md#update-delete-docs-in-a-backing-index).
:::

**Data streams naming pattern**<br>
{{es}} uses a structured naming convention for the backing indices of data streams, following this pattern:

```console
.ds-<DATA-STREAM-NAME>-<yyyy.MM.dd>-<GENERATION>
```
For more information about data stream naming patterns, refer to the [Generation](../../data-store/data-streams.md#data-streams-generation) section of the Data streams page.

### Rotating your indices with aliases [rollover-with-aliases]

 Rotating indices with aliases requires additional configuration steps, including bootstrapping the initial index. For more details about this approach, refer to the [Manage time series data without data streams](../index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-without-data-streams) tutorial.

:::{important}
The use of aliases for rollover requires meeting certain conditions. Review these considerations before applying this approach:

* The index name must match the pattern `^.-\d+$*`, for example `my-index-000001`.
* The `index.lifecycle.rollover_alias` must be configured as the alias to roll over.
* The index must be the [write index](../../data-store/aliases.md#write-index) for the alias.
:::

::::{note}
When an alias or data stream is rolled over, the previous write index’s rollover time is stored. This date, rather than the index’s `creation_date`, is used in {{ilm}} `min_age` phase calculations. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::

**Alias-based naming pattern**<br>
When configured correctly, the newly created write index will have a similar name to one that's been rolled over, however the six-digit, zero-padded suffix will be incremented. For example before rollover, the write index was called `my-index-000001` and after rollover, the newly created index becomes `my-index-000002` and also becomes the new write index. The alias typically shares the base name which in this example is `my-index`.
