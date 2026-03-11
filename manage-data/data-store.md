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

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable document store, and vector database built on [Apache Lucene](https://lucene.apache.org/). It stores data as JSON documents, organized into _indices_. Each index holds a dataset with its own structure, defined by a _mapping_ that specifies the fields and their types.

Behind the scenes, {{es}} divides each index into _shards_ and distributes them across the nodes in your cluster. This allows it to scale horizontally to handle large volumes of data. Replica shards provide fault tolerance, keeping your data available even when individual nodes fail.

You can store many independent datasets side by side — each in its own index or [data stream](/manage-data/data-store/data-streams.md) — and search them individually or together. For append-only time series data like logs and metrics, data streams manage rolling indices automatically.

This section covers the core storage concepts, how to configure data structure and behavior, and how to manage your indices and documents.

## Understand data storage

Learn about the core storage concepts in {{es}}.

* [](/manage-data/data-store/index-basics.md): Learn about index fundamentals, including index naming and aliases, document structure, metadata fields, and mappings.
* [](/manage-data/data-store/near-real-time-search.md): Understand how {{es}} makes newly indexed data searchable within seconds of indexing.
* [](/manage-data/data-store/data-streams.md): Learn when to use data streams for timestamped and append-only time series data, like logs, events, or metrics. You work with one stream name while {{es}} manages multiple backing indices behind the scenes.

## Configure how data is stored

Control how {{es}} indexes, maps, and analyzes your data.

* [](/manage-data/data-store/mapping.md): Define how documents and their fields are stored and indexed. Choose between dynamic mapping for automatic field detection and explicit mapping for full control over field types and indexing behavior.
* [](/manage-data/data-store/text-analysis.md): Configure how unstructured text is converted into a structured format optimized for full-text search, including tokenization, normalization, and custom analyzers.
* [](/manage-data/data-store/templates.md): Define reusable index configurations including settings, mappings, and aliases that are automatically applied when new indices or data streams are created.
* [](/manage-data/data-store/aliases.md): Create named references that point to one or more indices or data streams, enabling zero-downtime reindexing and simplified query targeting.

## Manage data

Work with your indices and data using the {{kib}} UI or the {{es}} REST API.

* [](/manage-data/data-store/perform-index-operations.md): Use {{kib}}'s **Index Management** page to view and manage your indices, data streams, templates, component templates, and enrich policies.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Index, update, retrieve, search, and delete documents using curl and the {{es}} REST API.

::::{tip}
If you manage append-only timestamped data with data streams, use [Data lifecycle](/manage-data/lifecycle.md) to plan retention and performance over time.
::::