---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-rollover.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# About rollover [index-rollover]

In {{es}}, the [rollover action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) replaces your active write index with a new one whenever your index grows beyond a specified size, age, or number of documents.
This is particularly useful for time-series data, such as logs or metrics where index growth is continuous, in order to meet performance and retention requirements.

Without rollover, a single index would continue to grow, causing search performance to drop and having a higher administrative burden on the cluster.

The rollover feature is an important part of how [index lifecycle](../index-lifecycle-management/index-lifecycle.md) ({{ilm-init}}) and [data stream lifecycles](../data-stream.md) ({{dlm-init}}) work to keep your indices fast and manageable. By switching the write target of an index, the rollover action provides the following benefits:

* **Lifecycle** - works with lifecycle management ({{ilm-init}} or {{dlm-init}}) to transition the index through its lifecycle actions and allows for granular control over retention cycles
* **Optimized performance** - keeps shard sizes within [recommended limits](/deploy-manage/production-guidance/optimize-performance/size-shards.md) (10-50 GB)
* **Queries run faster** - improves search performance

Rollover can be triggered via the [API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover), {{ilm-init}}, or {{dlm-init}}.

:::{tip}
The following tutorials are available to help you configure rollover for your indices, for three different scenarios:
* [](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md)
* [](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md)
* [](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md)

Refer to [](/manage-data/lifecycle/index-lifecycle-management/ilm-tutorials.md) for an overview of these.

:::

## How rollover works in {{ilm-init}}

You define a rollover action in the hot phase of an index lifecycle policy. It will run when any of the configured conditions are met and the write index contains at least one document.
You can configure the following rollover conditions:

* **Size** - an index will rollover when its shards reach a set size, for example 50 GB.
* **Age** - an index will rollover when it reaches a certain age, for example 7 days.
* **Document count** - an index will rollover when a shard contains a certain number of documents, for example 2 million.

::::{tip}
Rolling over to a new index based on size, document count, or age is preferable to time-based rollovers. Rolling over at an arbitrary time often results in many small indices, which can have a negative impact on performance and resource usage.
::::

After rollover, indices move through other configured index lifecycle phases: warm, cold, frozen, and delete. Rollover creates a new write index while the previous one continues through the lifecycle phases.

**Special rules:**

* Rollover for an empty write index is skipped even if it has an associated `max_age` that would otherwise result in a rollover occurring. A policy can override this behavior if you set `min_docs: 0` in the rollover conditions. This can also be disabled on a cluster-wide basis if you set `indices.lifecycle.rollover.only_if_has_documents` to `false`.
* Forced rollover occurs if any shard reaches 200 million documents. Usually, a shard will reach 50 GB long before it reaches 200 million documents, but this isn’t the case for space efficient data sets.

## Recommended approaches

Decide your approach to index rotation based on your use case and requirements.

| Use case               | Recommended approach                                      | Setup benefits and limitations                                                                  |
| ---------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Logs, metrics          | [Data streams](rollover.md#rollover-data-stream)          | Configure rollover with lifecycle management, *minimal setup*, control over rollover timing ^1^ |
| Legacy indexing setup  | [Alias-based rollover](rollover.md#rollover-with-aliases) | Configure rollover with lifecycle management, *advanced setup*, control over rollover timing    |
| Small, static datasets | No rollover                                               | Simpler management                                                                              |

^1^ Rollover is handled automatically for data streams in {{es-serverless}} projects. {applies_to}`serverless: ga`

:::{tip}
For new projects, use data streams. Unlike aliases, they're simpler to manage by defining lifecycle actions without requiring additional configuration for rollover.
:::


### Rotating your indices with data streams [rollover-data-stream]

We recommend using [data streams](../../data-store/data-streams.md) to manage time series data. When set up to use an {{ilm-init}} policy that includes rollover, a data stream manages the rotation of your indices without additional configuration.
When targeting a data stream, each time the current write index reaches a specified age or size, a new backing index is generated (with an incremented number and timestamp), and it becomes the data stream's writing index.

Each data stream requires an [index template](../../data-store/templates.md) that contains the following:

* A name or wildcard (`*`) pattern for the data stream.
* A configuration that indicates a data stream is used for the index pattern.
* Optional: The mappings and settings applied to each backing index when it’s created.

For more information about this approach, refer to the [](../index-lifecycle-management/tutorial-time-series-with-data-streams.md) tutorial.

:::{tip}
Data streams are designed for append-only data, where the data stream name can be used as the operations (read, write, rollover, shrink etc.) target. If your use case requires data to be updated in place, you can perform [update or delete operations directly on the backing indices](../../data-store/data-streams/use-data-stream.md#update-delete-docs-in-a-backing-index).
:::

**Data streams naming pattern**<br>
{{es}} uses a structured naming convention for the backing indices of data streams, following this pattern:

```
.ds-<DATA-STREAM-NAME>-<yyyy.MM.dd>-<GENERATION>
```

For more information about the data stream naming pattern, refer to the [Generation](../../data-store/data-streams.md#data-streams-generation) section of the Data streams page.

### Rotating your indices with aliases [rollover-with-aliases]

 Rotating indices with aliases requires additional configuration steps, including bootstrapping the initial index. For more details about this approach, refer to the [](../index-lifecycle-management/tutorial-time-series-without-data-streams.md) tutorial.

:::{important}
The use of aliases for rollover requires meeting certain conditions. Review these considerations before applying this approach:

* The index name must match the pattern `<INDEX_NAME>-<INDEX_NUMBER>`, for example `my-index-000001`.
* The `index.lifecycle.rollover_alias` must be configured as the alias to roll over.
* The index must be the [write index](../../data-store/aliases.md#write-index) for the alias.
:::

::::{note}
When an alias or data stream is rolled over, the previous write index’s rollover time is stored. This date, rather than the index’s `creation_date`, is used in {{ilm}} `min_age` phase calculations. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::

**Alias-based naming pattern**<br>
When configured correctly, the newly created write index will have a similar name to one that's been rolled over, however the six-digit, zero-padded suffix will be incremented. For example before rollover, the write index was called `my-index-000001` and after rollover, the newly created index becomes `my-index-000002` and also becomes the new write index. The alias typically shares the base name which in this example is `my-index`.
