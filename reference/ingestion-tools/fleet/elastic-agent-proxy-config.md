---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-proxy-config.html
---

# When to configure proxy settings [elastic-agent-proxy-config]

Configure proxy settings for {{agent}} when it must connect through a proxy server to:

* Download artifacts from `artifacts.elastic.co` for subprocesses or binary upgrades (use [Agent binary download settings](/reference/ingestion-tools/fleet/fleet-settings.md#fleet-agent-binary-download-settings))
* Send data to {es}
* Retrieve agent policies from {fleet-server}
* Retrieve agent policies from {{es}} (only needed for agents running {{fleet-server}})

:::{image} images/agent-proxy-server.png
:alt: Image showing connections between {agent}
:::

If {{fleet}} is unable to access the {{package-registry}} because {{kib}} is behind a proxy server, you may also need to set the registry proxy URL in the {{kib}} configuration.

:::{image} images/fleet-epr-proxy.png
:alt: Image showing connections between {{fleet}} and the {package-registry}
:::

