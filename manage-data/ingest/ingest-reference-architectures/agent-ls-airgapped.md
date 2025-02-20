---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-ls-airgapped.html
---

# Elastic Agent to Logstash: Air-gapped environment [agent-ls-airgapped]

:::{image} ../../../images/ingest-ea-ls-airgapped.png
:alt: Image showing {{agent}}
:::

Ingest model
:   All {{stack}} components deployed inside a DMZ:

    * Control path: {{agent}} to {{fleet}} to {{es}}<br>
    * Data path: {{agent}} to {{es}}


Use when
:   Your self-managed {{stack}} deployment has no access to outside networks


## Resources [airgapped-ls-resources]

Info for air-gapped environments:

* [Installing the {{stack}} in an air-gapped environment](../../../deploy-manage/deploy/cloud-enterprise/air-gapped-install.md)
* [Using a proxy server with Elastic Agent and Fleet](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-agent-proxy-support.md)


## Geoip database management in air-gapped environments [ls-geoip]

The [{{ls}} geoip filter](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/plugins-filters-geoip.md) requires regular database updates to remain up-to-date with the latest information. If you are using the {{ls}} geoip filter plugin in an air-gapped environment, you can manage updates through a proxy, a custom endpoint, or manually. Check out [Manage your own database updates](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/plugins-filters-geoip.md#plugins-filters-geoip-manage_update) for more info.

