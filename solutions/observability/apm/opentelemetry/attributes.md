---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-resource-attributes.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-resource-attributes.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Attributes and labels [apm-open-telemetry-resource-attributes]

In OpenTelemetry, an attribute is a key-value pair. Attributes are similar to [labels](/solutions/observability/apm/metadata.md#apm-data-model-labels) in that they add metadata to transactions, spans, and other entities.

Resource attributes are a type of attribute that contains information about the entities that produce telemetry. Resource attributes map to Elastic Common Schema (ECS) fields like `service.*`, `cloud.*`, `process.*`, and so on. These fields describe the service and its environment.

For example, Elastic APM maps the OpenTelemetry `deployment.environment` field to the ECS `service.environment` field on ingestion.

## Setting resource attributes

You can set resource attributes through environment variables or by editing the configuration of the resource processor of the OpenTelemetry Collector.

### OpenTelemetry agent

Use the `OTEL_RESOURCE_ATTRIBUTES` environment variable to pass resource attributes at process invocation. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
```

### Elastic Distribution of OpenTelemetry Collector (EDOT Collector)

Use the [resource processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor) to set or apply changes to resource attributes when using the EDOT Collector.

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

When sending telemetry to Elastic APM, only a subset of OpenTelemetry attributes are directly mapped to Elastic APM document fields, such as ECS fields. If an attribute doesn't have a predefined mapping, the system stores it under `labels.*`, with dots replaced by underscores.

Unmapped resource attributes are treated as global labels in Elastic APM, meaning they apply to all telemetry data from the resource. In contrast, unmapped record-level attributes, such as those specific to a log record, span, or data point, are stored as normal labels associated only with that specific record.

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

## Scope attributes translation

Scope attributes are translated as follows:

| OpenTelemetry attribute | Elastic APM field |
|-------------------------|-------------------|
| scope.name | service.framework.name |
| scope.version | service.framework.version |

Unmapped scope attributes are ignored.