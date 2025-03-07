---
navigation_title: "ELSER"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-elser.html
applies_to:
  stack:
  serverless:
---

# ELSER inference integration [infer-service-elser]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `elser` service. You can also deploy ELSER by using the [Elasticsearch {{infer}} integration](elasticsearch-inference-integration.md).

::::{note} 
* Your {{es}} deployment contains [a preconfigured ELSER {{infer}} endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference), you only need to create the enpoint using the API if you want to customize the settings.
* The API request will automatically download and deploy the ELSER model if it isn’t already downloaded.

::::


::::{admonition} Deprecated in 8.16
:class: warning

The `elser` service is deprecated and will be removed in a future release. Use the [Elasticsearch {{infer}} integration](elasticsearch-inference-integration.md) instead, with `model_id` included in the `service_settings`.

::::



## {{api-request-title}} [infer-service-elser-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-elser-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `sparse_embedding`.



## {{api-request-body-title}} [infer-service-elser-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `elser`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `elser` service.

    `adaptive_allocations`
    :   (Optional, object) Adaptive allocations configuration object. If enabled, the number of allocations of the model is set based on the current load the process gets. When the load is high, a new model allocation is automatically created (respecting the value of `max_number_of_allocations` if it’s set). When the load is low, a model allocation is automatically removed (respecting the value of `min_number_of_allocations` if it’s set). If `adaptive_allocations` is enabled, do not set the number of allocations manually.

        `enabled`
        :   (Optional, Boolean) If `true`, `adaptive_allocations` is enabled. Defaults to `false`.

        `max_number_of_allocations`
        :   (Optional, integer) Specifies the maximum number of allocations to scale to. If set, it must be greater than or equal to `min_number_of_allocations`.

        `min_number_of_allocations`
        :   (Optional, integer) Specifies the minimum number of allocations to scale to. If set, it must be greater than or equal to `0`. If not defined, the deployment scales to `0`.


    `num_allocations`
    :   (Required, integer) The total number of allocations this model is assigned across machine learning nodes. Increasing this value generally increases the throughput. If `adaptive_allocations` is enabled, do not set this value, because it’s automatically set.

    `num_threads`
    :   (Required, integer) Sets the number of threads used by each model allocation during inference. This generally increases the speed per inference request. The inference process is a compute-bound process; `threads_per_allocations` must not exceed the number of available allocated processors per node. Must be a power of 2. Max allowed value is 32.



## ELSER service example with adaptive allocations [inference-example-elser-adaptive-allocation] 

When adaptive allocations are enabled, the number of allocations of the model is set automatically based on the current load.

::::{note} 
For more information on how to optimize your ELSER endpoints, refer to [the ELSER recommendations](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-recommendations) section in the model documentation. To learn more about model autoscaling, refer to the [trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md) page.
::::


The following example shows how to create an {{infer}} endpoint called `my-elser-model` to perform a `sparse_embedding` task type and configure adaptive allocations.

The request below will automatically download the ELSER model if it isn’t already downloaded and then deploy the model.

```console
PUT _inference/sparse_embedding/my-elser-model
{
  "service": "elser",
  "service_settings": {
    "adaptive_allocations": {
      "enabled": true,
      "min_number_of_allocations": 3,
      "max_number_of_allocations": 10
    },
    "num_threads": 1
  }
}
```
%  TEST[skip:TBD]


## ELSER service example without adaptive allocations [inference-example-elser] 

The following example shows how to create an {{infer}} endpoint called `my-elser-model` to perform a `sparse_embedding` task type. Refer to the [ELSER model documentation](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md) for more info.

::::{note} 
If you want to optimize your ELSER endpoint for ingest, set the number of threads to `1` (`"num_threads": 1`). If you want to optimize your ELSER endpoint for search, set the number of threads to greater than `1`.
::::


The request below will automatically download the ELSER model if it isn’t already downloaded and then deploy the model.

```console
PUT _inference/sparse_embedding/my-elser-model
{
  "service": "elser",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1
  }
}
```
%  TEST[skip:TBD]

Example response:

```console-result
{
  "inference_id": "my-elser-model",
  "task_type": "sparse_embedding",
  "service": "elser",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1
  },
  "task_settings": {}
}
```
%  NOTCONSOLE

::::{note} 
You might see a 502 bad gateway error in the response when using the {{kib}} Console. This error usually just reflects a timeout, while the model downloads in the background. You can check the download progress in the {{ml-app}} UI. If using the Python client, you can set the `timeout` parameter to a higher value.

::::


