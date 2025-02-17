---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-config-api.html
---

# Agent Configuration API [apm-agent-config-api]

The APM agent configuration API allows you to fine-tune your APM agent configuration, without needing to redeploy your application.

The following APM agent configuration APIs are available:

* [Create or update configuration](#apm-update-config) to create or update an APM agent configuration
* [Delete configuration](#apm-delete-config) to delete an APM agent configuration.
* [List configuration](#apm-list-config) to list all APM agent configurations.
* [Search configuration](#apm-search-config) to search for an APM agent configuration.


### How to use APM APIs [use-agent-config-api] 

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


## Create or update configuration [apm-update-config]


#### Request [apm-update-config-req] 

`PUT /api/apm/settings/agent-configuration`


#### Request body [apm-update-config-req-body] 

`service`
:   (required, object) Service identifying the configuration to create or update.

    ::::{dropdown} Properties of `service`
    `name`
    :   (required, string) Name of service

    `environment`
    :   (optional, string) Environment of service

    ::::


`settings`
:   (required) Key/value object with option name and option value.

`agent_name`
:   (optional) The agent name is used by the UI to determine which settings to display.


#### Example [apm-update-config-example] 

```bash
PUT /api/apm/settings/agent-configuration
{
    "service": {
        "name": "frontend",
        "environment": "production"
    },
    "settings": {
        "transaction_sample_rate": "0.4",
        "capture_body": "off",
        "transaction_max_spans": "500"
    },
    "agent_name": "nodejs"
}
```


## Delete configuration [apm-delete-config]


#### Request [apm-delete-config-req] 

`DELETE /api/apm/settings/agent-configuration`


#### Request body [apm-delete-config-req-body] 

`service`
:   (required, object) Service identifying the configuration to delete

    ::::{dropdown} Properties of `service`
    `name`
    :   (required, string) Name of service

    `environment`
    :   (optional, string) Environment of service

    ::::



#### Example [apm-delete-config-example] 

```bash
DELETE /api/apm/settings/agent-configuration
{
    "service" : {
        "name": "frontend",
        "environment": "production"
    }
}
```


## List configuration [apm-list-config]


#### Request [apm-list-config-req] 

`GET  /api/apm/settings/agent-configuration`


#### Response body [apm-list-config-body] 

```js
[
  {
    "agent_name": "go",
    "service": {
      "name": "opbeans-go",
      "environment": "production"
    },
    "settings": {
      "transaction_sample_rate": "1",
      "capture_body": "off",
      "transaction_max_spans": "200"
    },
    "@timestamp": 1581934104843,
    "applied_by_agent": false,
    "etag": "1e58c178efeebae15c25c539da740d21dee422fc"
  },
  {
    "agent_name": "go",
    "service": {
      "name": "opbeans-go"
    },
    "settings": {
      "transaction_sample_rate": "1",
      "capture_body": "off",
      "transaction_max_spans": "300"
    },
    "@timestamp": 1581934111727,
    "applied_by_agent": false,
    "etag": "3eed916d3db434d9fb7f039daa681c7a04539a64"
  },
  {
    "agent_name": "nodejs",
    "service": {
      "name": "frontend"
    },
    "settings": {
      "transaction_sample_rate": "1",
    },
    "@timestamp": 1582031336265,
    "applied_by_agent": false,
    "etag": "5080ed25785b7b19f32713681e79f46996801a5b"
  }
]
```


#### Example [apm-list-config-example] 

```bash
GET  /api/apm/settings/agent-configuration
```


## Search configuration [apm-search-config]


#### Request [apm-search-config-req] 

`POST /api/apm/settings/agent-configuration/search`


#### Request body [apm-search-config-req-body] 

`service`
:   (required, object) Service identifying the configuration.

    ::::{dropdown} Properties of `service`
    `name`
    :   (required, string) Name of service

    `environment`
    :   (optional, string) Environment of service

    ::::


`etag`
:   (required) etag is sent by the APM agent to indicate the etag of the last successfully applied configuration. If the etag matches an existing configuration its `applied_by_agent` property will be set to `true`. Every time a configuration is edited `applied_by_agent` is reset to `false`.


#### Response body [apm-search-config-body] 

```js
{
  "_index": ".apm-agent-configuration",
  "_id": "CIaqXXABmQCdPphWj8EJ",
  "_score": 2,
  "_source": {
    "agent_name": "nodejs",
    "service": {
      "name": "frontend"
    },
    "settings": {
      "transaction_sample_rate": "1",
    },
    "@timestamp": 1582031336265,
    "applied_by_agent": false,
    "etag": "5080ed25785b7b19f32713681e79f46996801a5b"
  }
}
```


#### Example [apm-search-config-example] 

```bash
POST /api/apm/settings/agent-configuration/search
{
    "etag": "1e58c178efeebae15c25c539da740d21dee422fc",
    "service" : {
        "name": "frontend",
        "environment": "production"
    }
}
```


