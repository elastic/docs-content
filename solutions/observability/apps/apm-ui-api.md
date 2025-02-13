---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-api.html
---

# APM UI API [apm-app-api]

Some Applications UI features are provided via a REST API:

* [Agent Configuration API](agent-configuration-api.md)
* [Annotation API](annotation-api.md)
* [RUM source map API](rum-source-map-api.md)
* [APM agent Key API](apm-agent-key-api.md)


## Using the APIs [apm-api-example] 

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

Here’s an example CURL request that adds an annotation to the Applications UI:

```curl
curl -X POST \
  http://localhost:5601/api/apm/services/opbeans-java/annotation \
-H 'Content-Type: application/json' \
-H 'kbn-xsrf: true' \
-H 'Authorization: Basic YhUlubWZhM0FDbnlQeE6WRtaW49FQmSGZ4RUWXdX' \
-d '{
      "@timestamp": "2020-05-11T10:31:30.452Z",
      "service": {
        "version": "1.2"
      },
      "message": "Revert upgrade",
      "tags": [
        "elastic.co", "customer"
      ]
    }'
```


## Kibana API [kibana-api] 

In addition to the APM specific API endpoints, Kibana provides its own [REST API](https://www.elastic.co/guide/en/observability/current/apm-api.html) which you can use to automate certain aspects of configuring and deploying Kibana.





