---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/retrievers-overview.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Retrievers [retrievers-overview]

A retriever is an abstraction that was added to the `_search` API in **8.14.0** and was made generally available in **8.16.0**.

This syntax enables the configuration of multi-stage retrieval pipelines within a single `_search` call. This simplifies your search application logic, because you no longer need to configure complex searches via multiple {{es}} calls or implement additional client-side logic to combine results from different queries.

::::{note}
This document provides a general overview of the retriever abstraction. For a full syntax reference and implementation overview, check out the [reference documentation](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md).
::::

## Retriever types [retrievers-overview-types]

% KEEP IN SYNC with https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/rest-apis/retrievers.md

Retrievers come in various types, each tailored for different search operations. The following retrievers are currently available:

* [**kNN retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#knn-retriever). Returns top documents from a [knn search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#search-api-knn), in the context of a retriever framework.
* [**Linear retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#linear-retriever). Combines the top results from multiple sub-retrievers using a weighted sum of their scores.
* [**Pinned retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#pinned-retriever). Always places specified documents at the top of the results, with the remaining hits provided by a secondary retriever.
* [**Rescorer retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#rescorer-retriever). Re-scores the results produced by its child retriever.
* [**RRF retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#rrf-retriever). Compound retriever which combines and ranks multiple first-stage retrievers using the reciprocal rank fusion (RRF) algorithm. 
* [**Rule retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#rule-retriever). Applies [query rules](elasticsearch://reference/elasticsearch/rest-apis/searching-with-query-rules.md#query-rules) to the query before returning results.
* [**Standard retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#standard-retriever). Returns top documents from a traditional [query](/explore-analyze/query-filter/languages/querydsl.md).
* [**Text Similarity Re-ranker retriever**](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#text-similarity-reranker-retriever). Used for semantic reranking.

## What makes retrievers useful? [retrievers-overview-why-are-they-useful]

Here’s an overview of what makes retrievers useful and how they differ from regular queries.

1. **Simplified user experience**. Retrievers simplify the user experience by allowing entire retrieval pipelines to be configured in a single API call. This maintains backward compatibility with traditional query elements by automatically translating them to the appropriate retriever.
2. **Structured retrieval**. Retrievers provide a more structured way to define search operations. They allow searches to be described using a "retriever tree", a hierarchical structure that clarifies the sequence and logic of operations, making complex searches more understandable and manageable.
3. **Composability and flexibility**. Retrievers enable flexible composability, allowing you to build pipelines and seamlessly integrate different retrieval strategies into these pipelines. Retrievers make it easy to test out different retrieval strategy combinations.
4. **Compound operations**. A retriever can have sub retrievers. This allows complex nested searches where the results of one retriever feed into another, supporting sophisticated querying strategies that might involve multiple stages or criteria.
5. **Retrieval as a first-class concept**. Unlike traditional queries, where the query is a part of a larger search API call, retrievers are designed as standalone entities that can be combined or used in isolation. This enables a more modular and flexible approach to constructing searches.
6. **Enhanced control over document scoring and ranking**. Retrievers allow for more explicit control over how documents are scored and filtered. For instance, you can specify minimum score thresholds, apply complex filters without affecting scoring, and use parameters like `terminate_after` for performance optimizations.
7. **Integration with existing {{es}} functionalities**. Even though retrievers can be used instead of existing `_search` API syntax (like the `query` and `knn`), they are designed to integrate seamlessly with things like pagination (`search_after`) and sorting. They also maintain compatibility with aggregation operations by treating the combination of all leaf retrievers as `should` clauses in a boolean query.
8. **Cleaner separation of concerns**. When using compound retrievers, only the query element is allowed, which enforces a cleaner separation of concerns and prevents the complexity that might arise from overly nested or interdependent configurations.


## Example [retrievers-overview-example]

The following example demonstrates how using retrievers simplify the composability of queries for RRF ranking.

```js
GET example-index/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "sparse_vector": {
                "field": "vector.tokens",
                "inference_id": "my-elser-endpoint",
                "query": "What blue shoes are on sale?"
              }
            }
          }
        },
        {
          "standard": {
            "query": {
              "match": {
                "text": "blue shoes sale"
              }
            }
          }
        }
      ]
    }
  }
}
```

This example demonstrates how you can combine different retrieval strategies into a single `retriever` pipeline.

Compare to `RRF` with `sub_searches` approach (which is deprecated as of 8.16.0):

::::{dropdown} Expand for example
```js
GET example-index/_search
{
  "sub_searches":[
    {
      "query":{
        "match":{
          "text":"blue shoes sale"
        }
      }
    },
    {
      "query":{
        "sparse_vector": {
            "field": "vector.tokens",
            "inference_id": "my-elser-endoint",
            "query": "What blue shoes are on sale?"
          }
        }
      }
  ],
  "rank":{
    "rrf":{
      "rank_window_size":50,
      "rank_constant":20
    }
  }
}
```
::::

For more examples, refer to [retriever examples](elasticsearch://reference/elasticsearch/rest-apis/retrievers/retrievers-examples.md).

## Glossary [retrievers-overview-glossary]

Here are some important terms:

* **Retrieval Pipeline**. Defines the entire retrieval and ranking logic to produce top hits.
* **Retriever Tree**. A hierarchical structure that defines how retrievers interact.
* **First-stage Retriever**. Returns an initial set of candidate documents.
* **Compound Retriever**. Builds on one or more retrievers, enhancing document retrieval and ranking logic.
* **Combiners**. Compound retrievers that merge top hits from multiple sub-retrievers.
* **Rerankers**. Special compound retrievers that reorder hits and may adjust the number of hits, with distinctions between first-stage and second-stage rerankers.


## Retrievers in action [retrievers-overview-play-in-search]

The Search Playground builds Elasticsearch queries using the retriever abstraction. It automatically detects the fields and types in your index and builds a retriever tree based on your selections.

You can use the Playground to experiment with different retriever configurations and see how they affect search results.

Refer to the [Playground documentation](/solutions/elasticsearch-solution-project/playground.md) for more information.


## Reference docs and examples [retrievers-overview-api-reference]

For implementation details, including notable restrictions, refer to the [reference documentation](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md).

For additional examples, refer to [Retrievers examples](elasticsearch://reference/elasticsearch/rest-apis/retrievers/retrievers-examples.md).


