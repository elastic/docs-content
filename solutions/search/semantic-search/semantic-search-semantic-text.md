---
navigation_title: Semantic search with `semantic_text`
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-search-semantic-text.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
type: tutorial
description: Learn how to set up semantic search using the semantic_text field type, from creating an index mapping to ingesting data and running queries.
---

# Semantic search with `semantic_text` [semantic-search-semantic-text]

This tutorial walks you through setting up semantic search using the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type. By the end, you will be able to:

- Create an index mapping with a `semantic_text` field
- Ingest documents that are automatically converted to vector embeddings
- Query your data using semantic search with both Query DSL and {{esql}}

The `semantic_text` field type simplifies the {{infer}} workflow by providing {{infer}} at ingestion time with sensible defaults. You don’t need to define model-related settings and parameters, or create {{infer}} ingest pipelines.

We recommend using the `semantic_text` workflow for [semantic search](../semantic-search.md) in the {{stack}}. When you need more control over indexing and query settings, you can use the complete {{infer}} workflow instead (refer to [Semantic search with the Inference API](semantic-search-inference.md) for details).

This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), but you can use any service and model supported by the [{{infer-cap}} API](/explore-analyze/elastic-inference/inference-api.md).

## Requirements [semantic-text-requirements]

- This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), which is automatically enabled on {{ech}} deployments and {{serverless-short}} projects.
::::{note}
You can also use [EIS for self-managed clusters](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).
::::
- To use the `semantic_text` field type with an {{infer}} service other than Elastic {{infer-cap}} Service, you must create an inference endpoint using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

:::{tip}
To run the `curl` examples in this tutorial, set the following environment variables:
```bash
export ELASTICSEARCH_URL="your-elasticsearch-url"
export API_KEY="your-api-key"
```
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md). [Learn more about finding your endpoint and credentials](/solutions/elasticsearch-solution-project/search-connection-details.md).
:::

## Create the index mapping [semantic-text-index-mapping]

Create a destination index with a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. This field stores the vector embeddings that the inference endpoint generates from your input text.

You can run {{infer}} either using the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) or on your own ML-nodes. The following examples show you both scenarios.

:::::::{tab-set}

::::::{tab-item} Using EIS

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "content": { <1>
        "type": "semantic_text" <2>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings.
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.

::::::

::::::{tab-item} Using ML-nodes

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "content": { <1>
        "type": "semantic_text", <2>
        "inference_id": ".elser-2-elasticsearch" <3>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings.
2. The field to contain the embeddings is a `semantic_text` field.
3. The `.elser-2-elasticsearch` preconfigured {{infer}} endpoint for the `elasticsearch` service is used. To use a different {{infer}} service, you must create an {{infer}} endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put) and then specify it in the `semantic_text` field mapping using the `inference_id` parameter.

::::::

::::::{tab-item} Using curl (EIS)

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content": { <1>
             "type": "semantic_text" <2>
           }
         }
       }
     }'
```

1. The name of the field to contain the generated embeddings.
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) is used.

::::::

:::::::

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

:::{note}
For large-scale deployments using dense vector embeddings, you can significantly reduce memory usage by configuring quantization strategies like [BBQ](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md). For advanced configuration, refer to [Optimizing vector storage](../vector/vector-storage-for-semantic-search.md).
:::


::::{note}
If you're using web crawlers or connectors to generate indices, you have to [update the index mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) for these indices to include the `semantic_text` field. Once the mapping is updated, you'll need to run a full web crawl or a full connector sync. This ensures that all existing documents are reprocessed and updated with the new semantic embeddings, enabling semantic search on the updated data.
::::

## Ingest data [semantic-text-load-data]

With your index mapping in place, you can add some data. When you index a document, {{es}} automatically sends the `semantic_text` field's contents to the configured {{infer}} endpoint, generates vector embeddings, and stores them in the document.

Use the [`_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) to ingest a few sample documents:

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
2. Each document was successfully created. The `semantic_text` field contents are automatically sent to the configured {{infer}} endpoint for embedding generation.

