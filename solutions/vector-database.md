---
navigation_title: Vector Database project
applies_to:
  serverless: preview
description: >-
  The Elasticsearch Vector Database project type on Elastic Cloud Serverless is
  built for AI-powered retrieval workloads such as RAG, recommendations, and semantic search.
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# {{es}} Vector Database project

The {{es}} Vector Database {{serverless-short}} project type provides optimized defaults for vector search workloads. Use it when you are building AI-powered retrieval, such as a chatbot, RAG pipeline, or recommendation engine, where embeddings and similarity search are central. Typical use cases include RAG, semantic retrieval, recommendations, and hybrid search.

[Vector search](/solutions/search/vector.md) works the same way as in other {{es}} projects. The difference is that the default configuration of the Vector Database project is tuned for vector-first workloads.

## What you get

The {{es}} Vector Database project type is designed for load-once, query-often vector workloads that your application calls over the API. Compared with a general-purpose {{es-serverless}} project, it prioritizes vector-friendly index defaults suited to embedding storage and similarity search.

### Vector index mode by default

Indices in a Vector Database project use the [`index.mode: vectordb_document`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode) vector index mode automatically. It applies storage, indexing, and merge defaults tuned for similarity search on dense vectors, so you get efficient embedding storage and approximate [kNN](/solutions/search/vector/knn.md) search without configuring each setting yourself.

:::{tip}
On other [deployment types](/deploy-manage/deploy.md), you can set the vector index mode explicitly when you create an index.
:::

### Built for vector query patterns

The Vector Database project type favors workloads where you ingest and embed data, then serve similarity or hybrid queries repeatedly. Aggressive segment merging improves recall and query speed for relatively stable corpora, which is a common pattern for knowledge bases, product catalogs with semantic search, and RAG document stores.

<!-- Fact-check: confirm messaging around merge behavior and guidance for high-churn ingest (e.g. logs) before publish. -->

### Multi-tenant partitioning with slices

For multi-tenant or multi-customer vector apps, you can use slices to partition an index so each tenant’s vectors are indexed and searched in isolation. Slice mode is opt-in and is not enabled automatically on Vector Database projects.

<!-- Link "slices" to the Partitioning with _slice section on knn.md when that content lands. -->

### Usage-based {{serverless-short}} operations

Similar to other {{serverless-full}} projects, Elastic manages the infrastructure, scaling, and upgrades. You create a project, get an endpoint, and start indexing and querying without sizing nodes for vector RAM yourself.

Billing uses storage, searchable capacity, indexing volume, and infrastructure hours rather than the VCU model used by {{es-serverless}}. See [{{es}} Vector Database billing dimensions](/deploy-manage/cloud-organization/billing/vector-database-billing-dimensions.md).

## When to use this project type

Choose {{es}} Vector Database when you are building retrieval for AI features: a chatbot, RAG pipeline, recommendation engine, or similar workloads where your application consumes results. This provides out of the box vector-tuned defaults.

Choose the [{{es}} project type](/solutions/elasticsearch-solution-project.md) when you are building a search application people interact with directly (a search bar, catalog, or knowledge base), or when you need broader search application tooling in {{kib}} such as [Playground](/solutions/elasticsearch-solution-project/playground.md), [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md), or [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md).

| Use case | Fit | Why |
| --- | --- | --- |
| [RAG and question answering](/solutions/search/vector/vector-search-use-cases.md#rag-and-question-answering-on-your-own-data) | Strong | Retrieve passages from documents, wikis, tickets, or knowledge bases and pass them to an LLM for assistants, support bots, and cited answers |
| [Discovery and recommendations](/solutions/search/vector/vector-search-use-cases.md#discovery-and-recommendations) | Strong | Find related products, articles, or other items by similarity when keywords alone are not enough |
| [Multimodal search](/solutions/search/vector/vector-search-use-cases.md#multimodal-search) | Strong | Search across images, audio, video, or text with embeddings from a multimodal model |
| [Duplicate detection, fraud, and anomaly detection](/solutions/search/vector/vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection) | Strong | Compare embeddings to find near-duplicates, suspicious matches, or unusual patterns at scale |
| [Long-term memory for LLMs](/solutions/search/vector/vector-search-use-cases.md#long-term-memory-for-llms) | Strong | Store facts, chat turns, or summaries so an assistant can retrieve relevant past context |
| Full-text or keyword search without vectors | Prefer the {{es}} project | The {{es}} project is built for lexical search, filters, and analytics on document-centric data |
| Log, event, or other time series search | Prefer {{es}} project | Choose the {{es}} project for continuously ingested logs and events, where general-purpose defaults fit write-heavy, frequently updated data |

## Get started

Ready to try the Vector Database project type? Follow [Get started](/solutions/vector-database/get-started.md) to create a project, ingest embeddings, and run your first searches.

## Related pages

* [Vector search in {{es}}](/solutions/search/vector.md)
* [Vector search use cases](/solutions/search/vector/vector-search-use-cases.md)
* [Semantic search](/solutions/search/semantic-search.md)
* [{{es}} solution overview](/solutions/elasticsearch-solution-project.md)
* [Search use case documentation](/solutions/search.md)
* [{{es-serverless}} API documentation]({{es-serverless-apis}})
