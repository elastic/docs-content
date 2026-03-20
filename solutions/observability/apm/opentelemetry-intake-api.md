---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-otlp.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# OpenTelemetry intake API [apm-api-otlp]

{{apm-server}} supports receiving traces, metrics, and logs over the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp/). OTLP is the default transfer protocol for OpenTelemetry and is supported natively by {{apm-server}}.

{{apm-server}} supports two OTLP communication protocols on the same port:

* OTLP/HTTP (protobuf)
* OTLP/gRPC

The OTLP endpoint on {{apm-server}} is not recommended for new users; use the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) or [Managed OTLP](opentelemetry://reference/motlp.md) instead. EDOT SDKs are only supported with [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md), and using them with this intake is not supported.

## OTLP/gRPC paths [_otlpgrpc_paths]

| Name | Endpoint |
| --- | --- |
| OTLP metrics intake | `/opentelemetry.proto.collector.metrics.v1.MetricsService/Export` |
| OTLP trace intake | `/opentelemetry.proto.collector.trace.v1.TraceService/Export` |
| OTLP logs intake | `/opentelemetry.proto.collector.logs.v1.LogsService/Export` |

## OTLP/HTTP paths [_otlphttp_paths]

| Name | Endpoint |
| --- | --- |
| OTLP metrics intake | `/v1/metrics` |
| OTLP trace intake | `/v1/traces` |
| OTLP logs intake | `/v1/logs` |