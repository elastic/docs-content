---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-key-api.html
---

# APM agent Key API [apm-agent-key-api]

The APM agent Key API allows you to configure APM agent keys to authorize requests from APM agents to the APM Server.

The following APM agent key APIs are available:

* [Create agent key](#apm-create-agent-key) to create an APM agent key


### How to use APM APIs [use-agent-key-api] 

::::{dropdown} Expand for required headers, privileges, and usage details
Interact with APM APIs using cURL or another API tool. All APM APIs are Kibana APIs, not Elasticsearch APIs; because of this, the Kibana dev tools console cannot be used to interact with APM APIs.

For all APM APIs, you must use a request header. Supported headers are `Authorization`, `kbn-xsrf`, and `Content-Type`.

`Authorization: ApiKey {{credentials}}`
:   Kibana supports token-based authentication with the Elasticsearch API key service. The API key returned by the  [Elasticsearch create API key API](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html) can be used by sending a request with an `Authorization` header that has a value of `ApiKey` followed by the `{{credentials}}`, where `{{credentials}}` is the base64 encoding of `id` and `api_key` joined by a colon.

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


## Create agent key [apm-create-agent-key]

Create an APM agent API key. Specify API key privileges in the request body at creation time.


#### Privileges [apm-create-agent-key-privileges] 

The user creating an APM agent API key must have at least the `manage_own_api_key` cluster privilege and the APM application-level privileges that it wishes to grant.


##### Example role [_example_role] 

The example below uses the Kibana [role management API](https://www.elastic.co/guide/en/kibana/current/role-management-api.html) to create a role named `apm_agent_key_user`. Create and assign this role to a user that wishes to create APM agent API keys.

```js
POST /_security/role/apm_agent_key_user
{
  "cluster": ["manage_own_api_key"],
  "applications": [
    {
      "application": "kibana-.kibana",
      "privileges": ["feature_apm.all"],
      "resources": ["*"]
    },
    {
      "application": "apm",
      "privileges": ["event:write", "config_agent:read"],
      "resources": ["*"]
    }
  ]
}
```


#### Request [apm-create-agent-key-req] 

`POST /api/apm/agent_keys`


#### Request body [apm-create-agent-key-req-body] 

`name`
:   (required, string) Name of the APM agent key.

`privileges`
:   (required, array) APM agent key privileges. It can take one or more of the following values:

    * `event:write`. Required for ingesting APM agent events.
    * `config_agent:read`. Required for APM agents to read agent configuration remotely.



#### Example [apm-agent-key-create-example] 

```curl
POST /api/apm/agent_keys
{
    "name": "apm-key",
    "privileges": ["event:write", "config_agent:read"]
}
```


#### Response body [apm-agent-key-create-body] 

```js
{
  "agentKey": {
    "id": "3DCLmn0B3ZMhLUa7WBG9",
    "name": "apm-key",
    "api_key": "PjGloCGOTzaZr8ilUPvkjA",
    "encoded": "M0RDTG1uMEIzWk1oTFVhN1dCRzk6UGpHbG9DR09UemFacjhpbFVQdmtqQQ=="
  }
}
```

Once created, you can copy the API key (Base64 encoded) and use it to to authorize requests from APM agents to the APM Server.


