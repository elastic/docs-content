---
navigation_title: Vector search
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---
# Vector search in {{es}}

Sometimes [full-text search](full-text.md) alone isn't enough. {{ml-cap}} techniques help users find data based on intent and contextual meaning, not just keywords. Vector search is the foundation for these capabilities in {{es}}.

Vector search uses {{ml}} models to convert content into numerical representations called _vector embeddings_. These embeddings capture meaning and relationships, enabling {{es}} to retrieve results based on similarity rather than exact term matches.

:::{tip}
New to vector search? Start with the `semantic_text` workflow, which provides an easy-to-use abstraction over vector search with sensible defaults and automatic model management. Learn more [in this hands-on tutorial](semantic-search/semantic-search-semantic-text.md).
:::

## How it works

To understand the core concepts behind vector search, including vectors, embeddings, similarity, and the difference between dense and sparse approaches, refer to [How vector search works](vector/how-vector-search-works.md).

## Use cases

Vector search enables a wide range of applications:

- **Natural language search**: Let users search in everyday language and get results based on meaning, not just keywords. 
- **Retrieval Augmented Generation (RAG)**: Retrieve relevant documents from {{es}} and feed them into a large language model (LLM) to generate grounded, context-aware answers.
- **Question answering**: Match natural language questions to the most relevant answers in your data. 
- **Content recommendations**: Suggest related articles, products, or media based on vector similarity. 
- **Large-scale information retrieval**: Search across millions or billions of documents efficiently.
- **Product discovery**: Help users find products that match their intent, even when they don't use exact product terms. 
- **Workplace document search**: Search internal knowledge bases, wikis, and documents by meaning rather than exact keywords. 
- **Image and multimedia similarity**: Find visually or semantically similar images, audio, or video by comparing their vector representations.

## Which workflow should I use?

{{es}} offers several ways to implement vector search. Your choice depends on how much control you need and what type of content you are searching.

### Semantic search workflows

Semantic search workflows are managed and require minimal configuration. They handle embedding generation and model management for you. Choose semantic search when:

- You want to get started quickly with natural language search
- You prefer Elastic to manage models and indexing defaults
- Your use case is text-based and fits common patterns (document search, RAG, question answering)

Explore these guides:

- [Semantic search](semantic-search.md)
- [Semantic search with `semantic_text`](semantic-search/semantic-search-semantic-text.md)
- [Semantic search with the {{infer}} API](semantic-search/semantic-search-inference.md)
- [Semantic search with ELSER](semantic-search/semantic-search-elser-ingest-pipelines.md)

### Direct vector search

Direct vector search uses the `dense_vector` and `sparse_vector` field types. Choose this when:

- You already have pre-computed embeddings or generate them outside {{es}}
- You need to search non-text content (images, audio) with embeddings from external models
- You require fine-grained control over indexing, quantization, or query parameters

Explore these guides:

- [Dense vector search](vector/dense-vector.md)
- [Sparse vector search](vector/sparse-vector.md)
- [Bring your own dense vectors](vector/bring-own-vectors.md)

:::{tip}
You can combine vector search with full-text search for [hybrid search](hybrid-search.md) that leverages both meaning-based and keyword-based matching.
:::

## Resources

Resources are grouped by implementation path. Start here for a quick win, or jump to the workflow that matches how much control you need.

### Start here

- [Get started with semantic search](get-started/semantic-search.md): Set up hybrid search using `semantic_text` with dense vector embeddings. The recommended starting point.
- [How vector search works](vector/how-vector-search-works.md): Core concepts: vectors, embeddings, dimensions, similarity, dense vs. sparse vectors, and quantization.

### Managed workflows

Use `semantic_text`, the {{infer-cap}} APIs, or ELSER for semantic search with managed embedding generation and model deployment.

- [Semantic search with `semantic_text`](semantic-search/semantic-search-semantic-text.md): Implement semantic search with automatic embedding generation and model management.
- [Hybrid search with `semantic_text`](hybrid-semantic-text.md): Combine vector search with full-text search using reciprocal rank fusion.
- [Semantic search with the {{infer}} API](semantic-search/semantic-search-inference.md): Configure {{infer}} endpoints for more control over embedding generation.
- [Semantic search with ELSER](semantic-search/semantic-search-elser-ingest-pipelines.md): Deploy the ELSER sparse vector model and build a semantic search pipeline.

### Manual implementation

Work directly with `dense_vector` and `sparse_vector` field types when you need more control over indexing, quantization, and query parameters.

- [Bring your own dense vectors to {{es}}](vector/bring-own-vectors.md): Store and search pre-computed dense vectors using the `dense_vector` field type.
- [Dense vector search in {{es}}](vector/dense-vector.md): How dense vectors capture semantic meaning using neural embeddings, and how to use them in {{es}}.
- [Sparse vector search in {{es}}](vector/sparse-vector.md): How ELSER generates sparse vectors for explainable, term-based semantic matching.
- [Tutorial: Dense and sparse workflows using ingest pipelines](vector/dense-versus-sparse-ingest-pipelines.md): A side-by-side walkthrough of dense and sparse vector ingest pipelines.

### Querying and pipelines

Build multi-stage retrieval and improve result ranking.

- [kNN search in {{es}}](vector/knn.md): Run approximate and exact k-nearest neighbor searches, with filtering, multi-kNN, and nested vector support.
- [Retrievers](retrievers-overview.md): Compose multi-stage retrieval pipelines that combine different search strategies in a single request.
- [Semantic reranking](ranking/semantic-reranking.md): Rerank search results using a cross-encoder model to improve relevance after initial retrieval.

### Models and infrastructure

Learn about the models and services that power vector search in {{es}}.

- [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md): Elastic's built-in sparse vector model for semantic search with explainable, term-based matching.
- [E5](/explore-analyze/machine-learning/nlp/ml-nlp-e5.md): A multilingual dense embedding model that can be deployed directly in {{es}}.
- [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md): A managed service for running {{ml}} models for embedding generation and other NLP tasks.
- [Search and compare text](/explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md): Use deployed NLP models to search and compare text at query time.
- [Text embedding and semantic search](/explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md): Deploy a text embedding model and use it for vector search, from model setup to query.
- [Using Cohere with {{es}}](semantic-search/cohere-es.md): Generate embeddings and perform semantic search using Cohere's models.

### Optimization

Tune vector search for production performance.

- [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md): Optimize vector search performance by tuning quantization, HNSW parameters, memory, and recall tradeoffs.
