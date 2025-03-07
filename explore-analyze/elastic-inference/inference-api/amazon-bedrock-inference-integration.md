---
navigation_title: "Amazon Bedrock"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-amazon-bedrock.html
applies_to:
  stack:
  serverless:
---

# Amazon Bedrock inference integration [infer-service-amazon-bedrock]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `amazonbedrock` service.


## {{api-request-title}} [infer-service-amazon-bedrock-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-amazon-bedrock-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-amazon-bedrock-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `amazonbedrock`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `amazonbedrock` service.

    `access_key`
    :   (Required, string) A valid AWS access key that has permissions to use Amazon Bedrock and access to models for inference requests.

    `secret_key`
    :   (Required, string) A valid AWS secret key that is paired with the `access_key`. To create or manage access and secret keys, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.md) in the AWS documentation.


::::{important} 
You need to provide the access and secret keys only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not retrieve your access or secret keys. After creating the {{infer}} model, you cannot change the associated key pairs. If you want to use a different access and secret key pair, delete the {{infer}} model and recreate it with the same name and the updated keys.
::::


`provider`
:   (Required, string) The model provider for your deployment. Note that some providers may support only certain task types. Supported providers include:

    * `amazontitan` - available for `text_embedding` and `completion` task types
    * `anthropic` - available for `completion` task type only
    * `ai21labs` - available for `completion` task type only
    * `cohere` - available for `text_embedding` and `completion` task types
    * `meta` - available for `completion` task type only
    * `mistral` - available for `completion` task type only


`model`
:   (Required, string) The base model ID or an ARN to a custom model based on a foundational model. The base model IDs can be found in the [Amazon Bedrock model IDs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html) documentation. Note that the model ID must be available for the provider chosen, and your IAM user must have access to the model.

`region`
:   (Required, string) The region that your model or ARN is deployed in. The list of available regions per model can be found in the [Model support by AWS region](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) documentation.

`rate_limit`
:   (Optional, object) By default, the `amazonbedrock` service sets the number of requests allowed per minute to `240`. This helps to minimize the number of rate limit errors returned from Amazon Bedrock. To modify this, set the `requests_per_minute` setting of this object in your service settings:

    ```text
    "rate_limit": {
        "requests_per_minute": <<number_of_requests>>
    }
    ```

    `task_settings`
    :   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `completion` task type
    `max_new_tokens`
    :   (Optional, integer) Sets the maximum number for the output tokens to be generated. Defaults to 64.

    `temperature`
    :   (Optional, float) A number between 0.0 and 1.0 that controls the apparent creativity of the results. At temperature 0.0 the model is most deterministic, at temperature 1.0 most random. Should not be used if `top_p` or `top_k` is specified.

    `top_p`
    :   (Optional, float) Alternative to `temperature`. A number in the range of 0.0 to 1.0, to eliminate low-probability tokens. Top-p uses nucleus sampling to select top tokens whose sum of likelihoods does not exceed a certain value, ensuring both variety and coherence. Should not be used if `temperature` is specified.

    `top_k`
    :   (Optional, float) Only available for `anthropic`, `cohere`, and `mistral` providers. Alternative to `temperature`. Limits samples to the top-K most likely words, balancing coherence and variability. Should not be used if `temperature` is specified.

    ::::



## Amazon Bedrock service example [inference-example-amazonbedrock] 

The following example shows how to create an {{infer}} endpoint called `amazon_bedrock_embeddings` to perform a `text_embedding` task type.

Choose chat completion and embeddings models that you have access to from the [Amazon Bedrock base models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html).

```console
PUT _inference/text_embedding/amazon_bedrock_embeddings
{
    "service": "amazonbedrock",
    "service_settings": {
        "access_key": "<aws_access_key>",
        "secret_key": "<aws_secret_key>",
        "region": "us-east-1",
        "provider": "amazontitan",
        "model": "amazon.titan-embed-text-v2:0"
    }
}
```
%  TEST[skip:TBD]

The next example shows how to create an {{infer}} endpoint called `amazon_bedrock_completion` to perform a `completion` task type.

```console
PUT _inference/completion/amazon_bedrock_completion
{
    "service": "amazonbedrock",
    "service_settings": {
        "access_key": "<aws_access_key>",
        "secret_key": "<aws_secret_key>",
        "region": "us-east-1",
        "provider": "amazontitan",
        "model": "amazon.titan-text-premier-v1:0"
    }
}
```
%  TEST[skip:TBD]

