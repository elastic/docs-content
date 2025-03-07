---
navigation_title: "Cohere"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-cohere.html
applies_to:
  stack:
  serverless:
---

# Cohere inference integration [infer-service-cohere]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `cohere` service.


## {{api-request-title}} [infer-service-cohere-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-cohere-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`,
    * `rerank`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-cohere-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `cohere`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `cohere` service.

    `api_key`
    :   (Required, string) A valid API key of your Cohere account. You can find your Cohere API keys or you can create a new one [on the API keys settings page](https://dashboard.cohere.com/api-keys).

        ::::{important} 
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `rate_limit`
    :   (Optional, object) By default, the `cohere` service sets the number of requests allowed per minute to `10000`. This value is the same for all task types. This helps to minimize the number of rate limit errors returned from Cohere. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```

        More information about Cohere’s rate limits can be found in [Cohere’s production key docs](https://docs.cohere.com/docs/going-live#production-key-specifications).

        ::::{dropdown} `service_settings` for the `completion` task type
        `model_id`
        :   (Optional, string) The name of the model to use for the {{infer}} task. To review the available `completion` models, refer to the [Cohere docs](https://docs.cohere.com/docs/models#command).

        ::::


        ::::{dropdown} `service_settings` for the `rerank` task type
        `model_id`
        :   (Optional, string) The name of the model to use for the {{infer}} task. To review the available `rerank` models, refer to the [Cohere docs](https://docs.cohere.com/reference/rerank-1).

        ::::


        ::::{dropdown} `service_settings` for the `text_embedding` task type
        `embedding_type`
        :   (Optional, string) Specifies the types of embeddings you want to get back. Defaults to `float`. Valid values are:

            * `byte`: use it for signed int8 embeddings (this is a synonym of `int8`).
            * `float`: use it for the default float embeddings.
            * `int8`: use it for signed int8 embeddings.


        `model_id`
        :   (Optional, string) The name of the model to use for the {{infer}} task. To review the available `text_embedding` models, refer to the [Cohere docs](https://docs.cohere.com/reference/embed). The default value for `text_embedding` is `embed-english-v2.0`.

        `similarity`
        :   (Optional, string) Similarity measure. One of `cosine`, `dot_product`, `l2_norm`. Defaults based on the `embedding_type` (`float` → `dot_product`, `int8/byte` → `cosine`).

        ::::


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `rerank` task type
    `return_documents`
    :   (Optional, boolean) Specify whether to return doc text within the results.

    `top_n`
    :   (Optional, integer) The number of most relevant documents to return, defaults to the number of the documents. If this {{infer}} endpoint is used in a `text_similarity_reranker` retriever query and `top_n` is set, it must be greater than or equal to `rank_window_size` in the query.

    ::::


    ::::{dropdown} `task_settings` for the `text_embedding` task type
    `input_type`
    :   (Optional, string) Specifies the type of input passed to the model. Valid values are:

        * `classification`: use it for embeddings passed through a text classifier.
        * `clusterning`: use it for the embeddings run through a clustering algorithm.
        * `ingest`: use it for storing document embeddings in a vector database.
        * `search`: use it for storing embeddings of search queries run against a vector database to find relevant documents.

            ::::{important} 
            The `input_type` field is required when using embedding models `v3` and higher.
            ::::


    `truncate`
    :   (Optional, string) Specifies how the API handles inputs longer than the maximum token length. Defaults to `END`. Valid values are:

        * `NONE`: when the input exceeds the maximum input token length an error is returned.
        * `START`: when the input exceeds the maximum input token length the start of the input is discarded.
        * `END`: when the input exceeds the maximum input token length the end of the input is discarded.


    ::::



## Cohere service examples [inference-example-cohere] 

The following example shows how to create an {{infer}} endpoint called `cohere-embeddings` to perform a `text_embedding` task type.

```console
PUT _inference/text_embedding/cohere-embeddings
{
    "service": "cohere",
    "service_settings": {
        "api_key": "<api_key>",
        "model_id": "embed-english-light-v3.0",
        "embedding_type": "byte"
    }
}
```
%  TEST[skip:TBD]

The following example shows how to create an {{infer}} endpoint called `cohere-rerank` to perform a `rerank` task type.

```console
PUT _inference/rerank/cohere-rerank
{
    "service": "cohere",
    "service_settings": {
        "api_key": "<API-KEY>",
        "model_id": "rerank-english-v3.0"
    },
    "task_settings": {
        "top_n": 10,
        "return_documents": true
    }
}
```
%  TEST[skip:TBD]

For more examples, also review the [Cohere documentation](https://docs.cohere.com/docs/elasticsearch-and-cohere#rerank-search-results-with-cohere-and-elasticsearch).

