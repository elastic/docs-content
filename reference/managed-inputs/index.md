---
navigation_title: Managed inputs
description: Managed inputs are fully managed ingestion endpoints for sending data to Elastic Cloud.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Managed inputs [managed-inputs]

Managed inputs are fully managed ingestion endpoints for sending data to {{ecloud}}. Each input exposes a protocol-specific endpoint that buffers data, applies back-pressure, and routes it into {{es}}, so you don't need to run your own ingestion infrastructure.

Managed inputs are the recommended ingestion path for {{ecloud}}. The following managed inputs are available:

| Input | Protocol | Use it to |
| --- | --- | --- |
| [Managed OTLP Endpoint](managed-otlp-endpoint.md) | OpenTelemetry Protocol (OTLP) | Ingest OpenTelemetry logs, metrics, and traces from {{agent}} collectors and EDOT SDKs, {{edot-cf}}, upstream OpenTelemetry collectors and SDKs, or any OTLP-compliant shipper. |
| [Managed Prometheus Remote Write endpoint](prometheus-remote-write.md) | Prometheus Remote Write v1 (PRW) | Ingest Prometheus metrics into {{es}} time series data streams. |
| [Managed {{es}} _bulk endpoint](elasticsearch-bulk.md) | {{es}} `_bulk` API | Ingest log data from `_bulk`-based shippers such as standalone {{product.elastic-agent}}, {{product.logstash}}, and other {{es}}-compatible shippers. |
| [Managed Vercel endpoint](integration-docs://reference/vercel.md) | JSON or NDJSON | Ingest Vercel logs, audit logs, Web Analytics, and Speed Insights to {{es}} |
| [Managed Supabase endpoint](integration-docs://reference/supabase.md) | OpenTelemetry Protocol (OTLP) | Ingest Supabase logs using the OpenTelemetry. |


For authentication, buffering and delivery, how indexing errors are handled, and {{ech}} network limitations shared by all managed inputs, refer to [Authentication, delivery, and failure handling with managed inputs](authentication-delivery-and-failure-handling.md). For `429` responses and capacity guidance, refer to [Managed inputs rate limiting](rate-limiting.md).
