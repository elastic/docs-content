---
applies_to:
  stack:
  serverless:
---
# Search approaches

To deliver relevant search results, you need to choose the right search approach for your data and use case.

## Overview of search techniques

The following table provides an overview of the fundamental search techniques available in {{es}}:

| Name | Description | Notes |
|------|-------------|--------|
| [**Full-text search**](full-text.md) | Traditional lexical search with analyzers and relevance tuning | Essential foundation for keyword matching, works out of the box |
| [**AI-powered search**](ai-search/ai-search.md) | Machine learning-based search using natural language understanding | Includes [vector search](vector.md) and [semantic search](semantic-search.md) approaches |
| [**Hybrid search**](hybrid-search.md) | Combines lexical and vector/semantic approaches | Best balance for both keyword precision and semantic relevance |
| [**Ranking and reranking**](ranking.md) | Post-processing results to improve relevance | Optional ML-based enhancement for fine-tuned relevance |
| [**Geospatial search**](/explore-analyze/geospatial-analysis.md) | Location-based search and spatial relationships | For maps, distance calculations, and shape queries |

:::::{tip}
 Full-text search is a very powerful tool in itself. One of the key strengths of {{es}} is its flexibility, allowing you to start with full-text search and gradually incorporate more complex or resource-intensive approaches over time.
:::::

## Next step

Once you've chosen your search approach(es), you'll need to select a query language to implement them. Refer to [query languages for search use cases](querying-for-search.md) to learn about the available options.