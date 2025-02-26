---
navigation_title: "Feature flags"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-standalone-feature-flags.html
---

# Configure feature flags for standalone {{agent}}s [elastic-agent-standalone-feature-flags]


The Feature Flags section of the elastic-agent.yml config file contains settings in {{agent}} that are disabled by default. These may include experimental features, changes to behaviors within {{agent}} or its components, or settings that could cause a breaking change. For example a setting that changes information included in events might be inconsistent with the naming pattern expected in your configured {{agent}} output.

To enable any of the settings listed on this page, change the associated `enabled` flag from `false` to `true`.

```yaml
agent.features:
  mysetting:
    enabled: true
```


## Feature flag configuration settings [elastic-agent-standalone-feature-flag-settings]

You can specify the following settings in the Feature Flag section of the `elastic-agent.yml` config file.

Fully qualified domain name (FQDN)
:   When enabled, information provided about the current host through the [host.name](/reference/ingestion-tools/fleet/host-provider.md) key, in events produced by {{agent}}, is in FQDN format (`somehost.example.com` rather than `somehost`). This helps you to distinguish between hosts on different domains that have similar names. With `fqdn` enabled, the fully qualified hostname allows each host to be more easily identified when viewed in {{kib}}.

    ::::{note}
    FQDN reporting is not currently supported in APM.
    ::::


    For FQDN reporting to work as expected, the hostname of the current host must either:

    * Have a CNAME entry defined in DNS.
    * Have one of its corresponding IP addresses respond successfully to a reverse DNS lookup.

    If neither pre-requisite is satisfied, `host.name` continues to report the hostname of the current host as if the FQDN feature flag were not enabled.

    To enable fully qualified domain names set `enabled: true` for the `fqdn` setting:

    ```yaml
    agent.features:
      fqdn:
        enabled: true
    ```


