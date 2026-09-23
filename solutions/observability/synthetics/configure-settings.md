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
description: Configure Synthetics settings including alerting rules, private locations and their agents, global parameters, data retention, project API keys, cross-cluster search, and advanced settings.
---

# Configure Synthetics settings [synthetics-settings]

There are several Synthetics settings you can adjust in Observability.

## Alerting [synthetics-settings-alerting]

Alerting enables you to detect complex conditions using **rules** across Observability and send a notification using **connectors**.

When you create a new synthetic monitor, Synthetics applies default rules to the monitor. To edit the default rules:

1. Click **Alerts** in the application menu.
2. Select a rule to open a panel where you can edit the rule’s configuration:

    * **Monitor status rule** for receiving notifications for errors and outages
    * **TLS certificate rule** for receiving notifications when one or more of your HTTP or TCP lightweight monitors has a TLS certificate expiring within a specified threshold or when it exceeds an age limit

However, the automatically created Synthetics internal alert is intentionally preconfigured, and some configuration options can’t be changed. For example, you can’t change how often it checks the rule.

If you need specific alerting behavior, set up a different rule. To view all existing rules or create a new rule:

1. Click **Alerts** in the application menu.
2. Click **Manage rules** to go to the *Rules* page.

On the *Rules* page, you can manage the default synthetics rules including snoozing rules, disabling rules, deleting rules, and more.

:::{image} /solutions/images/observability-synthetics-settings-disable-default-rules.png
:alt: Rules page with default Synthetics rules
:screenshot:
:::

::::{note}
You can turn on and turn off default alerts for individual monitors in a few ways:

* In the Synthetics UI when you [create a monitor](/solutions/observability/synthetics/create-monitors-ui.md).
* In the Synthetics UI *after* a monitor is already created, on the **Monitors** page or on the **Edit monitor** page for the monitor.
* In Synthetics projects when [configuring a lightweight monitor](/solutions/observability/synthetics/configure-lightweight-monitors.md).

::::

In the **Alerting** tab on the **Monitor** Settings page, you can:
- Turn on or turn off default rules.
- Add and configure connectors. For available connectors, refer to [Action types](/solutions/observability/incident-management/create-an-apm-anomaly-rule.md).
- Set up email alerts, if you are running in Elastic Cloud. An SMTP connector is automatically configured.

:::{image} /solutions/images/observability-synthetics-settings-alerting.png
:alt: Alerting tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::

## {{private-location}}s [synthetics-settings-private-locations]

{{private-location}}s allow you to run monitors from your own premises.

