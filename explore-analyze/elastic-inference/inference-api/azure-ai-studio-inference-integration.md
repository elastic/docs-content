---
navigation_title: "Azure AI Studio"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-azure-ai-studio.html
applies_to:
  stack:
  serverless:
---

# Azure AI Studio inference integration [infer-service-azure-ai-studio]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `azureaistudio` service.


## {{api-request-title}} [infer-service-azure-ai-studio-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-azure-ai-studio-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-azure-ai-studio-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `azureaistudio`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `azureaistudio` service.

    `api_key`
    :   (Required, string) A valid API key of your Azure AI Studio model deployment. This key can be found on the overview page for your deployment in the management section of your [Azure AI Studio](https://ai.azure.com/) account.

        ::::{important} 
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `target`
    :   (Required, string) The target URL of your Azure AI Studio model deployment. This can be found on the overview page for your deployment in the management section of your [Azure AI Studio](https://ai.azure.com/) account.

    `provider`
    :   (Required, string) The model provider for your deployment. Note that some providers may support only certain task types. Supported providers include:

        * `cohere` - available for `text_embedding` and `completion` task types
        * `databricks` - available for `completion` task type only
        * `meta` - available for `completion` task type only
        * `microsoft_phi` - available for `completion` task type only
        * `mistral` - available for `completion` task type only
        * `openai` - available for `text_embedding` and `completion` task types


    `endpoint_type`
    :   (Required, string) One of `token` or `realtime`. Specifies the type of endpoint that is used in your model deployment. There are [two endpoint types available](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/deployments-overview#billing-for-deploying-and-inferencing-llms-in-azure-ai-studio) for deployment through Azure AI Studio. "Pay as you go" endpoints are billed per token. For these, you must specify `token` for your `endpoint_type`. For "real-time" endpoints which are billed per hour of usage, specify `realtime`.

    `rate_limit`
    :   (Optional, object) By default, the `azureaistudio` service sets the number of requests allowed per minute to `240`. This helps to minimize the number of rate limit errors returned from Azure AI Studio. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `completion` task type
    `do_sample`
    :   (Optional, float) Instructs the inference process to perform sampling or not. Has no effect unless `temperature` or `top_p` is specified.

    `max_new_tokens`
    :   (Optional, integer) Provides a hint for the maximum number of output tokens to be generated. Defaults to 64.

    `temperature`
    :   (Optional, float) A number in the range of 0.0 to 2.0 that specifies the sampling temperature to use that controls the apparent creativity of generated completions. Should not be used if `top_p` is specified.

    `top_p`
    :   (Optional, float) A number in the range of 0.0 to 2.0 that is an alternative value to temperature that causes the model to consider the results of the tokens with nucleus sampling probability. Should not be used if `temperature` is specified.

    ::::


    ::::{dropdown} `task_settings` for the `text_embedding` task type
    `user`
    :   (optional, string) Specifies the user issuing the request, which can be used for abuse detection.

    ::::



## Azure AI Studio service example [inference-example-azureaistudio] 

The following example shows how to create an {{infer}} endpoint called `azure_ai_studio_embeddings` to perform a `text_embedding` task type. Note that we do not specify a model here, as it is defined already via our Azure AI Studio deployment.

The list of embeddings models that you can choose from in your deployment can be found in the [Azure AI Studio model explorer](https://ai.azure.com/explore/models?selectedTask=embeddings).

```console
PUT _inference/text_embedding/azure_ai_studio_embeddings
{
    "service": "azureaistudio",
    "service_settings": {
        "api_key": "<api_key>",
        "target": "<target_uri>",
        "provider": "<model_provider>",
        "endpoint_type": "<endpoint_type>"
    }
}
```
%  TEST[skip:TBD]

The next example shows how to create an {{infer}} endpoint called `azure_ai_studio_completion` to perform a `completion` task type.

```console
PUT _inference/completion/azure_ai_studio_completion
{
    "service": "azureaistudio",
    "service_settings": {
        "api_key": "<api_key>",
        "target": "<target_uri>",
        "provider": "<model_provider>",
        "endpoint_type": "<endpoint_type>"
    }
}
```
%  TEST[skip:TBD]

The list of chat completion models that you can choose from in your deployment can be found in the [Azure AI Studio model explorer](https://ai.azure.com/explore/models?selectedTask=chat-completion).

