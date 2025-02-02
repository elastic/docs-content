---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-jaeger.html
---

# Jaeger event intake [apm-api-jaeger]

::::{warning}
* Support for Jaeger is deprecated, and will be removed in a future release [#1167](https://github.com/elastic/apm-server/issues/11671)

::::


Elastic APM natively supports Jaeger, an open-source, distributed tracing system. [Learn more](integrate-with-jaeger-deprecated.md).

**Jaeger/gRPC paths**

| Name | Endpoint |
| --- | --- |
| Jaeger span intake | `/jaeger.api_v2.CollectorService/PostSpans` |
| Sampling endpoint | `/jaeger.api_v2.SamplingManager/GetSamplingStrategy` |
