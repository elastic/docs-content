---
navigation_title: Dense vector
applies_to:
  stack:
  serverless:
---
# Dense vector search in {{es}}

Dense vectors use neural embeddings to represent semantic meaning. They translate text, images, or other data into fixed-length vectors of floating-point numbers. Content with similar meaning is mapped to nearby points in vector space, making dense vector search a powerful technique for:

- Finding semantically similar content
- Matching natural language questions with relevant answers
- Performing image and multimedia similarity search
- Delivering content-based recommendations

## Working with dense vectors in {{es}}

:::{tip}
For most use cases, the [`semantic_text` field type](../semantic-search/semantic-search-semantic-text.md) is the recommended starting point. It provides automatic model management and sensible defaults for vector search.
:::

To implement dense vector search in {{es}}, you need both an index configuration and a way to generate embeddings:

1. **Index documents with embeddings**
   - Generate embeddings directly in {{es}}
     - Refer to the [overview of NLP model options](../semantic-search.md#using-nlp-models)
   - Or [bring your own embeddings](bring-own-vectors.md)
     - Store them using the `dense_vector` field type

2. **Query the index with k-NN search**
   - Use the [`knn` query](knn.md) to retrieve results based on vector similarity

## Better Binary Quantization (BBQ) [bbq]

Better Binary Quantization (BBQ) is an advanced vector quantization technique for `dense_vector` fields. It compresses embeddings into compact binary form, enabling faster similarity search and reducing memory usage. This improves both search relevance and cost efficiency, especially when used with HNSW (Hierarchical Navigable Small World).

Learn more about how BBQ works, supported algorithms, and configuration examples in the [Better Binary Quantization (BBQ) documentation](https://www.elastic.co/docs/reference/elasticsearch/index-settings/bbq).
