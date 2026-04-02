---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-installed.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
---

# Elastic Agent to Elasticsearch: Agent installed [agent-installed]

:::{image} /manage-data/images/ingest-ea-agent-installed.png
:alt: Image showing {{agent}} collecting data and sending to {{es}}
:::

Ingest model
:   Control path: {{agent}} to {{fleet}} to {{es}}<br> Data path: {{agent}} to {{es}}

Use when
:   An {{agent}} integration exists in the {{kib}} integrations UI for the software you want to monitor, observe, and protect.

Examples
:   * System integration that collects metrics and logs from operating systems
* Kubernetes integration that collects metrics and logs from Kubernetes master and worker nodes, and from workloads running on worker node pods



## Process overview [agent-proc]

* Find the integration for your data source. In {{kib}},  go to **Management> Integrations**.
* Enable the integration and set up {{agent}}.
* Launch discover/dashboard to explore.

For details and next steps, check out the [{{agent}} integrations](https://docs.elastic.co/en/integrations) docs for your data source.

