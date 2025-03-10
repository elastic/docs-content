---
navigation_title: "Semantic search with ELSER (ingest pipelines)"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-search-elser.html
applies_to:
  stack:
  serverless:
---



# Semantic search with ELSER [semantic-search-elser]


Elastic Learned Sparse EncodeR - or ELSER - is an NLP model trained by Elastic that enables you to perform semantic search by using sparse vector representation. Instead of literal matching on search terms, semantic search retrieves results based on the intent and the contextual meaning of a search query.

The instructions in this tutorial shows you how to use ELSER to perform semantic search on your data.

::::{important}
For the easiest way to perform semantic search in the {{stack}}, refer to the [`semantic_text`](semantic-search-semantic-text.md) end-to-end tutorial.
::::


::::{note}
Only the first 512 extracted tokens per field are considered during semantic search with ELSER. Refer to [this page](/explore-analyze/machine-learning/nlp/ml-nlp-limitations.md#ml-nlp-elser-v1-limit-512) for more information.
::::



### Requirements [requirements]

To perform semantic search by using ELSER, you must have the NLP model deployed in your cluster. Refer to the [ELSER documentation](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to learn how to download and deploy the model.

::::{note}
The minimum dedicated ML node size for deploying and using the ELSER model is 4 GB in {{ech}} if [deployment autoscaling](../../../deploy-manage/autoscaling.md) is turned off. Turning on autoscaling is recommended because it allows your deployment to dynamically adjust resources based on demand. Better performance can be achieved by using more allocations or more threads per allocation, which requires bigger ML nodes. Autoscaling provides bigger nodes when required. If autoscaling is turned off, you must provide suitably sized nodes yourself.
::::

### Create the index mapping [elser-mappings]

First, the mapping of the destination index - the index that contains the tokens that the model created based on your text - must be created. The destination index must have a field with the [`sparse_vector`](elasticsearch://reference/elasticsearch/mapping-reference/sparse-vector.md) or [`rank_features`](elasticsearch://reference/elasticsearch/mapping-reference/rank-features.md) field type to index the ELSER output.

::::{note}
ELSER output must be ingested into a field with the `sparse_vector` or `rank_features` field type. Otherwise, {{es}} interprets the token-weight pairs as a massive amount of fields in a document. If you get an error similar to this: `"Limit of total fields [1000] has been exceeded while adding new fields"` then the ELSER output field is not mapped properly and it has a field type different than `sparse_vector` or `rank_features`.
::::


```console
PUT my-index
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "sparse_vector" <2>
      },
      "content": { <3>
        "type": "text" <4>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `sparse_vector` field.
3. The name of the field from which to create the sparse vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
4. The field type which is text in this example.
%  TEST[skip:TBD]

To learn how to optimize space, refer to the [Saving disk space by excluding the ELSER tokens from document source](/manage-data/ingest/transform-enrich/ingest-pipelines.md) with an [{{infer}} processor](elasticsearch://reference/ingestion-tools/enrich-processor/inference-processor.md) to use ELSER to infer against the data that is being ingested in the pipeline.

```console
PUT _ingest/pipeline/elser-v2-test
{
  "processors": [
    {
      "inference": {
        "model_id": ".elser_model_2",
        "input_output": [ <1>
          {
            "input_field": "content",
            "output_field": "content_embedding"
          }
        ]
      }
    }
  ]
}
```

1. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.



### Load data [load-data]

In this step, you load the data that you later use in the {{infer}} ingest pipeline to extract tokens from it.

Use the `msmarco-passagetest2019-top1000` data set, which is a subset of the MS MARCO Passage Ranking data set. It consists of 200 queries, each accompanied by a list of relevant text passages. All unique passages, along with their IDs, have been extracted from that data set and compiled into a [tsv file](https://github.com/elastic/stack-docs/blob/main/docs/en/stack/ml/nlp/data/msmarco-passagetest2019-unique.tsv).

::::{important}
The `msmarco-passagetest2019-top1000` dataset was not utilized to train the model. We use this sample dataset in the tutorial because is easily accessible for demonstration purposes. You can use a different data set to test the workflow and become familiar with it.
::::


Download the file and upload it to your cluster using the [File Uploader](../../../manage-data/ingest/upload-data-files.md) in the UI. After your data is analyzed, click **Override settings**. Under **Edit field names***, assign `id` to the first column and `content` to the second. Click ***Apply***, then ***Import**. Name the index `test-data`, and click **Import**. After the upload is complete, you will see an index named `test-data` with 182,469 documents.


### Ingest the data through the {{infer}} ingest pipeline [reindexing-data-elser]

Create the tokens from the text by reindexing the data throught the {{infer}} pipeline that uses ELSER as the inference model.

```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "my-index",
    "pipeline": "elser-v2-test"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.
%  TEST[skip:TBD]

The call returns a task ID to monitor the progress:

```console
GET _tasks/<task_id>
```
%  TEST[skip:TBD]

You can also open the Trained Models UI, select the Pipelines tab under ELSER to follow the progress.

Reindexing large datasets can take a long time. You can test this workflow using only a subset of the dataset. Do this by cancelling the reindexing process, and only generating embeddings for the subset that was reindexed. The following API request will cancel the reindexing task:

```console
POST _tasks/<task_id>/_cancel
```
%  TEST[skip:TBD]


### Semantic search by using the `sparse_vector` query [text-expansion-query]

To perform semantic search, use the [`sparse_vector` query](elasticsearch://reference/query-languages/query-dsl-sparse-vector-query.md), and provide the query text and the inference ID associated with your ELSER model. The example below uses the query text "How to avoid muscle soreness after running?", the `content_embedding` field contains the generated ELSER output:

```console
GET my-index/_search
{
   "query":{
      "sparse_vector":{
         "field": "content_embedding",
         "inference_id": "my-elser-endpoint",
         "query": "How to avoid muscle soreness after running?"
      }
   }
}
```
%  TEST[skip:TBD]

The result is the top 10 documents that are closest in meaning to your query text from the `my-index` index sorted by their relevancy. The result also contains the extracted tokens for each of the relevant search results with their weights. Tokens are learned associations capturing relevance, they are not synonyms. To learn more about what tokens are, refer to [this page](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-tokens). It is possible to exclude tokens from source, refer to [this section](#save-space) to learn more.

```console-result
"hits": {
  "total": {
    "value": 10000,
    "relation": "gte"
  },
  "max_score": 26.199875,
  "hits": [
    {
      "_index": "my-index",
      "_id": "FPr9HYsBag9jXmT8lEpI",
      "_score": 26.199875,
      "_source": {
        "content_embedding": {
          "muscular": 0.2821541,
          "bleeding": 0.37929374,
          "foods": 1.1718726,
          "delayed": 1.2112266,
          "cure": 0.6848574,
          "during": 0.5886185,
          "fighting": 0.35022718,
          "rid": 0.2752442,
          "soon": 0.2967024,
          "leg": 0.37649947,
          "preparation": 0.32974035,
          "advance": 0.09652356,
          (...)
        },
        "id": 1713868,
        "model_id": ".elser_model_2",
        "content": "For example, if you go for a run, you will mostly use the muscles in your lower body. Give yourself 2 days to rest those muscles so they have a chance to heal before you exercise them again. Not giving your muscles enough time to rest can cause muscle damage, rather than muscle development."
      }
    },
    (...)
  ]
}
```
%  NOTCONSOLE

### Combining semantic search with other queries [text-expansion-compound-query]

You can combine [`sparse_vector`](elasticsearch://reference/query-languages/query-dsl-sparse-vector-query.md) with other queries in a [compound query](elasticsearch://reference/query-languages/compound-queries.md). For example, use a filter clause in a [Boolean](elasticsearch://reference/query-languages/query-dsl-bool-query.md) or a full text query with the same (or different) query text as the `sparse_vector` query. This enables you to combine the search results from both queries.

The search hits from the `sparse_vector` query tend to score higher than other {{es}} queries. Those scores can be regularized by increasing or decreasing the relevance scores of each query by using the `boost` parameter. Recall on the `sparse_vector` query can be high where there is a long tail of less relevant results. Use the `min_score` parameter to prune those less relevant documents.

```console
GET my-index/_search
{
  "query": {
    "bool": { <1>
      "should": [
        {
          "sparse_vector": {
            "field": "content_embedding",
            "inference_id": "my-elser-endpoint",
            "query": "How to avoid muscle soreness after running?",
            "boost": 1 <2>
          }
        },
        {
          "query_string": {
            "query": "toxins",
            "boost": 4 <3>
          }
        }
      ]
    }
  },
  "min_score": 10 <4>
}
```

1. Both the `sparse_vector` and the `query_string` queries are in a `should` clause of a `bool` query.
2. The `boost` value is `1` for the `sparse_vector` query which is the default value. This means that the relevance score of the results of this query are not boosted.
3. The `boost` value is `4` for the `query_string` query. The relevance score of the results of this query is increased causing them to rank higher in the search results.
4. Only the results with a score equal to or higher than `10` are displayed.
%  TEST[skip:TBD]


## Optimizing performance [optimization]


### Saving disk space by excluding the ELSER tokens from document source [save-space]

The tokens generated by ELSER must be indexed for use in the [sparse_vector query](elasticsearch://reference/query-languages/query-dsl-sparse-vector-query.md). However, it is not necessary to retain those terms in the document source. You can save disk space by using the [source exclude](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) mapping to remove the ELSER terms from the document source.

::::{warning}
Reindex uses the document source to populate the destination index. **Once the ELSER terms have been excluded from the source, they cannot be recovered through reindexing.** Excluding the tokens from the source is a space-saving optimization that should only be applied if you are certain that reindexing will not be required in the future! It’s important to carefully consider this trade-off and make sure that excluding the ELSER terms from the source aligns with your specific requirements and use case. Review the [Disabling the `_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#disable-source-field) and [Including / Excluding fields from `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) sections carefully to learn more about the possible consequences of excluding the tokens from the `_source`.
::::


The mapping that excludes `content_embedding` from the  `_source` field can be created by the following API call:

```console
PUT my-index
{
  "mappings": {
    "_source": {
      "excludes": [
        "content_embedding"
      ]
    },
    "properties": {
      "content_embedding": {
        "type": "sparse_vector"
      },
      "content": {
        "type": "text"
      }
    }
  }
}
```
%  TEST[skip:TBD]

::::{note}
Depending on your data, the `sparse_vector` query may be faster with `track_total_hits: false`.

::::



### Further reading [further-reading]

* [How to download and deploy ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md)
* [ELSER limitation](/explore-analyze/machine-learning/nlp/ml-nlp-limitations.md#ml-nlp-elser-v1-limit-512)
* [Improving information retrieval in the Elastic Stack: Introducing Elastic Learned Sparse Encoder, our new retrieval model](https://www.elastic.co/blog/may-2023-launch-information-retrieval-elasticsearch-ai-model)


### Interactive example [interactive-example]

* The `elasticsearch-labs` repo has an interactive example of running [ELSER-powered semantic search](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/03-ELSER.ipynb) using the {{es}} Python client.
