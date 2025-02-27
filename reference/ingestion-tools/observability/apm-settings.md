---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuring-howto-apm-server.html
---

# APM settings [apm-configuring-howto-apm-server]

How you configure the APM Server depends on your deployment method.

* **APM Server binary** users need to edit the `apm-server.yml` configuration file. The location of the file varies by platform. To locate the file, see [Installation layout](/solutions/observability/apps/installation-layout.md).
* **Fleet-managed** users configure the APM Server directly in {{kib}}. Each configuration page describes the specific location.
* **Elastic cloud** users should see [Add APM user settings](/reference/ingestion-tools/cloud/apm-settings.md) for information on how to configure Elastic APM.

The following topics describe how to configure APM Server:

* [General configuration options](/solutions/observability/apps/general-configuration-options.md)
* [Anonymous authentication](/solutions/observability/apps/configure-anonymous-authentication.md)
* [APM agent authorization](/solutions/observability/apps/apm-agent-authorization.md)
* [APM agent central configuration](/solutions/observability/apps/configure-apm-agent-central-configuration.md)
* [Instrumentation](/solutions/observability/apps/configure-apm-instrumentation.md)
* [{{kib}} endpoint](/solutions/observability/apps/configure-kibana-endpoint.md)
* [Logging](/solutions/observability/apps/configure-logging.md)
* [Output](/solutions/observability/apps/configure-output.md)
* [Project paths](/solutions/observability/apps/configure-project-paths.md)
* [Real User Monitoring (RUM)](/solutions/observability/apps/configure-real-user-monitoring-rum.md)
* [SSL/TLS settings](/solutions/observability/apps/ssltls-settings.md)
* [Tail-based sampling](/solutions/observability/apps/tail-based-sampling.md)
* [Use environment variables in the configuration](/solutions/observability/apps/use-environment-variables-in-configuration.md)
