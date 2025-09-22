---
navigation_title: Vector search
applies_to:
  stack:
  serverless:
---
# Vector search in {{es}}

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type provides an abstraction over vector search implementations with sensible defaults and automatic model management. It's the recommended way to start with {{es}} vector search. [Learn more about semantic_text](semantic-search/semantic-search-semantic-text.md).
:::

Vector search in {{es}} uses vector embeddings to power modern, AI-driven search experiences. With vectorized content, Elasticsearch retrieves results based on meaning and similarity, not just keywords or exact term matches.

Vector search is a core component of most [semantic search](semantic-search.md) workflows, but it can also be used independently for similarity matching use cases. Learn more about the broader benefits in the [AI-powered search overview](ai-search/ai-search.md).

This guide focuses on the more manual technical implementations of vector search, outside of the higher-level `semantic_text` workflow.  
The right approach depends on your requirements, data type, and use case.

## Vector queries and field types in {{es}} [vector-queries-and-field-types]

Here’s a quick reference for the main **vector field types** and **query types** you can use:

| Vector type     | Field type      | Query type      | Primary use case                                            |
| --------------- | --------------- | --------------- | ----------------------------------------------------------- |
| Dense vectors   | `dense_vector`  | `knn`           | Semantic similarity with your own embeddings model          |
| Sparse vectors  | `sparse_vector` | `sparse_vector` | Semantic term expansion using the ELSER model               |
| Sparse or dense | `semantic_text` | `semantic`      | Managed semantic search, agnostic to implementation details |

## Dense vector search in {{es}}

Dense vector search uses neural embeddings to capture semantic meaning. It translates content into fixed-length numeric vectors, where similar items cluster close together in vector space. This makes dense vectors ideal for:

- Finding semantically similar documents  
- Matching user questions with answers  
- Image and multimedia similarity search  
- Content-based recommendations  

[Learn more about dense vector search in {{es}}](vector/dense-vector.md).

## Sparse vector search with ELSER

Sparse vector search relies on the **ELSER model** to expand content with semantically related terms. This approach combines semantic understanding with explainability, making it a strong fit for:

- Enhanced keyword search  
- Use cases requiring explainable results  
- Domain-specific search  
- Large-scale deployments

[Learn more about sparse vector search with ELSER](vector/sparse-vector.md).
