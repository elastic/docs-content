---
navigation_title: "Semantic search with the {{infer}} API"
---

# Tutorial: semantic search with the {{infer}} API [semantic-search-inference]


The instructions in this tutorial shows you how to use the {{infer}} API workflow with various services to perform semantic search on your data.

::::{important}
For the easiest way to perform semantic search in the {{stack}}, refer to the [`semantic_text`](../../../solutions/search/semantic-search/semantic-search-semantic-text.md) end-to-end tutorial.
::::


The following examples use the:

* `embed-english-v3.0` model for [Cohere](https://docs.cohere.com/docs/cohere-embed)
* `all-mpnet-base-v2` model from [HuggingFace](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)
* `text-embedding-ada-002` second generation embedding model for OpenAI
* models available through [Azure AI Studio](https://ai.azure.com/explore/models?selectedTask=embeddings) or [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)
* `text-embedding-004` model for [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api)
* `mistral-embed` model for [Mistral](https://docs.mistral.ai/getting-started/models/)
* `amazon.titan-embed-text-v1` model for [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.md)
* `ops-text-embedding-zh-001` model for [AlibabaCloud AI](https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-embedding-api-details)

You can use any Cohere and OpenAI models, they are all supported by the {{infer}} API. For a list of recommended models available on HuggingFace, refer to [the supported model list](../../../solutions/search/inference-api/huggingface-inference-integration.md#inference-example-hugging-face-supported-models).

Click the name of the service you want to use on any of the widgets below to review the corresponding instructions.


## Requirements [infer-service-requirements]

:::::::{tab-set}

::::::{tab-item} Cohere
A [Cohere account](https://cohere.com/) is required to use the {{infer}} API with the Cohere service.
::::::

::::::{tab-item} ELSER
ELSER is a model trained by Elastic. If you have an {{es}} deployment, there is no further requirement for using the {{infer}} API with the `elasticsearch` service.
::::::

::::::{tab-item} HuggingFace
A [HuggingFace account](https://huggingface.co/) is required to use the {{infer}} API with the HuggingFace service.
::::::

::::::{tab-item} OpenAI
An [OpenAI account](https://openai.com/) is required to use the {{infer}} API with the OpenAI service.
::::::

::::::{tab-item} Azure OpenAI
* An [Azure subscription](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
* Access granted to Azure OpenAI in the desired Azure subscription. You can apply for access to Azure OpenAI by completing the form at [https://aka.ms/oai/access](https://aka.ms/oai/access).
* An embedding model deployed in [Azure OpenAI Studio](https://oai.azure.com/).
::::::

::::::{tab-item} Azure AI Studio
* An [Azure subscription](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
* Access to [Azure AI Studio](https://ai.azure.com/)
* A deployed [embeddings](https://ai.azure.com/explore/models?selectedTask=embeddings) or [chat completion](https://ai.azure.com/explore/models?selectedTask=chat-completion) model.
::::::

::::::{tab-item} Google Vertex AI
* A [Google Cloud account](https://console.cloud.google.com/)
* A project in Google Cloud
* The Vertex AI API enabled in your project
* A valid service account for the Google Vertex AI API
* The service account must have the Vertex AI User role and the `aiplatform.endpoints.predict` permission.
::::::

::::::{tab-item} Mistral
* A Mistral Account on [La Plateforme](https://console.mistral.ai/)
* An API key generated for your account
::::::

::::::{tab-item} Amazon Bedrock
* An AWS Account with [Amazon Bedrock](https://aws.amazon.com/bedrock/) access
* A pair of access and secret keys used to access Amazon Bedrock
::::::

::::::{tab-item} AlibabaCloud AI Search
* An AlibabaCloud Account with [AlibabaCloud](https://console.aliyun.com) access
* An API key generated for your account from the [API keys section](https://opensearch.console.aliyun.com/cn-shanghai/rag/api-key)
::::::

:::::::

## Create an inference endpoint [infer-text-embedding-task]

Create an {{infer}} endpoint by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put):

:::::::{tab-set}

::::::{tab-item} Cohere
```console
PUT _inference/text_embedding/cohere_embeddings <1>
{
    "service": "cohere",
    "service_settings": {
        "api_key": "<api_key>", <2>
        "model_id": "embed-english-v3.0", <3>
        "embedding_type": "byte"
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `cohere_embeddings`.
2. The API key of your Cohere account. You can find your API keys in your Cohere dashboard under the [API keys section](https://dashboard.cohere.com/api-keys). You need to provide your API key only once. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not return your API key.
3. The name of the embedding model to use. You can find the list of Cohere embedding models [here](https://docs.cohere.com/reference/embed).


::::{note}
When using this model the recommended similarity measure to use in the `dense_vector` field mapping is `dot_product`. In the case of Cohere models, the embeddings are normalized to unit length in which case the `dot_product` and the `cosine` measures are equivalent.
::::
::::::

::::::{tab-item} ELSER
```console
PUT _inference/sparse_embedding/elser_embeddings <1>
{
  "service": "elasticsearch",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1
  }
}
```

1. The task type is `sparse_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `elser_embeddings`.


You don’t need to download and deploy the ELSER model upfront, the API request above will download the model if it’s not downloaded yet and then deploy it.

::::{note}
You might see a 502 bad gateway error in the response when using the {{kib}} Console. This error usually just reflects a timeout, while the model downloads in the background. You can check the download progress in the {{ml-app}} UI. If using the Python client, you can set the `timeout` parameter to a higher value.

::::
::::::

::::::{tab-item} HuggingFace
First, you need to create a new {{infer}} endpoint on [the Hugging Face endpoint page](https://ui.endpoints.huggingface.co/) to get an endpoint URL. Select the model `all-mpnet-base-v2` on the new endpoint creation page, then select the `Sentence Embeddings` task under the Advanced configuration section. Create the endpoint. Copy the URL after the endpoint initialization has been finished, you need the URL in the following {{infer}} API call.

```console
PUT _inference/text_embedding/hugging_face_embeddings <1>
{
  "service": "hugging_face",
  "service_settings": {
    "api_key": "<access_token>", <2>
    "url": "<url_endpoint>" <3>
  }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `hugging_face_embeddings`.
2. A valid HuggingFace access token. You can find on the [settings page of your account](https://huggingface.co/settings/tokens).
3. The {{infer}} endpoint URL you created on Hugging Face.
::::::

::::::{tab-item} OpenAI
```console
PUT _inference/text_embedding/openai_embeddings <1>
{
    "service": "openai",
    "service_settings": {
        "api_key": "<api_key>", <2>
        "model_id": "text-embedding-ada-002" <3>
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `openai_embeddings`.
2. The API key of your OpenAI account. You can find your OpenAI API keys in your OpenAI account under the [API keys section](https://platform.openai.com/api-keys). You need to provide your API key only once. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not return your API key.
3. The name of the embedding model to use. You can find the list of OpenAI embedding models [here](https://platform.openai.com/docs/guides/embeddings/embedding-models).


::::{note}
When using this model the recommended similarity measure to use in the `dense_vector` field mapping is `dot_product`. In the case of OpenAI models, the embeddings are normalized to unit length in which case the `dot_product` and the `cosine` measures are equivalent.
::::
::::::

::::::{tab-item} Azure OpenAI
```console
PUT _inference/text_embedding/azure_openai_embeddings <1>
{
    "service": "azureopenai",
    "service_settings": {
        "api_key": "<api_key>", <2>
        "resource_name": "<resource_name>", <3>
        "deployment_id": "<deployment_id>", <4>
        "api_version": "2024-02-01"
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `azure_openai_embeddings`.
2. The API key for accessing your Azure OpenAI services. Alternately, you can provide an `entra_id` instead of an `api_key` here. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not return this information.
3. The name our your Azure resource.
4. The id of your deployed model.


::::{note}
It may take a few minutes for your model’s deployment to become available after it is created. If you try and create the model as above and receive a `404` error message, wait a few minutes and try again. Also, when using this model the recommended similarity measure to use in the `dense_vector` field mapping is `dot_product`. In the case of Azure OpenAI models, the embeddings are normalized to unit length in which case the `dot_product` and the `cosine` measures are equivalent.
::::
::::::

::::::{tab-item} Azure AI Studio
```console
PUT _inference/text_embedding/azure_ai_studio_embeddings <1>
{
    "service": "azureaistudio",
    "service_settings": {
        "api_key": "<api_key>", <2>
        "target": "<target_uri>", <3>
        "provider": "<provider>", <4>
        "endpoint_type": "<endpoint_type>" <5>
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `azure_ai_studio_embeddings`.
2. The API key for accessing your Azure AI Studio deployed model. You can find this on your model deployment’s overview page.
3. The target URI for accessing your Azure AI Studio deployed model. You can find this on your model deployment’s overview page.
4. The model provider, such as `cohere` or `openai`.
5. The deployed endpoint type. This can be `token` (for "pay as you go" deployments), or `realtime` for real-time deployment endpoints.


::::{note}
It may take a few minutes for your model’s deployment to become available after it is created. If you try and create the model as above and receive a `404` error message, wait a few minutes and try again. Also, when using this model the recommended similarity measure to use in the `dense_vector` field mapping is `dot_product`.
::::
::::::

::::::{tab-item} Google Vertex AI
```console
PUT _inference/text_embedding/google_vertex_ai_embeddings <1>
{
    "service": "googlevertexai",
    "service_settings": {
        "service_account_json": "<service_account_json>", <2>
        "model_id": "text-embedding-004", <3>
        "location": "<location>", <4>
        "project_id": "<project_id>" <5>
    }
}
```

1. The task type is `text_embedding` per the path. `google_vertex_ai_embeddings` is the unique identifier of the {{infer}} endpoint (its `inference_id`).
2. A valid service account in JSON format for the Google Vertex AI API.
3. For the list of the available models, refer to the [Text embeddings API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api) page.
4. The name of the location to use for the {{infer}} task. Refer to [Generative AI on Vertex AI locations](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) for available locations.
5. The name of the project to use for the {{infer}} task.
::::::

::::::{tab-item} Mistral
```console
PUT _inference/text_embedding/mistral_embeddings <1>
{
    "service": "mistral",
    "service_settings": {
        "api_key": "<api_key>", <2>
        "model": "<model_id>" <3>
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `mistral_embeddings`.
2. The API key for accessing the Mistral API. You can find this in your Mistral account’s API Keys page.
3. The Mistral embeddings model name, for example `mistral-embed`.
::::::

::::::{tab-item} Amazon Bedrock
```console
PUT _inference/text_embedding/amazon_bedrock_embeddings <1>
{
    "service": "amazonbedrock",
    "service_settings": {
        "access_key": "<aws_access_key>", <2>
        "secret_key": "<aws_secret_key>", <3>
        "region": "<region>", <4>
        "provider": "<provider>", <5>
        "model": "<model_id>" <6>
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `amazon_bedrock_embeddings`.
2. The access key can be found on your AWS IAM management page for the user account to access Amazon Bedrock.
3. The secret key should be the paired key for the specified access key.
4. Specify the region that your model is hosted in.
5. Specify the model provider.
6. The model ID or ARN of the model to use.
::::::

::::::{tab-item} AlibabaCloud AI Search
```console
PUT _inference/text_embedding/alibabacloud_ai_search_embeddings <1>
{
    "service": "alibabacloud-ai-search",
    "service_settings": {
        "api_key": "<api_key>", <2>
        "service_id": "<service_id>", <3>
        "host": "<host>", <4>
        "workspace": "<workspace>" <5>
    }
}
```

1. The task type is `text_embedding` in the path and the `inference_id` which is the unique identifier of the {{infer}} endpoint is `alibabacloud_ai_search_embeddings`.
2. The API key for accessing the AlibabaCloud AI Search API. You can find your API keys in your AlibabaCloud account under the [API keys section](https://opensearch.console.aliyun.com/cn-shanghai/rag/api-key). You need to provide your API key only once. The [Get {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-get) does not return your API key.
3. The AlibabaCloud AI Search embeddings model name, for example `ops-text-embedding-zh-001`.
4. The name our your AlibabaCloud AI Search host address.
5. The name our your AlibabaCloud AI Search workspace.
::::::

:::::::

## Create the index mapping [infer-service-mappings]

The mapping of the destination index - the index that contains the embeddings that the model will create based on your input text - must be created. The destination index must have a field with the [`dense_vector`](https://www.elastic.co/guide/en/elasticsearch/reference/current/dense-vector.html) field type for most models and the [`sparse_vector`](https://www.elastic.co/guide/en/elasticsearch/reference/current/sparse-vector.html) field type for the sparse vector models like in the case of the `elasticsearch` service to index the output of the used model.

:::::::{tab-set}

::::::{tab-item} Cohere
```console
PUT cohere-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1024, <3>
        "element_type": "byte"
      },
      "content": { <4>
        "type": "text" <5>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be refrenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. Find this value in the [Cohere documentation](https://docs.cohere.com/reference/embed) of the model you use.
4. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
5. The field type which is text in this example.
::::::

::::::{tab-item} ELSER
```console
PUT elser-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "sparse_vector" <2>
      },
      "content": { <3>
        "type": "text" <4>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be refrenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `sparse_vector` field for ELSER.
3. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
4. The field type which is text in this example.
::::::

::::::{tab-item} HuggingFace
```console
PUT hugging-face-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 768, <3>
        "element_type": "float"
      },
      "content": { <4>
        "type": "text" <5>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. Find this value in the [HuggingFace model documentation](https://huggingface.co/sentence-transformers/all-mpnet-base-v2).
4. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
5. The field type which is text in this example.
::::::

::::::{tab-item} OpenAI
```console
PUT openai-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1536, <3>
        "element_type": "float",
        "similarity": "dot_product" <4>
      },
      "content": { <5>
        "type": "text" <6>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. Find this value in the [OpenAI documentation](https://platform.openai.com/docs/guides/embeddings/embedding-models) of the model you use.
4. The faster` dot_product` function can be used to calculate similarity because OpenAI embeddings are normalised to unit length. You can check the [OpenAI docs](https://platform.openai.com/docs/guides/embeddings/which-distance-function-should-i-use) about which similarity function to use.
5. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
6. The field type which is text in this example.
::::::

::::::{tab-item} Azure OpenAI
```console
PUT azure-openai-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1536, <3>
        "element_type": "float",
        "similarity": "dot_product" <4>
      },
      "content": { <5>
        "type": "text" <6>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. Find this value in the [Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#embeddings-models) of the model you use.
4. For Azure OpenAI embeddings, the `dot_product` function should be used to calculate similarity as Azure OpenAI embeddings are normalised to unit length. See the [Azure OpenAI embeddings](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/understand-embeddings) documentation for more information on the model specifications.
5. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
6. The field type which is text in this example.
::::::

::::::{tab-item} Azure AI Studio
```console
PUT azure-ai-studio-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1536, <3>
        "element_type": "float",
        "similarity": "dot_product" <4>
      },
      "content": { <5>
        "type": "text" <6>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. This value may be found on the model card in your Azure AI Studio deployment.
4. For Azure AI Studio embeddings, the `dot_product` function should be used to calculate similarity.
5. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
6. The field type which is text in this example.
::::::

::::::{tab-item} Google Vertex AI
```console
PUT google-vertex-ai-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 768, <3>
        "element_type": "float",
        "similarity": "dot_product" <4>
      },
      "content": { <5>
        "type": "text" <6>
      }
    }
  }
}
```

1. The name of the field to contain the generated embeddings. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the embeddings is a `dense_vector` field.
3. The output dimensions of the model. This value may be found on the [Google Vertex AI model reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api). The {{infer}} API attempts to calculate the output dimensions automatically if `dims` are not specified.
4. For Google Vertex AI embeddings, the `dot_product` function should be used to calculate similarity.
5. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
6. The field type which is `text` in this example.
::::::

::::::{tab-item} Mistral
```console
PUT mistral-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1024, <3>
        "element_type": "float",
        "similarity": "dot_product" <4>
      },
      "content": { <5>
        "type": "text" <6>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. This value may be found on the [Mistral model reference](https://docs.mistral.ai/getting-started/models/).
4. For Mistral embeddings, the `dot_product` function should be used to calculate similarity.
5. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
6. The field type which is text in this example.
::::::

::::::{tab-item} Amazon Bedrock
```console
PUT amazon-bedrock-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1024, <3>
        "element_type": "float",
        "similarity": "dot_product" <4>
      },
      "content": { <5>
        "type": "text" <6>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. This value may be different depending on the underlying model used. See the [Amazon Titan model](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-multiemb-models.md) or the [Cohere Embeddings model](https://docs.cohere.com/reference/embed) documentation.
4. For Amazon Bedrock embeddings, the `dot_product` function should be used to calculate similarity for Amazon titan models, or `cosine` for Cohere models.
5. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
6. The field type which is text in this example.
::::::

::::::{tab-item} AlibabaCloud AI Search
```console
PUT alibabacloud-ai-search-embeddings
{
  "mappings": {
    "properties": {
      "content_embedding": { <1>
        "type": "dense_vector", <2>
        "dims": 1024, <3>
        "element_type": "float"
      },
      "content": { <4>
        "type": "text" <5>
      }
    }
  }
}
```

1. The name of the field to contain the generated tokens. It must be referenced in the {{infer}} pipeline configuration in the next step.
2. The field to contain the tokens is a `dense_vector` field.
3. The output dimensions of the model. This value may be different depending on the underlying model used. See the [AlibabaCloud AI Search embedding model](https://help.aliyun.com/zh/open-search/search-platform/developer-reference/text-embedding-api-details) documentation.
4. The name of the field from which to create the dense vector representation. In this example, the name of the field is `content`. It must be referenced in the {{infer}} pipeline configuration in the next step.
5. The field type which is text in this example.
::::::

:::::::

## Create an ingest pipeline with an inference processor [infer-service-inference-ingest-pipeline]

Create an [ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) with an [{{infer}} processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/inference-processor.html) and use the model you created above to infer against the data that is being ingested in the pipeline.

:::::::{tab-set}

::::::{tab-item} Cohere
```console
PUT _ingest/pipeline/cohere_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "cohere_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} ELSER
```console
PUT _ingest/pipeline/elser_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "elser_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} HuggingFace
```console
PUT _ingest/pipeline/hugging_face_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "hugging_face_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} OpenAI
```console
PUT _ingest/pipeline/openai_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "openai_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} Azure OpenAI
```console
PUT _ingest/pipeline/azure_openai_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "azure_openai_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} Azure AI Studio
```console
PUT _ingest/pipeline/azure_ai_studio_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "azure_ai_studio_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} Google Vertex AI
```console
PUT _ingest/pipeline/google_vertex_ai_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "google_vertex_ai_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} Mistral
```console
PUT _ingest/pipeline/mistral_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "mistral_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} Amazon Bedrock
```console
PUT _ingest/pipeline/amazon_bedrock_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "amazon_bedrock_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

::::::{tab-item} AlibabaCloud AI Search
```console
PUT _ingest/pipeline/alibabacloud_ai_search_embeddings_pipeline
{
  "processors": [
    {
      "inference": {
        "model_id": "alibabacloud_ai_search_embeddings", <1>
        "input_output": { <2>
          "input_field": "content",
          "output_field": "content_embedding"
        }
      }
    }
  ]
}
```

1. The name of the inference endpoint you created by using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put), it’s referred to as `inference_id` in that step.
2. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.
::::::

:::::::

## Load data [infer-load-data]

In this step, you load the data that you later use in the {{infer}} ingest pipeline to create embeddings from it.

Use the `msmarco-passagetest2019-top1000` data set, which is a subset of the MS MARCO Passage Ranking data set. It consists of 200 queries, each accompanied by a list of relevant text passages. All unique passages, along with their IDs, have been extracted from that data set and compiled into a [tsv file](https://github.com/elastic/stack-docs/blob/main/docs/en/stack/ml/nlp/data/msmarco-passagetest2019-unique.tsv).

Download the file and upload it to your cluster using the [Data Visualizer](../../../manage-data/ingest/upload-data-files.md) in the {{ml-app}} UI. After your data is analyzed, click **Override settings**. Under **Edit field names***, assign `id` to the first column and `content` to the second. Click ***Apply***, then ***Import**. Name the index `test-data`, and click **Import**. After the upload is complete, you will see an index named `test-data` with 182,469 documents.


## Ingest the data through the {{infer}} ingest pipeline [reindexing-data-infer]

Create embeddings from the text by reindexing the data through the {{infer}} pipeline that uses your chosen model. This step uses the [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) to simulate data ingestion through a pipeline.

:::::::{tab-set}

::::::{tab-item} Cohere
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "cohere-embeddings",
    "pipeline": "cohere_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.


::::{note}
The [rate limit of your Cohere account](https://dashboard.cohere.com/billing) may affect the throughput of the reindexing process.
::::
::::::

::::::{tab-item} ELSER
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "elser-embeddings",
    "pipeline": "elser_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.
::::::

::::::{tab-item} HuggingFace
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "hugging-face-embeddings",
    "pipeline": "hugging_face_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.
::::::

::::::{tab-item} OpenAI
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "openai-embeddings",
    "pipeline": "openai_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.


::::{note}
The [rate limit of your OpenAI account](https://platform.openai.com/account/limits) may affect the throughput of the reindexing process. If this happens, change `size` to `3` or a similar value in magnitude.
::::
::::::

::::::{tab-item} Azure OpenAI
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "azure-openai-embeddings",
    "pipeline": "azure_openai_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.


::::{note}
The [rate limit of your Azure OpenAI account](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits#quotas-and-limits-reference) may affect the throughput of the reindexing process. If this happens, change `size` to `3` or a similar value in magnitude.
::::
::::::

::::::{tab-item} Azure AI Studio
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "azure-ai-studio-embeddings",
    "pipeline": "azure_ai_studio_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.


::::{note}
Your Azure AI Studio model deployment may have rate limits in place that might affect the throughput of the reindexing process. If this happens, change `size` to `3` or a similar value in magnitude.
::::
::::::

::::::{tab-item} Google Vertex AI
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "google-vertex-ai-embeddings",
    "pipeline": "google_vertex_ai_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` will make updates to the reindexing process faster. This enables you to follow the progress closely and detect errors early.
::::::

::::::{tab-item} Mistral
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "mistral-embeddings",
    "pipeline": "mistral_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.
::::::

::::::{tab-item} Amazon Bedrock
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "amazon-bedrock-embeddings",
    "pipeline": "amazon_bedrock_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.
::::::

::::::{tab-item} AlibabaCloud AI Search
```console
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "test-data",
    "size": 50 <1>
  },
  "dest": {
    "index": "alibabacloud-ai-search-embeddings",
    "pipeline": "alibabacloud_ai_search_embeddings_pipeline"
  }
}
```

1. The default batch size for reindexing is 1000. Reducing `size` to a smaller number makes the update of the reindexing process quicker which enables you to follow the progress closely and detect errors early.
::::::

:::::::
The call returns a task ID to monitor the progress:

```console
GET _tasks/<task_id>
```

Reindexing large datasets can take a long time. You can test this workflow using only a subset of the dataset. Do this by cancelling the reindexing process, and only generating embeddings for the subset that was reindexed. The following API request will cancel the reindexing task:

```console
POST _tasks/<task_id>/_cancel
```


## Semantic search [infer-semantic-search]

After the data set has been enriched with the embeddings, you can query the data using [semantic search](../../../solutions/search/vector/knn.md#knn-semantic-search). In case of dense vector models, pass a `query_vector_builder` to the k-nearest neighbor (kNN) vector search API, and provide the query text and the model you have used to create the embeddings. In case of a sparse vector model like ELSER, use a `sparse_vector` query, and provide the query text with the model you have used to create the embeddings.

::::{note}
If you cancelled the reindexing process, you run the query only a part of the data which affects the quality of your results.
::::


:::::::{tab-set}

::::::{tab-item} Cohere
```console
GET cohere-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "cohere_embeddings",
        "model_text": "Muscles in human body"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `cohere-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "cohere-embeddings",
        "_id": "-eFWCY4BECzWLnMZuI78",
        "_score": 0.737484,
        "_source": {
          "id": 1690948,
          "content": "Oxygen is supplied to the muscles via red blood cells. Red blood cells carry hemoglobin which oxygen bonds with as the hemoglobin rich blood cells pass through the blood vessels of the lungs.The now oxygen rich blood cells carry that oxygen to the cells that are demanding it, in this case skeletal muscle cells.ther ways in which muscles are supplied with oxygen include: 1  Blood flow from the heart is increased. 2  Blood flow to your muscles in increased. 3  Blood flow from nonessential organs is transported to working muscles."
        }
      },
      {
        "_index": "cohere-embeddings",
        "_id": "HuFWCY4BECzWLnMZuI_8",
        "_score": 0.7176013,
        "_source": {
          "id": 1692482,
          "content": "The thoracic cavity is separated from the abdominal cavity by the  diaphragm. This is a broad flat muscle.    (muscular) diaphragm The diaphragm is a muscle that separat…e the thoracic from the abdominal cavity. The pelvis is the lowest part of the abdominal cavity and it has no physical separation from it    Diaphragm."
        }
      },
      {
        "_index": "cohere-embeddings",
        "_id": "IOFWCY4BECzWLnMZuI_8",
        "_score": 0.7154432,
        "_source": {
          "id": 1692489,
          "content": "Muscular Wall Separating the Abdominal and Thoracic Cavities; Thoracic Cavity of a Fetal Pig; In Mammals the Diaphragm Separates the Abdominal Cavity from the"
        }
      },
      {
        "_index": "cohere-embeddings",
        "_id": "C-FWCY4BECzWLnMZuI_8",
        "_score": 0.695313,
        "_source": {
          "id": 1691493,
          "content": "Burning, aching, tenderness and stiffness are just some descriptors of the discomfort you may feel in the muscles you exercised one to two days ago.For the most part, these sensations you experience after exercise are collectively known as delayed onset muscle soreness.urning, aching, tenderness and stiffness are just some descriptors of the discomfort you may feel in the muscles you exercised one to two days ago."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} ELSER
```console
GET elser-embeddings/_search
{
  "query":{
    "sparse_vector":{
      "field": "content_embedding",
      "inference_id": "elser_embeddings",
      "query": "How to avoid muscle soreness after running?"
    }
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `cohere-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "elser-embeddings",
        "_id": "ZLGc_pABZbBmsu5_eCoH",
        "_score": 21.472063,
        "_source": {
          "id": 2258240,
          "content": "You may notice some muscle aches while you are exercising. This is called acute soreness. More often, you may begin to feel sore about 12 hours after exercising, and the discomfort usually peaks at 48 to 72 hours after exercise. This is called delayed-onset muscle soreness.It is thought that, during this time, your body is repairing the muscle, making it stronger and bigger.You may also notice the muscles feel better if you exercise lightly. This is normal.his is called delayed-onset muscle soreness. It is thought that, during this time, your body is repairing the muscle, making it stronger and bigger. You may also notice the muscles feel better if you exercise lightly. This is normal."
        }
      },
      {
        "_index": "elser-embeddings",
        "_id": "ZbGc_pABZbBmsu5_eCoH",
        "_score": 21.421381,
        "_source": {
          "id": 2258242,
          "content": "Photo Credit Jupiterimages/Stockbyte/Getty Images. That stiff, achy feeling you get in the days after exercise is a normal physiological response known as delayed onset muscle soreness. You can take it as a positive sign that your muscles have felt the workout, but the pain may also turn you off to further exercise.ou are more likely to develop delayed onset muscle soreness if you are new to working out, if you’ve gone a long time without exercising and start up again, if you have picked up a new type of physical activity or if you have recently boosted the intensity, length or frequency of your exercise sessions."
        }
      },
      {
        "_index": "elser-embeddings",
        "_id": "ZrGc_pABZbBmsu5_eCoH",
        "_score": 20.542095,
        "_source": {
          "id": 2258248,
          "content": "They found that stretching before and after exercise has no effect on muscle soreness. Exercise might cause inflammation, which leads to an increase in the production of immune cells (comprised mostly of macrophages and neutrophils). Levels of these immune cells reach a peak 24-48 hours after exercise.These cells, in turn, produce bradykinins and prostaglandins, which make the pain receptors in your body more sensitive. Whenever you move, these pain receptors are stimulated.hey found that stretching before and after exercise has no effect on muscle soreness. Exercise might cause inflammation, which leads to an increase in the production of immune cells (comprised mostly of macrophages and neutrophils). Levels of these immune cells reach a peak 24-48 hours after exercise."
        }
      },
    (...)
  ]
```
::::::

::::::{tab-item} HuggingFace
```console
GET hugging-face-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "hugging_face_embeddings",
        "model_text": "What's margin of error?"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `hugging-face-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "hugging-face-embeddings",
        "_id": "ljEfo44BiUQvMpPgT20E",
        "_score": 0.8522128,
        "_source": {
          "id": 7960255,
          "content": "The margin of error can be defined by either of the following equations. Margin of error = Critical value x Standard deviation of the statistic. Margin of error = Critical value x Standard error of the statistic. If you know the standard deviation of the statistic, use the first equation to compute the margin of error. Otherwise, use the second equation. Previously, we described how to compute the standard deviation and standard error."
        }
      },
      {
        "_index": "hugging-face-embeddings",
        "_id": "lzEfo44BiUQvMpPgT20E",
        "_score": 0.7865497,
        "_source": {
          "id": 7960259,
          "content": "1 y ou are told only the size of the sample and are asked to provide the margin of error for percentages which are not (yet) known. 2  This is typically the case when you are computing the margin of error for a survey which is going to be conducted in the future."
        }
      },
      {
        "_index": "hugging-face-embeddings1",
        "_id": "DjEfo44BiUQvMpPgT20E",
        "_score": 0.6229427,
        "_source": {
          "id": 2166183,
          "content": "1. In general, the point at which gains equal losses. 2. In options, the market price that a stock must reach for option buyers to avoid a loss if they exercise. For a call, it is the strike price plus the premium paid. For a put, it is the strike price minus the premium paid."
        }
      },
      {
        "_index": "hugging-face-embeddings1",
        "_id": "VzEfo44BiUQvMpPgT20E",
        "_score": 0.6034223,
        "_source": {
          "id": 2173417,
          "content": "How do you find the area of a circle? Can you measure the area of a circle and use that to find a value for Pi?"
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} OpenAI
```console
GET openai-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "openai_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `openai-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "openai-embeddings",
        "_id": "DDd5OowBHxQKHyc3TDSC",
        "_score": 0.83704096,
        "_source": {
          "id": 862114,
          "body": "How to calculate fuel cost for a road trip. By Tara Baukus Mello • Bankrate.com. Dear Driving for Dollars, My family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost.It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes.y family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost. It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes."
        }
      },
      {
        "_index": "openai-embeddings",
        "_id": "ajd5OowBHxQKHyc3TDSC",
        "_score": 0.8345704,
        "_source": {
          "id": 820622,
          "body": "Home Heating Calculator. Typically, approximately 50% of the energy consumed in a home annually is for space heating. When deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important.This calculator can help you estimate the cost of fuel for different heating appliances.hen deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important. This calculator can help you estimate the cost of fuel for different heating appliances."
        }
      },
      {
        "_index": "openai-embeddings",
        "_id": "Djd5OowBHxQKHyc3TDSC",
        "_score": 0.8327426,
        "_source": {
          "id": 8202683,
          "body": "Fuel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel.If you are paying $4 per gallon, the trip would cost you $200.Most boats have much larger gas tanks than cars.uel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} Azure OpenAI
```console
GET azure-openai-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "azure_openai_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `azure-openai-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "azure-openai-embeddings",
        "_id": "DDd5OowBHxQKHyc3TDSC",
        "_score": 0.83704096,
        "_source": {
          "id": 862114,
          "body": "How to calculate fuel cost for a road trip. By Tara Baukus Mello • Bankrate.com. Dear Driving for Dollars, My family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost.It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes.y family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost. It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes."
        }
      },
      {
        "_index": "azure-openai-embeddings",
        "_id": "ajd5OowBHxQKHyc3TDSC",
        "_score": 0.8345704,
        "_source": {
          "id": 820622,
          "body": "Home Heating Calculator. Typically, approximately 50% of the energy consumed in a home annually is for space heating. When deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important.This calculator can help you estimate the cost of fuel for different heating appliances.hen deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important. This calculator can help you estimate the cost of fuel for different heating appliances."
        }
      },
      {
        "_index": "azure-openai-embeddings",
        "_id": "Djd5OowBHxQKHyc3TDSC",
        "_score": 0.8327426,
        "_source": {
          "id": 8202683,
          "body": "Fuel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel.If you are paying $4 per gallon, the trip would cost you $200.Most boats have much larger gas tanks than cars.uel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} Azure AI Studio
```console
GET azure-ai-studio-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "azure_ai_studio_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `azure-ai-studio-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "azure-ai-studio-embeddings",
        "_id": "DDd5OowBHxQKHyc3TDSC",
        "_score": 0.83704096,
        "_source": {
          "id": 862114,
          "body": "How to calculate fuel cost for a road trip. By Tara Baukus Mello • Bankrate.com. Dear Driving for Dollars, My family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost.It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes.y family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost. It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes."
        }
      },
      {
        "_index": "azure-ai-studio-embeddings",
        "_id": "ajd5OowBHxQKHyc3TDSC",
        "_score": 0.8345704,
        "_source": {
          "id": 820622,
          "body": "Home Heating Calculator. Typically, approximately 50% of the energy consumed in a home annually is for space heating. When deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important.This calculator can help you estimate the cost of fuel for different heating appliances.hen deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important. This calculator can help you estimate the cost of fuel for different heating appliances."
        }
      },
      {
        "_index": "azure-ai-studio-embeddings",
        "_id": "Djd5OowBHxQKHyc3TDSC",
        "_score": 0.8327426,
        "_source": {
          "id": 8202683,
          "body": "Fuel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel.If you are paying $4 per gallon, the trip would cost you $200.Most boats have much larger gas tanks than cars.uel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} Google Vertex AI
```console
GET google-vertex-ai-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "google_vertex_ai_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `mistral-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "google-vertex-ai-embeddings",
        "_id": "Ryv0nZEBBFPLbFsdCbGn",
        "_score": 0.86815524,
        "_source": {
          "id": 3041038,
          "content": "For example, the cost of the fuel could be 96.9, the amount could be 10 pounds, and the distance covered could be 80 miles. To convert between Litres per 100KM and Miles Per Gallon, please provide a value and click on the required button.o calculate how much fuel you'll need for a given journey, please provide the distance in miles you will be covering on your journey, and the estimated MPG of your vehicle. To work out what MPG you are really getting, please provide the cost of the fuel, how much you spent on the fuel, and how far it took you."
        }
      },
      {
        "_index": "google-vertex-ai-embeddings",
        "_id": "w4j0nZEBZ1nFq1oiHQvK",
        "_score": 0.8676357,
        "_source": {
          "id": 1541469,
          "content": "This driving cost calculator takes into consideration the fuel economy of the vehicle that you are travelling in as well as the fuel cost. This road trip gas calculator will give you an idea of how much would it cost to drive before you actually travel.his driving cost calculator takes into consideration the fuel economy of the vehicle that you are travelling in as well as the fuel cost. This road trip gas calculator will give you an idea of how much would it cost to drive before you actually travel."
        }
      },
      {
        "_index": "google-vertex-ai-embeddings",
        "_id": "Hoj0nZEBZ1nFq1oiHQjJ",
        "_score": 0.80510974,
        "_source": {
          "id": 7982559,
          "content": "What's that light cost you? 1  Select your electric rate (or click to enter your own). 2  You can calculate results for up to four types of lights. 3  Select the type of lamp (i.e. 4  Select the lamp wattage (lamp lumens). 5  Enter the number of lights in use. 6  Select how long the lamps are in use (or click to enter your own; enter hours on per year). 7  Finally, ..."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} Mistral
```console
GET mistral-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "mistral_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `mistral-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "mistral-embeddings",
        "_id": "DDd5OowBHxQKHyc3TDSC",
        "_score": 0.83704096,
        "_source": {
          "id": 862114,
          "body": "How to calculate fuel cost for a road trip. By Tara Baukus Mello • Bankrate.com. Dear Driving for Dollars, My family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost.It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes.y family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost. It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes."
        }
      },
      {
        "_index": "mistral-embeddings",
        "_id": "ajd5OowBHxQKHyc3TDSC",
        "_score": 0.8345704,
        "_source": {
          "id": 820622,
          "body": "Home Heating Calculator. Typically, approximately 50% of the energy consumed in a home annually is for space heating. When deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important.This calculator can help you estimate the cost of fuel for different heating appliances.hen deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important. This calculator can help you estimate the cost of fuel for different heating appliances."
        }
      },
      {
        "_index": "mistral-embeddings",
        "_id": "Djd5OowBHxQKHyc3TDSC",
        "_score": 0.8327426,
        "_source": {
          "id": 8202683,
          "body": "Fuel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel.If you are paying $4 per gallon, the trip would cost you $200.Most boats have much larger gas tanks than cars.uel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} Amazon Bedrock
```console
GET amazon-bedrock-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "amazon_bedrock_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `amazon-bedrock-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "amazon-bedrock-embeddings",
        "_id": "DDd5OowBHxQKHyc3TDSC",
        "_score": 0.83704096,
        "_source": {
          "id": 862114,
          "body": "How to calculate fuel cost for a road trip. By Tara Baukus Mello • Bankrate.com. Dear Driving for Dollars, My family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost.It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes.y family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost. It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes."
        }
      },
      {
        "_index": "amazon-bedrock-embeddings",
        "_id": "ajd5OowBHxQKHyc3TDSC",
        "_score": 0.8345704,
        "_source": {
          "id": 820622,
          "body": "Home Heating Calculator. Typically, approximately 50% of the energy consumed in a home annually is for space heating. When deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important.This calculator can help you estimate the cost of fuel for different heating appliances.hen deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important. This calculator can help you estimate the cost of fuel for different heating appliances."
        }
      },
      {
        "_index": "amazon-bedrock-embeddings",
        "_id": "Djd5OowBHxQKHyc3TDSC",
        "_score": 0.8327426,
        "_source": {
          "id": 8202683,
          "body": "Fuel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel.If you are paying $4 per gallon, the trip would cost you $200.Most boats have much larger gas tanks than cars.uel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel."
        }
      },
      (...)
    ]
```
::::::

::::::{tab-item} AlibabaCloud AI Search
```console
GET alibabacloud-ai-search-embeddings/_search
{
  "knn": {
    "field": "content_embedding",
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "alibabacloud_ai_search_embeddings",
        "model_text": "Calculate fuel cost"
      }
    },
    "k": 10,
    "num_candidates": 100
  },
  "_source": [
    "id",
    "content"
  ]
}
```

As a result, you receive the top 10 documents that are closest in meaning to the query from the `alibabacloud-ai-search-embeddings` index sorted by their proximity to the query:

```console-result
"hits": [
      {
        "_index": "alibabacloud-ai-search-embeddings",
        "_id": "DDd5OowBHxQKHyc3TDSC",
        "_score": 0.83704096,
        "_source": {
          "id": 862114,
          "body": "How to calculate fuel cost for a road trip. By Tara Baukus Mello • Bankrate.com. Dear Driving for Dollars, My family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost.It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes.y family is considering taking a long road trip to finish off the end of the summer, but I'm a little worried about gas prices and our overall fuel cost. It doesn't seem easy to calculate since we'll be traveling through many states and we are considering several routes."
        }
      },
      {
        "_index": "alibabacloud-ai-search-embeddings",
        "_id": "ajd5OowBHxQKHyc3TDSC",
        "_score": 0.8345704,
        "_source": {
          "id": 820622,
          "body": "Home Heating Calculator. Typically, approximately 50% of the energy consumed in a home annually is for space heating. When deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important.This calculator can help you estimate the cost of fuel for different heating appliances.hen deciding on a heating system, many factors will come into play: cost of fuel, installation cost, convenience and life style are all important. This calculator can help you estimate the cost of fuel for different heating appliances."
        }
      },
      {
        "_index": "alibabacloud-ai-search-embeddings",
        "_id": "Djd5OowBHxQKHyc3TDSC",
        "_score": 0.8327426,
        "_source": {
          "id": 8202683,
          "body": "Fuel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel.If you are paying $4 per gallon, the trip would cost you $200.Most boats have much larger gas tanks than cars.uel is another important cost. This cost will depend on your boat, how far you travel, and how fast you travel. A 33-foot sailboat traveling at 7 knots should be able to travel 300 miles on 50 gallons of diesel fuel."
        }
      },
      (...)
    ]
```
::::::

:::::::

## Interactive tutorials [infer-interactive-tutorials]

You can also find tutorials in an interactive Colab notebook format using the {{es}} Python client:

* [Cohere {{infer}} tutorial notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/integrations/cohere/inference-cohere.ipynb)
* [OpenAI {{infer}} tutorial notebook](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/search/07-inference.ipynb)
