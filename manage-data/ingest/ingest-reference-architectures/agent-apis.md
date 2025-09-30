---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-apis.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
---

# Elastic Agent to Elasticsearch: APIs for collection [agent-apis]

:::{image} /manage-data/images/ingest-ea-apis.png
:alt: Image showing {{agent}} collecting data using APIs and sending to {{es}}
:::

Ingest model
:   Control path: {{agent}} to {{fleet}} to {{es}}<br> Data path: {{agent}} running on a user-managed host to collect data about the external infrastructure through APIs, and then forwarding to {{es}}

Use when
:   An {{agent}} integration exists for software components that expose APIs for data collection

Examples
:   Cloudflare or any other data sources that exposes API for data retrieval


## Process overview [api-proc]

* Find the integration for your data source. In {{kib}},  go to **Management> Integrations**.
* Enable the integration and set up {{agent}}.
* Create a collector VM/container and run {{agent}} and the integration to scrape the external API. Or, set up the external API to push data to the {{agent}} running the integration.

For details and next steps, check out the [{{agent}} integrations](https://docs.elastic.co/en/integrations) docs for your data source.

