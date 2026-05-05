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

{{es}} can ingest metrics through the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp) and store them as [time series data streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md).

The {{es}} OTLP/HTTP endpoint writes metrics to `metrics-*` data streams.
It automatically sets up the time series data streams, index templates, dimensions, and metric mappings from the incoming OTLP metadata.

For more details, refer to the [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) reference.
