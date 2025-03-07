---
navigation_title: "JinaAI"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/master/infer-service-jinaai.html
applies_to:
  stack:
  serverless:
---

# JinaAI inference integration [infer-service-jinaai]

:::{tip} Inference API reference  
Refer to the [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) for further information.  
:::

Creates an {{infer}} endpoint to perform an {{infer}} task with the `jinaai` service.


## {{api-request-title}} [infer-service-jinaai-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-jinaai-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `text_embedding`,
    * `rerank`.



## {{api-request-body-title}} [infer-service-jinaai-api-request-body] 

`chunking_settings`
:   (Optional, object) Chunking configuration object. Refer to [Configuring chunking](https://www.elastic.co/guide/en/elasticsearch/reference/master/inference-apis.html#infer-chunking-config) to learn more about chunking.

    `max_chunk_size`
    :   (Optional, integer) Specifies the maximum size of a chunk in words. Defaults to `250`. This value cannot be higher than `300` or lower than `20` (for `sentence` strategy) or `10` (for `word` strategy).

    `overlap`
    :   (Optional, integer) Only for `word` chunking strategy. Specifies the number of overlapping words for chunks. Defaults to `100`. This value cannot be higher than the half of `max_chunk_size`.

    `sentence_overlap`
    :   (Optional, integer) Only for `sentence` chunking strategy. Specifies the numnber of overlapping sentences for chunks. It can be either `1` or `0`. Defaults to `1`.

    `strategy`
    :   (Optional, string) Specifies the chunking strategy. It could be either `sentence` or `word`.


`service`
:   (Required, string) The type of service supported for the specified task type. In this case, `jinaai`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `jinaai` service.

    `api_key`
    :   (Required, string) A valid API key for your JinaAI account. You can find it at [https://jina.ai/embeddings/](https://jina.ai/embeddings/).

        ::::{important} 
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/guide/en/elasticsearch/reference/master/get-inference-api.html) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `rate_limit`
    :   (Optional, object) The default rate limit for the `jinaai` service is 2000 requests per minute for all task types. You can modify this using the `requests_per_minute` setting in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```

        More information about JinaAI’s rate limits can be found in [https://jina.ai/contact-sales/#rate-limit](https://jina.ai/contact-sales/#rate-limit).

        ::::{dropdown} `service_settings` for the `rerank` task type
        `model_id`
        :   (Required, string) The name of the model to use for the {{infer}} task. To review the available `rerank` compatible models, refer to [https://jina.ai/reranker](https://jina.ai/reranker).

        ::::


        ::::{dropdown} `service_settings` for the `text_embedding` task type
        `model_id`
        :   (Optional, string) The name of the model to use for the {{infer}} task. To review the available `text_embedding` models, refer to the [https://jina.ai/embeddings/](https://jina.ai/embeddings/).

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
    `task`
    :   (Optional, string) Specifies the task passed to the model. Valid values are:

        * `classification`: use it for embeddings passed through a text classifier.
        * `clustering`: use it for the embeddings run through a clustering algorithm.
        * `ingest`: use it for storing document embeddings in a vector database.
        * `search`: use it for storing embeddings of search queries run against a vector database to find relevant documents.


    ::::



## JinaAI service examples [inference-example-jinaai] 

The following examples demonstrate how to create {{infer}} endpoints for `text_embeddings` and `rerank` tasks using the JinaAI service and use them in search requests.

First, we create the `embeddings` service:

```console
PUT _inference/text_embedding/jinaai-embeddings
{
    "service": "jinaai",
    "service_settings": {
        "model_id": "jina-embeddings-v3",
        "api_key": "<api_key>"
    }
}
```
%  TEST[skip:uses ML]

Then, we create the `rerank` service:

```console
PUT _inference/rerank/jinaai-rerank
{
    "service": "jinaai",
    "service_settings": {
        "api_key": "<api_key>",
        "model_id": "jina-reranker-v2-base-multilingual"
    },
    "task_settings": {
        "top_n": 10,
        "return_documents": true
    }
}
```
%  TEST[skip:uses ML]

Now we can create an index that will use `jinaai-embeddings` service to index the documents.

```console
PUT jinaai-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": "jinaai-embeddings"
      }
    }
  }
}
```
%  TEST[skip:uses ML]

```console
PUT jinaai-index/_bulk
{ "index" : { "_index" : "jinaai-index", "_id" : "1" } }
{"content": "Sarah Johnson is a talented marine biologist working at the Oceanographic Institute. Her groundbreaking research on coral reef ecosystems has garnered international attention and numerous accolades."}
{ "index" : { "_index" : "jinaai-index", "_id" : "2" } }
{"content": "She spends months at a time diving in remote locations, meticulously documenting the intricate relationships between various marine species. "}
{ "index" : { "_index" : "jinaai-index", "_id" : "3" } }
{"content": "Her dedication to preserving these delicate underwater environments has inspired a new generation of conservationists."}
```
%  TEST[skip:uses ML]

Now, with the index created, we can search with and without the reranker service.

```console
GET jinaai-index/_search
{
  "query": {
    "semantic": {
      "field": "content",
      "query": "who inspired taking care of the sea?"
    }
  }
}
```
%  TEST[skip:uses ML]

```console
POST jinaai-index/_search
{
  "retriever": {
    "text_similarity_reranker": {
      "retriever": {
        "standard": {
          "query": {
            "semantic": {
              "field": "content",
              "query": "who inspired taking care of the sea?"
            }
          }
        }
      },
      "field": "content",
      "rank_window_size": 100,
      "inference_id": "jinaai-rerank",
      "inference_text": "who inspired taking care of the sea?"
    }
  }
}
```
%  TEST[skip:uses ML]

