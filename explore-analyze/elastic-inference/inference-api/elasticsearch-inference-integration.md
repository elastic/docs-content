---
navigation_title: "Elasticsearch"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-elasticsearch.html
applies_to:
  stack:
  serverless:
---

# Elasticsearch inference integration [infer-service-elasticsearch]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `elasticsearch` service.

::::{note} 
* Your {{es}} deployment contains [preconfigured ELSER and E5 {{infer}} endpoints](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference), you only need to create the enpoints using the API if you want to customize the settings.
* If you use the ELSER or the E5 model through the `elasticsearch` service, the API request will automatically download and deploy the model if it isn’t downloaded yet.

::::



## {{api-request-title}} [infer-service-elasticsearch-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-elasticsearch-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `rerank`,
    * `sparse_embedding`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-elasticsearch-api-request-body] 

`chunking_settings`
:   (Optional, object) Chunking configuration object. Refer to [Configuring chunking](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) to learn more about chunking.

    `max_chunk_size`
    :   (Optional, integer) Specifies the maximum size of a chunk in words. Defaults to `250`. This value cannot be higher than `300` or lower than `20` (for `sentence` strategy) or `10` (for `word` strategy).

    `overlap`
    :   (Optional, integer) Only for `word` chunking strategy. Specifies the number of overlapping words for chunks. Defaults to `100`. This value cannot be higher than the half of `max_chunk_size`.

    `sentence_overlap`
    :   (Optional, integer) Only for `sentence` chunking strategy. Specifies the numnber of overlapping sentences for chunks. It can be either `1` or `0`. Defaults to `1`.

    `strategy`
    :   (Optional, string) Specifies the chunking strategy. It could be either `sentence` or `word`.


