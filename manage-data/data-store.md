---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# The {{es}} data store [elasticsearch-intro-what-is-es]

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable document store, and [vector database](/solutions/search.md#es-as-vector-database) built on [Apache Lucene](https://lucene.apache.org/). It stores data as JSON documents, organized into _indices_. You can interact with an [index](/manage-data/data-store/index-basics.md) using its unique name or through a logical reference such as an [alias](/manage-data/data-store/aliases.md). Each index holds a dataset with its own schema, defined by a [mapping](elasticsearch://reference/elasticsearch/mapping-reference/index.md) that specifies the fields and their types.

You can store many independent datasets side by side — each in its own index or [data stream](/manage-data/data-store/data-streams.md) — and search them individually or together.

As your data grows, how you structure, size, and manage your indices directly affects query performance, storage costs, and operational complexity. This section covers the core storage concepts, how to configure data structure and behavior, and how to manage your indices and documents. 

For production architecture guidance, including resilience, scaling, and performance optimization, refer to [](/deploy-manage/production-guidance/elasticsearch-in-production-environments.md).

:::{tip}
You can index a document using the [Index]({{es-apis}}operation/operation-index) API. For production ingestion workflows and related concepts such as pipelines, agents, and Logstash, refer to [Ingest: Bring your data to Elastic](/manage-data/ingest.md).
:::

## Understand data storage

{{es}} provides two main ways to organize your data:
* **Index**: The general-purpose storage unit. Use an index when you need to update or delete individual documents, or when your data is not time-based.
* **Data stream**: The recommended approach for timestamped, append-only data like logs, events, and metrics. A data stream manages rolling backing indices automatically and integrates with data lifecycle management out of the box.

Both use the same foundational concepts such as documents, mappings, templates, and aliases. The configuration topics in this section apply regardless of which you choose.

* [](/manage-data/data-store/index-basics.md): Learn about index fundamentals, including index naming and aliases, document structure, metadata fields, and mappings.
* [](/manage-data/data-store/data-streams.md): Learn when to use data streams for timestamped and append-only time series data, like logs, events, or metrics. You work with one stream name while {{es}} manages multiple backing indices behind the scenes.
* [](/manage-data/data-store/near-real-time-search.md): Understand how {{es}} makes newly indexed data searchable within seconds of indexing.

## Understand index modes [understand-index-modes]

An index mode is the storage and query profile for an index or for the backing indices of a data stream.
It changes default settings and how {{es}} stores documents on disk.

Set [`index.mode`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting) when you create the index or put it in an [index template](/manage-data/data-store/templates.md) so new indices inherit it.
You cannot change the mode after the index is created.
For every supported value, refer to [`index.mode`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting).

Standard (`standard`) {applies_to}`vectordb: unavailable`
:   Optimized for search and any type of retrieval.

LogsDB (`logsdb`) {applies_to}`stack: ga 9.0+` {applies_to}`vectordb: unavailable`
:   Optimized for logs use cases, with log-oriented defaults. [Logs data streams](/manage-data/data-store/data-streams/logs-data-stream.md) use this mode.

LogsDB columnar (`logsdb_columnar`) {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview` {applies_to}`vectordb: unavailable`
:   Optimized for logs use cases that align with columnar semantics and [limitations](elasticsearch://reference/elasticsearch/columnar/index.md#columnar-limitations). Refer to [Columnar index mode](/manage-data/data-store/columnar.md).

TSDB (`time_series`) {applies_to}`vectordb: unavailable`
:   Optimized for metrics and time series use cases. [Time series data streams](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) use this mode. This mode is for data streams only.

Columnar (`columnar`) {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview` {applies_to}`vectordb: unavailable`
:   Optimized for storage efficiency and analytics. Refer to [Columnar index mode](/manage-data/data-store/columnar.md).

VectorDB (`vectordb_document`) {applies_to}`stack: ga 9.5+` {applies_to}`vectordb: ga`
:   Optimized for vector search use cases, enabling similarity search on dense vectors. Refer to [Vector index mode](/solutions/search/vector.md#vector-index-mode). In {{vectordb}} projects, it is the only mode available.

Lookup (`lookup`) {applies_to}`vectordb: unavailable`
:   Use it for reference data you join in {{esql}}, for example a list of users, hosts, or known threat IPs. Refer to [Join data from multiple indices with LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md). Only the lookup index needs this mode, not the source index.

Index mode works together with [mappings](/manage-data/data-store/mapping.md) and [templates](/manage-data/data-store/templates.md).
The mode changes default settings and whether {{es}} stores the original JSON document ([`_source`](/manage-data/data-store/index-basics.md#elasticsearch-intro-documents-fields)) or reconstructs it.
For how documents, mappings, and `_source` fit together, refer to [index fundamentals](/manage-data/data-store/index-basics.md).

## Configure how data is stored

An [index mode](#understand-index-modes) is the storage profile for the whole index. The topics in this section describe the fields and the names you use to reach the data. A [template](/manage-data/data-store/templates.md) can include both the mode and these settings so new indices get them together.

{{es}} provides tools to control document field types, manage unstructured text, standardize index configurations, and to simplify and automate access logic:

* [](/manage-data/data-store/mapping.md): Define how documents and their fields are stored and indexed. Choose between dynamic mapping for automatic field detection and explicit mapping for full control over field types and indexing behavior.
* [](/manage-data/data-store/text-analysis.md): Configure how unstructured text is converted into a structured format optimized for full-text search, including tokenization, normalization, and custom analyzers.
* [](/manage-data/data-store/templates.md): Define reusable index configurations including settings, mappings, and aliases that are automatically applied when new indices or data streams are created.
* [](/manage-data/data-store/aliases.md): Create named references that point to one or more indices or data streams. Aliases are logical groupings that have no impact on disk layout or data structure. Instead, they provide an organizational layer for query targeting, zero-downtime reindexing, and abstracting away physical index names.

## Manage data

Work with your indices and data using the {{kib}} UI or the {{es}} REST API.

* [](/manage-data/data-store/perform-index-operations.md): Use {{kib}}'s **Index Management** page to view and manage your indices, data streams, templates, component templates, and enrich policies.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Index, update, retrieve, search, and delete documents using curl and the {{es}} REST API.

## What's next

After you understand how your data is stored, explore these topics to move to practical data workflows and growth planning:

* [Ingest](/manage-data/ingest.md): Explore ingestion options, from sample data and manual uploads to automated pipelines and API-driven workflows.
* [Query and filter your data](/explore-analyze/query-filter.md): Search, filter, aggregate data, and learn about search approaches and query languages.
* [Data lifecycle](/manage-data/lifecycle.md): Plan data retention, storage tiers, and roll over as your data grows.
* [Scaling considerations](/deploy-manage/production-guidance/scaling-considerations.md): Learn how to evaluate workload growth and scale your deployment effectively.
