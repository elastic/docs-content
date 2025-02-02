# Limitations [observability-apm-agents-opentelemetry-limitations]


## OpenTelemetry traces [observability-apm-agents-opentelemetry-limitations-opentelemetry-traces] 

* Traces of applications using `messaging` semantics might be wrongly displayed as `transactions` in the Applications UI, while they should be considered `spans` (see issue [#7001](https://github.com/elastic/apm-server/issues/7001)).
* Inability to see Stack traces in spans.
* Inability in APM views to view the "Time Spent by Span Type"  (see issue [#5747](https://github.com/elastic/apm-server/issues/5747)).


## OpenTelemetry logs [open-telemetry-logs-intake] 

* [preview]  The OpenTelemetry logs intake via Elastic is in technical preview.
* The application logs data stream (`app_logs`) has dynamic mapping disabled. This means the automatic detection and mapping of new fields is disabled (see issue [#9093](https://github.com/elastic/apm-server/issues/9093)).


## OpenTelemetry Line Protocol (OTLP) [open-telemetry-otlp-limitations] 

Elastic supports both the [(OTLP/gRPC)](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/otlp.md#otlpgrpc) and [(OTLP/HTTP)](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/otlp.md#otlphttp) protocol with ProtoBuf payload. Elastic does not yet support JSON Encoding for OTLP/HTTP.


## OpenTelemetry Collector exporter for Elastic [open-telemetry-collector-exporter] 

The [OpenTelemetry Collector exporter for Elastic](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter#legacy-opentelemetry-collector-exporter-for-elastic) has been deprecated and replaced by the native support of the OpenTelemetry Line Protocol in Elastic Observability (OTLP). To learn more, see [migration](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter#migration).

The [OpenTelemetry Collector exporter for Elastic](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter) (which is different from the legacy exporter mentioned above) is not intended to be used with Elastic APM and {{obs-serverless}}. Use [Elastic’s native OTLP support](../../../solutions/observability/apps/upstream-opentelemetry-collectors-language-sdks.md) instead.

