---
mapped_pages:
applies_to:
  stack: ga
  serverless: ga
---

# Data stream routing [apm-open-telemetry-data-stream-routing]

Elastic APM supports [routing APM data](/solutions/observability/apm/data-streams.md#apm-data-stream-rerouting) to user-defined data stream names using the [`reroute` processor](elasticsearch://reference/enrich-processor/reroute-processor.md). However, you can also ingest OTLP data without having to create new ingest pipelines.

## Setting data stream attributes

To automatically route OTLP data, set the `data_stream.dataset` and `data_stream.namespace` attributes. These attributes map to the respective [ECS fields](ecs://reference/ecs-data_stream.md).

You can set the `data_stream` attributes at resource level, scope level, and record level. Elastic parses the attributes in increasing order of precedence. For example, record `data_stream` attributes override the scope `data_stream` attributes. This implies that `data_stream` attributes are inherited from previous levels. If a scope does not specify `data_stream` attributes, it uses the resource attributes.

For guidance on how to set resource attributes in OpenTelemetry, refer to [setting resource attributes](/solutions/observability/apm/opentelemetry/attributes.md#setting-resource-attributes).
