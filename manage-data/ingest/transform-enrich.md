---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest-overview/current/ingest-addl-proc.html
---

# Transform and enrich data [ingest-addl-proc]

You can start with {{agent}} and Elastic [integrations](https://docs.elastic.co/en/integrations), and still take advantage of additional processing options if you need them.

{{agent}} processors
:   You can use [{{agent}} processors](https://www.elastic.co/guide/en/fleet/current/elastic-agent-processor-configuration.html) to sanitize or enrich raw data at the source. Use {{agent}} processors if you need to control what data is sent across the wire, or if you need to enrich the raw data with information available on the host.

{{es}} ingest pipelines
:   You can use {{es}} [ingest pipelines](https://www.elastic.co/guide/en/elasticsearch/reference/current/) to enrich incoming data or normalize field data before the data is indexed. {{es}} ingest pipelines enable you to manipulate the data as it comes in. This approach helps you avoid adding processing overhead to the hosts from which you’re collecting data.

{{es}} runtime fields
:   You can use {{es}} [runtime fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime.html) to define or alter the schema at query time. You can start working with your data without needing to understand how it is structured, add fields to existing documents without reindexing your data, override the value returned from an indexed field, and/or define fields for a specific use without modifying the underlying schema.

{{ls}} `elastic_integration filter`
:   You can use the {{ls}} [`elastic_integration filter`](https://www.elastic.co/guide/en/logstash/current/) and other [{{ls}} filters](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html) to [extend Elastic integrations](https://www.elastic.co/guide/en/logstash/current/ea-integrations.html) by transforming data before it goes to {{es}}.

