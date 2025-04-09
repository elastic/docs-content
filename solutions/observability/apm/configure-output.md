---
navigation_title: "Output"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuring-output.html
applies_to:
  stack:
---

# Configure the output [apm-configuring-output]

Output configuration options.

* [{{ech}}](/solutions/observability/apm/configure-output-for-elasticsearch-service-on-elastic-cloud.md)
* [{{es}}](/solutions/observability/apm/configure-elasticsearch-output.md)
* [{{ls}}](/solutions/observability/apm/configure-logstash-output.md)
* [Kafka](/solutions/observability/apm/configure-kafka-output.md)
* [Redis](/solutions/observability/apm/configure-redis-output.md)
* [Console](/solutions/observability/apm/configure-console-output.md)

## Source maps [apm-sourcemap-output]

Source maps can be uploaded through all outputs but must eventually be stored in {{es}}. When using outputs other than {{es}}, `source_mapping.elasticsearch` must be set for source maps to be applied. Be sure to update `source_mapping.index_pattern` if source maps are stored in the non-default location. See [`source_mapping.elasticsearch`](/solutions/observability/apm/configure-real-user-monitoring-rum.md#apm-config-sourcemapping-elasticsearch) for more details.

