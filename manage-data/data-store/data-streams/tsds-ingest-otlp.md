---
navigation_title: "OTLP/HTTP endpoint"
description: "How OpenTelemetry metrics sent to the Elasticsearch OTLP/HTTP endpoint are stored in time series data streams."
applies_to:
  deployment:
    self: ga 9.2
    ece: ga
    eck: ga
products:
  - id: elasticsearch
---

# Ingest metrics into a TSDS using the OTLP/HTTP endpoint

{{es}} accepts OpenTelemetry metrics on `/_otlp/v1/metrics`, one of the [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) paths.
The endpoint is a native ingest API, like the [bulk API]({{es-apis}}operation/operation-bulk).
To decide how to send OpenTelemetry metrics to {{es}}, refer to [When to use the {{es}} OTLP endpoint](/manage-data/ingest/otlp-endpoint.md#when-to-use): in most setups, applications send metrics to the {{motlp}} or to an [{{agent}} in Gateway mode](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode) rather than to this endpoint.

Metrics that arrive on `/_otlp/v1/metrics` are stored as follows:

* Records are written to [{{tsdses}}](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md).
  Built-in index templates create the data streams on first write, and [routing](/manage-data/ingest/otlp-endpoint.md#routing-to-data-streams) follows the `<type>-<dataset>.otel-<namespace>` pattern.
* Dimensions and metric mappings are derived from OTLP metadata, so there's no need to set them up manually.
  Metric points are [deduplicated based on their dimensions and timestamp](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension).
* Histogram metrics are stored using the `exponential_histogram` or `histogram` field type, depending on the [histogram handling setting](/manage-data/ingest/otlp-endpoint.md#configure-histogram-handling-for-metrics).
* {applies_to}`stack: ga 9.5+` The [temporality](/manage-data/data-store/data-streams/metric-temporality.md) of each metric is preserved in a `temporality` dimension, so counters and histograms are interpreted correctly in {{esql}} time series queries and during downsampling.

For request details, authentication, and limitations, refer to the [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) reference.