In the **{{private-location}}s** tab, you can add and manage {{private-location}}s. After you [Set up {{fleet-server}} and {{agent}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent) and [Connect to the {{stack}} or your serverless Observability project](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-connect), this is where you add the {{private-location}} so you can specify it as the location for a monitor created using the Synthetics UI or a Synthetics project.

:::{image} /solutions/images/observability-synthetics-settings-private-locations.png
:alt: {{private-location}}s tab on the Synthetics Settings page in {{kib}}
:screenshot:
:::

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` When a private location has monitors with broken {{fleet}} integrations, a badge showing the count of unhealthy monitors appears in the location's row. Click the badge to open a popover listing the affected monitors. From the popover, use **Reset monitors** to bulk-reset all monitors at that location that have a `missing_package_policy` status. Monitors with other failure types are excluded and must be resolved manually. Refer to [Monitor integration health](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-health) for details on failure types and remediation steps.

### Agents and health [synthetics-settings-private-locations-agents]
```{applies_to}
stack: ga 9.6+
```

The **{{private-location}}s** table shows the state of the {{agents}} that run each location's monitors:

* **Agent Policy**: The name of the location's agent policy. A [scalable {{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-scalable) shows a **Scalable** badge with the number of enrolled agents. A classic location shows the number of agents on its policy. Click the policy name to view its status, enrolled agents, and healthy agents, then click **View policy in {{fleet}}** to open it in {{fleet}}.
* **Health**: How many of the location's agents are healthy, for example `2/3 healthy`. An agent is healthy when {{fleet}} reports it as online.

To view details for each agent, expand the location's row. The **Agents overview** panel shows:

* The number of **Monitors**, **Agents**, and **Healthy agents** in the location, and the **Total memory** used and available across its agents.
* **Monitors per agent**: One row for each agent, with its **Monitors**, **Monitors run**, **Memory (used / total)**, **CPU**, **Status**, and **Last agent check-in**. **Monitors run** is the share of the location's monitors that the agent runs. In a scalable location, each monitor runs on one agent. In a classic location, every agent runs all of the location's monitors.
* A **Needs attention** callout when agents aren't reporting as online, or when an agent uses 85% or more of its memory.

Click an agent's name to view its health, capacity, and {{fleet}} details, then click **View full details in {{fleet}}** to open the agent in {{fleet}}. Use **View agent policy** and **Manage agents in {{fleet}}** to open the agent policy and its agents in {{fleet}}.

Memory and CPU show **N/A** for agents that don't report host metrics. To report them, add the System integration to the agent policy.

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

- The **Elastic managed locations enabled** toggle controls whether your Synthetics monitors are permitted to run from Elastic's globally distributed, cloud-hosted testing infrastructure. If enabled, the key can push monitors to both Elastic-managed and private locations. If disabled, the key is restricted to private locations only.
- The **Spaces** menu allows you to select the space where your API keys are available.

## Remote clusters [synthetics-settings-remote-clusters]
```{applies_to}
stack: ga 9.5+
serverless: unavailable
```

In the **Remote clusters** tab, you can configure {{ccs}} ({{ccs-init}}) settings so that Synthetics can include monitor data from remote {{es}} clusters alongside local monitors. {{ccs-init}} is off by default; on first save, the settings are anchored to the space you are currently in.

These settings are stored as a single shared configuration — one per deployment, not a separate copy per space. Use the **Spaces** field to control which {{kib}} spaces it applies to.

::::{note}
To edit these settings, you must have the **All** privilege for the **Synthetics and Uptime** feature in **{{stack-manage-app}} → Roles → {{kib}} privileges → {{observability}}**. Users with only the **Read** privilege see the form as read-only.
::::

::::{admonition} View monitors from linked projects
:applies_to: serverless: ga
On {{serverless-full}}, after you [link projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), you can view monitors from those projects without any additional configuration. Refer to [Monitors from linked projects](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-linked-monitors).
::::

### Source settings [synthetics-settings-remote-clusters-source]

Use the **Use all remote clusters** toggle or **Select remote clusters** combo box to control which remote clusters Synthetics queries:

- Turn on **Use all remote clusters** to include monitor data from all configured remote clusters.
- Turn off **Use all remote clusters** and use the **Select remote clusters** combo box to choose specific clusters. Each cluster is shown with a connected or disconnected status indicator.

To configure remote clusters, go to **{{stack-manage-app}} → Remote Clusters**.

### Spaces with access [synthetics-settings-remote-clusters-spaces]

Use the **Spaces** combo box to control which {{kib}} spaces can access these {{ccs-init}} settings. Select one or more specific spaces, or select **All spaces** to make the settings available across your entire deployment. Removing a space makes these settings inaccessible there, and Synthetics no longer includes monitor data from remote clusters in that space.

::::{note}
The **Spaces** field shows the current sharing configuration when you open the tab (your current space by default). Clearing the field and saving leaves that configuration unchanged, meaning it does not remove access from existing spaces. To update which spaces have access, select the new spaces explicitly.
::::

## Advanced [synthetics-settings-advanced]
```{applies_to}
stack: ga 9.4+
serverless: ga
```

In the **Advanced** tab, you can configure advanced settings for your Synthetics deployment.

### {{maint-windows-cap}} sync interval [synthetics-settings-advanced-sync-interval]

Private location monitors are periodically synced to apply active maintenance window changes. The **{{maint-windows-cap}} sync interval** setting controls how frequently this sync occurs.

Use the **Sync interval (minutes)** field to set the interval. The default is 5 minutes, and valid values range from 5 to 1440 minutes. When you apply a new interval, an immediate sync is triggered so the change takes effect right away.

When a maintenance window becomes active, a callout in the Synthetics UI displays the estimated delay for applying changes to private location monitors: *"It may take up to X minutes for maintenance window changes to be applied to private location monitors,"* where X equals the configured sync interval. Click **Sync now** in the callout to trigger an immediate sync without waiting for the interval.

A separate callout appears when maintenance windows are modified or deleted but changes have not yet propagated to your private location monitors.

### Private location shard rebalancing [synthetics-settings-advanced-rebalancing]
```{applies_to}
stack: ga 9.6+
```

Synthetics regularly reassigns monitors across the healthy agents of [scalable {{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-scalable). The **Rebalance private location shards** switch controls this for all {{kib}} spaces. It's on by default.

::::{warning}
Turning off **Rebalance private location shards** also removes the agent assignment from every monitor in every scalable {{private-location}}. Each monitor then runs on every agent enrolled on its location's agent policy, which duplicates test runs. When you turn the switch back on, Synthetics reassigns the monitors right away.
::::
