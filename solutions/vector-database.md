---
navigation_title: Vector Database project
applies_to:
  serverless: ga
description: >-
  The Elasticsearch Vector Database project type on Elastic Cloud Serverless is
  optimized for vector workloads, with vector-tuned defaults, hardware profile,
  inference access, and pricing. It supports semantic and hybrid search.
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# {{es}} Vector Database project overview

The {{es}} Vector Database {{serverless-short}} project type is optimized for vector workloads. Compared with the general-purpose [{{es}} project type](/solutions/elasticsearch-solution-project.md), it uses a vector-tuned default configuration, a hardware profile suited to embeddings, streamlined access to {{infer}}, and a pricing model built for vector storage and search.

[Vector search](/solutions/search/vector.md) uses the same query APIs in both project types.

Use it when embeddings and similarity search are central to your application, for example RAG, recommendations, [semantic search](/solutions/search/semantic-search.md), [hybrid search](/solutions/search/hybrid-search.md), or multimodal search.

## What you get

A Vector Database project gives you {{serverless-full}} operations with defaults and project settings aimed at embedding storage, {{infer}}, and similarity or hybrid search.

### Vector-optimized defaults and hardware profile

Indices in a Vector Database project use the [`index.mode: vectordb_document`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode) vector index mode automatically. It applies storage, indexing, and merge defaults tuned for similarity search on dense vectors, so you get efficient embedding storage and approximate [kNN](/solutions/search/vector/knn.md) search without configuring each setting yourself. The project hardware profile is also tuned for vector workloads.

:::{tip}
On other [deployment types](/deploy-manage/deploy.md), you can set the vector index mode explicitly when you create an index.
:::

### Built for vector query patterns

The Vector Database project type favors workloads where you ingest and embed data, then serve similarity or hybrid queries repeatedly. Aggressive segment merging improves recall and query speed for relatively stable corpora, which is a common pattern for knowledge bases, product catalogs with semantic search, and RAG document stores.

<!-- Fact-check: confirm messaging around merge behavior and guidance for high-churn ingest (e.g. logs) before publish. -->

### Access to {{infer}}

Vector Database projects are set up for embedding workflows: generate vectors in {{es}} with managed models (for example through `semantic_text`), or store vectors you create yourself and attach the same model at query time. In-product setup guides walk through both paths.

### Pricing designed for vector workloads

Similar to other {{serverless-full}} projects, Elastic manages the infrastructure, scaling, and upgrades. You create a project, get an endpoint, and start indexing and querying without sizing nodes for vector RAM yourself.

Billing uses storage, search, ingest, and infrastructure, rather than the compute-based VCU model used by {{es-serverless}} projects. Refer to [{{es}} Vector Database billing dimensions](/deploy-manage/cloud-organization/billing/vector-database-billing-dimensions.md) for details.

## When to use this project type

Both the {{es}} Vector Database and the {{es}} project types support [vector search](/solutions/search/vector.md). Choose Vector Database when embeddings and similarity search are central to the workload. Choose the [{{es}} project type](/solutions/elasticsearch-solution-project.md) for general-purpose data storage and search, including mixed lexical, time series, and analytics workloads, or {{kib}} search tooling such as [Playground](/solutions/elasticsearch-solution-project/playground.md), [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md), and [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md). You might prefer the {{es}} project type if you are an existing {{es}} or OpenSearch user.

| Use case | Fit | Why |
| --- | --- | --- |
| [RAG and question answering](/solutions/search/vector/vector-search-use-cases.md#rag-and-question-answering-on-your-own-data) | Strong | Retrieve passages from documents, wikis, tickets, or knowledge bases and pass them to an LLM. Hybrid search combines semantic similarity with keyword matching when queries mix natural language with exact terms, IDs, or product names |
| [Discovery and recommendations](/solutions/search/vector/vector-search-use-cases.md#discovery-and-recommendations) | Strong | Find related products, articles, or other items by similarity when keywords alone are not enough. Use hybrid ranking when you also need lexical or attribute matches in the same result set |
| [Multimodal search](/solutions/search/vector/vector-search-use-cases.md#multimodal-search) | Strong | Search across images, audio, video, or text with embeddings from a multimodal model |
| [Duplicate detection, fraud, and anomaly detection](/solutions/search/vector/vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection) | Strong | Compare embeddings to find near-duplicates, suspicious matches, or unusual patterns at scale |
| [Long-term memory for LLMs](/solutions/search/vector/vector-search-use-cases.md#long-term-memory-for-llms) | Strong | Store facts, chat turns, or summaries so an assistant can retrieve relevant past context by meaning, optionally combined with keyword filters on metadata |
| Full-text or keyword search without vectors | Prefer the {{es}} project | General-purpose defaults suit lexical search, filters, and document-centric analytics |
| Log, event, or other time series search | Prefer the {{es}} project | General-purpose defaults suit write-heavy, frequently updated time series data |

:::{note}
Vector Database projects use vector index mode only. Time series (tsdb) and LogsDB index modes are not supported; use the {{es}} project type for those workloads. Data streams are supported when their backing indices use vector index mode.
:::

## Get started

Ready to try the Vector Database project type? Follow [Get started](/solutions/vector-database/get-started.md) to create a project, ingest embeddings, and run your first searches.

## Related pages

* [Vector search in {{es}}](/solutions/search/vector.md)
* [Vector search use cases](/solutions/search/vector/vector-search-use-cases.md)
* [Semantic search](/solutions/search/semantic-search.md)
* [{{es}} solution overview](/solutions/elasticsearch-solution-project.md)
* [Search use case documentation](/solutions/search.md)
* [{{es-serverless}} API documentation]({{es-serverless-apis}})