`service`
:   (Required, string) The type of service supported for the specified task type. In this case, `elasticsearch`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `elasticsearch` service.

    `deployment_id`
    :   (Optional, string) The `deployment_id` of an existing trained model deployment. When `deployment_id` is used the `model_id` is optional.

    `adaptive_allocations`
    :   (Optional, object) Adaptive allocations configuration object. If enabled, the number of allocations of the model is set based on the current load the process gets. When the load is high, a new model allocation is automatically created (respecting the value of `max_number_of_allocations` if it’s set). When the load is low, a model allocation is automatically removed (respecting the value of `min_number_of_allocations` if it’s set). If `adaptive_allocations` is enabled, do not set the number of allocations manually.

        `enabled`
        :   (Optional, Boolean) If `true`, `adaptive_allocations` is enabled. Defaults to `false`.

        `max_number_of_allocations`
        :   (Optional, integer) Specifies the maximum number of allocations to scale to. If set, it must be greater than or equal to `min_number_of_allocations`.

        `min_number_of_allocations`
        :   (Optional, integer) Specifies the minimum number of allocations to scale to. If set, it must be greater than or equal to `0`. If not defined, the deployment scales to `0`.


    `model_id`
    :   (Required, string) The name of the model to use for the {{infer}} task. It can be the ID of either a built-in model (for example, `.multilingual-e5-small` for E5), a text embedding model already [uploaded through Eland](../../../explore-analyze/machine-learning/nlp/ml-nlp-import-model.md#ml-nlp-import-script).

    `num_allocations`
    :   (Required, integer) The total number of allocations this model is assigned across machine learning nodes. Increasing this value generally increases the throughput. If `adaptive_allocations` is enabled, do not set this value, because it’s automatically set.

    `num_threads`
    :   (Required, integer) Sets the number of threads used by each model allocation during inference. This generally increases the speed per inference request. The inference process is a compute-bound process; `threads_per_allocations` must not exceed the number of available allocated processors per node. Must be a power of 2. Max allowed value is 32.


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `rerank` task type
    `return_documents`
    :   (Optional, Boolean) Returns the document instead of only the index. Defaults to `true`.

    ::::



## ELSER via the `elasticsearch` service [inference-example-elasticsearch-elser] 

The following example shows how to create an {{infer}} endpoint called `my-elser-model` to perform a `sparse_embedding` task type.

The API request below will automatically download the ELSER model if it isn’t already downloaded and then deploy the model.

```console
PUT _inference/sparse_embedding/my-elser-model
{
  "service": "elasticsearch",
  "service_settings": {
    "adaptive_allocations": { <1>
      "enabled": true,
      "min_number_of_allocations": 1,
      "max_number_of_allocations": 4
    },
    "num_threads": 1,
    "model_id": ".elser_model_2" <2>
  }
}
```

1. Adaptive allocations will be enabled with the minimum of 1 and the maximum of 10 allocations.
2. The `model_id` must be the ID of one of the built-in ELSER models. Valid values are `.elser_model_2` and `.elser_model_2_linux-x86_64`. For further details, refer to the [ELSER model documentation](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md).
%  TEST[skip:TBD]


## Elastic Rerank via the `elasticsearch` service [inference-example-elastic-reranker] 

The following example shows how to create an {{infer}} endpoint called `my-elastic-rerank` to perform a `rerank` task type using the built-in [Elastic Rerank](../../../explore-analyze/machine-learning/nlp/ml-nlp-rerank.md) cross-encoder model.

::::{tip} 
Refer to this [Python notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/12-semantic-reranking-elastic-rerank.ipynb) for an end-to-end example using Elastic Rerank.

::::


The API request below will automatically download the Elastic Rerank model if it isn’t already downloaded and then deploy the model. Once deployed, the model can be used for semantic re-ranking with a [`text_similarity_reranker` retriever](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever).

```console
PUT _inference/rerank/my-elastic-rerank
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".rerank-v1", <1>
    "num_threads": 1,
    "adaptive_allocations": { <2>
      "enabled": true,
      "min_number_of_allocations": 1,
      "max_number_of_allocations": 4
    }
  }
}
```

1. The `model_id` must be the ID of the built-in Elastic Rerank model: `.rerank-v1`.
2. [Adaptive allocations](../../../deploy-manage/autoscaling/trained-model-autoscaling.md#enabling-autoscaling-through-apis-adaptive-allocations) will be enabled with the minimum of 1 and the maximum of 10 allocations.
%  TEST[skip:TBD]


## E5 via the `elasticsearch` service [inference-example-elasticsearch] 

The following example shows how to create an {{infer}} endpoint called `my-e5-model` to perform a `text_embedding` task type.

The API request below will automatically download the E5 model if it isn’t already downloaded and then deploy the model.

```console
PUT _inference/text_embedding/my-e5-model
{
  "service": "elasticsearch",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1,
    "model_id": ".multilingual-e5-small" <1>
  }
}
```

1. The `model_id` must be the ID of one of the built-in E5 models. Valid values are `.multilingual-e5-small` and `.multilingual-e5-small_linux-x86_64`. For further details, refer to the [E5 model documentation](../../../explore-analyze/machine-learning/nlp/ml-nlp-e5.md).
%  TEST[skip:TBD]

::::{note} 
You might see a 502 bad gateway error in the response when using the {{kib}} Console. This error usually just reflects a timeout, while the model downloads in the background. You can check the download progress in the {{ml-app}} UI. If using the Python client, you can set the `timeout` parameter to a higher value.

::::



## Models uploaded by Eland via the `elasticsearch` service [inference-example-eland] 

The following example shows how to create an {{infer}} endpoint called `my-msmarco-minilm-model` to perform a `text_embedding` task type.

```console
PUT _inference/text_embedding/my-msmarco-minilm-model <1>
{
  "service": "elasticsearch",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1,
    "model_id": "msmarco-MiniLM-L12-cos-v5" <2>
  }
}
```

1. Provide an unique identifier for the inference endpoint. The `inference_id` must be unique and must not match the `model_id`.
2. The `model_id` must be the ID of a text embedding model which has already been [uploaded through Eland](../../../explore-analyze/machine-learning/nlp/ml-nlp-import-model.md#ml-nlp-import-script).
%  TEST[skip:TBD]


## Setting adaptive allocation for E5 via the `elasticsearch` service [inference-example-adaptive-allocation] 

The following example shows how to create an {{infer}} endpoint called `my-e5-model` to perform a `text_embedding` task type and configure adaptive allocations.

The API request below will automatically download the E5 model if it isn’t already downloaded and then deploy the model.

```console
PUT _inference/text_embedding/my-e5-model
{
  "service": "elasticsearch",
  "service_settings": {
    "adaptive_allocations": {
      "enabled": true,
      "min_number_of_allocations": 3,
      "max_number_of_allocations": 10
    },
    "num_threads": 1,
    "model_id": ".multilingual-e5-small"
  }
}
```
%  TEST[skip:TBD]


## Using an existing model deployment with the `elasticsearch` service [inference-example-existing-deployment] 

The following example shows how to use an already existing model deployment when creating an {{infer}} endpoint.

```console
PUT _inference/sparse_embedding/use_existing_deployment
{
  "service": "elasticsearch",
  "service_settings": {
    "deployment_id": ".elser_model_2" <1>
  }
}
```

1. The `deployment_id` of the already existing model deployment.
%  TEST[skip:TBD]

The API response contains the `model_id`, and the threads and allocations settings from the model deployment:

```console-result
{
  "inference_id": "use_existing_deployment",
  "task_type": "sparse_embedding",
  "service": "elasticsearch",
  "service_settings": {
    "num_allocations": 2,
    "num_threads": 1,
    "model_id": ".elser_model_2",
    "deployment_id": ".elser_model_2"
  },
  "chunking_settings": {
    "strategy": "sentence",
    "max_chunk_size": 250,
    "sentence_overlap": 1
  }
}
```
%  NOTCONSOLE

