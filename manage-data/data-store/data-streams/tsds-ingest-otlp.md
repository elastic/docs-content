---
navigation_title: "OTLP/HTTP endpoint"
description: "Ingest OpenTelemetry metrics into time series data streams through the Elasticsearch OTLP/HTTP endpoint."
applies_to:
  deployment:
    self: ga 9.2
    ece: ga
    eck: ga
products:
  - id: elasticsearch
---

# Ingest metrics into a TSDS using the OTLP/HTTP endpoint

{{es}} supports metrics ingestion through the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp).

For OpenTelemetry metrics, prefer the {{es}} OTLP/HTTP endpoint over the Bulk API because it's optimized for OTLP ingest performance.
It also simplifies setup by automatically creating [TSDS](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) through built-in index templates, and deriving dimensions and metric mappings from OTLP metadata.

For more details, refer to the [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) reference.
