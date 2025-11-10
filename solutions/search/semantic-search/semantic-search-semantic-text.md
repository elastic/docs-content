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

This tutorial uses the [`elasticsearch` service](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elasticsearch) for demonstration, but you can use any service and their supported models offered by the {{infer-cap}} API.

## Requirements [semantic-text-requirements]

This tutorial uses the `elasticsearch` service for demonstration, which is created automatically as needed. To use the `semantic_text` field type with an {{infer}} service other than `elasticsearch` service, you must create an inference endpoint using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

## Create the index mapping [semantic-text-index-mapping]

The mapping of the destination index - the index that contains the embeddings that the inference endpoint will generate based on your input text - must be created. The destination index must have a field with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type to index the output of the used inference endpoint.

You can run {{infer}} either using the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) or on your own ML-nodes. The following examples show you both scenarios.

::::{tip}
For production deployments with dense vector embeddings, consider optimizing storage and performance using [`index_options`](#semantic-text-index-options). This allows you to configure quantization strategies like BBQ (Better Binary Quantization) that can reduce memory usage by up to 32x.
::::

:::::::{tab-set}

::::::{tab-item} Using EIS on Serverless

```{applies_to}
serverless: ga
```

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
2. The field to contain the embeddings is a `semantic_text` field. Since no `inference_id` is provided, the default endpoint `.elser-2-elastic` for the `elasticsearch` service is used. This {{infer}} endpoint uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).

::::::

::::::{tab-item} Using EIS in Cloud

```{applies_to}
stack: ga
deployment:
  self: unavailable
```

```console
PUT semantic-embeddings
{
  "mappings": {
    "properties": {
      "content": { <1>
        "type": "semantic_text", <2>
        "inference_id": ".elser-v2-elastic" <3>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings.
2. The field to contain the embeddings is a `semantic_text` field.
3. The `.elser-v2-elastic` preconfigured {{infer}} endpoint for the `elasticsearch` service is used. This {{infer}} endpoint uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).

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

To try the ELSER model on the Elastic Inference Service, explicitly set the `inference_id` to `.elser-2-elastic`. For instructions, refer to [Using `semantic_text` with ELSER on EIS](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text#using-elser-on-eis).

### Optimizing vector storage with `index_options` [semantic-text-index-options]

When using `semantic_text` with dense vector embeddings (such as E5 or other text embedding models), you can optimize storage and search performance by configuring `index_options` on the underlying `dense_vector` field. This is particularly useful for large-scale deployments.

The `index_options` parameter controls how vectors are indexed and stored. For dense vector embeddings, you can specify quantization strategies like Better Binary Quantization (BBQ) that significantly reduce memory footprint while maintaining search quality. For details on available options and their trade-offs, refer to the [`dense_vector` `index_options` documentation](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).

::::{tip}
For most production use cases with dense vector embeddings, using BBQ is recommended as it provides up to 32x memory reduction with minimal accuracy loss. Choose from:
- `bbq_hnsw` - Best for most use cases (default for 384+ dimensions)
- `bbq_flat` - Simpler option for smaller datasets
- `bbq_disk` - Disk-based storage for very large datasets with minimal memory requirements (Elasticsearch 9.2+)
::::

Here's an example using `semantic_text` with a text embedding inference endpoint and BBQ quantization:

```console
PUT semantic-embeddings-optimized
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": "my-e5-model", <1>
        "index_options": {
          "dense_vector": {
            "type": "bbq_hnsw" <2>
          }
        }
      }
    }
  }
}
```

1. Reference to a text embedding inference endpoint (e.g., E5, OpenAI, or Cohere embeddings). You must create this endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).
2. Use Better Binary Quantization with HNSW indexing for optimal memory efficiency. This setting applies to the underlying `dense_vector` field that stores the embeddings.

You can also use `bbq_flat` for simpler datasets or when you don't need the HNSW graph:

```console
PUT semantic-embeddings-flat
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": "my-e5-model",
        "index_options": {
          "dense_vector": {
            "type": "bbq_flat" <1>
          }
        }
      }
    }
  }
}
```

1. Use BBQ without HNSW for simpler use cases with fewer vectors. This requires less compute resources during indexing.

For very large datasets where memory is constrained, use `bbq_disk` (DiskBBQ) to store vectors on disk:

```console
PUT semantic-embeddings-disk
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": "my-e5-model",
        "index_options": {
          "dense_vector": {
            "type": "bbq_disk" <1>
          }
        }
      }
    }
  }
}
```

```{applies_to}
stack: ga 9.2
serverless: unavailable
```

1. Use DiskBBQ for disk-based vector storage with minimal memory requirements. Available in Elasticsearch 9.2+. This option stores compressed vectors on disk, reducing RAM usage to as little as 100 MB while maintaining query latencies around 15ms.

Other quantization options include `int8_hnsw` (8-bit integer quantization) and `int4_hnsw` (4-bit integer quantization):

```console
PUT semantic-embeddings-int8
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": "my-e5-model",
        "index_options": {
          "dense_vector": {
            "type": "int8_hnsw" <1>
          }
        }
      }
    }
  }
}
```

1. Use 8-bit integer quantization for 4x memory reduction with high accuracy retention. For 4-bit quantization, use `"type": "int4_hnsw"` instead, which provides 8x memory reduction.

For HNSW-specific tuning parameters like `m` and `ef_construction`, you can include them in the `index_options`:

```console
PUT semantic-embeddings-custom
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": "my-e5-model",
        "index_options": {
          "dense_vector": {
            "type": "bbq_hnsw",
            "m": 32, <1>
            "ef_construction": 200 <2>
          }
        }
      }
    }
  }
}
```

1. Number of bidirectional links per node in the HNSW graph. Higher values improve recall but increase memory usage. Default is 16.
2. Number of candidates considered during graph construction. Higher values improve index quality but slow down indexing. Default is 100.

::::{note}
The `index_options` parameter is only applicable when using inference endpoints that produce dense vector embeddings (like E5, OpenAI embeddings, Cohere embeddings, etc.). It does not apply to sparse vector models like ELSER, which use a different internal representation.
::::

::::{note}
If you're using web crawlers or connectors to generate indices, you have to [update the index mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) for these indices to include the `semantic_text` field. Once the mapping is updated, you'll need to run a full web crawl or a full connector sync. This ensures that all existing documents are reprocessed and updated with the new semantic embeddings, enabling semantic search on the updated data.

::::

## Load data [semantic-text-load-data]

In this step, you load the data that you later use to create embeddings from it.

Use the `msmarco-passagetest2019-top1000` data set, which is a subset of the MS MARCO Passage Ranking data set. It consists of 200 queries, each accompanied by a list of relevant text passages. All unique passages, along with their IDs, have been extracted from that data set and compiled into a [tsv file](https://github.com/elastic/stack-docs/blob/main/docs/en/stack/ml/nlp/data/msmarco-passagetest2019-unique.tsv).

Download the file and upload it to your cluster using the [Data Visualizer](../../../manage-data/ingest/upload-data-files.md) in the {{ml-app}} UI. After your data is analyzed, click **Override settings**. Under **Edit field names**, assign `id` to the first column and `content` to the second. Click **Apply**, then **Import**. Name the index `test-data`, and click **Import**. After the upload is complete, you will see an index named `test-data` with 182,469 documents.

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

After the data has been indexed with the embeddings, you can query the data using semantic search. Choose between [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) or [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax to execute the query.

::::{tab-set}
:group: query-type

:::{tab-item} Query DSL
:sync: dsl

The Query DSL approach uses the [`match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) type with the `semantic_text` field:

```esql
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
