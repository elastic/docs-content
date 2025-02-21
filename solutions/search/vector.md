---
applies_to:
  stack:
  serverless:
---
# Vector search

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type provides an abstraction over these vector search implementations with sensible defaults and automatic model management. It's the recommended approach for most users. [Learn more about semantic_text](semantic-search/semantic-search-semantic-text.md).
:::

Vector embeddings are a core technology in modern search, enabling models to learn and represent complex relationships in input data. When your content is vectorized, Elasticsearch can help users find content based on meaning and similarity, instead of just keyword or exact term matches.

Vector search is an important component of most modern [semantic search](semantic-search.md) implementations. It can also be used independently for various similarity matching use cases. Learn more about use cases for AI-powered search in the [overview](ai-search/ai-search.md) page.

This guide explores the more manual technical implementation of vector search approaches, that do not use the higher-level `semantic_text` workflow.

Which approach you use depends on your specific requirements and use case.

## Vector queries and field types

Here's a quick reference overview of vector search field types and queries available in Elasticsearch:

| Vector type | Field type      | Query type      | Primary use case                                   |
| ----------- | --------------- | --------------- | -------------------------------------------------- |
| Dense       | `dense_vector`  | `knn`           | Semantic similarity using your chosen embeddings model          |
| Sparse      | `sparse_vector` | `sparse_vector` | Semantic term expansion with the ELSER model                |
| Sparse or dense | `semantic_text` | `semantic` | Managed semantic search that is agnostic to implementation details  |

## Dense vector search

Dense neural embeddings capture semantic meaning by translating content into fixed-length vectors of floating-point bumbers. Similar content maps to nearby points in the vector space, making them ideal for:
- Finding semantically similar content
- Matching questions with answers
- Image similarity search
- Content-based recommendations

[Learn more about dense vector search](vector/dense-vector.md).

## Sparse vector search 

The sparse vector approach uses the ELSER model to expand content with semantically related terms. This approach preserves explainability while adding semantic understanding, making it well-suited for:
- Enhanced keyword search
- Cases requiring explainable results
- Domain-specific search
- Large-scale deployments

[Learn more about sparse vector search with ELSER](vector/sparse-vector.md).