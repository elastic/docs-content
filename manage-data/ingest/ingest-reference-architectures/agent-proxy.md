---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-proxy.html
products:
  - id: elastic-agent
---

# Elastic Agent to proxy to Elasticsearch [agent-proxy]

:::{image} /manage-data/images/ingest-ea-proxy-fs-es.png
:alt: Image showing connections between {{agent}} and {{es}} using a proxy when Fleet Server is managed by Elastic
:::

:::{image} /manage-data/images/ingest-ea-fs-proxy-es.png
:alt: Image showing connections between {{agent}} and {{es}} using a proxy
:::

::::{tip}
This architecture works with a variety of proxying tools to allow for more flexibility in your environment. Consider using [{{ls}} as a proxy](ls-networkbridge.md), as {{ls}} and the rest of the {{stack}} are designed and tested to work together, and can be easier to support.
::::


Ingest model
:   <br> Control path for {{fleet-server}} on {{ecloud}}: {{agent}} to proxy to {{fleet-server}} to {{es}}<br> Control path for self-managed {{fleet-server}}: {{agent}} to {{fleet-server}} to proxy to {{es}}<br> Data path: {{agent}} to proxy to {{es}}

Use when
:   * Network restrictions prevent connection between {{agent}} network and network where {{fleet-server}} and {{stack}} are deployed, as when {{fleet-server}} is deployed on {{ecloud}}
* Network restrictions prevent connection between {{agent}} and {{fleet-server}} network and the network where {{stack}} is deployed, as when {{stack}} is deployed on {{ecloud}}
* Using [{{ls}} as proxy](ls-networkbridge.md) is not feasible.


Currently {{agent}} is not able to present a certificate for connectivity to {{fleet-server}}. Therefore if a proxy placed between the {{agent}} and {{fleet-server}} is configured for mutual TLS, {{agents}} won’t be able to establish connectivity to {{fleet-server}}.


## Resources [agent-proxy-resources]

Info on {{agent}} and agent integrations:

* [Fleet and Elastic Agent Guide](/reference/fleet/index.md)
* [{{agent}} integrations](https://docs.elastic.co/en/integrations)

Info on using a proxy server:

* [Using a proxy server with {{agent}} and {{fleet}}](/reference/fleet/fleet-agent-proxy-support.md)

Info on {{es}}:

* [{{es}} Guide](elasticsearch://reference/index.md)

