---
navigation_title: "Elastic Inference Service"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/master/infer-service-elastic.html
applies_to:
  stack:
  serverless:
---

# Elastic Inference Service (EIS) [infer-service-elastic]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `elastic` service.


## {{api-request-title}} [infer-service-elastic-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-elastic-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `chat_completion`,
    * `sparse_embedding`.


::::{note} 
The `chat_completion` task type only supports streaming and only through the `_stream` API.

For more information on how to use the `chat_completion` task type, please refer to the [chat completion documentation](chat-completion-inference-api.md).

::::



## {{api-request-body-title}} [infer-service-elastic-api-request-body] 

`max_chunk_size`
:   (Optional, integer) Specifies the maximum size of a chunk in words. Defaults to `250`. This value cannot be higher than `300` or lower than `20` (for `sentence` strategy) or `10` (for `word` strategy).

`overlap`
:   (Optional, integer) Only for `word` chunking strategy. Specifies the number of overlapping words for chunks. Defaults to `100`. This value cannot be higher than the half of `max_chunk_size`.

`sentence_overlap`
:   (Optional, integer) Only for `sentence` chunking strategy. Specifies the numnber of overlapping sentences for chunks. It can be either `1` or `0`. Defaults to `1`.

`strategy`
:   (Optional, string) Specifies the chunking strategy. It could be either `sentence` or `word`.

    `service`
    :   (Required, string) The type of service supported for the specified task type. In this case, `elastic`.

    `service_settings`
    :   (Required, object) Settings used to install the {{infer}} model.


`model_id`
:   (Required, string) The name of the model to use for the {{infer}} task.

`rate_limit`
:   (Optional, object) By default, the `elastic` service sets the number of requests allowed per minute to `1000` in case of `sparse_embedding` and `240` in case of `chat_completion`. This helps to minimize the number of rate limit errors returned. To modify this, set the `requests_per_minute` setting of this object in your service settings:

    ```text
    "rate_limit": {
        "requests_per_minute": <<number_of_requests>>
    }
    ```



## Elastic {{infer-cap}} Service example [inference-example-elastic] 

The following example shows how to create an {{infer}} endpoint called `elser-model-eis` to perform a `text_embedding` task type.

```console
PUT _inference/sparse_embedding/elser-model-eis
{
    "service": "elastic",
    "service_settings": {
        "model_name": "elser"
    }
}
```
%  TEST[skip:TBD]

The following example shows how to create an {{infer}} endpoint called `chat-completion-endpoint` to perform a `chat_completion` task type.

```console
PUT /_inference/chat_completion/chat-completion-endpoint
{
    "service": "elastic",
    "service_settings": {
        "model_id": "model-1"
    }
}
```
%  TEST[skip:TBD]

