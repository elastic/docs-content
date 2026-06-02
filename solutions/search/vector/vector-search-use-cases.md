---
navigation_title: Use cases
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
# Vector search use cases

:::{tip}
New to semantic search? Start with the [semantic search quickstart](../get-started/semantic-search.md), which uses the managed `semantic_text` workflow.

To understand core vector search concepts in {{es}}, including embeddings, field types, retrieval methods, and available workflows, refer to [Vector search in {{es}}](../vector.md#vectors-and-embeddings).
:::

Sometimes [full-text search](../full-text.md) alone isn't enough. {{ml-cap}} techniques help you find data based on intent and contextual meaning, not just keywords. Vector search is the foundation for these capabilities in {{es}}.

This page introduces common vector search use cases and provides guidance on how to implement them in {{es}}.

## RAG and question answering on your own data

Use vector search to retrieve relevant pieces of your data and provide them to a language model. This helps generate answers that are grounded in your own content instead of relying on general knowledge.

Use this approach when building applications such as question answering over your own documents (PDFs, wikis, or tickets), internal or customer-facing knowledge assistants, chatbots powered by your own data, or customer support systems based on FAQs and ticket history. It is also commonly used for internal knowledge search across tools like Confluence, SharePoint, or Notion.

In practice, these systems are often applied to enterprise search across internal knowledge bases, customer support centers and help desks, and legal or patent search where LLMs help explore and summarize large document sets. Other common use cases include intelligence and investigation systems (for example, homeland security), academic research assistants, and tools for exploring libraries and archives.

::::::{stepper}
:::::{step} Learn about RAG in Elasticsearch

Read how retrieval-augmented generation fits into {{es}} and how it relates to search and orchestration.

- [RAG](../rag.md)

:::::

:::::{step} Choose a search strategy

Implement retrieval that matches your content and latency needs. Use [semantic search](../semantic-search.md) when you want a managed workflow (for example the `semantic_text` field type), [vector search](../vector.md) when you configure embeddings and vector fields directly, or [hybrid search](../hybrid-search.md) to combine full-text with semantic or vector retrieval in one request. Hybrid setups often use [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) to merge rankings.

You can run retrieval using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [Search approaches](../search-approaches.md)
- [Semantic search and vector search](../vector.md#semantic-search-vs-vector-search)
- [Hybrid search](../hybrid-search.md)
- [Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md)
- [The search API](../the-search-api.md)
- [kNN search](knn.md)
- [{{esql}} for search](../esql-for-search.md)
- [{{esql}} `KNN`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/knn.md)
- [Reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md)

:::::

:::::{step} Generate answers with an LLM

Pass the top hits (and their source fields) to your chosen model or orchestration layer so generation is grounded in retrieved passages rather than the model’s general knowledge alone.

- [Core search options](../rag.md#core-search-options) ({{esql}} `COMPLETION`, Agent Builder, custom apps)

:::::
::::::

## Discovery and recommendations

Use vector similarity to find related items or rank results based on relevance beyond keyword matching.

This approach is commonly used to build recommendation and discovery experiences, such as suggesting similar products, ranking content, or helping users explore large datasets.

In practice, this includes e-commerce recommendations like “similar products” or “you may also like”, matching systems in dating platforms, and finding compatible teammates or opponents in gaming. It is also widely used in content platforms to recommend articles, videos, or music based on user behavior and preferences.

::::::{stepper}
:::::{step} Represent catalog items as vectors

Index each item (or the text and metadata you want to match on) so it produces a comparable embedding across the catalog. Consistent embeddings make “similar item” retrieval meaningful.

- [Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md)
- [Elastic Inference](../../../explore-analyze/elastic-inference.md)
- [Bring your own dense vectors](bring-own-vectors.md)
- [Dense vector search](dense-vector.md)
- [`dense_vector` field](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md)

:::::

:::::{step} Retrieve neighbors with kNN

Run approximate kNN (or exact kNN when your candidate set is small) using the embedding of the anchor item or user profile vector. This is the core similarity search behind “more like this” and related-item panels.

You can run kNN retrieval using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [The search API](../the-search-api.md)
- [kNN search](knn.md)
- [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn)
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md)
- [kNN retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/knn-retriever.md)
- [{{esql}} for search](../esql-for-search.md)
- [{{esql}} `KNN`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/knn.md)

:::::

:::::{step} Apply business constraints

Narrow candidates with structured filters (availability, region, permissions, category) in the same search request so similarity runs over the right subset of documents.

You can apply filters using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [Querying for search](../querying-for-search.md)
- [The search API](../the-search-api.md)
- [{{esql}} for search](../esql-for-search.md)

:::::

:::::{step} Refine ranking

When raw top-k similarity is not enough, combine vector retrieval with full-text search or add a second-stage ranker. Use [hybrid search](../hybrid-search.md) when you need keyword matching and similarity search in one ranked list, or LTR when you have labeled training data.

You can refine ranking using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [Ranking and reranking](../ranking.md)
- [The search API](../the-search-api.md)
- [{{esql}} for search](../esql-for-search.md)
- [Semantic reranking](../ranking/semantic-reranking.md)
- [Hybrid search](../hybrid-search.md)
- [Hybrid search with `semantic_text`](../hybrid-semantic-text.md)
- [Learning To Rank (LTR)](../ranking/learning-to-rank-ltr.md)

:::::
::::::

## Multimodal search

Use embeddings from different data types to enable search across non-text content such as images, audio, or video.

This approach is useful when users need to search using one modality to find another, or when working with rich media content.

In practice, this includes image search (for example, visual product search), audio and video search, and cross-modal scenarios such as using text queries to find images or other media.

::::::{stepper}
:::::{step} Select a multimodal embedding workflow

Use the {{infer}} APIs with a model and service that supports the modalities you need (for example, text and image inputs to a shared embedding space). Configure endpoints so documents and queries use the same task type and model; otherwise similarity scores are not comparable.

- [Elastic {{infer-cap}}](../../../explore-analyze/elastic-inference.md)
- [Semantic search with the {{infer}} API](../semantic-search/semantic-search-inference.md)

:::::

:::::{step} Index vectors for each media object

Store embeddings in `dense_vector` fields when vectors are produced outside a managed `semantic_text` path, and keep textual or structured fields you still filter on.

- [Bring your own dense vectors](bring-own-vectors.md)
- [Dense vector search](dense-vector.md)
- [`dense_vector` field](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md)

:::::

:::::{step} Encode queries in the same space

At search time, turn the user’s text or media into an embedding using the same {{infer}} endpoint and settings as at ingest (task type, model, dimensions).

You can encode queries using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [Semantic search with the {{infer}} API](../semantic-search/semantic-search-inference.md)
- [The search API](../the-search-api.md)
- [{{esql}} for search](../esql-for-search.md)
- [{{esql}} `EMBEDDING`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/embedding.md)

:::::

:::::{step} Run kNN retrieval (and optional hybrid passes)

Execute kNN against the indexed vectors, and add lexical or metadata filters when you need constraints beyond raw similarity, for example surfacing visually similar products only within a category.

You can run kNN retrieval using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [The search API](../the-search-api.md)
- [kNN search](knn.md)
- [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn)
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md)
- [{{esql}} for search](../esql-for-search.md)
- [{{esql}} `KNN`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/knn.md)
- [Hybrid search](../hybrid-search.md)

:::::
::::::

## Duplicate detection, fraud, and {{anomaly-detect}}

Use vector similarity to identify patterns, duplicates, or unusual behavior in your data.

This approach is useful when you need to compare items at scale and detect similarities or deviations that are not easily captured by exact matching.

In practice, this includes detecting duplicate content, identifying fraudulent activity, and spotting anomalies in large datasets across domains such as finance, security, and operations.

::::::{stepper}
:::::{step} Normalize records before embedding

Clean and canonicalize the text or features you fingerprint (for example, normalized URLs, stripped boilerplate, hashed identifiers) so trivial differences do not fragment clusters in embedding space.

- [Ingest for search](../ingest-for-search.md)

:::::

:::::{step} Index vectors for each entity or event

Use `semantic_text` when you want {{es}} to manage inference, or `dense_vector` when you generate vectors upstream. You need one comparable vector per document or chunk you want to compare.

- [Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md)
- [Bring your own dense vectors](bring-own-vectors.md)

:::::

:::::{step} Query for nearest neighbors and cutoffs

Use kNN to fetch the closest documents to a candidate and interpret similarity scores or ranks in your application, for example flagging pairs above a cosine-similarity threshold as likely duplicates, or surfacing accounts whose behavior vectors sit unusually close to known fraud exemplars.

You can query for nearest neighbors using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [The search API](../the-search-api.md)
- [kNN search](knn.md)
- [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn)
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md)
- [{{esql}} for search](../esql-for-search.md)
- [{{esql}} `KNN`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/knn.md)

