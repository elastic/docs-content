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
description: Learn how to combine lexical and semantic search using a `text` field with `copy_to` into `semantic_text`, from mapping through bulk ingest to hybrid queries.
---

# Hybrid search with `semantic_text` [semantic-text-hybrid-search]

This tutorial walks you through hybrid search using the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type together with a `text` field for lexical search. By the end, you will be able to:

- Create an index mapping with `semantic_text` and a `text` field linked by `copy_to`
- Ingest documents so the same text is embedded for semantic search and available for full-text search
- Run hybrid queries using [retrievers](retrievers-overview.md)

In hybrid search, semantic retrieval scores by meaning while lexical search scores by term overlap. Combining them often results in more robust rankings than either alone.

The recommended way to use hybrid search in the {{stack}} follows the `semantic_text` workflow: you avoid hand-building {{infer}} ingest pipelines for embeddings while still keeping a dedicated `text` field for keyword-style matching. 

## Requirements [semantic-text-requirements]

- This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), which is automatically enabled on {{ech}} deployments and {{serverless-short}} projects.
::::{note}
You can also use [EIS for self-managed clusters](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).
::::
- To use the `semantic_text` field type with an {{infer}} service other than Elastic {{infer-cap}} Service, you must create an {{infer}} endpoint using the [Create {{infer}} API]({{es-apis}}operation/operation-inference-put).

:::{tip}
To run the `curl` examples in this tutorial, set the following environment variables:
```bash
export ELASTICSEARCH_URL="your-elasticsearch-url"
export API_KEY="your-api-key"
```
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md). [Learn more about finding your endpoint and credentials](/solutions/elasticsearch-solution-project/search-connection-details.md).
:::

## Create the index mapping [hybrid-search-create-index-mapping]

::::{note}
If you want to run a search on indices that were populated by web crawlers or connectors, you have to [update the index mappings]({{es-apis}}operation/operation-indices-put-mapping) for these indices to include the `semantic_text` field. Once the mapping is updated, you’ll need to run a full web crawl or a full connector sync. This ensures that all existing documents are reprocessed and updated with the new semantic embeddings, enabling hybrid search on the updated data.
::::

The destination index will contain both the embeddings for semantic search and the original text field for full-text search. This structure enables the combination of semantic search and full-text search.

For large-scale deployments using dense vector embeddings, you can significantly reduce memory usage by configuring quantization strategies like [BBQ](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md). For advanced configuration, refer to [Optimizing vector storage](vector/vector-storage-for-semantic-search.md).

You can run {{infer}} either using the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) or on your own ML-nodes. 

### Using EIS

::::{tab-set}

:::{tab-item} Console

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "semantic_text": { <1>
        "type": "semantic_text" <2>
      },
      "content": { <3>
        "type": "text",
        "copy_to": "semantic_text" <4>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.
3. The name of the field to contain the original text for lexical search.
4. The textual data stored in the `content` field will be copied to `semantic_text` and processed by the {{infer}} endpoint.

:::

:::{tab-item} curl

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "semantic_text": { <1>
             "type": "semantic_text" <2>
           },
           "content": { <3>
             "type": "text",
             "copy_to": "semantic_text" <4>
           }
         }
       }
     }'
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.
3. The name of the field to contain the original text for lexical search.
4. The textual data stored in the `content` field will be copied to `semantic_text` and processed by the {{infer}} endpoint.

:::

::::

### Using ML-nodes

::::{tab-set}

:::{tab-item} Console

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "semantic_text": { <1>
        "type": "semantic_text", <2>
        "inference_id": ".elser-2-elasticsearch" <3>
      },
      "content": { <4>
        "type": "text",
        "copy_to": "semantic_text" <5>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field.
3. The `.elser-2-elasticsearch` preconfigured {{infer}} endpoint for the `elasticsearch` service is used. To use a different {{infer}} service, you must create an {{infer}} endpoint first using the [Create {{infer}} API]({{es-apis}}operation/operation-inference-put) and then specify it in the `semantic_text` field mapping using the `inference_id` parameter.
4. The name of the field to contain the original text for lexical search.
5. The textual data stored in the `content` field will be copied to `semantic_text` and processed by the {{infer}} endpoint.

:::

:::{tab-item} curl

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "semantic_text": { <1>
             "type": "semantic_text", <2>
             "inference_id": ".elser-2-elasticsearch" <3>
           },
           "content": { <4>
             "type": "text",
             "copy_to": "semantic_text" <5>
           }
         }
       }
     }'
```

1. The name of the field to contain the generated embeddings for semantic search.
2. The field to contain the embeddings is a `semantic_text` field.
3. The `.elser-2-elasticsearch` preconfigured {{infer}} endpoint for the `elasticsearch` service is used. To use a different {{infer}} service, you must create an {{infer}} endpoint first using the [Create {{infer}} API]({{es-apis}}operation/operation-inference-put) and then specify it in the `semantic_text` field mapping using the `inference_id` parameter.
4. The name of the field to contain the original text for lexical search.
5. The textual data stored in the `content` field will be copied to `semantic_text` and processed by the {{infer}} endpoint.

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

:::{note}
Relying on the default {{infer}} endpoint is convenient for getting started, but for production environments we recommend explicitly specifying the `inference_id`. The default endpoint can change across versions and deployment types, which can lead to indices with mixed embedding models and cause ranking issues in multi-index searches. For details, refer to [Potential issues when mixing embedding models across indices](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoint-considerations).
:::


## Ingest data [hybrid-semantic-text-ingest-data]

With your index mapping in place, you can add some data. You only need to populate the `content` field: {{es}} stores it as `text` for lexical search and, because of `copy_to`, copies the same string into `semantic_text`, which sends the text to the configured {{infer}} endpoint and stores embeddings on the document.

Use the [`_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) to ingest the same sample documents as in [Semantic search with `semantic_text`](semantic-search/semantic-search-semantic-text.md):

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

