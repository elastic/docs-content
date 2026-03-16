---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# The Elasticsearch data store [elasticsearch-intro-what-is-es]

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable document store, and vector database built on [Apache Lucene](https://lucene.apache.org/). It stores data as JSON documents, organized into _indices_. You interact with an index through its unique name or logical references such as [aliases](/manage-data/data-store/aliases.md). Each index holds a dataset with its own schema, defined by a [mapping](elasticsearch://reference/elasticsearch/mapping-reference/index.md) that specifies the fields and their types.

You can store many independent datasets side by side — each in its own index or [data stream](/manage-data/data-store/data-streams.md) — and search them individually or together.

As your data grows, how you structure, size, and manage your indices directly affects query performance, storage costs, and operational complexity. This section covers the core storage concepts, how to configure data structure and behavior, and how to manage your indices and documents.

:::{tip}
You can index a document using the [Index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-index) API. For production ingestion workflows and related concepts such as pipelines, agents, and Logstash, refer to [Ingest](/manage-data/ingest.md).
:::

## Understand data storage

{{es}} provides two main ways to organize your data:
* **Index**: The general-purpose storage unit. Use an index when you need to update or delete individual documents, or when your data is not time-based.
* **Data stream**: The recommended approach for timestamped, append-only data like logs, events, and metrics. A data stream manages rolling backing indices automatically and integrates with data lifecycle management out of the box.

Both use the same foundational concepts such as documents, mappings, templates, and aliases. The configuration topics in this section apply regardless of which you choose.

* [](/manage-data/data-store/index-basics.md): Learn about index fundamentals, including index naming and aliases, document structure, metadata fields, and mappings.
* [](/manage-data/data-store/data-streams.md): Learn when to use data streams for timestamped and append-only time series data, like logs, events, or metrics. You work with one stream name while {{es}} manages multiple backing indices behind the scenes.
* [](/manage-data/data-store/near-real-time-search.md): Understand how {{es}} makes newly indexed data searchable within seconds of indexing.

## Configure how data is stored

How you structure and manage your indices affects query performance, storage efficiency, and how easily your cluster scales. {{es}} provides tools to control field mappings, standardize index configurations, simplify and automate access logic, and manage data retention over time:

* [](/manage-data/data-store/mapping.md): Define how documents and their fields are stored and indexed. Choose between dynamic mapping for automatic field detection and explicit mapping for full control over field types and indexing behavior.
* [](/manage-data/data-store/text-analysis.md): Configure how unstructured text is converted into a structured format optimized for full-text search, including tokenization, normalization, and custom analyzers.
* [](/manage-data/data-store/templates.md): Define reusable index configurations including settings, mappings, and aliases that are automatically applied when new indices or data streams are created.
* [](/manage-data/data-store/aliases.md): Create named references that point to one or more indices or data streams. Aliases are logical groupings that have no impact on disk layout or data structure. Instead, they provide an organizational layer for query targeting, zero-downtime reindexing, and abstracting away physical index names.

## Manage data

Work with your indices and data using the {{kib}} UI or the {{es}} REST API.

* [](/manage-data/data-store/perform-index-operations.md): Use {{kib}}'s **Index Management** page to view and manage your indices, data streams, templates, component templates, and enrich policies.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Index, update, retrieve, search, and delete documents using curl and the {{es}} REST API.

## What's next

Once your data is stored, you can:

* [Ingest](/manage-data/ingest.md): Set up production ingestion workflows using pipelines, agents, and Logstash.
* [Query and filter your data](/explore-analyze/query-filter.md): Search, filter, and aggregate your data using full-text queries, ES|QL, and more.
* [Data lifecycle](/manage-data/lifecycle.md): Plan retention, tiering, and performance strategies as your data grows.

:::{admonition} Autoscaling
:applies_to: { serverless: ga, ess:, ece:, eck: }
Alongside lifecycle management, consider how your cluster handles growth. On {{serverless-full}}, autoscaling is fully managed and automatic. On {{ech}}, {{ece}}, and {{eck}}, you can configure autoscaling policies to adjust resources based on demand. Learn more about [autoscaling](/deploy-manage/autoscaling.md).
:::
