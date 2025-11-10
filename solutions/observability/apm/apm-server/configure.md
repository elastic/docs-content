---
navigation_title: Configure
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-apm-settings.html
  - https://www.elastic.co/guide/en/observability/current/apm-configuring-howto-apm-server.html
applies_to:
  stack: ga
products:
  - id: cloud-hosted
  - id: observability
---

# Configure APM Server [apm-configuring-howto-apm-server]

How you configure the APM Server depends on your deployment method.

* **APM Server binary** users need to edit the `apm-server.yml` configuration file. The location of the file varies by platform. To locate the file, see [Installation layout](/solutions/observability/apm/apm-server/installation-layout.md).
* **Fleet-managed** users configure the APM Server directly in {{kib}}. Each configuration page describes the specific location.
* **Elastic cloud** users should see [Add APM user settings](/solutions/observability/apm/apm-server/configure.md) for information on how to configure Elastic APM.

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

## Edit APM user settings [ec-manage-apm-settings]

Change how Elastic APM runs by providing your own user settings. Starting in {{stack}} version 8.0, how you change APM settings and the settings that are available to you depend on how you spin up Elastic APM. There are two modes:

{{fleet}}-managed APM integration
:   New deployments created in {{stack}} version 8.0 and later will be managed by {{fleet}}.

    Check [APM configuration reference](/solutions/observability/apm/apm-server/configure.md) for information on how to configure Elastic APM in this mode.

Standalone APM Server (legacy)
:   Deployments created prior to {{stack}} version 8.0 are in legacy mode. Upgrading to or past {{stack}} 8.0 will not remove you from legacy mode.

    Check [Edit standalone APM settings (legacy)](/solutions/observability/apm/apm-server/configure.md#ec-edit-apm-standalone-settings) and [Supported standalone APM settings (legacy)](/solutions/observability/apm/apm-server/configure.md#ec-apm-settings) for information on how to configure Elastic APM in this mode.

To learn more about the differences between these modes, or to switch from Standalone APM Server (legacy) mode to {{fleet}}-managed, check [Switch to the Elastic APM integration](/solutions/observability/apm/switch-to-elastic-apm-integration.md).

## Edit standalone APM settings (legacy) [ec-edit-apm-standalone-settings]

User settings are appended to the `apm-server.yml` configuration file for your instance and provide custom configuration options.

To add user settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. In the **APM** section, select **Edit user settings**. (For existing deployments with user settings, you may have to expand the **Edit apm-server.yml** caret instead.)
5. Update the user settings.
6. Select **Save changes**.

::::{note}
If a setting is not supported on {{ecloud}}, you will get an error message when you try to save.
::::

## Supported standalone APM settings (legacy) [ec-apm-settings]

{{ech}} supports the settings listed in [APM documentation](/solutions/observability/apm/apm-server/configure.md) under "APM Server binary" when running APM in standalone mode (legacy). For versions before 9, refer to [older documentation](https://www.elastic.co/guide/en/observability/8.18/apm-configuring-howto-apm-server.html).

::::{note}
Some settings are intentionally restricted to maintain system stability.
::::

::::{note}
To change logging settings you must first [enable deployment logging](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md).
::::
