---
applies_to:
  stack: ga
  serverless: unavailable
---

# Work with APM Server

When self-managing the Elastic Stack, APM Server receives performance data from APM agents,
validates and processes it, and transforms the data into {{es}} documents.

This section contains information on working with APM Server including:

* Learning how to [set up APM Server](/solutions/observability/apm/apm-server/setup.md)
* Browsing all available [APM Server configuration options](/solutions/observability/apm/apm-server/configure.md)
* [Monitoring the real-time health and performance](/solutions/observability/apm/apm-server/monitor.md) of your APM Server

:::{tip}
If you're using {{serverless-full}}, there is no APM Server running. Instead the _managed intake service_ receives and transforms data. Read more in [](/solutions/observability/apm/get-started.md).
:::
