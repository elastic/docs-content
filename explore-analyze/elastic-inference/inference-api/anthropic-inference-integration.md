---
navigation_title: "Anthropic"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-anthropic.html
applies_to:
  stack:
  serverless:
---

# Anthropic inference integration [infer-service-anthropic]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `anthropic` service.


## {{api-request-title}} [infer-service-anthropic-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-anthropic-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`



## {{api-request-body-title}} [infer-service-anthropic-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `anthropic`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `anthropic` service.

    `api_key`
    :   (Required, string) A valid API key for the Anthropic API.

    `model_id`
    :   (Required, string) The name of the model to use for the {{infer}} task. You can find the supported models at [Anthropic models](https://docs.anthropic.com/en/docs/about-claude/models#model-names).

    `rate_limit`
    :   (Optional, object) By default, the `anthropic` service sets the number of requests allowed per minute to `50`. This helps to minimize the number of rate limit errors returned from Anthropic. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```


`task_settings`
:   (Required, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `completion` task type
    `max_tokens`
    :   (Required, integer) The maximum number of tokens to generate before stopping.

    `temperature`
    :   (Optional, float) The amount of randomness injected into the response.

        For more details about the supported range, see the [Anthropic messages API](https://docs.anthropic.com/en/api/messages).


    `top_k`
    :   (Optional, integer) Specifies to only sample from the top K options for each subsequent token.

        Recommended for advanced use cases only. You usually only need to use `temperature`.

        For more details, see the [Anthropic messages API](https://docs.anthropic.com/en/api/messages).


    `top_p`
    :   (Optional, float) Specifies to use Anthropic’s nucleus sampling.

        In nucleus sampling, Anthropic computes the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

        Recommended for advanced use cases only. You usually only need to use `temperature`.

        For more details, see the [Anthropic messages API](https://docs.anthropic.com/en/api/messages).


    ::::



## Anthropic service example [inference-example-anthropic] 

The following example shows how to create an {{infer}} endpoint called `anthropic_completion` to perform a `completion` task type.

```console
PUT _inference/completion/anthropic_completion
{
    "service": "anthropic",
    "service_settings": {
        "api_key": "<api_key>",
        "model_id": "<model_id>"
    },
    "task_settings": {
        "max_tokens": 1024
    }
}
```
%  TEST[skip:TBD]

