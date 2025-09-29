---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-config.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Elastic APM agent configuration API [apm-api-config]

APM Server exposes API endpoints that allow Elastic APM agents to query the APM Server for configuration changes. More information on this feature is available in [{{apm-agent}} configuration in {{kib}}](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md).

## Agent configuration endpoints [apm-api-config-endpoint]

| Name | Endpoint |
| --- | --- |
| Agent configuration intake | `/config/v1/agents` |
| RUM configuration intake | `/config/v1/rum/agents` |

The Agent configuration endpoints accepts both `HTTP GET` and `HTTP POST` requests. If an [API keys](/solutions/observability/apm/api-keys.md) or [Secret token](/solutions/observability/apm/secret-token.md) is configured, requests to this endpoint must be authenticated.

### HTTP GET [apm-api-config-api-get]

`service.name` is a required query string parameter.

```bash
http(s)://{hostname}:{port}/config/v1/agents?service.name=SERVICE_NAME
```

### HTTP POST [apm-api-config-api-post]

Encode parameters as a JSON object in the body. `service.name` is a required parameter.

```bash
http(s)://{hostname}:{port}/config/v1/agents
{
  "service": {
      "name": "test-service",
      "environment": "all"
  },
  "CAPTURE_BODY": "off"
}
```

### Responses [apm-api-config-api-response]

* Successful - `200`
* APM Server is configured to fetch agent configuration from {{es}} but the configuration is invalid - `403`
* APM Server is starting up or {{es}} is unreachable - `503`

### Example request [apm-api-config-api-example]

Example Agent configuration `GET` request including the service name "test-service":

```sh
curl -i http://127.0.0.1:8200/config/v1/agents?service.name=test-service
```

Example Agent configuration `POST` request including the service name "test-service":

```sh
curl -X POST http://127.0.0.1:8200/config/v1/agents \
  -H "Authorization: Bearer secret_token" \
  -H 'content-type: application/json' \
  -d '{"service": {"name": "test-service"}}'
```

### Example response [apm-api-config-api-ex-response]

```sh
HTTP/1.1 200 OK
Cache-Control: max-age=30, must-revalidate
Content-Type: application/json
Etag: "7b23d63c448a863fa"
Date: Mon, 24 Feb 2020 20:53:07 GMT
Content-Length: 98

{
    "capture_body": "off",
    "transaction_max_spans": "500",
    "transaction_sample_rate": "0.3"
}
```

