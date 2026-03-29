---
navigation_title: Semantic search with `semantic_text`
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-search-semantic-text.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Semantic search with `semantic_text` [semantic-search-semantic-text]

This tutorial shows you how to use the semantic text feature to perform semantic search on your data.

Semantic text simplifies the {{infer}} workflow by providing {{infer}} at ingestion time and sensible default values automatically. You don’t need to define model related settings and parameters, or create {{infer}} ingest pipelines.

The recommended way to use [semantic search](../semantic-search.md) in the {{stack}} is following the `semantic_text` workflow. When you need more control over indexing and query settings, you can still use the complete {{infer}} workflow (refer to [this tutorial](../../../explore-analyze/elastic-inference/inference-api.md) to review the process).

This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), but you can use any service and model supported by the [{{infer-cap}} API](/explore-analyze/elastic-inference/inference-api.md).

## Requirements [semantic-text-requirements]

- This tutorial uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), which is automatically enabled on {{ech}} deployments and {{serverless-short}} projects. 
::::{note}
You can also use [EIS for self-managed clusters](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).
::::
- To use the `semantic_text` field type with an {{infer}} service other than Elastic {{infer-cap}} Service, you must create an inference endpoint using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

## Create the index mapping [semantic-text-index-mapping]

The mapping of the destination index - the index that contains the embeddings that the inference endpoint will generate based on your input text - must be created. The destination index must have a field with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type to index the output of the used inference endpoint.

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

<!-- We possibly want to replace this with a programmatic _bulk API call

## Load data [semantic-text-load-data]

In this step, you load the data that you later use to create embeddings from it.

Use the `msmarco-passagetest2019-top1000` data set, which is a subset of the MS MARCO Passage Ranking data set. It consists of 200 queries, each accompanied by a list of relevant text passages. All unique passages, along with their IDs, have been extracted from that data set and compiled into a [tsv file](https://github.com/elastic/stack-docs/blob/main/docs/en/stack/ml/nlp/data/msmarco-passagetest2019-unique.tsv).

Download the file and upload it to your cluster using the [Data Visualizer](../../../manage-data/ingest/upload-data-files.md) in the {{ml-app}} UI. After your data is analyzed, click **Override settings**. Under **Edit field names**, assign `id` to the first column and `content` to the second. Click **Apply**, then **Import**. Name the index `test-data`, and click **Import**. After the upload is complete, you will see an index named `test-data` with 182,469 documents. -->


<!-- Removing reindexing step
## Reindex the data [semantic-text-reindex-data]

Create the embeddings from the text by reindexing the data from the `test-data` index to the `semantic-embeddings` index. The data in the `content` field will be reindexed into the `content` semantic text field of the destination index. The reindexed data will be processed by the {{infer}} endpoint associated with the `content` semantic text field.

::::{note}
This step uses the reindex API to simulate data ingestion. If you are working with data that has already been indexed, rather than using the test-data set, reindexing is required to ensure that the data is processed by the {{infer}} endpoint and the necessary embeddings are generated.

::::

```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 10 <1>
  },
  "dest": {
    "index": "semantic-embeddings"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing size to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.

The call returns a task ID to monitor the progress:

```console
GET _tasks/<task_id>
```

Reindexing large datasets can take a long time. You can test this workflow using only a subset of the dataset. Do this by cancelling the reindexing process, and only generating embeddings for the subset that was reindexed. The following API request will cancel the reindexing task:

```console
POST _tasks/<task_id>/_cancel
```

-->

::::{note}
If you're using web crawlers or connectors to generate indices, you have to [update the index mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) for these indices to include the `semantic_text` field. Once the mapping is updated, you'll need to run a full web crawl or a full connector sync. This ensures that all existing documents are reprocessed and updated with the new semantic embeddings, enabling semantic search on the updated data.
::::

## Ingest data [semantic-text-load-data]

Now, add some data to your index. Because you mapped the `content` field as `semantic_text`, {{es}} automatically intercepts the text during ingestion, sends it to the inference endpoint, and stores the resulting vector embeddings alongside your document.

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

## Semantic search [semantic-text-semantic-search]

With your data ingested and automatically embedded, you can instantly query it using semantic search. Choose between [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax to execute the query.

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
1. The `METADATA _score` clause is used to return the score of each document
2. The [match (`:`) operator](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) is used on the `content` field for standard keyword matching
3. Sorts by descending score to display the most relevant results first
4. Limits the results to 1000 documents

:::
::::


## Further examples and reading [semantic-text-further-examples]

* For an overview of all query types supported by `semantic_text` fields and guidance on when to use them, see [Querying `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#querying-semantic-text-fields).
* If you want to use `semantic_text` in hybrid search, refer to [this notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb) for a step-by-step guide.
* For more information on how to optimize your ELSER endpoints, refer to [the ELSER recommendations](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-recommendations) section in the model documentation.
* To learn more about model autoscaling, refer to the [trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md) page.
* To learn how to optimize storage and search performance when using dense vector embeddings, read about [Optimizing vector storage](vector-storage-for-semantic-search.md).