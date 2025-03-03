---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/ls-for-input.html
---

# Logstash to Elasticsearch [ls-for-input]

:::{image} ../../../images/ingest-ls-es.png
:alt: Image showing {{ls}} collecting data and sending to {{es}}
:::

Ingest model
:   {{ls}} to collect data from sources not currently supported by {{agent}} and sending the data to {{es}}. Note that the data transformation still happens within the {{es}} ingest pipeline.

Use when
:   {{agent}} doesn’t currently support your data source.

Examples
:   AWS Kinesis, databases, Kafka


## Resources [ls-for-input-resources]

Before you implement this approach, check to see if an {{agent}} integration exists and, if so, use it instead:

* [{{agent}} integrations](https://docs.elastic.co/en/integrations)

Info on {{ls}} and {{ls}} input and output plugins:

* [{{ls}} plugin support matrix](https://www.elastic.co/support/matrix#logstash_plugins)
* [{{ls}} Reference](https://www.elastic.co/guide/en/logstash/current)
* [{{ls}} input plugins](logstash://reference/input-plugins.md)
* [{{es}} output plugin](logstash://reference/plugins-outputs-elasticsearch.md)

Info on {{es}} and ingest pipelines:

* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)
* [{{es}} Ingest Pipelines](../transform-enrich/ingest-pipelines.md)

