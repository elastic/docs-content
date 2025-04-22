---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-resource-attributes.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-resource-attributes.html
applies_to:
  stack:
  serverless:
---

# Resource attributes [apm-open-telemetry-resource-attributes]

A resource attribute is a key-value pair containing information about the entity producing telemetry. Resource attributes are mapped to Elastic Common Schema (ECS) fields like `service.*`, `cloud.*`, `process.*`, and so on. These fields describe the service and the environment that the service runs in.

The examples set the Elastic (ECS) `service.environment` field for the resource that's producing trace events. Elastic maps the OpenTelemetry `deployment.environment` field to the ECS `service.environment` field on ingestion.

## Setting resource attributes

You can set resource attributes through the environment variables or by editing the configuration of the resource processor of the Collector.

### OpenTelemetry configuration

Use the `OTEL_RESOURCE_ATTRIBUTES` environment variable to pass resource attributes at process invocation. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
```

### Resource processor

Use the [resource processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor) to set or apply changes to resource attributes.

```yaml
...
processors:
  resource:
    attributes:
    - key: deployment.environment
      action: insert
      value: production
...
```

## Handling of unmapped attributes

Only a subset of OpenTelemetry resource attributes are directly mapped to ECS fields. If an attribute doesn't have a predefined ECS mapping, it's stored under `labels.*`, with dots replaced by underscores.

The following table shows how OTel resource attributes are mapped to ECS fields and how they're stored if unmapped.

| OTel resource attribute | Mapped ECS field | If unmapped, stored as |
|-------------------------|------------------|------------------------|
| `service.name` | `service.name` | - |
| `service.version` | `service.version` | - |
| `deployment.environment` | `service.environment` | - |
| `cloud.provider` | `cloud.provider` | - |
| `cloud.account.id` | `cloud.account.id` | - |

When an attribute doesn't have a direct ECS field mapping, the system stores it under the `labels` namespace and replaces dots with underscores in the attribute key to comply with field name limitations.

For example, if an OpenTelemetry resource contains:

```json
{
  "service.name": "user-service",
  "deployment.environment": "production",
  "otel.library.name": "my-lib",
  "custom.attribute.with.dots": "value"
}
```

Elastic APM stores the following:

```json
{
  "service.name": "user-service",
  "service.environment": "production",
  "labels": {
    "otel_library_name": "my-lib",
    "custom_attribute_with_dots": "value"
  }
}
```

## APM transactions and spans

Not all OpenTelemetry spans are mapped the same way:

- Root spans, such as entry points, are mapped to APM transactions.
- Child spans, such as internal operations and DB queries, are mapped to APM spans.

| OpenTelemetry span kind | Mapped to APM | Example |
|------------------------|---------------|---------|
| `SERVER` | Transaction | Incoming HTTP request (`GET /users/{id}`) |
| `CONSUMER` | Transaction | Message queue consumer event |
| `CLIENT` | Span | Outgoing database query (`SELECT * FROM users`) |
| `PRODUCER` | Span | Sending a message to a queue |
| `INTERNAL` | Span | Internal function execution |

The following example shows OpenTelemetry spans:

```json
[
  {
    "traceId": "abcd1234",
    "spanId": "root5678",
    "parentId": null,
    "name": "GET /users/{id}",
    "kind": "SERVER"
  },
  {
    "traceId": "abcd1234",
    "spanId": "db1234",
    "parentId": "root5678",
    "name": "SELECT FROM users",
    "kind": "CLIENT"
  }
]
```

The previous OTel spans are stored by Elastic APM as follows:

```
Transaction: GET /users/{id}
 ├── Span: SELECT FROM users
```

## Conditional attribute translation

Some OpenTelemetry attributes are conditionally converted based on their value type.

The following table shows how OTel resource attributes are converted.

| OpenTelemetry Resource attribute | Incoming value type | Converted value | APM field |
|------------------------|---------------------|----------------|-----------|
| `http.status_code` | `200` (Integer) | `200` (Integer) | `http.response.status_code` |
| `feature.enabled` | `true` (Boolean) | `true` (Boolean) | `labels.feature_enabled` |
| `http.request_headers` | `["accept:json", "auth:token"]` (Array) | Individual array values as separate labels | `labels.http_request_headers.0`, `labels.http_request_headers.1` |

Consider the following resource attributes:

```json
{
  "http.status_code": 200,
  "feature.enabled": true,
  "http.request_headers": ["accept:json", "auth:token"]
}
```

The previous resource attributes are stored by Elastic APM as follows:

```json
{
  "http.response.status_code": 200,
  "labels": {
    "feature_enabled": true,
    "http_request_headers.0": "accept:json",
    "http_request_headers.1": "auth:token"
  }
}
```