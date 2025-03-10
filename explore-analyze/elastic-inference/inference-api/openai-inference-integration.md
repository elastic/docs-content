---
navigation_title: "OpenAI"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-openai.html
applies_to:
  stack:
  serverless:
---

# OpenAI inference integration [infer-service-openai]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `openai` service.


## {{api-request-title}} [infer-service-openai-api-request]

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-openai-api-path-params]

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `chat_completion`,
    * `completion`,
    * `text_embedding`.


::::{note}
The `chat_completion` task type only supports streaming and only through the `_stream` API.

For more information on how to use the `chat_completion` task type, please refer to the [chat completion documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/chat-completion-inference-api.html).

::::



## {{api-request-body-title}} [infer-service-openai-api-request-body]

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
:   (Required, string) The type of service supported for the specified task type. In this case, `openai`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `openai` service.

    `api_key`
    :   (Required, string) A valid API key of your OpenAI account. You can find your OpenAI API keys in your OpenAI account under the [API keys section](https://platform.openai.com/api-keys).

        ::::{important}
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `dimensions`
    :   (Optional, integer) The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models. If not set the OpenAI defined default for the model is used.

    `model_id`
    :   (Required, string) The name of the model to use for the {{infer}} task. Refer to the [OpenAI documentation](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) for the list of available text embedding models.

    `organization_id`
    :   (Optional, string) The unique identifier of your organization. You can find the Organization ID in your OpenAI account under [**Settings** > **Organizations**](https://platform.openai.com/account/organization).

    `url`
    :   (Optional, string) The URL endpoint to use for the requests. Can be changed for testing purposes. Defaults to `https://api.openai.com/v1/embeddings`.

    `rate_limit`
    :   (Optional, object) The `openai` service sets a default number of requests allowed per minute depending on the task type. For `text_embedding` it is set to `3000`. For `completion` it is set to `500`. This helps to minimize the number of rate limit errors returned from OpenAI. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```

        More information about the rate limits for OpenAI can be found in your [Account limits](https://platform.openai.com/account/limits).


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `completion` task type
    `user`
    :   (Optional, string) Specifies the user issuing the request, which can be used for abuse detection.

    ::::


    ::::{dropdown} `task_settings` for the `text_embedding` task type
    `user`
    :   (optional, string) Specifies the user issuing the request, which can be used for abuse detection.

    ::::



## OpenAI service example [inference-example-openai]

The following example shows how to create an {{infer}} endpoint called `openai-embeddings` to perform a `text_embedding` task type. The embeddings created by requests to this endpoint will have 128 dimensions.

```console
PUT _inference/text_embedding/openai-embeddings
{
    "service": "openai",
    "service_settings": {
        "api_key": "<api_key>",
        "model_id": "text-embedding-3-small",
        "dimensions": 128
    }
}
```
%  TEST[skip:TBD]

The next example shows how to create an {{infer}} endpoint called `openai-completion` to perform a `completion` task type.

```console
PUT _inference/completion/openai-completion
{
    "service": "openai",
    "service_settings": {
        "api_key": "<api_key>",
        "model_id": "gpt-3.5-turbo"
    }
}
```
%  TEST[skip:TBD]
