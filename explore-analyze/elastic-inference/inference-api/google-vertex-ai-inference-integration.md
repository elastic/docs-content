---
navigation_title: "Google Vertex AI"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-google-vertex-ai.html
applies_to:
  stack:
  serverless:
---

# Google Vertex AI inference integration [infer-service-google-vertex-ai]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `googlevertexai` service.


## {{api-request-title}} [infer-service-google-vertex-ai-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-google-vertex-ai-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `rerank`
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-google-vertex-ai-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `googlevertexai`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `googlevertexai` service.

    `service_account_json`
    :   (Required, string) A valid service account in json format for the Google Vertex AI API.

    `model_id`
    :   (Required, string) The name of the model to use for the {{infer}} task. You can find the supported models at [Text embeddings API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api).

    `location`
    :   (Required, string) The name of the location to use for the {{infer}} task. You find the supported locations at [Generative AI on Vertex AI locations](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations).

    `project_id`
    :   (Required, string) The name of the project to use for the {{infer}} task.

    `rate_limit`
    :   (Optional, object) By default, the `googlevertexai` service sets the number of requests allowed per minute to `30.000`. This helps to minimize the number of rate limit errors returned from Google Vertex AI. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```

        More information about the rate limits for Google Vertex AI can be found in the [Google Vertex AI Quotas docs](https://cloud.google.com/vertex-ai/docs/quotas).


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `rerank` task type
    `top_n`
    :   (optional, boolean) Specifies the number of the top n documents, which should be returned.

    ::::


    ::::{dropdown} `task_settings` for the `text_embedding` task type
    `auto_truncate`
    :   (optional, boolean) Specifies if the API truncates inputs longer than the maximum token length automatically.

    ::::



## Google Vertex AI service example [inference-example-google-vertex-ai] 

The following example shows how to create an {{infer}} endpoint called `google_vertex_ai_embeddings` to perform a `text_embedding` task type.

```console
PUT _inference/text_embedding/google_vertex_ai_embeddings
{
    "service": "googlevertexai",
    "service_settings": {
        "service_account_json": "<service_account_json>",
        "model_id": "<model_id>",
        "location": "<location>",
        "project_id": "<project_id>"
    }
}
```
%  TEST[skip:TBD]

The next example shows how to create an {{infer}} endpoint called `google_vertex_ai_rerank` to perform a `rerank` task type.

```console
PUT _inference/rerank/google_vertex_ai_rerank
{
    "service": "googlevertexai",
    "service_settings": {
        "service_account_json": "<service_account_json>",
        "project_id": "<project_id>"
    }
}
```
%  TEST[skip:TBD]

