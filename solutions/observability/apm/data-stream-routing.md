---
mapped_pages:
applies_to:
  stack:
  serverless:
---

# Data stream routing [apm-open-telemetry-data-stream-routing]

APM already [supports routing APM data to user-defined data stream names](/solutions/observability/apm/data-streams.md#apm-data-stream-rerouting) via the [`reroute` processor](elasticsearch://reference/enrich-processor/reroute-processor.md). However, for users ingesting OTLP data, there is an alternative without having to create new ingest pipelines.

## Setting data stream attributes

To automatically route OTLP data, set the `data_stream.dataset` and `data_stream.namespace` attributes. These attributes will be mapped to the respective [ECS fields](ecs://reference/ecs-data_stream.md).

The `data_stream` attributes can be set in either the resource-level, scope-level, span-level or span-event-level, and they are parsed in increasing order of precedence. In other words, a span event `data_stream` attributes will override the span `data_stream` attributes. This also implies that the `data_stream` attributes are inherited from previous levels, i.e. if a span does not specify the `data_stream` attributes, it will use the scope's.

For more guidance on how to set resource attributes in OpenTelemetry, see [setting resource attributes](/solutions/observability/apm/attributes.md#setting-resource-attributes).
