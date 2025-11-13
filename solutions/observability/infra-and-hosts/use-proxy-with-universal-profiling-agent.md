---
navigation_title: Use a proxy
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-use-a-proxy.html
applies_to:
  stack: ga
products:
  - id: observability
---



# Use a proxy with the Universal Profiling Agent [profiling-use-a-proxy]


In some cases, your infrastructure Universal Profiling Agent installation needs to use an HTTP proxy to reach {{ecloud}}. In these cases, you can use the `HTTPS_PROXY` environment variable to configure a proxy used by the Universal Profiling Agent. The connection to the backend ({{ecloud}}) will be tunneled through the proxy (no MITM-TLS) using the CONNECT method. Basic authentication is supported. This can be useful in environments with security policies or network restrictions that block direct connections to outside hosts.

::::{important}
You need to set the `HTTPS_PROXY` environment variable in the machines that will run the Universal Profiling Agents. If you set the environment variable after the Universal Profiling Agent is installed, you may need to reinstall the Universal Profiling Agent.
::::


The following example shows how to use the `HTTPS_PROXY` environment variable:

```bash
export HTTPS_PROXY=http://username:password@proxy:port
```

