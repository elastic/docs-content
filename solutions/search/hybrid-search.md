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

Hybrid search runs [full-text search](full-text.md) and [vector search](vector.md) in one request. For the vector part, you can use managed [semantic search](semantic-search.md) workflows or set up vector fields yourself. Either way, you return one ranked list that combines keyword matching with similarity search.

The recommended way to use hybrid search in the {{stack}} is the [`semantic_text` workflow](semantic-search/semantic-search-semantic-text.md). Check out the [hands-on tutorial](hybrid-semantic-text.md) for a step-by-step guide.

We recommend implementing hybrid search with the [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) algorithm. This approach merges rankings from the full-text and vector queries, giving more weight to documents that score well in either one. The final list balances exact keyword matches with similarity-based matches.