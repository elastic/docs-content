---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-to-es.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
---

# Elastic Agent to Elasticsearch [agent-to-es]

To ingest data into {{es}}, use the *simplest option that meets your needs* and satisfies your use case.

Integrations offer advantages beyond easier data collection—advantages such as dashboards, central agent management, and easy enablement of [Elastic solutions](https://www.elastic.co/products/), such as Security and Observability.

:::{image} /manage-data/images/ingest-ea-es.png
:alt: Image showing {{agent}} collecting data and sending to {{es}}
:::


## {{agent}} to {{es}} architectures [agent-flavors]

* [{{agent}} to {{es}}: Agent installed](agent-installed.md)
* [{{agent}} to {{es}}: APIs for collection](agent-apis.md)


## Resources [agent-resources]

Info on {{agent}} and agent integrations:

* [Fleet and Elastic Agent Guide](/reference/fleet/index.md)
* [{{agent}} integrations](https://docs.elastic.co/en/integrations)

Info on {{es}}:

* [{{es}} Guide](elasticsearch://reference/index.md)

This basic architecture is a common approach for ingesting data for the [Elastic Observability](https://www.elastic.co/observability) and [Elastic Security](https://www.elastic.co/security) solutions:

* [Elastic Observability tutorials](/solutions/observability/get-started.md)
* [Ingest data to Elastic Security](../../../solutions/security/get-started/ingest-data-to-elastic-security.md)



