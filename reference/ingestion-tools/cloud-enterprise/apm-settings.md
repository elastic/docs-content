---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-apm-settings.html#ece_logging_settings_legacy
---

# APM settings for Elastic Cloud Enterprise [ece-manage-apm-settings]

Starting in {{stack}} version 8.0, how you change APM settings and the settings that are available to you depend on how you spin up Elastic APM. There are two modes:

{{fleet}}-managed APM integration
:   New deployments created in {{stack}} version 8.0 and later will be managed by {{fleet}}.

    * This mode requires SSL/TLS configuration. Check [TLS configuration for {{fleet}}-managed mode](#ece-edit-apm-fleet-tls) for details.
    * Check [APM integration input settings](/solutions/observability/apps/configure-apm-server.md) for all other Elastic APM configuration options in this mode.


Standalone APM Server (legacy)
:   Deployments created prior to {{stack}} version 8.0 are in legacy mode. Upgrading to or past {{stack}} 8.0 does not remove you from legacy mode.

    Check [Edit standalone APM settings (legacy)](#ece-edit-apm-standalone-settings-ece)for information on how to configure Elastic APM in this mode.


To learn more about the differences between these modes, or to switch from Standalone APM Server (legacy) mode to {{fleet}}-managed, check [Switch to the Elastic APM integration](/solutions/observability/apps/switch-to-elastic-apm-integration.md).


## TLS configuration for {{fleet}}-managed mode [ece-edit-apm-fleet-tls]

Users running {{stack}} versions 7.16 or 7.17 need to manually configure TLS. This step is not necessary for {{stack}} versions ≥ 8.0.

Pick one of the following options:

1. Upload and configure a publicly signed {{es}} TLS certificates. Check [Encrypt traffic in clusters with a self-managed Fleet Server](/reference/ingestion-tools/fleet/secure-connections.md) for details.
2. Change the {{es}} hosts where {{agent}}s send data from the default public URL, to the internal URL. In {{kib}}, navigate to **Fleet** and select the **Elastic Cloud agent policy**. Click **Fleet settings** and update the {{es}} hosts URL. For example, if the current URL is `https://123abc.us-central1.gcp.foundit.no:9244`, change it to `http://123abc.containerhost:9244`.


## Edit standalone APM settings (legacy) [ece-edit-apm-standalone-settings-ece]

Elastic Cloud Enterprise supports most of the legacy APM settings. Through a YAML editor in the console, you can append your APM Server properties to the `apm-server.yml` file. Your changes to the configuration file are read on startup.

::::{important}
Be aware that some settings could break your cluster if set incorrectly and that the syntax might change between major versions. Before upgrading, be sure to review the full list of the [latest APM settings and syntax](/solutions/observability/apps/configure-apm-server.md).
::::


To change APM settings:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **APM** section, select **Edit user settings**. (For existing deployments with user settings, you may have to expand the **Edit apm-server.yml** caret instead.)
5. Update the user settings.
6. Select **Save changes**.

::::{note}
If a setting is not supported by Elastic Cloud Enterprise, you get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported.
::::



## Example: Enable RUM and increase the rate limit (legacy) [ece_example_enable_rum_and_increase_the_rate_limit_legacy]

When capturing the user interaction with clients with real user monitoring (RUM), particularly for situations with concurrent clients, you can increase the number of times each IP address can send a request to the RUM endpoint. Version 6.5 includes an additional settings for the LRU cache.

For APM Server with RUM agent version 2.x or 3.x:

```sh
apm-server:
  rum:
    enabled: true
    event rate:
      limit: 3000
      lru_size: 5000
```


## Example: Disable RUM (legacy) [ece_example_disable_rum_legacy]

If you know that you won’t be tracking RUM data, you can disable the endpoint proactively.

```sh
apm-server:
  rum:
    enabled: false
```


## Example: Adjust the event limits configuration (legacy) [ece_example_adjust_the_event_limits_configuration_legacy]

If the size of the HTTP request frequently exceeds the maximum, you might need to change the limit on the APM Server and adjust the relevant settings in the agent.

```sh
apm-server:
  max_event_size: 407200
```
