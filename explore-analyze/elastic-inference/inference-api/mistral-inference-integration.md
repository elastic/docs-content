---
navigation_title: "Mistral"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-mistral.html
applies_to:
  stack:
  serverless:
---

# Mistral inference integration [infer-service-mistral]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `mistral` service.


## {{api-request-title}} [infer-service-mistral-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-mistral-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `text_embedding`.



## {{api-request-body-title}} [infer-service-mistral-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `mistral`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `mistral` service.

    `api_key`
    :   (Required, string) A valid API key for your Mistral account. You can find your Mistral API keys or you can create a new one [on the API Keys page](https://console.mistral.ai/api-keys/).

        ::::{important} 
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `model`
    :   (Required, string) The name of the model to use for the {{infer}} task. Refer to the [Mistral models documentation](https://docs.mistral.ai/getting-started/models/) for the list of available text embedding models.

    `max_input_tokens`
    :   (Optional, integer) Allows you to specify the maximum number of tokens per input before chunking occurs.

    `rate_limit`
    :   (Optional, object) By default, the `mistral` service sets the number of requests allowed per minute to `240`. This helps to minimize the number of rate limit errors returned from the Mistral API. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```



## Mistral service example [inference-example-mistral] 

The following example shows how to create an {{infer}} endpoint called `mistral-embeddings-test` to perform a `text_embedding` task type.

```console
PUT _inference/text_embedding/mistral-embeddings-test
{
  "service": "mistral",
  "service_settings": {
    "api_key": "<api_key>",
    "model": "mistral-embed" <1>
  }
}
```

1. The `model` must be the ID of a text embedding model which can be found in the [Mistral models documentation](https://docs.mistral.ai/getting-started/models/).
%  TEST[skip:TBD]

