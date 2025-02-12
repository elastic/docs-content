---
applies:
  stack:
  serverless:
---
# Dense vector

Dense neural embeddings capture semantic meaning by translating content into fixed-length vectors of floating-point numbers. Similar content maps to nearby points in the vector space, making them ideal for:

- Finding semantically similar content
- Matching questions with answers
- Image similarity search
- Content-based recommendations

## Working with dense vectors in Elasticsearch

:::{tip}
Using the `semantic_text` field type provides automatic model management and sensible defaults. [Learn more](../semantic-search/semantic-search-semantic-text.md).
:::

Dense vector search requires both index configuration and a strategy for generating embeddings. To use dense vectors in {{es}}:

1. Index documents with embeddings
  - You can generate embeddings within {{es}}
    - Refer to [this overview](../semantic-search.md#using-nlp-models) of the main options
  - You can also [bring your own embeddings](bring-own-vectors.md)
    - Use the `dense_vector` field type
2. Query the index using the [`knn` search](knn.md)