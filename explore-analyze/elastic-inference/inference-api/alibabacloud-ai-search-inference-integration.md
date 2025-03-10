---
navigation_title: "Alibaba Cloud AI Search"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-alibabacloud-ai-search.html
applies_to:
  stack:
  serverless:
---

# AlibabaCloud AI Search inference integration [infer-service-alibabacloud-ai-search]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::  


Creates an {{infer}} endpoint to perform an {{infer}} task with the `alibabacloud-ai-search` service.


## {{api-request-title}} [infer-service-alibabacloud-ai-search-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-alibabacloud-ai-search-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `completion`,
    * `rerank`
    * `sparse_embedding`,
    * `text_embedding`.



## {{api-request-body-title}} [infer-service-alibabacloud-ai-search-api-request-body] 

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
:   (Required, string) The type of service supported for the specified task type. In this case, `alibabacloud-ai-search`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `alibabacloud-ai-search` service.

    `api_key`
    :   (Required, string) A valid API key for the AlibabaCloud AI Search API.

    `service_id`
    :   (Required, string) The name of the model service to use for the {{infer}} task.

        Available service_ids for the `completion` task:

        * `ops-qwen-turbo`
        * `qwen-turbo`
        * `qwen-plus`
        * `qwen-max` ÷ `qwen-max-longcontext`

        For the supported `completion` service_ids, refer to the [documentation](https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-generation-api-details).

        Available service_id for the `rerank` task is:

        * `ops-bge-reranker-larger`

        For the supported `rerank` service_id, refer to the [documentation](https://help.aliyun.com/zh/open-search/search-platform/developer-reference/ranker-api-details).

        Available service_id for the `sparse_embedding` task:

        * `ops-text-sparse-embedding-001`

        For the supported `sparse_embedding` service_id, refer to the [documentation](https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-sparse-embedding-api-details).

        Available service_ids for the `text_embedding` task:

        * `ops-text-embedding-001`
        * `ops-text-embedding-zh-001`
        * `ops-text-embedding-en-001`
        * `ops-text-embedding-002`

        For the supported `text_embedding` service_ids, refer to the [documentation](https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-embedding-api-details).


    `host`
    :   (Required, string) The name of the host address used for the {{infer}} task. You can find the host address at [the API keys section](https://opensearch.console.aliyun.com/cn-shanghai/rag/api-key) of the documentation.

    `workspace`
    :   (Required, string) The name of the workspace used for the {{infer}} task.

    `rate_limit`
    :   (Optional, object) By default, the `alibabacloud-ai-search` service sets the number of requests allowed per minute to `1000`. This helps to minimize the number of rate limit errors returned from AlibabaCloud AI Search. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```


`task_settings`
:   (Optional, object) Settings to configure the {{infer}} task. These settings are specific to the `<task_type>` you specified.

    ::::{dropdown} `task_settings` for the `text_embedding` task type
    `input_type`
    :   (Optional, string) Specifies the type of input passed to the model. Valid values are:

        * `ingest`: for storing document embeddings in a vector database.
        * `search`: for storing embeddings of search queries run against a vector database to find relevant documents.


    ::::


    ::::{dropdown} `task_settings` for the `sparse_embedding` task type
    `input_type`
    :   (Optional, string) Specifies the type of input passed to the model. Valid values are:

        * `ingest`: for storing document embeddings in a vector database.
        * `search`: for storing embeddings of search queries run against a vector database to find relevant documents.


    `return_token`
    :   (Optional, boolean) If `true`, the token name will be returned in the response. Defaults to `false` which means only the token ID will be returned in the response.

    ::::



## AlibabaCloud AI Search service examples [inference-example-alibabacloud-ai-search] 

The following example shows how to create an {{infer}} endpoint called `alibabacloud_ai_search_completion` to perform a `completion` task type.

```console
PUT _inference/completion/alibabacloud_ai_search_completion
{
    "service": "alibabacloud-ai-search",
    "service_settings": {
        "host" : "default-j01.platform-cn-shanghai.opensearch.aliyuncs.com",
        "api_key": "{{API_KEY}}",
        "service_id": "ops-qwen-turbo",
        "workspace" : "default"
    }
}
```
%  TEST[skip:TBD]

The next example shows how to create an {{infer}} endpoint called `alibabacloud_ai_search_rerank` to perform a `rerank` task type.

```console
PUT _inference/rerank/alibabacloud_ai_search_rerank
{
    "service": "alibabacloud-ai-search",
    "service_settings": {
        "api_key": "<api_key>",
        "service_id": "ops-bge-reranker-larger",
        "host": "default-j01.platform-cn-shanghai.opensearch.aliyuncs.com",
        "workspace": "default"
    }
}
```
%  TEST[skip:TBD]

The following example shows how to create an {{infer}} endpoint called `alibabacloud_ai_search_sparse` to perform a `sparse_embedding` task type.

```console
PUT _inference/sparse_embedding/alibabacloud_ai_search_sparse
{
    "service": "alibabacloud-ai-search",
    "service_settings": {
        "api_key": "<api_key>",
        "service_id": "ops-text-sparse-embedding-001",
        "host": "default-j01.platform-cn-shanghai.opensearch.aliyuncs.com",
        "workspace": "default"
    }
}
```
%  TEST[skip:TBD]

The following example shows how to create an {{infer}} endpoint called `alibabacloud_ai_search_embeddings` to perform a `text_embedding` task type.

```console
PUT _inference/text_embedding/alibabacloud_ai_search_embeddings
{
    "service": "alibabacloud-ai-search",
    "service_settings": {
        "api_key": "<api_key>",
        "service_id": "ops-text-embedding-001",
        "host": "default-j01.platform-cn-shanghai.opensearch.aliyuncs.com",
        "workspace": "default"
    }
}
```
%  TEST[skip:TBD]

