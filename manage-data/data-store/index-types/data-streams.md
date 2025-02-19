---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html#manage-data-streams
  - https://www.elastic.co/guide/en/serverless/current/index-management.html#index-management-manage-data-streams

applies:
  stack: all
  serverless: all
  hosted: all
---

# Data streams [data-streams]

A data stream lets you store append-only time series data across multiple indices while giving you a single named resource for requests. Data streams are well-suited for logs, events, metrics, and other continuously generated data.

You can submit indexing and search requests directly to a data stream. The stream automatically routes the request to backing indices that store the stream’s data. You can use [{{ilm}} ({{ilm-init}})](../../../manage-data/lifecycle/index-lifecycle-management.md) to automate the management of these backing indices. For example, you can use {{ilm-init}} to automatically move older backing indices to less expensive hardware and delete unneeded indices. {{ilm-init}} can help you reduce costs and overhead as your data grows.


## Should you use a data stream? [should-you-use-a-data-stream]

To determine whether you should use a data stream for your data, you should consider the format of the data, and your expected interaction. A good candidate for using a data stream will match the following criteria:

* Your data contains a timestamp field, or one could be automatically generated.
* You mostly perform indexing requests, with occasional updates and deletes.
* You index documents without an `_id`, or when indexing documents with an explicit `_id` you expect first-write-wins behavior.

For most time series data use-cases, a data stream will be a good fit. However, if you find that your data doesn’t fit into these categories (for example, if you frequently send multiple documents using the same `_id` expecting last-write-wins), you may want to use an index alias with a write index instead. See documentation for [managing time series data without a data stream](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-without-data-streams) for more information.

Keep in mind that some features such as [Time Series Data Streams (TSDS)](../../../manage-data/data-store/index-types/time-series-data-stream-tsds.md) and [data stream lifecycles](../../../manage-data/lifecycle/data-stream.md) require a data stream.


## Backing indices [backing-indices]

A data stream consists of one or more [hidden](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-hidden), auto-generated backing indices.

:::{image} ../../../images/elasticsearch-reference-data-streams-diagram.svg
:alt: data streams diagram
:::

A data stream requires a matching [index template](../../../manage-data/data-store/templates.md). The template contains the mappings and settings used to configure the stream’s backing indices.

Every document indexed to a data stream must contain a `@timestamp` field, mapped as a [`date`](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html) or [`date_nanos`](https://www.elastic.co/guide/en/elasticsearch/reference/current/date_nanos.html) field type. If the index template doesn’t specify a mapping for the `@timestamp` field, {{es}} maps `@timestamp` as a `date` field with default options.

The same index template can be used for multiple data streams. You cannot delete an index template in use by a data stream.

The name pattern for the backing indices is an implementation detail and no intelligence should be derived from it. The only invariant the holds is that each data stream generation index will have a unique name.


## Read requests [data-stream-read-requests]

When you submit a read request to a data stream, the stream routes the request to all its backing indices.

:::{image} ../../../images/elasticsearch-reference-data-streams-search-request.svg
:alt: data streams search request
:::


## Write index [data-stream-write-index]

The most recently created backing index is the data stream’s write index. The stream adds new documents to this index only.

:::{image} ../../../images/elasticsearch-reference-data-streams-index-request.svg
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

We recommend using [{{ilm-init}}](../../../manage-data/lifecycle/index-lifecycle-management.md) to automatically roll over data streams when the write index reaches a specified age or size. If needed, you can also [manually roll over](../../../manage-data/data-store/index-types/use-data-stream.md#manually-roll-over-a-data-stream) a data stream.


## Generation [data-streams-generation]

Each data stream tracks its generation: a six-digit, zero-padded integer starting at `000001`.

When a backing index is created, the index is named using the following convention:

```text
.ds-<data-stream>-<yyyy.MM.dd>-<generation>
```

`<yyyy.MM.dd>` is the backing index’s creation date. Backing indices with a higher generation contain more recent data. For example, the `web-server-logs` data stream has a generation of `34`. The stream’s most recent backing index, created on 7 March 2099, is named `.ds-web-server-logs-2099.03.07-000034`.

Some operations, such as a [shrink](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink) or [restore](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md), can change a backing index’s name. These name changes do not remove a backing index from its data stream.

The generation of the data stream can change without a new index being added to the data stream (e.g. when an existing backing index is shrunk). This means the backing indices for some generations will never exist. You should not derive any intelligence from the backing indices names.


## Append-only (mostly) [data-streams-append-only]

Data streams are designed for use cases where existing data is rarely updated. You cannot send update or deletion requests for existing documents directly to a data stream. However, you can still [update or delete documents](../../../manage-data/data-store/index-types/use-data-stream.md#update-delete-docs-in-a-backing-index) in a data stream by submitting requests directly to the document’s backing index.

If you need to update a larger number of documents in a data stream, you can use the [update by query](../../../manage-data/data-store/index-types/use-data-stream.md#update-docs-in-a-data-stream-by-query) and [delete by query](../../../manage-data/data-store/index-types/use-data-stream.md#delete-docs-in-a-data-stream-by-query) APIs.

::::{tip}
If you frequently send multiple documents using the same `_id` expecting last-write-wins, you may want to use an index alias with a write index instead. See [Manage time series data without data streams](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-without-data-streams).
::::


