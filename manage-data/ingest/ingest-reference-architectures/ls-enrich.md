---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/ls-enrich.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
---

# Elastic Agent to Logstash (for enrichment) to Elasticsearch [ls-enrich]

:::{image} /manage-data/images/ingest-ea-ls-enrich.png
:alt: Image showing {{agent}} collecting data
:::

Ingest models
:   * {{agent}} to {{es}} using {{ls}} to enrich the data
* {{agent}} to {{ls}} for enrichment based on fields in the {{agent}} data to {{es}}


Use when
:   * Data enrichment in {{es}} is not practical for business or technical reasons
* Your use case requires data enrichment based on fields in the {{agent}} data. {{ls}} can collect enrichment data based on those fields, and then send the data to {{es}}.


Examples
:   * Data that changes frequently and is updated using an external source, such as stock ticker data
* Enrichment data is proprietary and cannot be stored elsewhere.
* Enrichment is done with an HTTP API whose return depends on values from the document.<br> Example: An API that takes geo points with the collected data and returns available real estate in the region, and then passes to {{ls}} enrichment for enrichment between agents and {{es}}.



## Resources [ls-enrich-resources]

Info on configuring {{agent}}:

* [Fleet and Elastic Agent Guide](/reference/fleet/index.md)
* [Configuring outputs for {{agent}}](/reference/fleet/elastic-agent-output-configuration.md)

For info on {{ls}} for enriching data, check out these sections in the [Logstash Reference](logstash://reference/index.md):

* [{{ls}} {{agent}} input](logstash-docs-md://lsr/plugins-inputs-elastic_agent.md)
* [{{ls}} plugins for enriching data](logstash://reference/lookup-enrichment.md)
* [Logstash filter plugins](logstash-docs-md://lsr/filter-plugins.md)
* [{{ls}} {{es}} output](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md)

Info on {{es}}:

* [{{es}} Guide](elasticsearch://reference/index.md)

