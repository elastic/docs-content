---
navigation_title: Vector search
description: An introduction to semantic search in Elasticsearch.
applies_to:
  serverless: all
  stack: all
products:
  - id: elasticsearch
---
# Get started with vector search

In this quickstart, you’ll set up a search that combines keyword-based and vector search approaches to find results based on both exact terms and meaning. This is called hybrid search, and in many cases it provides better results than using either approach alone.

:::{dropdown} What are keyword-based search, vector search, and hybrid search?

Keyword-based search matches exact terms in your data, while vector search understands the intent behind a query.

For example, if a document contains the phrase "annual leave policy", a keyword search for "annual leave" will return it because the terms match. However, a search for "vacation rules" may not return the same document, because those exact words are not present.

With vector search, a query like "vacation rules" can still return the "annual leave policy" document, because it matches based on meaning rather than exact terms.

With hybrid search, the same query can return both keyword and semantic matches, combining exact term matching with meaning-based retrieval to improve overall relevance.

:::

First, you create an index and store your data in two forms: plain text and vector embeddings. Then you run a query that searches both representations and combines the results.

## Prerequisites [semantic-search-quickstart-prerequisites]

- A running {{es}} cluster. Refer to [Choosing your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) for an overview of how you can run {{es}}. For the fastest way to follow this quickstart, we recommend [creating a serverless project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md) (includes a free {{serverless-short}} trial), or using a [local development installation](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

## Get the data in [semantic-search-quickstart-getting-data-in]

:::::{stepper}
::::{step} Create an index mapping

Define the index mapping. The mapping specifies the fields in your index and their data types, including both plain text fields and fields used to store vector embeddings for semantic search.

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

1. The `semantic_text` field with the `semantic_text` field type to create and store vector embeddings. Under the hood, it uses an {{infer}} endpoint to generate the embeddings. If you don’t specify the `inference_id` parameter (as in the example above), the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.
2. The `content` field with the `text` field type to store plain text. This field is used for keyword search.
3. Values indexed into `content` are copied to `semantic_text` and processed by the default {{infer}} endpoint.

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

Index sample documents with the [bulk API]({{es-apis}}operation/operation-bulk). You only need to provide the content to the `content` field. The `copy_to` field populates `semantic_text` and triggers embedding generation.

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

Run a search using the [Search API]({{es-apis}}operation/operation-search).

The JSON body defines a hybrid query, where an RRF retriever combines two standard retrievers running [match queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) on `content` and `semantic_text` fields.

::::{note}
An [RRF retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/rrf-retriever.md) returns top documents based on the RRF formula, combining two or more child retrievers. This enables hybrid search by combining results from both keyword-based and semantic queries into a single ranked list.
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
2. The [match query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) is run against the `semantic_text` field, which stores vector embeddings for meaning-based search.

Documents that score well on either side appear in the final merged list.

:::{dropdown} Example response

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.032786883,
    "hits": [
      {
        "_index": "semantic-embeddings",
        "_id": "akiYKZ0BGwHk8ONXXqmi",
        "_score": 0.032786883,
        "_source": {
          "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness."
        }
      },
      {
        "_index": "semantic-embeddings",
        "_id": "a0iYKZ0BGwHk8ONXXqmi",
        "_score": 0.016129032,
        "_source": {
          "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions."
        }
      }
    ]
  }
}
```

:::


## Next steps

- [Semantic search](../semantic-search.md) - Learn how to compare semantic search workflows and choose one for your scenario (for example `semantic_text`, the {{infer}} API, or deploying models directly in {{es}}).
- [Vector search](../vector.md) - Learn more about dense and sparse vectors, embeddings, and similarity search.
- [Ranking and reranking](../ranking.md) - Learn more about multi-stage retrieval, rescoring, and reranking for better relevance.
- [Build your search queries](../querying-for-search.md) - Learn more about Query DSL, {{esql}}, retrievers, and the Search API.

