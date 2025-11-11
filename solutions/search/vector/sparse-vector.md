---
applies_to:
  stack:
  serverless:
---
# Sparse vector search in {{es}} [sparse-vector-search]

When working with sparse vectors in {{es}}, you'll use the [**Elastic Learned Sparse Encoder (ELSER)**](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) at index and query time to expand content into semantically related, weighted terms.

This approach preserves explainability while adding semantic understanding, with each document or query expanded into a set of weighted terms.

Sparse vector search with ELSER is ideal for:

- Enhanced keyword search with semantic expansion
- Use cases requiring explainable results
- Domain-specific search
- Large-scale deployments

## Working with sparse vectors in {{es}}

:::{tip}
Using the `semantic_text` field type provides automatic model management and sensible defaults. [Learn more](../semantic-search/semantic-search-semantic-text.md).
:::

Sparse vector search with ELSER expands both documents and queries into weighted terms. To use sparse vectors in {{es}}:

1. **Index documents with ELSER**
   - Deploy and configure the ELSER model
   - Use the `sparse_vector` field type
   - See [this overview](../semantic-search.md#using-nlp-models) for implementation options
2. **Query the index** using the [`sparse_vector` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-sparse-vector-query.md).