---
navigation_title: "Semantic search with `semantic_text`"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-search-semantic-text.html
applies:
  stack:
  serverless:
---

# Semantic search with `semantic_text` [semantic-search-semantic-text]


::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


This tutorial shows you how to use the semantic text feature to perform semantic search on your data.

Semantic text simplifies the {{infer}} workflow by providing {{infer}} at ingestion time and sensible default values automatically. You don’t need to define model related settings and parameters, or create {{infer}} ingest pipelines.

The recommended way to use [semantic search](../semantic-search.md) in the {{stack}} is following the `semantic_text` workflow. When you need more control over indexing and query settings, you can still use the complete {{infer}} workflow (refer to  [this tutorial](../inference-api.md) to review the process).

This tutorial uses the [`elasticsearch` service](../inference-api/elasticsearch-inference-integration.md) for demonstration, but you can use any service and their supported models offered by the {{infer-cap}} API.


## Requirements [semantic-text-requirements]

This tutorial uses the [`elasticsearch` service](../inference-api/elasticsearch-inference-integration.md) for demonstration, which is created automatically as needed. To use the `semantic_text` field type with an {{infer}} service other than `elasticsearch` service, you must create an inference endpoint using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).


## Create the index mapping [semantic-text-index-mapping]

The mapping of the destination index - the index that contains the embeddings that the inference endpoint will generate based on your input text - must be created. The destination index must have a field with the [`semantic_text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text.html) field type to index the output of the used inference endpoint.

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
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the default endpoint `.elser-2-elasticsearch` for the [`elasticsearch` service](../inference-api/elasticsearch-inference-integration.md) is used. To use a different {{infer}} service, you must create an {{infer}} endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put) and then specify it in the `semantic_text` field mapping using the `inference_id` parameter.


::::{note}
If you’re using web crawlers or connectors to generate indices, you have to [update the index mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) for these indices to include the `semantic_text` field. Once the mapping is updated, you’ll need to run a full web crawl or a full connector sync. This ensures that all existing documents are reprocessed and updated with the new semantic embeddings, enabling semantic search on the updated data.

::::



## Load data [semantic-text-load-data]

In this step, you load the data that you later use to create embeddings from it.

Use the `msmarco-passagetest2019-top1000` data set, which is a subset of the MS MARCO Passage Ranking data set. It consists of 200 queries, each accompanied by a list of relevant text passages. All unique passages, along with their IDs, have been extracted from that data set and compiled into a [tsv file](https://github.com/elastic/stack-docs/blob/main/docs/en/stack/ml/nlp/data/msmarco-passagetest2019-unique.tsv).

Download the file and upload it to your cluster using the [Data Visualizer](../../../manage-data/ingest/upload-data-files.md) in the {{ml-app}} UI. After your data is analyzed, click **Override settings**. Under **Edit field names***, assign `id` to the first column and `content` to the second. Click ***Apply***, then ***Import**. Name the index `test-data`, and click **Import**. After the upload is complete, you will see an index named `test-data` with 182,469 documents.


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


## Semantic search [semantic-text-semantic-search]

After the data set has been enriched with the embeddings, you can query the data using semantic search. Provide the `semantic_text` field name and the query text in a `semantic` query type. The {{infer}} endpoint used to generate the embeddings for the `semantic_text` field will be used to process the query text.

```console
GET semantic-embeddings/_search
{
  "query": {
    "semantic": {
      "field": "content", <1>
      "query": "How to avoid muscle soreness while running?" <2>
    }
  }
}
```

1. The `semantic_text` field on which you want to perform the search.
2. The query text.


As a result, you receive the top 10 documents that are closest in meaning to the query from the `semantic-embedding` index.


## Further examples and reading [semantic-text-further-examples]

* If you want to use `semantic_text` in hybrid search, refer to [this notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb) for a step-by-step guide.
* For more information on how to optimize your ELSER endpoints, refer to [the ELSER recommendations](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-recommendations) section in the model documentation.
* To learn more about model autoscaling, refer to the [trained model autoscaling](/explore-analyze/machine-learning/nlp/ml-nlp-auto-scale.md) page.
