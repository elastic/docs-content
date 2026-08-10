---
navigation_title: Hybrid search with `semantic_text`
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text-hybrid-search.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
type: tutorial
description: Learn how to combine lexical and semantic search using a `text` field with `copy_to` into `content_embedding` (`semantic_text` type), from mapping through bulk ingest to hybrid queries.
---

# Hybrid search with `semantic_text` [semantic-text-hybrid-search]

This tutorial walks you through hybrid search using the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type together with a `text` field for lexical search. By the end, you will be able to:

- Create an index mapping that supports storing both text content and vector embeddings for hybrid search
- Ingest documents so the same text is embedded for semantic search and available for full-text search
- Run hybrid queries using [retrievers](retrievers-overview.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md)

In hybrid search, semantic retrieval scores by meaning while lexical search scores by textual similarity. Combining them often results in more robust rankings than either alone.

The recommended way to use hybrid search in the {{stack}} follows the `semantic_text` workflow: you avoid hand-building {{infer}} ingest pipelines for embeddings while still keeping a dedicated `text` field for keyword-style matching. 

## Requirements [semantic-text-requirements]

- In this tutorial, we show code examples for using both [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) and [{{ml}} nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#ml-node-role). EIS is automatically enabled on {{ech}} deployments and {{serverless-short}} projects. You can also use [EIS for self-managed clusters](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).

- To use the `semantic_text` field type with an {{infer}} service other than Elastic {{infer-cap}} Service, you must create an {{infer}} endpoint using the [Create {{infer}} API]({{es-apis}}operation/operation-inference-put).

:::{tip}
To run the `curl` examples in this tutorial, set the following environment variables:
```bash
export ELASTICSEARCH_URL="your-elasticsearch-url"
export API_KEY="your-api-key"
```
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md). [Learn more about finding your endpoint and credentials](/solutions/elasticsearch-solution-project/search-connection-details.md).
:::

## Step 1: Create the index mapping [hybrid-search-create-index-mapping]

The destination index will contain both the embeddings for semantic search and the original text field for full-text search. This structure enables the combination of semantic search and full-text search.

You can run {{infer}} either using the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) or on your own [{{ml}} nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#ml-node-role). 

:::{tip}
For large-scale dense vector deployments, quantization strategies like [BBQ](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md) can reduce memory usage. For details, refer to [Optimizing vector storage](vector/vector-storage-for-semantic-search.md).
:::

### Option 1: Use Elastic {{infer-cap}} Service (recommended)

In this example, you create an index for hybrid search using Elastic {{infer-cap}} Service. Embeddings are generated with the [default {{infer}} model](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) for the the `semantic_text` field type.

::::{tab-set}

:::{tab-item} Console

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "semantic_text" <2>
      },
      "content": { <3>
        "type": "text",
        "copy_to": "content_embedding" <4>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.
3. The name of the field to contain the original text for lexical search.
4. The textual data stored in the `content` field is copied to `content_embedding` and processed by the {{infer}} endpoint.

:::

:::{tab-item} curl

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content_embedding": { <1>
             "type": "semantic_text" <2>
           },
           "content": { <3>
             "type": "text",
             "copy_to": "content_embedding" <4>
           }
         }
       }
     }'
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.
3. The name of the field to contain the original text for lexical search.
4. The textual data stored in the `content` field is copied to `content_embedding` and processed by the {{infer}} endpoint.

:::

::::

:::{important}
For production environments, we recommend [explicitly specifying the `inference_id`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) for `semantic_text` fields. Default endpoints can change across versions and deployment types, which may lead to to [potential issues](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoint-considerations) like mixed embedding models and inconsistent ranking results.
:::

### Option 2: Use machine learning nodes

Below is an example of creating an index mapping using your own ML node with the `.elser-2-elasticsearch` {{infer}} endpoint.

::::{tab-set}

