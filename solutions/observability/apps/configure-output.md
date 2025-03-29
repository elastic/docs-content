---
navigation_title: "Output"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuring-output.html
applies_to:
  stack: all
---



# Configure the output [apm-configuring-output]


Output configuration options.

* [{{ech}}](configure-output-for-elasticsearch-service-on-elastic-cloud.md)
* [{{es}}](configure-elasticsearch-output.md)
* [{{ls}}](configure-logstash-output.md)
* [Kafka](configure-kafka-output.md)
* [Redis](configure-redis-output.md)
* [Console](configure-console-output.md)


## Source maps [apm-sourcemap-output]

Source maps can be uploaded through all outputs but must eventually be stored in {{es}}. When using outputs other than {{es}}, `source_mapping.elasticsearch` must be set for source maps to be applied. Be sure to update `source_mapping.index_pattern` if source maps are stored in the non-default location. See [`source_mapping.elasticsearch`](configure-real-user-monitoring-rum.md#apm-config-sourcemapping-elasticsearch) for more details.







