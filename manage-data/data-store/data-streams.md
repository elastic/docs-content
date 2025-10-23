---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html#manage-data-streams
  - https://www.elastic.co/guide/en/serverless/current/index-management.html#index-management-manage-data-streams
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Data streams [data-streams]

A data stream acts as a layer of abstraction over a set of indices that are optimized for storing append-only time series data. It stores data across multiple backing indices while giving you a single named resource to use for requests. Data streams are well-suited for logs, events, metrics, and other continuously generated data.

You can submit indexing and search requests directly to a data stream. The stream automatically routes the request to backing indices that store the stream’s data. You can use [{{ilm}} ({{ilm-init}})](../lifecycle/index-lifecycle-management.md) to automate the management of these backing indices. For example, you can use {{ilm-init}} to automatically move older backing indices to less expensive hardware and delete unneeded indices. {{ilm-init}} can help you reduce costs and overhead as your data grows.

You can also use a [data stream lifecycle](../lifecycle/data-stream.md) to automate lifecycle management according to your retention requirements.

:::{admonition} Managing data streams with Streams
:applies_to: {"stack": "ga 9.2, preview 9.1", "serverless": "ga"}

Starting with {{stack}} version 9.2, the [**Streams**](/solutions/observability/streams/streams.md) page provides a centralized interface for managing your data in {{kib}}. It consolidates common data management tasks and eliminates the need for manual configuration of multiple applications and components. A stream maps directly to an {{es}} data stream, for example `logs-myapp-default`. Any changes that you make on the **Streams** page are automatically propagated to the associated data stream.

For more information, refer to [Manage data streams on the Streams page](/manage-data/data-store/data-streams/manage-data-stream.md#manage-data-streams-with-streams).

:::

## Should you use a data stream? [should-you-use-a-data-stream]

To determine whether you should use a data stream for your data, you should consider the format of the data, and your expected interaction. A good candidate for using a data stream will match the following criteria:

* Your data contains a timestamp field, or one could be automatically generated.
* You mostly perform indexing requests, with occasional updates and deletes.
* You index documents without an `_id`, or when indexing documents with an explicit `_id` you expect first-write-wins behavior.

For most time series data use-cases, a data stream will be a good fit. However, if you find that your data doesn’t fit into these categories (for example, if you frequently send multiple documents using the same `_id` expecting last-write-wins), you may want to use an index alias with a write index instead. See the tutorial [](../lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md) for more information.

Keep in mind that some features such as [Time Series Data Streams (TSDS)](../data-store/data-streams/time-series-data-stream-tsds.md) and [data stream lifecycles](../lifecycle/data-stream.md) require a data stream.


## Backing indices [backing-indices]

A data stream consists of one or more [hidden](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-hidden), auto-generated backing indices.

:::{image} /manage-data/images/elasticsearch-reference-data-streams-diagram.svg
:alt: data streams diagram
:::

A data stream requires a matching [index template](templates.md). The template contains the mappings and settings used to configure the stream’s backing indices and defines the {{ilm-init}} policy that the data stream uses.

Every document indexed to a data stream must contain a `@timestamp` field, mapped as a [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) or [`date_nanos`](elasticsearch://reference/elasticsearch/mapping-reference/date_nanos.md) field type. If the index template doesn’t specify a mapping for the `@timestamp` field, {{es}} maps `@timestamp` as a `date` field with default options.

The same index template can be used for multiple data streams. You cannot delete an index template in use by a data stream.

The name pattern for the backing indices is an implementation detail and no intelligence should be derived from it. The only invariant the holds is that each data stream generation index will have a unique name.


## Read requests [data-stream-read-requests]

When you submit a read request to a data stream, the stream routes the request to all its backing indices.

:::{image} /manage-data/images/elasticsearch-reference-data-streams-search-request.svg
:alt: data streams search request
:::


## Write index [data-stream-write-index]

The most recently created backing index is the data stream’s write index. The stream adds new documents to this index only.

:::{image} /manage-data/images/elasticsearch-reference-data-streams-index-request.svg
:alt: data streams index request
:::

You cannot add new documents to other backing indices, even by sending requests directly to the index.

You also cannot perform operations on a write index that may hinder indexing, such as:

* [Clone](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clone)
* [Delete](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete)
* [Shrink](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink)
* [Split](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-split)


## Rollover [data-streams-rollover]

A [rollover](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover) creates a new backing index that becomes the stream’s new write index.

We recommend using [{{ilm-init}}](../lifecycle/index-lifecycle-management.md) to automatically roll over data streams when the write index reaches a specified age or size. If needed, you can also [manually roll over](data-streams/use-data-stream.md#manually-roll-over-a-data-stream) a data stream.


## Generation [data-streams-generation]

Each data stream tracks its generation: a six-digit, zero-padded integer starting at `000001`.

When a backing index is created, the index is named using the following convention:

```text
.ds-<data-stream>-<yyyy.MM.dd>-<generation>
```

`<yyyy.MM.dd>` is the backing index’s creation date. Backing indices with a higher generation contain more recent data. For example, the `web-server-logs` data stream has a generation of `34`. The stream’s most recent backing index, created on 7 March 2099, is named `.ds-web-server-logs-2099.03.07-000034`.

Some operations, such as a [shrink](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink) or [restore](../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md), can change a backing index’s name. These name changes do not remove a backing index from its data stream.

The generation of the data stream can change without a new index being added to the data stream (e.g. when an existing backing index is shrunk). This means the backing indices for some generations will never exist. You should not derive any intelligence from the backing indices names.


## Append-only (mostly) [data-streams-append-only]

Data streams are designed for use cases where existing data is rarely updated. You cannot send update or deletion requests for existing documents directly to a data stream. However, you can still [update or delete documents](data-streams/use-data-stream.md#update-delete-docs-in-a-backing-index) in a data stream by submitting requests directly to the document’s backing index.

If you need to update a larger number of documents in a data stream, you can use the [update by query](data-streams/use-data-stream.md#update-docs-in-a-data-stream-by-query) and [delete by query](data-streams/use-data-stream.md#delete-docs-in-a-data-stream-by-query) APIs.

::::{tip}
If you frequently send multiple documents using the same `_id` expecting last-write-wins, you may want to use an index alias with a write index instead. See the tutorial [](../lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md).
::::


