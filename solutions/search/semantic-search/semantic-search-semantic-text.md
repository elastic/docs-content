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

We recommend using the `semantic_text` workflow for [semantic search](../semantic-search.md) in the {{stack}}. When you need more control over indexing and query settings, you can use the complete {{infer}} workflow instead (refer to the [Inference API documentation](../../../explore-analyze/elastic-inference/inference-api.md) for details).

This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), but you can use any service and model supported by the [{{infer-cap}} API](/explore-analyze/elastic-inference/inference-api.md).

## Before you begin [semantic-text-requirements]

- This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), which is automatically enabled on {{ech}} deployments and {{serverless-short}} projects.
::::{note}
You can also use [EIS for self-managed clusters](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).
::::
- To use the `semantic_text` field type with an {{infer}} service other than Elastic {{infer-cap}} Service, you must create an inference endpoint using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

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

:::::::

:::{note}
For large-scale deployments using dense vector embeddings, you can significantly reduce memory usage by configuring quantization strategies like BBQ. For advanced configuration, refer to [Optimizing vector storage](vector-storage-for-semantic-search.md).
:::


::::{note}
If you're using web crawlers or connectors to generate indices, you have to [update the index mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) for these indices to include the `semantic_text` field. Once the mapping is updated, you'll need to run a full web crawl or a full connector sync. This ensures that all existing documents are reprocessed and updated with the new semantic embeddings, enabling semantic search on the updated data.
::::

## Ingest data [semantic-text-load-data]

With your index mapping in place, add some data. Because you mapped the `content` field as `semantic_text`, {{es}} automatically intercepts the text during ingestion, sends it to the {{infer}} endpoint, and stores the resulting vector embeddings alongside your document.

Use the [`_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) to ingest a few sample documents:

```
POST _bulk
{ "index": { "_index": "semantic-embeddings", "_id": "1" } }
{ "content": "After running, cool down with light cardio for a few minutes to lower your heart rate and reduce muscle soreness." }
{ "index": { "_index": "semantic-embeddings", "_id": "2" } }
{ "content": "Marathon plans stress weekly mileage; carb loading before a race does not replace recovery between hard sessions." }
{ "index": { "_index": "semantic-embeddings", "_id": "3" } }
{ "content": "Tune cluster performance by monitoring thread pools and refresh interval." }
```

The response returns `"errors": false` and an `items` array with a `"result": "created"` entry for each document. If you see errors, check that your index mapping and inference endpoint are configured correctly.

## Run a semantic search query [semantic-text-semantic-search]

With your data ingested and automatically embedded, you can query it using semantic search. Choose between [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax.

::::{tab-set}
:group: query-type

:::{tab-item} Query DSL
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
:::

:::{tab-item} ES|QL
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

:::
::::

Both queries return the documents ranked by semantic relevance. The documents about running and muscle soreness score highest because they are semantically closest to the query, while the document about cluster performance scores lower.

## Further examples and reading [semantic-text-further-examples]

* For an overview of all query types supported by `semantic_text` fields and guidance on when to use them, see [Querying `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#querying-semantic-text-fields).
* If you want to use `semantic_text` in hybrid search, refer to [this notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb) for a step-by-step guide.
* For more information on how to optimize your ELSER endpoints, refer to [the ELSER recommendations](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-recommendations) section in the model documentation.
* To learn more about model autoscaling, refer to the [trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md) page.
* To learn how to optimize storage and search performance when using dense vector embeddings, read about [Optimizing vector storage](vector-storage-for-semantic-search.md).