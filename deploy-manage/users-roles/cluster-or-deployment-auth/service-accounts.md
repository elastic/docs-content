---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/service-accounts.html
---

# Service accounts [service-accounts]

The {{stack-security-features}} provide *service accounts* specifically for integration with external services that connect to {{es}}, such as {{fleet}} server. Service accounts have a fixed set of privileges and cannot authenticate until you create a service account token for them. Additionally, service accounts are predefined in code, and are always enabled.

A service account corresponds to a specific external service. You create service account tokens for a service account. The service can then authenticate with the token and perform relevant actions. For example, {{fleet}} server can use its service token to authenticate with {{es}} and then manage its own API keys.

You can create multiple service tokens for the same service account, which prevents credential sharing between multiple instances of the same external service. Each instance can assume the same identity while using their own distinct service token for authentication.

Service accounts provide flexibility over [built-in users](built-in-users.md) because they:

* Do not rely on the [internal `native` realm](native.md), and aren’t always required to rely on the `.security` index
* Use a [role descriptor](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) named after the service account principal instead of traditional roles
* Support multiple credentials through service account tokens

Service accounts are not included in the response of the [get users API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-user). To retrieve a service account, use the [get service accounts API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-service-accounts). Use the [get service account credentials API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-service-credentials) to retrieve all service credentials for a service account.


## Service accounts usage [service-accounts-explanation] 

Service accounts have a [unique principal](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-service-accounts#security-api-get-service-accounts-path-params) that takes the format of `<namespace>/<service>`, where the `namespace` is a top-level grouping of service accounts, and `service` is the name of the service and must be unique within its namespace.

Service accounts are predefined in code. The following service accounts are available:

`elastic/fleet-server`
:   The service account used by the {{fleet}} server to communicate with {{es}}.

`elastic/kibana`
:   The service account used by {{kib}} to communicate with {{es}}.

`elastic/enterprise-search-server`
:   The service account used by Enterprise Search to communicate with {{es}}.

::::{important} 
Do not attempt to use service accounts for authenticating individual users. Service accounts can only be authenticated with service tokens, which are not applicable to regular users.
::::



## Service account tokens [service-accounts-tokens] 

A service account token, or service token, is a unique string that a service uses to authenticate with {{es}}. For a given service account, each token must have a unique name. Because tokens include access credentials, they should always be kept secret by whichever client is using them.

Service tokens can be backed by either the `.security` index (recommended) or the `service_tokens` file. You can create multiple service tokens for a single service account, which enables multiple instances of the same service to run with different credentials.

You must create a service token to use a service account. You can create a service token using either:

* The [create service account token API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-service-token), which saves the new service token in the `.security` index and returns the bearer token in the HTTP response.
* The [elasticsearch-service-tokens](https://www.elastic.co/guide/en/elasticsearch/reference/current/service-tokens-command.html) CLI tool, which saves the new service token in the `$ES_HOME/config/service_tokens` file and outputs the bearer token to your terminal

We recommend that you create service tokens via the REST API rather than the CLI. The API stores service tokens within the `.security` index which means that the tokens are available for authentication on all nodes, and will be backed up within cluster snapshots. The use of the CLI is intended for cases where there is an external orchestration process (such as [{{ece}}](https://www.elastic.co/guide/en/cloud-enterprise/{{ece-version-link}}) or [{{eck}}](https://www.elastic.co/guide/en/cloud-on-k8s/current)) that will manage the creation and distribution of the `service_tokens` file.

Both of these methods (API and CLI) create a service token with a guaranteed secret string length of `22`. The minimal, acceptable length of a secret string for a service token is `10`. If the secret string doesn’t meet this minimal length, authentication with {{es}} will fail without even checking the value of the service token.

Service tokens never expire. You must actively [delete](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-delete-service-token) them if they are no longer needed.


## Authenticate with service tokens [authenticate-with-service-account-token] 

::::{note} 
Service accounts currently do not support basic authentication.
::::


To use a service account token, include the generated token value in a request with an `Authorization: Bearer` header:

```shell
curl -H "Authorization: Bearer AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ" http://localhost:9200/_security/_authenticate
```

A successful authentication response includes a `token` field, which contains a `name` field for the name of the service token and a `type` field for the type of the service token:

```js
{
  "username": "elastic/fleet-server",
  "roles": [],
  "full_name": "Service account - elastic/fleet-server",
  "email": null,
  "token": {
    "name": "token1",                 <1>
    "type": "_service_account_index"  <2>
  },
  "metadata": {
    "_elastic_service_account": true
  },
  "enabled": true,
  "authentication_realm": {
    "name": "_service_account",
    "type": "_service_account"
  },
  "lookup_realm": {
    "name": "_service_account",
    "type": "_service_account"
  },
  "authentication_type": "token"
}
```

1. Name of the service account token.
2. Type of service account token. The value always begins with `_service_account_` and is followed by a string that indicates the service token backend in use (can be either `file` or `index`).


