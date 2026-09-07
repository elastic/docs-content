---
navigation_title: "{{vectordb}} project"
applies_to:
  serverless: ga
description: >-
  The {{es}} {{vectordb}} project type on Elastic Cloud Serverless is
  optimized for vector workloads, with vector-tuned defaults, hardware profile,
  inference access, and pricing. It supports semantic and hybrid search.
products:
  - id: cloud-serverless
  - id: serverless-vector-database
---

# {{es}} {{vectordb}} project overview

The {{es}} {{vectordb}} {{serverless-short}} project type is optimized for vector workloads. Compared with the general-purpose [{{es}} project type](/solutions/elasticsearch-solution-project.md), it uses a vector-tuned default configuration, a hardware profile suited to embeddings, streamlined access to {{infer}}, and a pricing model built for vector storage and search.

Use the {{vectordb}} project type when embeddings and similarity search are central to your application, for example [RAG](/solutions/search/rag.md), [recommendations](/solutions/search/vector/vector-search-use-cases.md#discovery-and-recommendations), [semantic search](/solutions/search/semantic-search.md), [hybrid search](/solutions/search/hybrid-search.md), or [multimodal search](/solutions/search/multimodal-search.md).

## What you get

A {{vectordb}} project gives you the same {{es}} vector search capabilities as other project types, plus {{serverless-full}} defaults and project settings aimed at embedding storage, {{infer}}, and similarity or hybrid search.

### Vectors and structured data in one index

Like any {{es}} index, you can store embeddings alongside standard [field types](/manage-data/data-store/mapping.md) in the same documents, such as `keyword`, `text`, numeric types, `date`, `boolean`, geo fields, `nested`, and more. Combine similarity search with [filters](/solutions/search/vector/knn.md#knn-search-filter-example) on that metadata using Query DSL queries such as `bool`, `range`, and `terms`. Combining vectors and structured fields in one engine is an advantage over a typical dedicated vector store.

### Vector-optimized defaults and hardware profile

Indices use the [`index.mode: vectordb_document`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode) vector index mode automatically. It applies storage, indexing, and merge defaults tuned for similarity search on dense vectors, so you get efficient embedding storage and approximate [kNN](/solutions/search/vector/knn.md) search without configuring each setting yourself.

Index-level vector tuning is managed for you. You can balance search capacity, latency, and cost by adjusting [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) settings.

The project hardware profile is also tuned for vector workloads.

Vectors are stored compressed to reduce storage size. If [`_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) is enabled for vector fields, it keeps the values you indexed. Retrieving those same vectors with the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#search-fields-param) parameter can return slightly different values because of compression. For example, `3.0` might read back as `2.9953578`. That difference is expected; it does not mean your data is corrupted.

### Vector query patterns

The {{vectordb}} project type favors workloads where you ingest and embed data, then serve similarity or hybrid queries repeatedly. Aggressive segment merging improves query speed for relatively stable corpora, which is a common pattern for knowledge bases, product catalogs with semantic search, and RAG document stores.

### Access to {{infer}}

{{vectordb}} projects are set up for embedding workloads: use managed workflows with [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) or [`semantic`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md) fields to generate embeddings in {{es}}, or [bring your own vectors](/solutions/search/vector/bring-own-vectors.md) and search them with a [kNN query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md). In-product setup guides walk through both paths.

### Pricing designed for vector workloads

Similar to other {{serverless-full}} projects, Elastic manages the infrastructure, scaling, and upgrades. You create a project, get an endpoint, and start indexing and querying without sizing nodes for vector RAM yourself. Each project can store up to 1 TB of data.

:::{tip}
You can check your dataset size with the [Get index information]({{es-serverless-apis}}operation/operation-cat-indices) API.
:::

Billing uses storage, search, ingest, and infrastructure, rather than the compute-based VCU model used by {{es-serverless}} projects. Refer to [{{es}} {{vectordb}} billing dimensions](/deploy-manage/cloud-organization/billing/vector-database-billing-dimensions.md) for details.

## When to use this project type

Both the {{es}} {{vectordb}} and the {{es}} project types support [vector search](/solutions/search/vector.md).

Choose {{vectordb}} when embeddings and similarity search are central to the workload, especially when you also need structured metadata and filters in the same index rather than a dedicated vector store plus a separate search system. For those projects, generate embeddings with managed models through the [Elastic Inference Service](/explore-analyze/elastic-inference/eis.md) or a [third-party inference endpoint](/explore-analyze/elastic-inference/external.md); you can't deploy custom ML models for in-cluster inference.

Choose the [{{es}} project type](/solutions/elasticsearch-solution-project.md) when you need general-purpose data storage and search, including mixed lexical, time series, and analytics workloads, {{kib}} search tooling such as [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md) and [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md), or the ability to run custom models on ML nodes. You might also prefer the {{es}} project type if you are an existing {{es}} or OpenSearch user.

| Use case | Fit | Why |
| --- | --- | --- |
| [RAG and question answering](/solutions/search/vector/vector-search-use-cases.md#rag-and-question-answering-on-your-own-data) | Strong | Retrieve passages from documents, wikis, tickets, or knowledge bases and pass them to an LLM. Hybrid search combines semantic similarity with keyword matching when queries mix natural language with exact terms, IDs, or product names. |
| [Discovery and recommendations](/solutions/search/vector/vector-search-use-cases.md#discovery-and-recommendations) | Strong | Find related products, articles, or other items by similarity when keywords alone are not enough. Use hybrid ranking when you also need lexical or attribute matches in the same result set. |
| [Multimodal search](/solutions/search/vector/vector-search-use-cases.md#multimodal-search) | Strong | Search across images, audio, video, or text with embeddings from a multimodal model. |
| [Duplicate detection, fraud, and anomaly detection](/solutions/search/vector/vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection) | Strong | Compare embeddings to find near-duplicates, suspicious matches, or unusual patterns at scale. |
| [Long-term memory for LLMs](/solutions/search/vector/vector-search-use-cases.md#long-term-memory-for-llms) | Strong | Store facts, chat turns, or summaries so an assistant can retrieve relevant past context by meaning, optionally combined with keyword filters on metadata. |
| Full-text or keyword search without vectors | Prefer the {{es}} project | General-purpose defaults suit lexical search, filters, and document-centric analytics. |
| Log, event, or other time series search | Prefer the {{es}} project | General-purpose defaults suit write-heavy, frequently updated time series data. |

:::{note}
{{vectordb}} projects use [vector index mode](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode) only. [Time series index mode](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) and [LogsDB index mode](/manage-data/data-store/data-streams/logs-data-stream.md) are not supported. Use the Elasticsearch project type for those workloads. Data streams are supported when their backing indices use vector index mode.
:::

## Get started

<!-- TODO: After https://github.com/elastic/docs-content/pull/7923 merges, replace the dummy link below with /solutions/vector-database/vector-full-text-search.md -->
Ready to try the {{vectordb}} project type? Follow [Get started](https://github.com/solutions/vector-database/get-started.md) to create a project and learn about the different methods you can ingest embeddings and run search queries.

## Learn more about using vector search

* [Search use case](/solutions/search.md): Explore {{es}} search capabilities available across all deployment types, including {{vectordb}} projects.
* [Vector search in {{es}}](/solutions/search/vector.md): Learn how vector search works, including vectors, embeddings, field types, and similarity search.
* [Vector search use cases](/solutions/search/vector/vector-search-use-cases.md): Explore common vector search applications and implementation guidance.
* [{{es-serverless}} API documentation]({{es-serverless-apis}}): Find API endpoints, request parameters, and response schemas supported by serverless projects.
