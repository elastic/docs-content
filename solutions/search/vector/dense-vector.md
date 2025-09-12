---
applies_to:
  stack:
  serverless:
---
# Dense vector

Dense neural embeddings capture semantic meaning by translating content into fixed-length vectors of floating-point numbers. Similar content maps to nearby points in the vector space, making them ideal for:

- Finding semantically similar content
- Matching questions with answers
- Image similarity search
- Content-based recommendations

## Working with dense vectors in {{es}}

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

### General and vector optimized projects [vector-profiles]
```{applies_to}
serverless:
```

When you use the [API]({{cloud-serverless-apis}}operation/operation-createelasticsearchproject) to create an {{es-serverless}} project, you can choose between two profiles: `general_purpose` and `vector`.
The general purpose profile is recommended for most search use cases, including full text search, sparse vectors, and dense vectors that use compression such as BBQ.
The vector profile is recommended only when your use case is based on uncompressed dense vectors with high dimensionality.

For more information about how the profile affects virtual compute unit (VCU) allocation and costs, refer to [](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md).

## Better Binary Quantization (BBQ) [bbq]

Better Binary Quantization (BBQ) is a vector quantization method for `dense_vector` fields that compresses vectors for faster and more memory-efficient similarity search. BBQ can improve relevance and cost efficiency, especially when used with HNSW.

For details on how BBQ works, supported algorithms, and configuration examples, refer to [Better Binary Quantization (BBQ)](https://www.elastic.co/docs/reference/elasticsearch/index-settings/bbq)