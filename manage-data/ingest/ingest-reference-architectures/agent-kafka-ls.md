---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-kafka-ls.html
---

# Elastic Agent to Logstash to Kafka to Logstash to Elasticsearch: Kafka as middleware message queue [agent-kafka-ls]

:::{image} ../../../images/ingest-ls-kafka-ls.png
:alt: Image showing connections between {{agent}} and {{es}} using a Kafka messaging queue
:::

Ingest model
:   Control path: {{agent}} to {{fleet}} to {{es}}<br> Data path: {{agent}} to {{ls}} to Kafka to {{ls}} to {{es}}: Kafka as middleware message queue.

    {{ls}} reads data from Kafka and routes it to {{es}} clusters (and/or other destinations)


Use when
:   You are standardizing on Kafka as middleware message queue between {{agent}} and {{es}}

Notes
:   The transformation from raw data to Elastic Common Schema (ECS) and any other enrichment can be handled by {{ls}} as described in [{{agent}} to {{ls}} (for enrichment) to {{es}}](ls-enrich.md).


## Resources [agent-kafka-resources]

Info on {{agent}} and agent integrations:

* [Fleet and Elastic Agent Guide](https://www.elastic.co/guide/en/fleet/current)
* [{{agent}} integrations](https://docs.elastic.co/en/integrations)

Info on {{ls}} and {{ls}} Kafka plugins:

* [{{ls}} Reference](https://www.elastic.co/guide/en/logstash/current)
* [{{ls}} {{agent}} input](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-elastic_agent.html)
* [{{ls}} Kafka input](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-kafka.html)
* [{{ls}} Kafka output](https://www.elastic.co/guide/en/logstash/current/plugins-outputs-kafka.html)
* [{{ls}} Elasticsearch output](https://www.elastic.co/guide/en/logstash/current/plugins-outputs-elasticsearch.html)

Info on {{es}}:

* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)

