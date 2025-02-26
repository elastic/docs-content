---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-proxy-standalone.html
---

# Standalone Elastic Agent connectivity using a proxy server [fleet-agent-proxy-standalone]

Proxy settings in the {{agent}} policy override proxy settings specified by environment variables. This means you can specify proxy settings for {{agent}} that are different from host or system-level environment settings.

The following proxy settings are valid in the agent policy:

| Setting | Description |
| --- | --- |
| `proxy_url` | (string) URL of the proxy server. If set, the configured URL is used as aproxy for all connection attempts by the component. The value may be either acomplete URL or a `host[:port]`, in which case the `http` scheme is assumed. Ifa value is not specified through the configuration, then proxy environmentvariables are used. The URL accepts optional `username` and `password` settingsfor authenticating with the proxy. For example:`http://<username>:<password>@<proxy host>/`. |
| `proxy_headers` | (string) Additional headers to send to the proxy during CONNECT requests. Youcan use this setting to pass keys/tokens required for authenticating with theproxy. |
| `proxy_disable` | (boolean) If set to `true`, all proxy settings, including the `HTTP_PROXY` and`HTTPS_PROXY` environment variables, are ignored. |


## Set the proxy for communicating with {{es}} [_set_the_proxy_for_communicating_with_es]

For standalone agents, to set the proxy for communicating with {{es}}, specify proxy settings in the `elastic-agent.yml` file. For example:

```yaml
outputs:
  default:
    api_key: API-KEY
    hosts:
    - https://10.0.1.2:9200
    proxy_url: http://10.0.1.7:3128
    type: elasticsearch
```

For more information, refer to [*Configure standalone {{agent}}s*](/reference/ingestion-tools/fleet/configure-standalone-elastic-agents.md).

