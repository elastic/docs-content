---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/lspq.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
  - id: logstash
---

# Elastic Agent to Logstash to Elasticsearch: Logstash Persistent Queue (PQ) for buffering [lspq]

:::{image} /manage-data/images/ingest-ea-lspq-es.png
:alt: Image showing {{agent}} collecting data
:::

Ingest model
:   {{agent}} to {{ls}} persistent queue to {{es}}

Use when
:   Your data flow may encounter network issues, bursts of events, or downstream unavailability, and you need the ability to buffer the data before ingestion.


## Resources [lspq-resources]

Info on configuring {{agent}}:

* [Fleet and Elastic Agent Guide](/reference/fleet/index.md)
* [Configuring outputs for {{agent}}](/reference/fleet/elastic-agent-output-configuration.md)

For info on {{ls}} plugins:

* [{{agent}} input](logstash-docs-md://lsr/plugins-inputs-elastic_agent.md)
* [{{es}} output plugin](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md)

For info on using {{ls}} for buffering and data resiliency, check out this section in the [Logstash Reference](logstash://reference/index.md):

* [{{ls}} Persistent Queues (PQ)](logstash://reference/persistent-queues.md)

Info on {{es}}:

* [{{es}} Guide](elasticsearch://reference/index.md)

