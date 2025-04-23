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

### OpenTelemetry agent

Use the `OTEL_RESOURCE_ATTRIBUTES` environment variable to pass resource attributes at process invocation. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
```

### OpenTelemetry Collector

Use the [resource processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor) to set or apply changes to resource attributes when using the OTel Collector.

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

Only a subset of OpenTelemetry resource attributes are directly mapped to ECS fields. If an attribute doesn't have a predefined ECS mapping, the systems stores it under `labels.*`, with dots replaced by underscores.

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

### Conditional attribute translation

Some OpenTelemetry attributes are conditionally converted based on their value type.

Consider the following resource attributes:

```json
{
  "http.status_code": 200,
  "feature.enabled": true
}
```

The previous resource attributes are stored by Elastic APM as follows:

```json
{
  "http.response.status_code": 200,
  "labels": {
    "feature_enabled": true
  }
}
```