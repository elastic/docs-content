---
navigation_title: Semantic search
description: Quickstart for semantic search in Elasticsearch with the semantic_text workflow, which uses vector search and embeddings to match documents by meaning.
applies_to:
  serverless: all
  stack: all
products:
  - id: elasticsearch
---
# Get started with semantic search

If you want to get a sense of how semantic search works in {{es}}, this quickstart is for you. You use the [`semantic_text`](../semantic-search/semantic-search-semantic-text.md) workflow, the simplest managed path for semantic search. First, you create an index and store your data in two forms: plain text for keyword matching and semantic representations in `semantic_text` (vector embeddings are generated and compared automatically using [vector search](../vector.md) under the hood). Then you run a hybrid query that combines keyword search with semantic search on those embeddings and merges the results.
:::{note}
This quickstart demonstrates [semantic search](../semantic-search.md) with the `semantic_text` field type and [hybrid search](../hybrid-search.md): it combines keyword-based full-text search with semantic search so you can match both exact terms and meaning. Semantic search relies on [vector search](../vector.md): text is converted to embeddings and matched by similarity in vector space.

For example, if a document contains the phrase "annual leave policy", a keyword search for "annual leave" will return it because the terms match. However, a search for "vacation rules" may not return the same document, because those exact words are not present.

With semantic search and [vector search](../vector.md), a query like "vacation rules" can still return the "annual leave policy" document, because it matches based on meaning rather than exact terms.

With hybrid search, the same query can return both keyword and semantic matches, combining exact words with vector search by meaning so results stay useful.
:::

## Prerequisites [semantic-search-quickstart-prerequisites]

A running {{es}} cluster. For the fastest way to follow this quickstart, [create a serverless project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md) which includes a free {{serverless-short}} trial.

## Get the data in [semantic-search-quickstart-getting-data-in]

:::::{stepper}
::::{step} Create an index mapping

