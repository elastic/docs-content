---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/epr-proxy-setting.html
---

# Set the proxy URL of the Elastic Package Registry [epr-proxy-setting]

{{fleet}} might be unable to access the {{package-registry}} because {{kib}} is behind a proxy server.

Also your organization might have network traffic restrictions that prevent {{kib}} from reaching the public {{package-registry}} (EPR) endpoints, like [epr.elastic.co](https://epr.elastic.co/), to download package metadata and content. You can route traffic to the public endpoint of EPR through a network gateway, then configure proxy settings in the [{{kib}} configuration file](kibana://docs/reference/configuration-reference/fleet-settings.md), `kibana.yml`. For example:

```yaml
xpack.fleet.registryProxyUrl: your-nat-gateway.corp.net
```

## What information is sent to the {{package-registry}}? [_what_information_is_sent_to_the_package_registry]

In production environments, {{kib}}, through the {{fleet}} plugin, is the only service interacting with the {{package-registry}}. Communication happens when interacting with the Integrations UI, and when upgrading {{kib}}. The shared information is about discovery of Elastic packages and their available versions. In general, the only deployment-specific data that is shared is the {{kib}} version.


