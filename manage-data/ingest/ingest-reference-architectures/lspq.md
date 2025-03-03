---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/lspq.html
---

# Elastic Agent to Logstash to Elasticsearch: Logstash Persistent Queue (PQ) for buffering [lspq]

:::{image} ../../../images/ingest-ea-lspq-es.png
:alt: Image showing {{agent}} collecting data
:::

Ingest model
:   {{agent}} to {{ls}} persistent queue to {{es}}

Use when
:   Your data flow may encounter network issues, bursts of events, and/or downstream unavailability and you need the ability to buffer the data before ingestion.


## Resources [lspq-resources]

Info on configuring {{agent}}:

* [Fleet and Elastic Agent Guide](https://www.elastic.co/guide/en/fleet/current)
* [Configuring outputs for {{agent}}](/reference/ingestion-tools/fleet/elastic-agent-output-configuration.md)

For info on {{ls}} plugins:

* [{{agent}} input](logstash://reference/plugins-inputs-elastic_agent.md)
* [{{es}} output plugin](logstash://reference/plugins-outputs-elasticsearch.md)

For info on using {{ls}} for buffering and data resiliency, check out this section in the [Logstash Reference](https://www.elastic.co/guide/en/logstash/current):

* [{{ls}} Persistent Queues (PQ)](logstash://reference/persistent-queues.md)

Info on {{es}}:

* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)

