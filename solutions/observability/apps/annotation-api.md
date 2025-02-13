---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-annotation-api.html
---

# Annotation API [apm-annotation-api]

The Annotation API allows you to annotate visualizations in the Applications UI with significant events, like deployments, allowing you to easily see how these events are impacting the performance of your existing applications.

By default, annotations are stored in a newly created `observability-annotations` index. The name of this index can be changed in your `config.yml` by editing `xpack.observability.annotations.index`. If you change the default index name, you’ll also need to [update your user privileges](applications-ui-annotation-user.md) accordingly.

The following APIs are available:

* [Create or update annotation](#apm-annotation-create) to create an annotation for APM.


### How to use APM APIs [use-annotation-api] 

::::{dropdown} Expand for required headers, privileges, and usage details
Interact with APM APIs using cURL or another API tool. All APM APIs are Kibana APIs, not Elasticsearch APIs; because of this, the Kibana dev tools console cannot be used to interact with APM APIs.

For all APM APIs, you must use a request header. Supported headers are `Authorization`, `kbn-xsrf`, and `Content-Type`.

`Authorization: ApiKey {{credentials}}`
:   Kibana supports token-based authentication with the Elasticsearch API key service. The API key returned by the  [Elasticsearch create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) can be used by sending a request with an `Authorization` header that has a value of `ApiKey` followed by the `{{credentials}}`, where `{{credentials}}` is the base64 encoding of `id` and `api_key` joined by a colon.

    Alternatively, you can create a user and use their username and password to authenticate API access: `-u $USER:$PASSWORD`.

    Whether using `Authorization: ApiKey {{credentials}}`, or `-u $USER:$PASSWORD`, users interacting with APM APIs must have [sufficient privileges](applications-ui-api-user.md).


`kbn-xsrf: true`
:   By default, you must use `kbn-xsrf` for all API calls, except in the following scenarios:

    * The API endpoint uses the `GET` or `HEAD` operations
    * The path is allowed using the `server.xsrf.allowlist` setting
    * XSRF protections are disabled using the `server.xsrf.disableProtection` setting


`Content-Type: application/json`
:   Applicable only when you send a payload in the API request. {{kib}} API requests and responses use JSON. Typically, if you include the `kbn-xsrf` header, you must also include the `Content-Type` header.

::::


## Create or update annotation [apm-annotation-create]


#### Request [apm-annotation-config-req] 

`POST /api/apm/services/:serviceName/annotation`


#### Request body [apm-annotation-config-req-body] 

`service`
:   (required, object) Service identifying the configuration to create or update.

    ::::{dropdown} Properties of `service`
    `version`
    :   (required, string) Version of service.

    `environment`
    :   (optional, string) Environment of service.

    ::::


`@timestamp`
:   (required, string) The date and time of the annotation. Must be in [ISO 8601](https://www.w3.org/TR/NOTE-datetime) format.

`message`
:   (optional, string) The message displayed in the annotation. Defaults to `service.version`.

`tags`
:   (optional, array) Tags are used by the Applications UI to distinguish APM annotations from other annotations. Tags may have additional functionality in future releases. Defaults to `[apm]`. While you can add additional tags, you cannot remove the `apm` tag.


#### Example [apm-annotation-config-example] 

The following example creates an annotation for a service named `opbeans-java`.

```curl
curl -X POST \
  http://localhost:5601/api/apm/services/opbeans-java/annotation \
-H 'Content-Type: application/json' \
-H 'kbn-xsrf: true' \
-H 'Authorization: Basic YhUlubWZhM0FDbnlQeE6WRtaW49FQmSGZ4RUWXdX' \
-d '{
      "@timestamp": "2020-05-08T10:31:30.452Z",
      "service": {
        "version": "1.2"
      },
      "message": "Deployment 1.2"
    }'
```


#### Response body [apm-annotation-config-body] 

```js
{
  "_index": "observability-annotations",
  "_id": "Lc9I93EBh6DbmkeV7nFX",
  "_version": 1,
  "_seq_no": 12,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "message": "Deployment 1.2",
    "@timestamp": "2020-05-08T10:31:30.452Z",
    "service": {
      "version": "1.2",
      "name": "opbeans-java"
    },
    "tags": [
      "apm",
      "elastic.co",
      "customer"
    ],
    "annotation": {
      "type": "deployment"
    },
    "event": {
      "created": "2020-05-09T02:34:43.937Z"
    }
  }
}
```


