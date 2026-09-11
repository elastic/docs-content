---
navigation_title: "{{vectordb}} project"
applies_to:
  serverless: ga
  stack: unavailable
description: >-
  The Elasticsearch Vector Database project type on Elastic Cloud Serverless is
  optimized for vector workloads, with vector-tuned defaults, hardware profile,
  inference access, and pricing. It supports semantic and hybrid search.
products:
  - id: cloud-serverless
  - id: serverless-vector-database
type: overview
---

# {{es}} {{vectordb}} project overview

The {{es}} {{vectordb}} project type is Elastic's solution for vector workloads, available on {{serverless-full}}. 

With its [optimized configuration and pricing](#what-you-get), it is best suited when embeddings and similarity search are central to your application, for example RAG, recommendations, semantic search, hybrid search, or multimodal search. 

Refer to the [When to use this project type](#when-to-use-this-project-type) section of this page for more information.

## What you get

{{vectordb}} projects offer a vector-optimized version of {{es}}. The following lists the main characteristics of {{vectordb}} projects:

### Vectors and structured data in one index

Like any {{es}} index, you can store embeddings alongside standard [field types](/manage-data/data-store/mapping.md) in the same documents, such as `keyword`, `text`, numeric types, `date`, `boolean`, geo fields, `nested`, and more. Combine similarity search with [filters](/solutions/search/vector/knn.md#knn-search-filter-example) on that metadata using Query DSL queries such as `bool`, `range`, and `terms`. Combining vectors and structured fields in one engine is an advantage over a typical dedicated vector store.

### Vector-optimized defaults and hardware profile

Indices use the [`index.mode: vectordb_document`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode) vector index mode automatically. It applies storage, indexing, and merge defaults tuned for similarity search on dense vectors, so you get efficient embedding storage and approximate [kNN](/solutions/search/vector/knn.md) search without configuring each setting yourself. This is the only index mode supported in this project.

Index-level vector tuning is managed for you. You can balance search capacity, latency, and cost by adjusting [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) settings.

The project hardware profile is also tuned for vector workloads.

Vectors are stored compressed to reduce storage size. If [`_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) is enabled for vector fields, it keeps the values you indexed. Retrieving those same vectors with the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#search-fields-param) parameter can return slightly different values because of compression. For example, `3.0` might read back as `2.9953578`. That difference is expected; it does not mean your data is corrupted.

### Vector query patterns

The {{vectordb}} project type favors workloads where you ingest and embed data, then serve similarity or hybrid queries repeatedly. Aggressive segment merging improves query speed for data that changes infrequently, which is a common pattern for knowledge bases, product catalogs with semantic search, and RAG document stores.

### Access to {{infer}}

{{vectordb}} projects are set up for embedding workloads: use managed workflows with [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) or [`semantic`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md) fields to generate embeddings in {{es}}, or [bring your own vectors](/solutions/search/vector/bring-own-vectors.md) and search them with a [kNN query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md).

### Pricing designed for vector workloads

Similar to other {{serverless-full}} projects, Elastic manages the infrastructure, scaling, and upgrades. You create a project, get an endpoint, and start indexing and querying without sizing nodes for vector RAM yourself. Each project can store up to 1 TB of data.

:::{tip}
You can check your dataset size with the [Get index information]({{es-serverless-apis}}operation/operation-cat-indices) API.
:::

Billing is based on storage, search, ingest, and infrastructure, rather than the compute-based VCU model used by {{es-serverless}} projects. That means costs follow how much you store and the search capacity you reserve with Search Power, not fluctuating compute or query volume, which is a better fit for embedding data you query often. Refer to [{{es}} {{vectordb}} billing dimensions](/deploy-manage/cloud-organization/billing/vector-database-billing-dimensions.md) for details.

## When to use this project type

Both the {{es}} {{vectordb}} project type and the {{es}} solution support [vector search](/solutions/search/vector.md). {{vectordb}} gives you the full power of the core {{es}} capabilities: The same query APIs, mappings, filters, and hybrid or semantic retrieval. 

It uses a vector-tuned default configuration, a hardware profile suited to embeddings, streamlined access to {{infer}}, and a pricing model built for vector storage and search.

Choose {{vectordb}} when embeddings and similarity search are the primary workload, and you don't need extra features like time series data support, search application management, or custom ML nodes.

Choose the [{{es}} solution](/solutions/elasticsearch-solution-project.md) when you need general-purpose data storage and search, including mixed lexical, time series, and analytics workloads, {{kib}} search tooling such as [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md), or the ability to run custom models on ML nodes. You might also prefer the {{es}} solution if you are an existing {{es}} or OpenSearch user.

| Use case | Best solution | Why |
| --- | --- | --- |
| [RAG and question answering](/solutions/search/vector/vector-search-use-cases.md#rag-and-question-answering-on-your-own-data) | {{vectordb}} project | Retrieve passages from documents, wikis, tickets, or knowledge bases and pass them to an LLM. Hybrid search combines semantic similarity with keyword matching when queries mix natural language with exact terms, IDs, or product names. |
| [Discovery and recommendations](/solutions/search/vector/vector-search-use-cases.md#discovery-and-recommendations) | {{vectordb}} project | Find related products, articles, or other items by similarity when keywords alone are not enough. Use hybrid ranking when you also need lexical or attribute matches in the same result set. |
| [Multimodal search](/solutions/search/vector/vector-search-use-cases.md#multimodal-search) | {{vectordb}} project | Search across images, audio, video, or text with embeddings from a multimodal model. |
| [Duplicate detection, fraud, and anomaly detection](/solutions/search/vector/vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection) | {{vectordb}} project | Compare embeddings to find near-duplicates, suspicious matches, or unusual patterns at scale. |
| [Long-term memory for LLMs](/solutions/search/vector/vector-search-use-cases.md#long-term-memory-for-llms) | {{vectordb}} project | Store facts, chat turns, or summaries so an assistant can retrieve relevant past context by meaning, optionally combined with keyword filters on metadata. |
| Full-text or keyword search without vectors | [{{es}} solution](/solutions/elasticsearch-solution-project.md) | General-purpose defaults suit lexical search, filters, and document-centric analytics. |
| Log, event, or other time series search | [{{es}} solution](/solutions/elasticsearch-solution-project.md) | General-purpose defaults suit write-heavy, frequently updated time series data. |
| Mixed search and analytics | [{{es}} solution](/solutions/elasticsearch-solution-project.md) | General-purpose defaults suit workloads that combine search with analytics or time series data. |

:::{note}
{{vectordb}} projects only support the [vector index mode](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode). [Time series index mode](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) and [LogsDB index mode](/manage-data/data-store/data-streams/logs-data-stream.md) are not supported. Use the Elasticsearch project type for those workloads. Data streams are supported when their backing indices use vector index mode.
:::

## Get started

Ready to try the {{vectordb}} project type? For a hands-on, step-by-step walkthrough with a client, sample data, and semantic, hybrid, and ES|QL searches, follow [](/solutions/vector-database/vector-full-text-search.md).

For an overview of creating a project and the ingest and search options available, refer to [](/solutions/vector-database/get-started.md).

## Learn more about using vector search

* [Search use case](/solutions/search.md): Explore {{es}} search capabilities available across all deployment types, including {{vectordb}} projects.
* [Vector search in {{es}}](/solutions/search/vector.md): Learn how vector search works, including vectors, embeddings, field types, and similarity search.
* [Vector search use cases](/solutions/search/vector/vector-search-use-cases.md): Explore common vector search applications and implementation guidance.
* [{{es-serverless}} API documentation]({{es-serverless-apis}}): Find API endpoints, request parameters, and response schemas supported by serverless projects.