:::

If you see errors, check that your index mapping and inference endpoint are configured correctly.

## Run a semantic search query [semantic-text-semantic-search]

With your data ingested and automatically embedded, you can query it using semantic search. You can use [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax.

::::::{tab-set}
:group: query-type

:::::{tab-item} Query DSL
:sync: dsl

The Query DSL approach uses the [`match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) type with the `semantic_text` field:

```console
GET semantic-embeddings/_search
{
  "query": {
    "match": {
      "content": { <1>
        "query": "What causes muscle soreness after running?" <2>
      }
    }
  }
}
```

1. The `semantic_text` field on which you want to perform the search.
2. The query text.

:::::

:::::{tab-item} ES|QL
:sync: esql

The ES|QL approach uses the [match (`:`) operator](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator), which automatically detects the `semantic_text` field and performs the search on it. The query uses `METADATA _score` to sort by `_score` in descending order.

```console
POST /_query?format=txt
{
  "query": """
    FROM semantic-embeddings METADATA _score <1>
    | WHERE content: "How to avoid muscle soreness while running?" <2>
    | SORT _score DESC <3>
    | LIMIT 1000 <4>
  """
}
```

1. The `METADATA _score` clause returns the relevance score of each document.
2. The [match (`:`) operator](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) detects the `semantic_text` field and performs semantic search on `content`.
3. Sorts by descending score to display the most relevant results first.
4. Limits the results to 1000 documents.

:::::

:::::{tab-item} Query DSL (curl)

```bash
curl -X GET "${ELASTICSEARCH_URL}/semantic-embeddings/_search" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "query": {
         "match": {
           "content": {
             "query": "What causes muscle soreness after running?"
           }
         }
       }
     }'
```

:::::

:::::{tab-item} ES|QL (curl)

```bash
curl -X POST "${ELASTICSEARCH_URL}/_query?format=txt" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "query": "FROM semantic-embeddings METADATA _score | WHERE content: \"How to avoid muscle soreness while running?\" | SORT _score DESC | LIMIT 1000"
     }'
```

:::::

::::::

Both queries return the documents ranked by semantic relevance. The documents about running and muscle soreness score highest because they are semantically closest to the query, while the document about cluster performance scores lower.

::::{dropdown} Example Query DSL response

```console
{
  "took": 87,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 21.098728,
    "hits": [
      {
        "_index": "semantic-embeddings2",
        "_id": "1",
        "_score": 21.098728,
        "_source": {
          "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness."
        }
      },
      {
        "_index": "semantic-embeddings2",
        "_id": "2",
        "_score": 8.030467,
        "_source": {
          "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions."
        }
      }
    ]
  }
}
```

1. Documents are ranked by `_score`. Higher scores indicate stronger semantic relevance to the query.
2. The `_source` contains the original document text. Embeddings are stored internally and excluded from the response by default.

::::

::::{dropdown} Example ES|QL response

```txt
                                                     content                                                     |      _score
-----------------------------------------------------------------------------------------------------------------+------------------
After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness.|26.408897399902344
Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions.|11.229613304138184
Tune cluster performance by monitoring thread pools and refresh interval.                                        |0.3044795095920563                                            |  1.235689
```

::::

## Related pages[semantic-text-further-examples]

* For an overview of all query types supported by `semantic_text` fields and guidance on when to use them, refer to [Querying `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#querying-semantic-text-fields).
* If you want to use `semantic_text` in hybrid search, refer to [this notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb) for a step-by-step guide.
* For more information on how to optimize your ELSER endpoints, refer to [the ELSER recommendations](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-recommendations) section in the model documentation.
* To learn more about model autoscaling, refer to the [trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md) page.
* To learn how to optimize storage and search performance when using dense vector embeddings, refer to [Optimizing vector storage](../vector/vector-storage-for-semantic-search.md).