---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-kafka-essink.html
---

# Elastic Agent to Logstash to Kafka to Kafka ES Sink to Elasticsearch: Kafka as middleware message queue [agent-kafka-essink]

:::{image} /manage-data/images/ingest-ls-kafka-essink.png
:alt: Image showing {{agent}} collecting data and using Kafka as a message queue enroute to {{es}}
:::

Ingest model
:   Control path: {{agent}} to {{fleet}} to {{es}}<br> Data path: {{agent}} to {{ls}} to Kafka to Kafka ES Sink to {{es}}: Kafka as middleware message queue.

    Kafka ES Sink connector reads from Kafka and writes to {{es}}.


Use when
:   You are standardizing on Kafka as middleware message queue between {{agent}} and {{es}}

Notes
:   The transformation from raw data to Elastic Common Schema (ECS) and any other enrichment can be handled by {{ls}} as described in [{{agent}} to {{ls}} (for enrichment) to {{es}}](ls-enrich.md).


## Resources [agent-kafka-essink-resources]

Info on {{agent}} and agent integrations:

* [Fleet and Elastic Agent Guide](https://www.elastic.co/guide/en/fleet/current)
* [{{agent}} integrations](https://docs.elastic.co/en/integrations)

Info on {{ls}} and {{ls}} plugins:

* [{{ls}} Reference](https://www.elastic.co/guide/en/logstash/current)
* [{{ls}} {{agent}} input](logstash://reference/plugins-inputs-elastic_agent.md)
* [{{ls}} Kafka output](logstash://reference/plugins-outputs-kafka.md)

Info on {{es}}:

* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)
* ES sink [ToDo: Add link]

