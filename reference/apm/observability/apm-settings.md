---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuring-howto-apm-server.html
products:
  - id: observability
---

# APM settings [apm-configuring-howto-apm-server]

How you configure the APM Server depends on your deployment method.

* **APM Server binary** users need to edit the `apm-server.yml` configuration file. The location of the file varies by platform. To locate the file, see [Installation layout](/solutions/observability/apm/apm-server/installation-layout.md).
* **Fleet-managed** users configure the APM Server directly in {{kib}}. Each configuration page describes the specific location.
* **Elastic cloud** users should see [Add APM user settings](/reference/apm/cloud/apm-settings.md) for information on how to configure Elastic APM.

The following topics describe how to configure APM Server:

* [General configuration options](/solutions/observability/apm/apm-server/general-configuration-options.md)
* [Anonymous authentication](/solutions/observability/apm/apm-server/configure-anonymous-authentication.md)
* [APM agent authorization](/solutions/observability/apm/apm-server/apm-agent-authorization.md)
* [APM agent central configuration](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md)
* [Instrumentation](/solutions/observability/apm/apm-server/configure-apm-instrumentation.md)
* [{{kib}} endpoint](/solutions/observability/apm/apm-server/configure-kibana-endpoint.md)
* [Logging](/solutions/observability/apm/apm-server/configure-logging.md)
* [Output](/solutions/observability/apm/apm-server/configure-output.md)
* [Project paths](/solutions/observability/apm/apm-server/configure-project-paths.md)
* [Real User Monitoring (RUM)](/solutions/observability/apm/apm-server/configure-real-user-monitoring-rum.md)
* [SSL/TLS settings](/solutions/observability/apm/apm-server/ssl-tls-settings.md)
* [Tail-based sampling](/solutions/observability/apm/apm-server/tail-based-sampling.md)
* [Use environment variables in the configuration](/solutions/observability/apm/apm-server/use-environment-variables-in-configuration.md)