:::::

::::::

## Long-term memory for LLMs

Use vector search as a memory layer for applications that need to store and retrieve past interactions or knowledge.

This approach enables systems to maintain context over time and provide more personalized or consistent responses. In practice, this includes persistent memory for AI assistants, personalized user experiences, and applications that retain and reuse knowledge across sessions.

::::::{stepper}
:::::{step} Design the memory index

Model memory documents with stable identifiers (user, session, agent), timestamps, optional TTL fields, and the text you will embed. Decide whether each memory is a short fact, a conversation turn, or a summarized chunk so retrieval returns the right granularity.

- [Index basics](../get-started/index-basics.md)

:::::

:::::{step} Ingest and embed new memories

Choose how you store embeddings so ingest and query use the same model.

- [Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md): index through a `semantic_text` mapping so {{es}} manages {{infer}} and embedding generation
- [Ingest data with `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-ingestions.md): mapping and ingest reference for `semantic_text`
- [{{infer-cap}} processor](elasticsearch://reference/enrich-processor/inference-processor.md): generate embeddings in an ingest pipeline for vector search
- [Bring your own dense vectors](bring-own-vectors.md): index precomputed vectors into a `dense_vector` field

:::::

:::::{step} Retrieve context for each prompt

Retrieve the top-k memories with the same approach you used at ingest, then pass those hits to your orchestration layer with the current user message.

You can retrieve context using the [Search API with Query DSL](../the-search-api.md), or [{{esql}}](../esql-for-search.md).

- [Semantic search](../semantic-search.md)
- [The search API](../the-search-api.md)
- [kNN search](knn.md)
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md)
- [Hybrid search](../hybrid-search.md)
- [{{esql}} for search](../esql-for-search.md)
- [{{esql}} `KNN`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/knn.md)


:::::

:::::{step} Govern retention and updates

Expire or consolidate stale memories using your application logic or index lifecycle policies so the vector index does not grow without bound or contradict newer facts.

- [{{ilm-cap}}](../../../manage-data/lifecycle/index-lifecycle-management.md)

:::::
::::::
