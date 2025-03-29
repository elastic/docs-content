---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-known-limitations.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-limitations.html
---

# Limitations [apm-open-telemetry-known-limitations]


## OpenTelemetry traces [apm-open-telemetry-traces-limitations]

* Traces of applications using `messaging` semantics might be wrongly displayed as `transactions` in the Applications UI, while they should be considered `spans` (see issue [#7001](https://github.com/elastic/apm-server/issues/7001)).
* Inability to see Stack traces in spans.
* Inability in APM views to view the "Time Spent by Span Type"  (see issue [#5747](https://github.com/elastic/apm-server/issues/5747)).


## OpenTelemetry logs [apm-open-telemetry-logs-intake]

* [preview] The OpenTelemetry logs intake via Elastic is in technical preview.
* The application logs data stream (`app_logs`) has dynamic mapping disabled. This means the automatic detection and mapping of new fields is disabled (see issue [#9093](https://github.com/elastic/apm-server/issues/9093)).


## OpenTelemetry Line Protocol (OTLP) [apm-open-telemetry-otlp-limitations]

Elastic supports both the  [OTLP/gRPC](https://opentelemetry.io/docs/specs/otlp/#otlpgrpc) and [OTLP/HTTP](https://opentelemetry.io/docs/specs/otlp/#otlphttp) protocol with ProtoBuf payload. Elastic does not yet support JSON Encoding for OTLP/HTTP.


## OpenTelemetry Collector exporter for Elastic [apm-open-telemetry-collector-exporter]

The [OpenTelemetry Collector exporter for Elastic](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.57.2/exporter/elasticexporter) has been deprecated and replaced by the native support of the OpenTelemetry Line Protocol in Elastic Observability (OTLP).

The [OpenTelemetry Collector exporter for Elastic](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter) (which is different from the legacy exporter mentioned above) is not intended to be used with Elastic APM and Elastic Observability. Use [Elastic’s native OTLP support](../../../solutions/observability/apps/upstream-opentelemetry-collectors-language-sdks.md) instead.

% Statefull only for tail-based sampling?

## OpenTelemetry’s tail-based sampling [apm-open-telemetry-tbs]
```{applies_to}
stack: all
```

Tail-based sampling allows to make sampling decisions after all spans of a trace have been completed. This allows for more powerful and informed sampling rules.

When using OpenTelemetry with Elastic APM, there are two different implementations available for tail-based sampling:

* Tail-based sampling using the [tailsamplingprocessor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor) in the OpenTelemetry Collector
* Native [tail-based sampling in the Elastic APM backend](../../../solutions/observability/apps/transaction-sampling.md#apm-tail-based-sampling)

Using the [tailsamplingprocessor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor) in the OpenTelemetry Collector comes with an important limitation. Elastic’s APM backend calculates span and transaction metrics based on the incoming span events. These metrics are accurate for 100% sampling scenarios. In scenarios with probabilistic sampling, Elastic’s APM backend is being informed about the sampling rate of spans and can extrapolate throughput metrics based on the incoming, partial data. However, with tail-based sampling there’s no clear probability for sampling decisions as the rules can be more complex and the OpenTelemetry Collector does not provide sampling probability information to the Elastic backend that could be used for extrapolation of data. Therefore, there’s no way for Elastic APM to properly extrapolate throughput and count metrics that are derived from span events that have been tail-based sampled in the OpenTelemetry Collector. In these scenarios, derived throughput and count metrics are likely to be inaccurate.

Therefore, we recommend using Elastic’s native tail-based sampling when integrating with OpenTelemetry.