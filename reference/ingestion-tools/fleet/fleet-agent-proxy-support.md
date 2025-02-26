---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-proxy-support.html
---

# Using a proxy server with Elastic Agent and Fleet [fleet-agent-proxy-support]

Many enterprises secure their assets by placing a proxy server between them and the internet. The main role of the proxy server is to filter content and provide a single gateway through which all traffic traverses in and out of a data center. These proxy servers provide a various degree of functionality, security and privacy.

Your organization’s security strategy and other considerations may require you to use a proxy server between some components in your deployment. For example, you may have a firewall rule that prevents endpoints from connecting directly to {{es}}. In this scenario, you can set up the {{agent}} to connect to a proxy, then the proxy can connect to {{es}} through the firewall.

Support is available in {{agent}} and {{fleet}} for connections through HTTP Connect (HTTP 1 only) and SOCKS5 proxy servers.

::::{note}
Some environments require users to authenticate with the proxy. There are no explicit settings for proxy authentication in {{agent}} or {{fleet}}, except the ability to pass credentials in the URL or as keys/tokens in headers, as described later.
::::


Refer to [When to configure proxy settings](/reference/ingestion-tools/fleet/elastic-agent-proxy-config.md) for more detail, or jump into one of the following guides:

* [Proxy Server connectivity using default host variables](/reference/ingestion-tools/fleet/host-proxy-env-vars.md)
* [Fleet managed {{agent}} connectivity using a proxy server](/reference/ingestion-tools/fleet/fleet-agent-proxy-managed.md)
* [Standalone {{agent}} connectivity using a proxy server](/reference/ingestion-tools/fleet/fleet-agent-proxy-standalone.md)






