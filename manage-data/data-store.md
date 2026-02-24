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

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene.

This section explains how {{es}} stores your data — from the fundamental storage unit (the index) to the mappings, templates, and abstractions that control how data is organized and retrieved.

## Understand data storage

Learn about the core storage concepts in {{es}}.

* [](/manage-data/data-store/index-basics.md): Learn about the fundamental unit of storage in {{es}} — a collection of documents identified by a name or alias. Understand the key components of an index, including documents, metadata fields, and mappings.
* [](/manage-data/data-store/data-streams.md): Use data streams for append-only timestamped data such as logs, events, and metrics. A data stream provides a single named resource backed by multiple auto-generated indices.
* [](/manage-data/data-store/near-real-time-search.md): Understand how {{es}} makes newly indexed data searchable within seconds.

## Configure how data is stored

Control how {{es}} indexes, maps, and analyzes your data.

* [](/manage-data/data-store/mapping.md): Define how documents and their fields are stored and indexed. Choose between dynamic mapping for automatic field detection and explicit mapping for full control over field types and indexing behavior.
* [](/manage-data/data-store/text-analysis.md): Configure how unstructured text is converted into a structured format optimized for full-text search, including tokenization, normalization, and custom analyzers.
* [](/manage-data/data-store/templates.md): Define reusable index configurations — including settings, mappings, and aliases — that are automatically applied when new indices or data streams are created.
* [](/manage-data/data-store/aliases.md): Create named references that point to one or more indices or data streams, enabling zero-downtime reindexing and simplified query targeting.

## Manage data

Work with your indices and data using the {{kib}} UI or the {{es}} REST API.

* [](/manage-data/data-store/index-management.md): Use {{kib}}'s **Index Management** page to view and manage your indices, data streams, templates, component templates, and enrich policies.
* [](/manage-data/data-store/manage-data-from-the-command-line.md): Index, update, retrieve, search, and delete documents using curl and the {{es}} REST API.
