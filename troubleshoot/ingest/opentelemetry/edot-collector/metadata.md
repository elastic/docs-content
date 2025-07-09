---
navigation_title: Collector doesn’t propagate metadata
description: Learn why the Collector doesn’t extract custom attributes and how to propagate such values using EDOT SDKs.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# EDOT Collector doesn’t propagate client metadata

By default, the Collector only propagates transport-level metadata. If you want the EDOT Collector to propagate metadata like `project_id`, `tenant`, or `environment`, you need a specific SDK instrumentation.

### What is client metadata

In the context of the EDOT, client metadata refers to gRPC metadata or HTTP headers that accompany telemetry data sent by clients (usually SDKs) to the Collector.

For example: 

- Authorization headers
- Trace propagation headers
- `user-agent` strings sent by HTTP clients or EDOT SDKs

This is transport-level metadata, and not application-level context.

### What isn’t client metadata

In this context, client metadata does not include:

- Custom attributes like `project_id`, `tenant`, or `environment`
- Application business logic fields
- Resource attributes

## Symptoms

Expected labels do not appear in Elastic APM or metric data.

Your collector configuration file, for example `otel-config.yaml`, looks similar to this:

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"

processors:
  resource:
    attributes:
      - key: project.id
        from_context: client_metadata
        action: insert
```

This will not work, as the Collector doesn't automatically extract such values from headers.

## Resolution

If you want to propagate customer IDs or project names into spans or metrics, you must instrument this in your code using one of the SDKs.

Use `span.set_attribute` in your application code, where OpenTelemetry spans are created. For example:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("handle_request") as span:
    span.set_attribute("project.id", get_project_id_from_context())
```

## Resources

- [gRPC metadata documentation](https://grpc.io/docs/guides/concepts/#metadata)
- [OpenTelemetry Protocol (OTLP) overview](https://opentelemetry.io/docs/specs/otlp/)