Define the [index mapping](/manage-data/data-store/mapping.md). The mapping specifies the fields in your index and their data types, including a plain text field for full-text search and a `semantic_text` field that powers semantic search through vector embeddings and [vector search](../vector.md).

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "semantic_text": { <1>
        "type": "semantic_text"
      },
      "content": { <2>
        "type": "text",
        "copy_to": "semantic_text" <3>
      }
    }
  }
}
```

1. The `semantic_text` field with the `semantic_text` field type for semantic search. Vector embeddings are generated and stored automatically using the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) and [vector search](../vector.md) under the hood.
2. The `content` field with the `text` field type to store plain text. This field is used for keyword search.
3. Values indexed into `content` are copied to `semantic_text`, converted to vector embeddings, and stored for vector search by the default {{infer}} endpoint.

:::{dropdown} Example response

```console-result
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "semantic-embeddings"
}
```

:::

::::
::::{step} Index documents

Index documents with the [bulk API]({{es-apis}}operation/operation-bulk). You only need to provide the content to the `content` field. The `copy_to` mapping copies the text into `semantic_text` and generates vector embeddings automatically, so you can run keyword search on `content` and semantic search on `semantic_text` for the same document.

```console
POST _bulk
{ "index": { "_index": "semantic-embeddings" } }
{ "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness." }
{ "index": { "_index": "semantic-embeddings" } }
{ "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions." }
{ "index": { "_index": "semantic-embeddings" } }
{ "content": "Tune cluster performance by monitoring thread pools and refresh interval." }
```

:::{dropdown} Example response

```console-result
{
  "errors": false,
  "took": 600,
  "items": [
    {
      "index": {
        "_index": "semantic-embeddings",
        "_id": "akiYKZ0BGwHk8ONXXqmi",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 0,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "semantic-embeddings",
        "_id": "a0iYKZ0BGwHk8ONXXqmi",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 0,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "semantic-embeddings",
        "_id": "bEiYKZ0BGwHk8ONXXqmi",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 1,
        "status": 201
      }
    }
  ]
}
```

:::

::::
:::::

## Search the data [search-data]

Run a hybrid search using the [Search API]({{es-apis}}operation/operation-search).

The JSON body is a hybrid query: a [reciprocal rank fusion (RRF) retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/rrf-retriever.md) runs two [match queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md), one on `content` for keyword matching and one on `semantic_text` for semantic search, which uses [vector search](../vector.md) under the hood, and merges the results.

::::{note}
An [RRF retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/rrf-retriever.md) returns top documents based on the RRF formula. This enables hybrid search by combining results from keyword-based full-text queries and semantic search (through [vector search](../vector.md)) into a single ranked list.
::::

```console
GET semantic-embeddings/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": { 
            "query": {
              "match": {
                "content": "muscle soreness after jogging" <1>
              }
            }
          }
        },
        {
          "standard": { 
            "query": {
              "match": {
                "semantic_text": "muscle soreness after jogging" <2>
              }
            }
          }
        }
      ]
    }
  }
}
```

1. The [match query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) is run against the `content` field, which stores plain text for keyword matching.
2. The [match query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) is run against the `semantic_text` field for semantic search using [vector search](../vector.md) (query and document vectors are stored and compared automatically).

If a document ranks well in either query, it can appear in the combined list.

:::{dropdown} Example response

In the example response below, the two hits show why combining keyword search and semantic search in a hybrid query matters.

The top document contains the phrase _muscle soreness_ and _running_, so it fits both keyword search and ranks highly in semantic and vector search. The second document does not use those words at all; it talks about marathon training and recovery between sessions. A keyword-only search on `content` would likely miss or rank that document much lower, because the query terms are not in the text.

Semantic search still matches it because marathon training and recovery relate to the same idea as soreness after a run - vector similarity captures the connection even without shared keywords. Hybrid search keeps the document that matches the words and also brings in documents that vector search surfaces by topic, even without the same vocabulary.

Each `_score` is a relevance score for this search only. A higher score means that document ranked higher than the ones below it in the same response.

```console-result
{
  "took": 202,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2, <1>
      "relation": "eq"
    },
    "max_score": 0.032786883, <2>
    "hits": [
      {
        "_index": "semantic-embeddings",
        "_id": "akiYKZ0BGwHk8ONXXqmi",
        "_score": 0.032786883, <3>
        "_source": {
          "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness."
        }
      },
      {
        "_index": "semantic-embeddings",
        "_id": "a0iYKZ0BGwHk8ONXXqmi",
        "_score": 0.016129032, <4>
        "_source": {
          "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions."
        }
      }
    ]
  }
}
```

1. How many documents matched the query (here, 2). The unrelated cluster-tuning document is not returned.
2. The highest relevance score among the returned hits (the same as the top-ranked document’s score).
3. Relevance score for the top-ranked document. Its text matches query terms like muscle soreness and post-run recovery (running is close to jogging), so both keyword search and semantic search (powered by vector similarity) can rank it highly.
4. Relevance score for the second-ranked document. It does not contain _muscle soreness_ or _jogging_; it shows up mainly because [vector search](../vector.md) matches marathon training and recovery to the query. Keyword-only search on `content` would often miss this kind of match.

:::

## Next steps

### End-to-end tutorials

- [Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md) - Follow a full tutorial on how to set up semantic search and vector search with the `semantic_text` field type.
- [Semantic search with the {{infer}} API](../semantic-search/semantic-search-inference.md) - Use the {{infer}} API with third-party embedding services (for example Cohere, Hugging Face, or OpenAI) to run semantic search with vector embeddings.
- [Hybrid search with `semantic_text`](../hybrid-semantic-text.md) - Combine semantic search on `semantic_text` with full-text search on a text field, then merge results using RRF. Vector embeddings are generated and compared automatically.
- [Semantic search with ELSER](../semantic-search/semantic-search-elser-ingest-pipelines.md) - Use the ELSER model for sparse vector search and semantic retrieval.
- [Dense and sparse vector ingest pipelines](../vector/dense-versus-sparse-ingest-pipelines.md) - Implement vector search end to end with NLP models deployed in {{es}}: pick dense or sparse, deploy the model, build ingest pipelines, and query—without relying on `semantic_text`.

### Concepts and reference

- [Semantic search](../semantic-search.md) - Compare the three workflows (`semantic_text`, {{infer}} API, or models deployed in-cluster) for meaning-based search and see how they differ in complexity.
- [Vector search](../vector.md) - Work directly with `dense_vector` and `sparse_vector` fields, related queries, and manual vector implementations when you need control beyond managed semantic workflows.
- [Ranking and reranking](../ranking.md) - Structure multi-stage pipelines: initial BM25, vector, or hybrid retrieval, then reranking with stronger models on smaller candidate sets.
- [Build your search queries](../querying-for-search.md) - Choose Query DSL, {{esql}}, or retrievers on the Search API depending on whether you need classic queries, analytics-style pipes, or composable retrieval pipelines.

To learn about more options, such as full-text, vector, and hybrid search, go to [Search approaches](/solutions/search/search-approaches.md).
For a summary of vector search use cases, go to [Vector search use cases](/solutions/search/vector/vector-search-use-cases.md).
