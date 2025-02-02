---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-otlp.html
---

# OpenTelemetry intake API [apm-api-otlp]

APM Server supports receiving traces, metrics, and logs over the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp/). OTLP is the default transfer protocol for OpenTelemetry and is supported natively by APM Server.

APM Server supports two OTLP communication protocols on the same port:

* OTLP/HTTP (protobuf)
* OTLP/gRPC


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

::::{tip} 
See our OpenTelemetry documentation to learn how to send data to the APM Server from an [OpenTelemetry agent](upstream-opentelemetry-collectors-language-sdks.md#apm-instrument-apps-otel) or [OpenTelemetry collector](upstream-opentelemetry-collectors-language-sdks.md#apm-connect-open-telemetry-collector).
::::


