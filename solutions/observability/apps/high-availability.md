---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-high-availability.html
applies_to:
  stack: all
---

# High Availability [apm-high-availability]

To achieve high availability you can place multiple instances of APM Server behind a regular HTTP load balancer, for example HAProxy or Nginx.

The endpoint `/` always returns an `HTTP 200`. You can configure your load balancer to send HTTP requests to this endpoint to determine if an APM Server is running. See [APM Server information API](apm-server-information-api.md) for more information on that endpoint.

In case of temporal issues, like unavailable {{es}} or a sudden high workload, APM Server does not have an internal queue to buffer requests, but instead leverages an HTTP request timeout to act as back-pressure.

If {{es}} goes down, the APM Server will eventually deny incoming requests. Both the APM Server and {{apm-agent}}(s) will issue logs accordingly.

::::{tip}
Fleet-managed APM Server users might also be interested in [Fleet/Agent proxy support](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-agent-proxy-support.md).
::::


