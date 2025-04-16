---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuring-howto-apm-server.html
---

# APM settings [apm-configuring-howto-apm-server]

How you configure the APM Server depends on your deployment method.

* **APM Server binary** users need to edit the `apm-server.yml` configuration file. The location of the file varies by platform. To locate the file, see [Installation layout](/solutions/observability/apm/installation-layout.md).
* **Fleet-managed** users configure the APM Server directly in {{kib}}. Each configuration page describes the specific location.
* **Elastic cloud** users should see [Add APM user settings](/reference/apm/cloud/apm-settings.md) for information on how to configure Elastic APM.

The following topics describe how to configure APM Server:

* [General configuration options](/solutions/observability/apm/general-configuration-options.md)
* [Anonymous authentication](/solutions/observability/apm/configure-anonymous-authentication.md)
* [APM agent authorization](/solutions/observability/apm/apm-agent-authorization.md)
* [APM agent central configuration](/solutions/observability/apm/configure-apm-agent-central-configuration.md)
* [Instrumentation](/solutions/observability/apm/configure-apm-instrumentation.md)
* [{{kib}} endpoint](/solutions/observability/apm/configure-kibana-endpoint.md)
* [Logging](/solutions/observability/apm/configure-logging.md)
* [Output](/solutions/observability/apm/configure-output.md)
* [Project paths](/solutions/observability/apm/configure-project-paths.md)
* [Real User Monitoring (RUM)](/solutions/observability/apm/configure-real-user-monitoring-rum.md)
* [SSL/TLS settings](/solutions/observability/apm/ssl-tls-settings.md)
* [Tail-based sampling](/solutions/observability/apm/tail-based-sampling.md)
* [Use environment variables in the configuration](/solutions/observability/apm/use-environment-variables-in-configuration.md)
