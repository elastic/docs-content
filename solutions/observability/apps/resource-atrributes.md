---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-resource-attributes.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-resource-attributes.html
applies_to:
  stack: all
---

# Resource attributes [apm-open-telemetry-resource-attributes]

A resource attribute is a key/value pair containing information about the entity producing telemetry. Resource attributes are mapped to Elastic Common Schema (ECS) fields like `service.*`, `cloud.*`, `process.*`, etc. These fields describe the service and the environment that the service runs in.

The examples shown here set the Elastic (ECS) `service.environment` field for the resource, i.e. service, that is producing trace events. Note that Elastic maps the OpenTelemetry `deployment.environment` field to the ECS `service.environment` field on ingestion.

**OpenTelemetry agent**

Use the `OTEL_RESOURCE_ATTRIBUTES` environment variable to pass resource attributes at process invocation.

```bash
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
```

**OpenTelemetry collector**

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

::::{tip}
Need to add event attributes instead? Use attributes—​not to be confused with resource attributes—​to add data to span, log, or metric events. Attributes can be added as a part of the OpenTelemetry instrumentation process or with the [attributes processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor).

::::

% Stateful only after this?

Elastic integrates with OpenTelemetry, allowing you to reuse your existing instrumentation to easily send observability data to the {{stack}}.

For more information on how to combine Elastic and OpenTelemetry, see [OpenTelemetry integration](../../../solutions/observability/apps/use-opentelemetry-with-apm.md).