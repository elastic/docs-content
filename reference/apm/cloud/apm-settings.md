---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-apm-settings.html#ec-apm-settings
products:
  - id: cloud-hosted
---

# APM settings for Elastic Cloud [ec-manage-apm-settings]

Change how Elastic APM runs by providing your own user settings. Starting in {{stack}} version 8.0, how you change APM settings and the settings that are available to you depend on how you spin up Elastic APM. There are two modes:

{{fleet}}-managed APM integration
:   New deployments created in {{stack}} version 8.0 and later will be managed by {{fleet}}.

    Check [APM configuration reference](/solutions/observability/apm/apm-server/configure.md) for information on how to configure Elastic APM in this mode.


Standalone APM Server (legacy)
:   Deployments created prior to {{stack}} version 8.0 are in legacy mode. Upgrading to or past {{stack}} 8.0 will not remove you from legacy mode.

    Check [Edit standalone APM settings (legacy)](#ec-edit-apm-standalone-settings) and [Supported standalone APM settings (legacy)](#ec-apm-settings) for information on how to configure Elastic APM in this mode.


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
If a setting is not supported by {{ech}}, you will get an error message when you try to save.
::::



## Supported standalone APM settings (legacy) [ec-apm-settings]

{{ech}} generally supports the settings listed in [APM documentation](/solutions/observability/apm/apm-server/configure.md) under "APM Server binary" when running APM in standalone mode (legacy). For versions before 9, refer to [older documentation](https://www.elastic.co/guide/en/observability/8.18/apm-configuring-howto-apm-server.html).

::::{note}
Some settings are intentionally restricted to maintain system stability.
::::

::::{note}
To change logging settings you must first [enable deployment logging](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md).
::::
