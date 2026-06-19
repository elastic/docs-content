## June 16, 2026 [elastic-2026-06-16-breaking-changes]

::::{dropdown} Deprecate elastic.apm settings
  For more information, check [#272414](https://github.com/elastic/kibana/pull/272414).

  **Impact:** Elastic APM instrumentation is deprecated and will be removed in future versions.

  **Action:** Use the OpenTelemetry instrumentation when collecting traces and metrics from Kibana. Refer to [these docs](https://www.elastic.co/docs/extend/kibana/kibana-debugging#_instrumenting_with_otel_traces) for more information about how to configure it.
::::
