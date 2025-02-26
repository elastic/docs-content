---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/ls-networkbridge.html
---

# Elastic Agent to Logstash to Elasticsearch: Logstash as a proxy [ls-networkbridge]

:::{image} ../../../images/ingest-ea-ls-bridge.png
:alt: Image showing {{agent}}s collecting data and sending to {{ls}} for proxying before sending on to {{es}}
:::

Ingest model
:   Data path: {{agent}} to {{ls}} as bridge to {{es}} on {{stack}} network<br> Control path: {{agent}} to {{fleet-server}} to {{es}}

Use when
:   Agents have network restrictions for connecting to {{es}} on {{stack}} deployed outside of the agent network

Example
:   You can send data from multiple {{agent}}s through your demilitarized zone (DMZ) to {{ls}}, and then use {{ls}} as a proxy through your firewall to {{ecloud}}. This approach helps reduce the number of firewall exceptions needed to forward data from large numbers of {{agent}}s.


## Resources [ls-networkbridge-resources]

Info on configuring {{agent}}:

* [Fleet and Elastic Agent Guide](https://www.elastic.co/guide/en/fleet/current)
* [Configuring outputs for {{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/elastic-agent-output-configuration.md)

Info on {{ls}} and {{ls}} plugins:

* [{{ls}} Reference](https://www.elastic.co/guide/en/logstash/current)
* [{{es}} output plugin](asciidocalypse://docs/logstash/docs/reference/plugins-outputs-elasticsearch.md)

Info on {{es}}:

* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)

