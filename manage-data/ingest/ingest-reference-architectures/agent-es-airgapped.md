---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-es-airgapped.html
---

# Elastic Agent to Elasticsearch: Air-gapped environment [agent-es-airgapped]

:::{image} /manage-data/images/ingest-ea-es-airgapped.png
:alt: Image showing {{agent}} and {{es}} in an air-gapped environment
:::

Ingest model
:   All {{stack}} components deployed inside a DMZ:

    * Control path: {{agent}} to {{fleet}} to {{es}}<br>
    * Data path: {{agent}} to {{es}}


Use when
:   Your self-managed {{stack}} deployment has no access to outside networks


## Resources [airgapped-es-resources]

Info for air-gapped environments:

* [Installing the {{stack}} in an air-gapped environment](../../../deploy-manage/deploy/cloud-enterprise/air-gapped-install.md)
* [Using a proxy server with Elastic Agent and Fleet](/reference/ingestion-tools/fleet/fleet-agent-proxy-support.md)