1. `false` indicates all indexing operations completed without errors.
2. Each document was created with `content` indexed for search; the same text was copied to `semantic_text` and embedded via the configured {{infer}} endpoint.

:::

If you encounter errors, check that your index mapping and {{infer}} endpoint are configured correctly.

## Run a hybrid search query [hybrid-search-perform-search]

With data ingested into `semantic-embeddings`, you can run hybrid search that combines lexical matches on `content` with semantic retrieval on `semantic_text`. Choose between [retrievers](retrievers-overview.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax.

For an overview of all query types supported by `semantic_text` fields and guidance on when to use them, refer to [Querying `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#querying-semantic-text-fields).

### Retrievers

#### Using EIS

::::{tab-set}

:::{tab-item} Query DSL

This example uses [retrievers syntax](retrievers-overview.md) with [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md). RRF is a technique that merges the rankings from both semantic and lexical queries, giving more weight to results that rank high in either search. This ensures that the final results are balanced and relevant.

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
              "semantic": {
                "field": "semantic_text", <4>
                "query": "How to avoid muscle soreness while running?"
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
3. The second `standard` retriever refers to the semantic search.
4. The `semantic_text` field is used to perform the semantic search.

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
                   "semantic": {
                     "field": "semantic_text",
                     "query": "How to avoid muscle soreness while running?"
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

#### Using ML-nodes

::::{tab-set}

:::{tab-item} Query DSL

This example uses [retrievers syntax](retrievers-overview.md) with [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md). RRF is a technique that merges the rankings from both semantic and lexical queries, giving more weight to results that rank high in either search. This ensures that the final results are balanced and relevant.

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
              "semantic": {
                "field": "semantic_text", <4>
                "query": "How to avoid muscle soreness while running?"
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
3. The second `standard` retriever refers to the semantic search.
4. The `semantic_text` field is used to perform the semantic search.

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
                   "semantic": {
                     "field": "semantic_text",
                     "query": "How to avoid muscle soreness while running?"
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

### {{esql}}

::::{tab-set}

:::{tab-item} Console

```console
POST /_query?format=txt
{
  "query": """
    FROM semantic-embeddings METADATA _score <1>
    | WHERE content: "muscle soreness running?" OR match(semantic_text, "How to avoid muscle soreness while running?", { "boost": 0.75 }) <2> <3>
    | SORT _score DESC <4>
    | LIMIT 1000
  """
}
```

1. The `METADATA _score` clause returns the relevance score of each document.
2. The [match (`:`) operator](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) performs keyword matching on the `content` field.
3. The `match()` function runs semantic search on the `semantic_text` field with a boost of `0.75`.
4. Sorts by descending score and limits to 1000 results.

:::

:::{tab-item} curl

```bash
curl -X POST "${ELASTICSEARCH_URL}/_query?format=txt" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "query": "FROM semantic-embeddings METADATA _score | WHERE content: \"muscle soreness running?\" OR match(semantic_text, \"How to avoid muscle soreness while running?\", { \"boost\": 0.75 }) | SORT _score DESC | LIMIT 1000"
     }'
```

:::

::::

Both the retriever and ES|QL approaches return hits ranked by a fused relevance score: lexical matches on `content` and semantic matches on `semantic_text` both contribute, so passages that align with the query in either sense tend to appear higher.

::::{dropdown} Example Query DSL response

```console
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "semantic-embeddings",
        "_id": "1",
        "_score": 0.032786883,
        "_rank": 1,
        "_source": {
          "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness."
        }
      },
      {
        "_index": "semantic-embeddings",
        "_id": "2",
        "_score": 0.027912449,
        "_rank": 2,
        "_source": {
          "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions."
        }
      },
      {
        "_index": "semantic-embeddings",
        "_id": "3",
        "_score": 0.016393441,
        "_rank": 3,
        "_source": {
          "content": "Tune cluster performance by monitoring thread pools and refresh interval."
        }
      }
    ]
  }
}
```

1. Hits are merged and ranked after RRF; `_rank` reflects the fused ordering. Scores and ranks are illustrative.
2. `_source` shows the indexed `content`. Embeddings are stored on `semantic_text` and are typically omitted from search hits by default.

::::

::::{dropdown} Example ES|QL response

```txt
                                                     content                                                     |      _score
-----------------------------------------------------------------------------------------------------------------+------------------
After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness.|      26.408897
Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions.|      11.229613
Tune cluster performance by monitoring thread pools and refresh interval.                                        |       0.304480
```

1. Rows are sorted by `_score` descending after combining the `content` keyword match and boosted `semantic_text` match. Values are illustrative.

::::

## Related pages

* For an overview of all query types supported by `semantic_text` fields and guidance on when to use them, refer to [Querying `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#querying-semantic-text-fields).
* For a notebook-style walkthrough of `semantic_text` in hybrid search, see [this notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb).
* To set up semantic-only search on the same sample data model, follow the [Semantic search with `semantic_text`](semantic-search/semantic-search-semantic-text.md) tutorial.
* To learn how to optimize storage and search performance when using dense vector embeddings, refer to [Optimizing vector storage](vector/vector-storage-for-semantic-search.md).

