---
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
# Hybrid search

Hybrid search combines [full-text search](full-text.md) (lexical, keyword-based matching) with [semantic search](semantic-search.md) (meaning-based matching) for more powerful search experiences that serve a wider range of user needs. Semantic search uses [vector search](vector.md) under the hood, but you typically implement hybrid search through managed workflows such as `semantic_text` rather than by configuring vector fields directly.

The recommended way to use hybrid search in the {{stack}} is the [`semantic_text` workflow](semantic-search/semantic-search-semantic-text.md). Check out the [hands-on tutorial](hybrid-semantic-text.md) for a step-by-step guide.

We recommend implementing hybrid search with the [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) algorithm. This approach merges rankings from lexical (full-text) and semantic queries, giving more weight to results that rank high in either branch. This ensures that the final results are balanced and relevant.