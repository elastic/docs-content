---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Text embedding and semantic search"
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-text-emb-vector-search-example.html
---

# Text embedding and semantic search [ml-nlp-text-emb-vector-search-example]

You can use these instructions to deploy a [text embedding](ml-nlp-search-compare.md#ml-nlp-text-embedding) model in {{es}}, test the model, and add it to an {{infer}} ingest pipeline. It enables you to generate vector representations of text and perform vector similarity search on the generated vectors. The model that is used in the example is publicly available on [HuggingFace](https://huggingface.co/).

The example uses a public data set from the [MS MARCO Passage Ranking Task](https://microsoft.github.io/msmarco/#ranking). It consists of real questions from the Microsoft Bing search engine and human generated answers for them. The example works with a sample of this data set, uses a model to produce text embeddings, and then runs vector search on it.

You can find [this example as a Jupyter notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/integrations/hugging-face/loading-model-from-hugging-face.ipynb) using the Python client in the `elasticsearch-labs` repo.

## Requirements [ex-te-vs-requirements]

To follow along the process on this page, you must have:

* an {{es}} Cloud cluster that is set up properly to use the {{ml-features}}. Refer to [Setup and security](../setting-up-machine-learning.md).
* The [appropriate subscription](https://www.elastic.co/subscriptions) level or the free trial period activated.
* [Docker](https://docs.docker.com/get-docker/) installed.

## Deploy a text embedding model [ex-te-vs-deploy]

You can use the [Eland client](https://www.elastic.co/guide/en/elasticsearch/client/eland/current) to install the {{nlp}} model. Use the prebuilt Docker image to run the Eland install model commands. Pull the latest image with:

```shell
docker pull docker.elastic.co/eland/eland
```

After the pull completes, your Eland Docker client is ready to use.

Select a text embedding model from the [third-party model reference list](ml-nlp-model-ref.md#ml-nlp-model-ref-ner). This example uses the [msmarco-MiniLM-L-12-v3](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L-12-v3) sentence-transformer model.

Install the model by running the `eland_import_model_hub` command in the Docker image:

```shell
docker run -it --rm docker.elastic.co/eland/eland \
    eland_import_hub_model \
      --cloud-id $CLOUD_ID \
      -u <username> -p <password> \
      --hub-model-id sentence-transformers/msmarco-MiniLM-L-12-v3 \
      --task-type text_embedding \
      --start
```

You need to provide an administrator username and password and replace the `$CLOUD_ID` with the ID of your Cloud deployment. This Cloud ID can be copied from the **Deployments** page on your Cloud website.

Since the `--start` option is used at the end of the Eland import command, {{es}} deploys the model ready to use. If you have multiple models and want to select which model to deploy, you can use the **{{ml-app}} > Model Management** user interface in {{kib}} to manage the starting and stopping of models.

Go to the **{{ml-app}} > Trained Models** page and synchronize your trained models. A warning message is displayed at the top of the page that says *"ML job and trained model synchronization required"*. Follow the link to *"Synchronize your jobs and trained models."* Then click **Synchronize**. You can also wait for the automatic synchronization that occurs in every hour, or use the [sync {{ml}} objects API](https://www.elastic.co/docs/api/doc/kibana/v8/group/endpoint-ml).

## Test the text embedding model [ex-text-emb-test]

Deployed models can be evaluated in {{kib}} under **{{ml-app}}** > **Trained Models** by selecting the **Test model** action for the respective model.

:::{image} ../../../images/machine-learning-ml-nlp-text-emb-test.png
:alt: Test trained model UI
:class: screenshot
:::

::::{dropdown} **Test the model by using the _infer API**
You can also evaluate your models by using the [_infer API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-infer-trained-model). In the following request, `text_field` is the field name where the model expects to find the input, as defined in the model configuration. By default, if the model was uploaded via Eland, the input field is `text_field`.

```js
POST /_ml/trained_models/sentence-transformers__msmarco-minilm-l-12-v3/_infer
{
  "docs": {
    "text_field": "How is the weather in Jamaica?"
  }
}
```

The API returns a response similar to the following:

```js
{
  "inference_results": [
    {
      "predicted_value": [
        0.39521875977516174,
        -0.3263707458972931,
        0.26809820532798767,
        0.30127981305122375,
        0.502890408039093,
        ...
      ]
    }
  ]
}
```

::::

The result is the predicted dense vector transformed from the example text.

## Load data [ex-text-emb-data]

In this step, you load the data that you later use in an ingest pipeline to get the embeddings.

The data set `msmarco-passagetest2019-top1000` is a subset of the MS MARCO Passage Ranking data set used in the testing stage of the 2019 TREC Deep Learning Track. It contains 200 queries and for each query a list of relevant text passages extracted by a simple information retrieval (IR) system. From that data set, all unique passages with their IDs have been extracted and put into a [tsv file](https://github.com/elastic/stack-docs/blob/8.5/docs/en/stack/ml/nlp/data/msmarco-passagetest2019-unique.tsv), totaling 182469 passages. In the following, this file is used as the example data set.

Upload the file by using the [Data Visualizer](../../../manage-data/ingest/upload-data-files.md). Name the first column `id` and the second one `text`. The index name is `collection`. After the upload is done, you can see an index named `collection` with 182469 documents.

:::{image} ../../../images/machine-learning-ml-nlp-text-emb-data.png
:alt: Importing the data
:class: screenshot
:::

## Add the text embedding model to an {{infer}} ingest pipeline [ex-text-emb-ingest]

Process the initial data with an [{{infer}} processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/inference-processor.md). It adds an embedding for each passage. For this, create a text embedding ingest pipeline and then reindex the initial data with this pipeline.

Now create an ingest pipeline either in the [{{stack-manage-app}} UI](ml-nlp-inference.md#ml-nlp-inference-processor) or by using the API:

```js
PUT _ingest/pipeline/text-embeddings
{
  "description": "Text embedding pipeline",
  "processors": [
    {
      "inference": {
        "model_id": "sentence-transformers__msmarco-minilm-l-12-v3",
        "target_field": "text_embedding",
        "field_map": {
          "text": "text_field"
        }
      }
    }
  ],
  "on_failure": [
    {
      "set": {
        "description": "Index document to 'failed-<index>'",
        "field": "_index",
        "value": "failed-{{{_index}}}"
      }
    },
    {
      "set": {
        "description": "Set error message",
        "field": "ingest.failure",
        "value": "{{_ingest.on_failure_message}}"
      }
    }
  ]
}
```

The passages are in a field named `text`. The `field_map` maps the text to the field `text_field` that the model expects. The `on_failure` handler is set to index failures into a different index.

Before ingesting the data through the pipeline, create the mappings of the destination index, in particular for the field `text_embedding.predicted_value` where the ingest processor stores the embeddings. The `dense_vector` field must be configured with the same number of dimensions (`dims`) as the text embedding produced by the model. That value can be found in the `embedding_size` option in the model configuration either under the Trained Models page in {{kib}} or in the response body of the [Get trained models API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models) call. The msmarco-MiniLM-L-12-v3 model has embedding_size of 384, so `dims` is set to 384.

```js
PUT collection-with-embeddings
{
  "mappings": {
    "properties": {
      "text_embedding.predicted_value": {
        "type": "dense_vector",
        "dims": 384
      },
      "text": {
        "type": "text"
      }
    }
  }
}
```

Create the text embeddings by reindexing the data to the `collection-with-embeddings` index through the {{infer}} pipeline. The {{infer}} ingest processor inserts the embedding vector into each document.

```js
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "collection",
    "size": 50 <1>
  },
  "dest": {
    "index": "collection-with-embeddings",
    "pipeline": "text-embeddings"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.

The API call returns a task ID that can be used to monitor the progress:

```js
GET _tasks/<task_id>
```

You can also open the model stat UI to follow the progress.

:::{image} ../../../images/machine-learning-ml-nlp-text-emb-reindex.png
:alt: Model status UI
:class: screenshot
:::

After the reindexing is finished, the documents in the new index contain the {{infer}} results – the vector embeddings.

## Semantic search [ex-text-emb-vect-search]

After the dataset has been enriched with vector embeddings, you can query the data using [semantic search](../../../solutions/search/vector/knn.md#knn-semantic-search). Pass a `query_vector_builder` to the k-nearest neighbor (kNN) vector search API, and provide the query text and the model you have used to create vector embeddings. This example searches for "How is the weather in Jamaica?":

```js
GET collection-with-embeddings/_search
{
  "knn": {
    "field": "text_embedding.predicted_value",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "sentence-transformers__msmarco-minilm-l-12-v3",
        "model_text": "How is the weather in Jamaica?"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "text"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `collection-with-embedings` index sorted by their proximity to the query:

```js
"hits" : [
      {
        "_index" : "collection-with-embeddings",
        "_id" : "47TPtn8BjSkJO8zzKq_o",
        "_score" : 0.94591534,
        "_source" : {
          "id" : 434125,
          "text" : "The climate in Jamaica is tropical and humid with warm to hot temperatures all year round. The average temperature in Jamaica is between 80 and 90 degrees Fahrenheit. Jamaican nights are considerably cooler than the days, and the mountain areas are cooler than the lower land throughout the year. Continue Reading."
        }
      },
      {
        "_index" : "collection-with-embeddings",
        "_id" : "3LTPtn8BjSkJO8zzKJO1",
        "_score" : 0.94536424,
        "_source" : {
          "id" : 4498474,
          "text" : "The climate in Jamaica is tropical and humid with warm to hot temperatures all year round. The average temperature in Jamaica is between 80 and 90 degrees Fahrenheit. Jamaican nights are considerably cooler than the days, and the mountain areas are cooler than the lower land throughout the year"
        }
      },
      {
        "_index" : "collection-with-embeddings",
        "_id" : "KrXPtn8BjSkJO8zzPbDW",
        "_score" :  0.9432083,
        "_source" : {
          "id" : 190804,
          "text" : "Quick Answer. The climate in Jamaica is tropical and humid with warm to hot temperatures all year round. The average temperature in Jamaica is between 80 and 90 degrees Fahrenheit. Jamaican nights are considerably cooler than the days, and the mountain areas are cooler than the lower land throughout the year. Continue Reading"
        }
      },
      (...)
]
```

If you want to do a quick verification of the results, follow the steps of the *Quick verification* section of [this blog post](https://www.elastic.co/blog/how-to-deploy-nlp-text-embeddings-and-vector-search#).
