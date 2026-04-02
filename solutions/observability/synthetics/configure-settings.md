---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-settings.html
  - https://www.elastic.co/guide/en/observability/current/synthetics-settings.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Configure Synthetics settings [synthetics-settings]

There are several Synthetics settings you can adjust in Observability.

## Alerting [synthetics-settings-alerting]

Alerting enables you to detect complex conditions using **rules** across Observability and send a notification using **connectors**.

When you create a new synthetic monitor, new default synthetics rules will be applied. To edit the default rules:

1. Click **Alerts and rules** in the top bar.
2. Select a rule to open a panel where you can edit the rule’s configuration:

    * **Monitor status rule** for receiving notifications for errors and outages.
    * **TLS certificate rule** for receiving notifications when one or more of your HTTP or TCP lightweight monitors has a TLS certificate expiring within a specified threshold or when it exceeds an age limit.

However, the automatically created Synthetics internal alert is intentionally preconfigured, and some configuration options can’t be changed. For example, you can’t change how often it checks the rule.

If you need specific alerting behavior, set up a different rule. To view all existing rules or create a new rule:

1. Click **Alerts and rules** in the top bar.
2. Click **Manage rules** to go to the *Rules* page.

On the *Rules* page, you can manage the default synthetics rules including snoozing rules, disabling rules, deleting rules, and more.

:::{image} /solutions/images/observability-synthetics-settings-disable-default-rules.png
:alt: Rules page with default Synthetics rules
:screenshot:
:::

::::{note}
You can enable and disable default alerts for individual monitors in a few ways:

* In the Synthetics UI when you [create a monitor](/solutions/observability/synthetics/create-monitors-ui.md).
* In the Synthetics UI *after* a monitor is already created, on the **Monitors** page or on the **Edit monitor** page for the monitor.
* In Synthetics projects when [configuring a lightweight monitor](/solutions/observability/synthetics/configure-lightweight-monitors.md).

::::

In the **Alerting** tab on the Synthetics Settings page, you can add and configure connectors. If you are running in Elastic Cloud, then an SMTP connector will automatically be configured, allowing you to easily set up email alerts. Read more about all available connectors in [Action types](/solutions/observability/incident-management/create-an-apm-anomaly-rule.md).

:::{image} /solutions/images/observability-synthetics-settings-alerting.png
:alt: Alerting tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::

## {{private-location}}s [synthetics-settings-private-locations]

{{private-location}}s allow you to run monitors from your own premises.

In the **{{private-location}}s** tab, you can add and manage {{private-location}}s. After you [Set up {{fleet-server}} and {{agent}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent) and [Connect to the {{stack}} or your serverless Observability project](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-connect), this is where you will add the {{private-location}} so you can specify it as the location for a monitor created using the Synthetics UI or a Synthetics project.

:::{image} /solutions/images/observability-synthetics-settings-private-locations.png
:alt: {{private-location}}s tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::

## Global parameters [synthetics-settings-global-parameters]

Global parameters can be defined once and used across the configuration of lightweight and browser-based monitors.

In the **Global parameters** tab, you can define variables and parameters. This is one of several methods you can use to define variables and parameters. To learn more about the other methods and which methods take precedence over others, see [Work with params and secrets](/solutions/observability/synthetics/work-with-params-secrets.md).

:::{image} /solutions/images/observability-synthetics-settings-global-parameters.png
:alt: Global parameters tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::

## Data retention [synthetics-settings-data-retention]

When you set up a synthetic monitor, data from the monitor is saved in [Elasticsearch data streams](/manage-data/data-store/data-streams.md), an append-only structure in Elasticsearch. You can customize how long synthetics data is stored by creating your own index lifecycle policy and attaching it to the relevant custom Component Template.

In the **Data retention** tab, use the links to jump to the relevant policy for each data stream. Learn more about the data included in each data stream in [Manage data retention](/solutions/observability/synthetics/manage-data-retention.md).

:::{image} /solutions/images/observability-synthetics-settings-data-retention.png
:alt: Data retention tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::

## Project API keys [synthetics-settings-api-keys]

Project API keys are used to push {{project-monitors}} remotely from a CLI or CD pipeline.

In the **Project API keys** tab, you can generate project API keys to use with your projects. Learn more about using API keys in [Use {{project-monitors-cap}}](/solutions/observability/synthetics/create-monitors-with-projects.md).

::::{important}
**In an Elastic Stack deployment**, to create a Project API key you must be logged into {{kib}} as a user with the privileges described in [Writer role](/solutions/observability/synthetics/writer-role.md).

In a serverless project, to create a Project API key you must be logged in as a user with [Editor](/solutions/observability/synthetics/grant-access-to-secured-resources.md) access.

::::

:::{image} /solutions/images/observability-synthetics-settings-api-keys.png
:alt: Project API keys tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::