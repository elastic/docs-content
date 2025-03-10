---
navigation_title: "Azure OpenAI"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-azure-openai.html
applies_to:
  stack:
  serverless:
---

# Azure OpenAI inference integration [infer-service-azure-openai]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `azureopenai` service.


## {{api-request-title}} [infer-service-azure-openai-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-azure-openai-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-azure-openai-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `azureopenai`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `azureopenai` service.

    `api_key` or `entra_id`
    :   (Required, string) You must provide *either* an API key or an Entra ID. If you do not provide either, or provide both, you will receive an error when trying to create your model. See the [Azure OpenAI Authentication documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#authentication) for more details on these authentication types.

        ::::{important} 
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `resource_name`
    :   (Required, string) The name of your Azure OpenAI resource. You can find this from the [list of resources](https://portal.azure.com/#view/HubsExtension/BrowseAll) in the Azure Portal for your subscription.

    `deployment_id`
    :   (Required, string) The deployment name of your deployed models. Your Azure OpenAI deployments can be found though the [Azure OpenAI Studio](https://oai.azure.com/) portal that is linked to your subscription.

    `api_version`
    :   (Required, string) The Azure API version ID to use. We recommend using the [latest supported non-preview version](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#embeddings).

    `rate_limit`
    :   (Optional, object) The `azureopenai` service sets a default number of requests allowed per minute depending on the task type. For `text_embedding` it is set to `1440`. For `completion` it is set to `120`. This helps to minimize the number of rate limit errors returned from Azure. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```

        More information about the rate limits for Azure can be found in the [Quota limits docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits) and [How to change the quotas](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/quota?tabs=rest).


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `completion` task type
    `user`
    :   (optional, string) Specifies the user issuing the request, which can be used for abuse detection.

    ::::


    ::::{dropdown} `task_settings` for the `text_embedding` task type
    `user`
    :   (optional, string) Specifies the user issuing the request, which can be used for abuse detection.

    ::::



## Azure OpenAI service example [inference-example-azure-openai] 

The following example shows how to create an {{infer}} endpoint called `azure_openai_embeddings` to perform a `text_embedding` task type. Note that we do not specify a model here, as it is defined already via our Azure OpenAI deployment.

The list of embeddings models that you can choose from in your deployment can be found in the [Azure models documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#embeddings).

```console
PUT _inference/text_embedding/azure_openai_embeddings
{
    "service": "azureopenai",
    "service_settings": {
        "api_key": "<api_key>",
        "resource_name": "<resource_name>",
        "deployment_id": "<deployment_id>",
        "api_version": "2024-02-01"
    }
}
```
%  TEST[skip:TBD]

The next example shows how to create an {{infer}} endpoint called `azure_openai_completion` to perform a `completion` task type.

```console
PUT _inference/completion/azure_openai_completion
{
    "service": "azureopenai",
    "service_settings": {
        "api_key": "<api_key>",
        "resource_name": "<resource_name>",
        "deployment_id": "<deployment_id>",
        "api_version": "2024-02-01"
    }
}
```
%  TEST[skip:TBD]

The list of chat completion models that you can choose from in your Azure OpenAI deployment can be found at the following places:

* [GPT-4 and GPT-4 Turbo models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#gpt-4-and-gpt-4-turbo-models)
* [GPT-3.5](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#gpt-35)