:::{tab-item} Console

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "semantic_text", <2>
        "inference_id": ".elser-2-elasticsearch" <3>
      },
      "content": { <4>
        "type": "text",
        "copy_to": "content_embedding" <5>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field.
3. The `.elser-2-elasticsearch` [preconfigured {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#preconfigured-endpoints) for the `elasticsearch` service is used. 
4. The name of the field to contain the original text for lexical search.
5. The textual data stored in the `content` field is copied to `content_embedding` and processed by the {{infer}} endpoint.

:::

:::{tab-item} curl

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content_embedding": { <1>
             "type": "semantic_text", <2>
             "inference_id": ".elser-2-elasticsearch" <3>
           },
           "content": { <4>
             "type": "text",
             "copy_to": "content_embedding" <5>
           }
         }
       }
     }'
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field.
3. The `.elser-2-elasticsearch` [preconfigured {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#preconfigured-endpoints) for the `elasticsearch` service is used. 
4. The name of the field to contain the original text for lexical search.
5. The textual data stored in the `content` field is copied to `content_embedding` and processed by the {{infer}} endpoint.

:::

::::

:::{dropdown} Example response
```console
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "semantic-embeddings"
}
```
:::

## Step 2: Ingest data [hybrid-semantic-text-ingest-data]

With your index mapping in place, you can add some data. You only need to populate the `content` field. {{es}} stores its value as `text` for lexical search, and `copy_to` duplicates that same value into the `content_embedding` field. Because `content_embedding` is of type `semantic_text`, {{es}} then sends the value to the {{infer}} endpoint and stores the resulting embeddings.

Use the [`_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) to ingest the same sample documents:

::::{tab-set}

:::{tab-item} Console

```console
POST _bulk
{ "index": { "_index": "semantic-embeddings", "_id": "1" } }
{ "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness." }
{ "index": { "_index": "semantic-embeddings", "_id": "2" } }
{ "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions." }
{ "index": { "_index": "semantic-embeddings", "_id": "3" } }
{ "content": "Tune cluster performance by monitoring thread pools and refresh interval." }
```

:::

:::{tab-item} curl

```bash
curl -X POST "${ELASTICSEARCH_URL}/_bulk" \
     -H "Content-Type: application/x-ndjson" \
     -H "Authorization: ApiKey ${API_KEY}" \
     --data-binary @- << 'EOF'
{ "index": { "_index": "semantic-embeddings", "_id": "1" } }
{ "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness." }
{ "index": { "_index": "semantic-embeddings", "_id": "2" } }
{ "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions." }
{ "index": { "_index": "semantic-embeddings", "_id": "3" } }
{ "content": "Tune cluster performance by monitoring thread pools and refresh interval." }
EOF
```

:::

::::

:::{dropdown} Example response

```console
{
  "errors": false, 
  "took": 400,
  "items": [
    {
      "index": {
        "_index": "semantic-embeddings",
        "_id": "1",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
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
        "_id": "2",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "semantic-embeddings",
        "_id": "3",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 2,
        "_primary_term": 1,
        "status": 201
      }
    }
  ]
}
```

Each document is indexed with `content` for search. The same text is copied to `content_embedding` and embedded through the configured {{infer}} endpoint.

:::

If you encounter errors, check that your index mapping and {{infer}} endpoint are configured correctly.

## Step 3: Run a hybrid search query [hybrid-search-perform-search]

Now that you have data in your index, you can run hybrid search to combine lexical matches on `content` with vector search over `content_embedding`. You can choose between [retrievers](retrievers-overview.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax.

Both the retriever and {{esql}} approaches return hits ranked by a score that fuses lexical matches on `content` with semantic matches on `content_embedding`. Passages that match on both signals rank highest, followed by those that match on only one.

:::{note}
For recommended ways to query and retrieve `semantic_text` data, refer to [Search and retrieve `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-search-retrieval.md).
:::

### Use retrievers

[Retrievers](retrievers-overview.md) provide a structured way to define and combine different search strategies, such as lexical and semantic search, within a single `_search` request.  This example uses the [RRF retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#rrf-retriever), which merges two [standard retrievers](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#standard-retriever): one runs a lexical `match` on `content`, the other a `match` on `content_embedding` for semantic retrieval.

::::{tab-set}

:::{tab-item} Console

```console
GET semantic-embeddings/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": { <1>
            "query": {
              "match": {
                "content": "How to avoid muscle soreness while running?" <2>
              }
            }
          }
        },
        {
          "standard": { <3>
            "query": {
              "match": {
                "content_embedding": "How to avoid muscle soreness while running?" <4>
              }
            }
          }
        }
      ]
    }
  }
}
```

1. The first `standard` retriever represents the traditional lexical search.
2. Lexical search is performed on the `content` field using the specified phrase.
3. The second `standard` retriever runs a `match` query on `content_embedding`, which performs semantic retrieval for that field type.
4. The same natural-language phrase is used as in the lexical branch. {{es}} scores `content_embedding` using semantic retrieval rather than term overlap alone.

:::

:::{tab-item} curl

```bash
curl -X GET "${ELASTICSEARCH_URL}/semantic-embeddings/_search" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "retriever": {
         "rrf": {
           "retrievers": [
             {
               "standard": {
                 "query": {
                   "match": {
                     "content": "How to avoid muscle soreness while running?"
                   }
                 }
               }
             },
             {
               "standard": {
                 "query": {
                  "match": {
                    "content_embedding": "How to avoid muscle soreness while running?"
                  }
                 }
               }
             }
           ]
         }
       }
     }'
```

:::

::::

:::{dropdown} Example response

```console
{
  "took": 176,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
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
      },
      {
        "_index": "semantic-embeddings",
        "_id": "bEiYKZ0BGwHk8ONXXqmi",
        "_score": 0.015873017,
        "_source": {
          "content": "Tune cluster performance by monitoring thread pools and refresh interval."
        }
      }
    ]
  }
}
```

The returned hits show fused `_score` rankings after RRF over lexical `content` and semantic `content_embedding` retrieval.

:::


### Use {{esql}}

[{{esql}}](/solutions/search/esql-for-search.md) is a piped query language which supports both lexical and semantic search. This enables combining keyword matching, vector search, scoring, and result processing in a single query.

::::{tab-set}

:::{tab-item} Console

```console
POST /_query?format=txt
{
  "query": """
    FROM semantic-embeddings METADATA _score <1>
    | WHERE content: "muscle soreness running?" OR match(content_embedding, "How to avoid muscle soreness while running?", { "boost": 0.75 }) <2>
    | KEEP content, content_embedding <3>
    | SORT _score DESC <4>
    | LIMIT 1000
  """
}
```

1. The `METADATA _score` clause returns the relevance score of each document.
2. The [match (`:`) operator](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) matches keywords on `content`. `match()` runs semantic retrieval on `content_embedding` with boost `0.75`.
3. `KEEP` selects `content` and `content_embedding` columns for the text-formatted response.
4. Sorts by descending score and limits to 1000 results.

:::

:::{tab-item} curl

```bash
curl -X POST "${ELASTICSEARCH_URL}/_query?format=txt" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "query": "FROM semantic-embeddings METADATA _score | WHERE content: \"muscle soreness running?\" OR match(content_embedding, \"How to avoid muscle soreness while running?\", { \"boost\": 0.75 }) | KEEP content, content_embedding | SORT _score DESC | LIMIT 1000"
     }'
```

:::

::::

::::{dropdown} Example response

```txt
                                                     content                                                     |                                                content_embedding                                                |      _score       
-----------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+-------------------
After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness.|After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness.|21.63957405090332  
Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions.|Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions.|8.419901847839355  
Tune cluster performance by monitoring thread pools and refresh interval.                                        |Tune cluster performance by monitoring thread pools and refresh interval.                                        |0.22893255949020386
```

Rows are sorted by `_score` descending after combining the `content` keyword match and boosted `content_embedding` match. 

::::

## Related pages

* For recommended ways to query and retrieve `semantic_text` data, refer to [Search and retrieve `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-search-retrieval.md).
* For a notebook-style walkthrough of `semantic_text` in hybrid search, see [this notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb).
* To set up semantic-only search on the same sample data model, follow the [Semantic search with `semantic_text`](semantic-search/semantic-search-semantic-text.md) tutorial.
* To learn how to optimize storage and search performance when using dense vector embeddings, refer to [Optimizing vector storage](vector/vector-storage-for-semantic-search.md).

