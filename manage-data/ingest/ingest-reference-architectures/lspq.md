---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/lspq.html
---

# Elastic Agent to Logstash to Elasticsearch: Logstash Persistent Queue (PQ) for buffering [lspq]

:::{image} ../../../images/ingest-ea-lspq-es.png
:alt: Image showing {{agent}} collecting data
:::

Ingest model
:   {{agent}} to {{ls}} persistent queue to {es}

Use when
:   Your data flow may encounter network issues, bursts of events, and/or downstream unavailability and you need the ability to buffer the data before ingestion.


## Resources [lspq-resources]

Info on configuring {{agent}}:

* [Fleet and Elastic Agent Guide](https://www.elastic.co/guide/en/fleet/current)
* [Configuring outputs for {{agent}}](https://www.elastic.co/guide/en/fleet/current/elastic-agent-output-configuration.html)

For info on {{ls}} plugins:

* [{{agent}} input](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-elastic_agent.html)
* [{{es}} output plugin](https://www.elastic.co/guide/en/logstash/current/plugins-outputs-elasticsearch.html)

For info on using {{ls}} for buffering and data resiliency, check out this section in the [Logstash Reference](https://www.elastic.co/guide/en/logstash/current):

* [{{ls}} Persistent Queues (PQ)](https://www.elastic.co/guide/en/logstash/current/persistent-queues.html)

Info on {{es}}:

* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)

