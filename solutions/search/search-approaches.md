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
# Search approaches

To deliver relevant search results, you need to choose the right search approach for your data and use case.

## Overview of search techniques

The following table provides an overview of the fundamental search techniques available in {{es}}:

| Name | Description | Use when |
|------|-------------|----------|
| [**Full-text search**](full-text.md) | Traditional lexical search with analyzers and relevance tuning | Exact words and phrases in the query should match the index. You want fast keyword matching without ML setup. |
| [**Semantic search**](semantic-search.md) | Search based on meaning and intent, not just keywords. A use case of vector search.| Queries use everyday language or synonyms instead of exact index terms. Get started with the managed [`semantic_text`](semantic-search/semantic-search-semantic-text.md) workflow. |
| [**Vector search**](vector.md) | Similarity search using vector embeddings stored in vector fields | You bring your own embeddings or need direct control over vector fields and models. |
| [**Hybrid search**](hybrid-search.md) | Combines full-text and vector search in one request | You need exact keyword matches and meaning based matches in one result set. |
| [**Ranking and reranking**](ranking.md) | Post-processing results to improve relevance | First stage retrieval is good enough but top results need finer ordering. |
| [**Geospatial search**](/explore-analyze/geospatial-analysis.md) | Location-based search and spatial relationships | Results depend on location, distance, or regions on a map. |

:::::{tip}
 Full-text search is a very powerful tool in itself. One of the key strengths of {{es}} is its flexibility, allowing you to start with full-text search and gradually incorporate more complex or resource-intensive approaches over time.
:::::

## Next step

Once you've chosen your search approach(es), you'll need to select a query language to implement them. Refer to [query languages for search use cases](querying-for-search.md) to learn about the available options.