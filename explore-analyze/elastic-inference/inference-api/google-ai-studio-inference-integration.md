---
navigation_title: "Google AI Studio"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-google-ai-studio.html
applies_to:
  stack:
  serverless:
---

# Google AI Studio inference integration [infer-service-google-ai-studio]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `googleaistudio` service.


## {{api-request-title}} [infer-service-google-ai-studio-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-google-ai-studio-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-google-ai-studio-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `googleaistudio`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `googleaistudio` service.

    `api_key`
    :   (Required, string) A valid API key for the Google Gemini API.

    `model_id`
    :   (Required, string) The name of the model to use for the {{infer}} task. You can find the supported models at [Gemini API models](https://ai.google.dev/gemini-api/docs/models/gemini).

    `rate_limit`
    :   (Optional, object) By default, the `googleaistudio` service sets the number of requests allowed per minute to `360`. This helps to minimize the number of rate limit errors returned from Google AI Studio. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```



## Google AI Studio service example [inference-example-google-ai-studio] 

The following example shows how to create an {{infer}} endpoint called `google_ai_studio_completion` to perform a `completion` task type.

```console
PUT _inference/completion/google_ai_studio_completion
{
    "service": "googleaistudio",
    "service_settings": {
        "api_key": "<api_key>",
        "model_id": "<model_id>"
    }
}
```
%  TEST[skip:TBD]

