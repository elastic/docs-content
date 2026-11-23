---
navigation_title: Feature flags
description: Turn feature flags on or off in elastic-agent.yml to change how a standalone Elastic Agent behaves, such as FQDN reporting, config encryption, default processors, and agent tags.
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-standalone-feature-flags.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Configure feature flags for standalone {{agent}}s [elastic-agent-standalone-feature-flags]


The `agent.features` section of the `elastic-agent.yml` file contains settings that change the default behavior of {{agent}}. These settings might include experimental features, changes to behaviors within {{agent}} or its components, or settings that could cause a breaking change. For example, a setting that changes information included in events might be inconsistent with the naming pattern expected in your configured {{agent}} output.

Most of these settings are turned off by default. To change a setting, set its `enabled` flag. For example, to turn on a setting that's off by default, set `enabled` to `true`:

```yaml
agent.features:
  mysetting:
    enabled: true
```


## Feature flag configuration settings [elastic-agent-standalone-feature-flag-settings]

You can specify the following settings in the `agent.features` section of the `elastic-agent.yml` file.

`default_processors` {applies_to}`stack: ga 9.4+`
:   Controls the default processors that {{agent}} uses to add metadata to the events it collects. Depending on the input, these are the [`add_host_metadata`](/reference/fleet/add_host_metadata-processor.md), [`add_cloud_metadata`](/reference/fleet/add-cloud-metadata-processor.md), [`add_docker_metadata`](/reference/fleet/add_docker_metadata-processor.md), and [`add_kubernetes_metadata`](/reference/fleet/add_kubernetes_metadata-processor.md) processors. You can turn off these processors when you don't need the metadata they add, for example to reduce the size of your events. Turning them off removes the fields they add, so check that the dashboards, alerts, and other features you use don't rely on those fields.

    Depending on your version, the default processor settings apply to the following:

    * {applies_to}`stack: ga 9.6+` All data that {{agent}} collects
    * {applies_to}`stack: ga =9.5` All data that {{agent}} collects except data from inputs that use variables from [dynamic providers](/reference/fleet/providers.md#dynamic-providers), such as `${kubernetes.*}` or `${docker.*}`
    * {applies_to}`stack: ga =9.4` Only metrics and {{agent}} monitoring data, except metrics from inputs that use variables from dynamic providers

    To turn off all four processors, set `enabled` to `false` for the `default_processors` setting:

    ```yaml
    agent.features:
      default_processors:
        enabled: false
    ```

    {applies_to}`stack: ga 9.6+` You can also [turn off individual processors for all outputs](#elastic-agent-standalone-feature-flag-default-processors), or [turn off processors only for the data sent to a specific output](/reference/fleet/elastic-agent-output-configuration.md#elastic-agent-output-default-processors).

`encrypted_config` {applies_to}`stack: ga 9.4+`
:   Encrypts the configuration of a standalone {{agent}}. When enabled, {{agent}} encrypts the contents of `elastic-agent.yml` and stores them in `fleet.enc`. It then replaces the contents of `elastic-agent.yml` with only the `encrypted_config` setting, to show that {{agent}} uses the encrypted configuration.

    ::::{note}
    {{fleet}}-managed {{agents}} ignore this flag as they always encrypt storage.
    ::::

    To reload the config, replace the `elastic-agent.yml` file and restart the {{agent}}.

    To enable encrypted config for a standalone {{agent}}, set `enabled: true` for the `encrypted_config` setting:

    ```yaml
    agent.features:
      encrypted_config:
        enabled: true
    ```

    ::::{note}
    If you turn off encryption, delete the `fleet.enc` file manually.
    ::::

`fqdn`
:   Reports the current host name in fully qualified domain name (FQDN) format. When enabled, the [host.name](/reference/fleet/host-provider.md) key in events produced by {{agent}} contains `somehost.example.com` rather than `somehost`. This helps you to distinguish between hosts on different domains that have similar names. With `fqdn` enabled, the fully qualified hostname allows each host to be more easily identified when viewed in {{kib}}.

    ::::{note}
    FQDN reporting is not currently supported in APM.
    ::::

    For FQDN reporting to work as expected, the hostname of the current host must either:

    * Have a CNAME entry defined in DNS.
    * Have one of its corresponding IP addresses respond successfully to a reverse DNS lookup.

    If neither prerequisite is satisfied, `host.name` continues to report the hostname of the current host as if the FQDN feature flag were not enabled.

    To enable fully qualified domain names, set `enabled: true` for the `fqdn` setting:

    ```yaml
    agent.features:
      fqdn:
        enabled: true
    ```

`include_tags_in_events` {applies_to}`stack: ga 9.6+`
:   Adds the {{agent}} tags that you list in the `agent.tags` setting of `elastic-agent.yml` to the `tags` field of each event, after any tags that the input sets. You can then filter and group the data by agent tag in Discover, dashboards, alerting rules, and detection rules, for example with the KQL query `tags : "production"`.

    To include agent tags in events, set `enabled: true` for the `include_tags_in_events` setting, and list the tags in `agent.tags`:

    ```yaml
    agent.features:
      include_tags_in_events:
        enabled: true
    agent.tags: [production, eu-west]
    ```

    When you change `agent.tags`, {{agent}} applies the new tags when it reloads its configuration.

    Agent tags are added to data from most inputs, including when they run in the [OTel runtime](/reference/fleet/elastic-agent-as-otel-collector.md). They aren't added to data from the following:

    * {{elastic-defend}}
    * Elastic APM
    * Synthetics monitors
    * Universal Profiling
    * OTel Collector components that you configure directly in `elastic-agent.yml`

## Turn off individual default processors [elastic-agent-standalone-feature-flag-default-processors]

```{applies_to}
stack: ga 9.6+
```

To turn off individual default processors, set them to `false` in the `default_processors` setting. The processors you don't list stay on:

```yaml
agent.features:
  default_processors:
    add_docker_metadata: false
    add_kubernetes_metadata: false
```

Individual processor settings take precedence over `enabled`. For example, this configuration turns off every default processor except `add_cloud_metadata`:

```yaml
agent.features:
  default_processors:
    enabled: false
    add_cloud_metadata: true
```

To turn off processors only for the data sent to a specific output, refer to [Turn off default processors for an output](/reference/fleet/elastic-agent-output-configuration.md#elastic-agent-output-default-processors).
