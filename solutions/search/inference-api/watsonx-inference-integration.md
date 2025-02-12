---
navigation_title: "Watsonx"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-service-watsonx-ai.html
applies:
  stack:
  serverless:
---

# Watsonx inference integration [infer-service-watsonx-ai]

::::{admonition} New API reference
For the most up-to-date API details, refer to [{{infer-cap}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference).

::::


Creates an {{infer}} endpoint to perform an {{infer}} task with the `watsonxai` service.

You need an [IBM Cloud® Databases for Elasticsearch deployment](https://cloud.ibm.com/docs/databases-for-elasticsearch?topic=databases-for-elasticsearch-provisioning&interface=api) to use the `watsonxai` {{infer}} service. You can provision one through the [IBM catalog](https://cloud.ibm.com/databases/databases-for-elasticsearch/create), the [Cloud Databases CLI plug-in](https://cloud.ibm.com/docs/databases-cli-plugin?topic=databases-cli-plugin-cdb-reference), the [Cloud Databases API](https://cloud.ibm.com/apidocs/cloud-databases-api), or [Terraform](https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs/resources/database).


## {{api-request-title}} [infer-service-watsonx-ai-api-request] 

`PUT /_inference/<task_type>/<inference_id>`


## {{api-path-parms-title}} [infer-service-watsonx-ai-api-path-params] 

`<inference_id>`
:   (Required, string) The unique identifier of the {{infer}} endpoint.

`<task_type>`
:   (Required, string) The type of the {{infer}} task that the model will perform.

    Available task types:

    * `text_embedding`.



## {{api-request-body-title}} [infer-service-watsonx-ai-api-request-body] 

`service`
:   (Required, string) The type of service supported for the specified task type. In this case, `watsonxai`.

`service_settings`
:   (Required, object) Settings used to install the {{infer}} model.

    These settings are specific to the `watsonxai` service.

    `api_key`
    :   (Required, string) A valid API key of your Watsonx account. You can find your Watsonx API keys or you can create a new one [on the API keys page](https://cloud.ibm.com/iam/apikeys).

        ::::{important} 
        You need to provide the API key only once, during the {{infer}} model creation. The [Get {{infer}} API](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-inference-api.html) does not retrieve your API key. After creating the {{infer}} model, you cannot change the associated API key. If you want to use a different API key, delete the {{infer}} model and recreate it with the same name and the updated API key.
        ::::


    `api_version`
    :   (Required, string) Version parameter that takes a version date in the format of `YYYY-MM-DD`. For the active version data parameters, refer to the [documentation](https://cloud.ibm.com/apidocs/watsonx-ai#active-version-dates).

    `model_id`
    :   (Required, string) The name of the model to use for the {{infer}} task. Refer to the IBM Embedding Models section in the [Watsonx documentation](https://www.ibm.com/products/watsonx-ai/foundation-models) for the list of available text embedding models.

    `url`
    :   (Required, string) The URL endpoint to use for the requests.

    `project_id`
    :   (Required, string) The name of the project to use for the {{infer}} task.

    `rate_limit`
    :   (Optional, object) By default, the `watsonxai` service sets the number of requests allowed per minute to `120`. This helps to minimize the number of rate limit errors returned from Watsonx. To modify this, set the `requests_per_minute` setting of this object in your service settings:

        ```text
        "rate_limit": {
            "requests_per_minute": <<number_of_requests>>
        }
        ```



## Watsonx AI service example [inference-example-watsonx-ai] 

The following example shows how to create an {{infer}} endpoint called `watsonx-embeddings` to perform a `text_embedding` task type.

```console
PUT _inference/text_embedding/watsonx-embeddings
{
    "service": "watsonxai",
    "service_settings": {
        "api_key": "<api_key>", <1>
        "url": "<url>", <2>
        "model_id": "ibm/slate-30m-english-rtrvr",
        "project_id": "<project_id>", <3>
        "api_version": "2024-03-14" <4>
    }
}
```

1. A valid Watsonx API key. You can find on the [API keys page of your account](https://cloud.ibm.com/iam/apikeys).
2. The {{infer}} endpoint URL you created on Watsonx.
3. The ID of your IBM Cloud project.
4. A valid API version parameter. You can find the active version data parameters [here](https://cloud.ibm.com/apidocs/watsonx-ai#active-version-dates).


