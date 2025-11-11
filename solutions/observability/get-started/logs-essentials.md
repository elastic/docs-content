---
navigation_title: Logs Essentials
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Get started with {{obs-serverless}} Logs Essentials [logs-essentials-get-started]

```{note}
Use this guide to get started with the Logs Essentials feature tier of {{obs-serverless}}. Refer to the main [{{observability}} getting started](/solutions/observability/get-started.md) docs to get started with {{obs-serverless}} Complete, which includes APM and Infrastructure metrics. The [{{obs-serverless}} feature tiers](../observability-serverless-feature-tiers.md) page details the difference between tiers.
```

New to {{obs-serverless}} Logs Essentials? Discover more about its features and how to get started. The following instructions guide you through setting up your first Elastic {{observability}} Logs Essentials deployment, collecting log data, and exploring your data.

## Get started with your use case [get-started-with-use-case]

Learn how to create an {{obs-serverless}} project and use Elastic {{observability}} to gain deeper insight into the behavior of your applications and systems.

:::::::{stepper}

::::::{step} Create an Observability project

An {{obs-serverless}} project allows you to run {{obs-serverless}} in an autoscaled and fully-managed environment, where you don’t have to manage the underlying {{es}} cluster or {{kib}} instances.

::::{dropdown} Steps for creating a project
:::{note}
The **Admin** role or higher is required to create projects. Refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).
:::

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/) and log in to your account, or create one.
1. Select **Create serverless project**.
1. Under **Elastic for Observability**, select **Next**.
1. Enter a name for your project.
1. Under **Product features**, select **Observability Logs Essentials**.
1. (Optional) Under **Settings** you can change the following:

    * **Cloud provider**: The cloud platform where you’ll deploy your project. We currently support Amazon Web Services (AWS).
    * **Region**: The [region](/deploy-manage/deploy/elastic-cloud/regions.md) where your project will live.

1. Select **Create serverless project**. It takes a few minutes to create your project.
1. When the project is ready, click **Continue**.

::::::

::::::{step} Collect infrastructure logs

Bring logs from your hosts and services into Elastic {{observability}} to monitor the health and performance of your infrastructure. You can collect this data from hosts, containers, Kubernetes, and Cloud services.

:::::{dropdown} Steps for collecting infrastructure logs and metrics

::::{tab-set}
:::{tab-item} Hosts

Elastic {{observability}} can collect logs from hosts through the Elastic Distribution of OpenTelemetry (EDOT) Collector or the Elastic Agent.

1. Select **Add data** from the main menu and then select **Host**.
2. Select one of these options:
    * **OpenTelemetry: Logs**: Collect native OpenTelemetry logs.
    * **Elastic Agent: Logs**: Bring data from Elastic integrations.
3. Follow the instructions for your platform.

For an overview of the EDOT, refer to [Elastic Distribution of OpenTelemetry (EDOT)](opentelemetry://reference/index.md).

:::

:::{tab-item} Kubernetes

Elastic {{observability}} can collect logs from Kubernetes through the Elastic Distribution of OpenTelemetry (EDOT) Collector or the Elastic Agent.

1. Select **Add data** from the main menu and then select **Kubernetes**.
2. Select one of these options:
    * **OpenTelemetry: Logs**: Collect native OpenTelemetry metrics and logs.
    * **Elastic Agent: Logs**: Bring data from Elastic integrations.
3. Follow the instructions for your platform.

For an overview of EDOT, refer to [Elastic Distribution of OpenTelemetry (EDOT)](opentelemetry://reference/index.md).

:::

:::{tab-item} Cloud

Elastic {{observability}} can collect logs from cloud services through Elastic integrations.

1. Select **Add data** from the main menu and then select **Cloud**.
2. Select your Cloud provider to view the collection of integrations available for that provider.
3. Select the integration you want to add.
4. Select **Add**.
:::

:::::

::::::

::::::{step} Explore logs in Discover

**Discover** lets you quickly search and filter your log data, get information about the structure of your log fields, and display findings in a visualization. Instead of having to log into different servers, change directories, and view individual files, all your logs are available in a single view.

For more information on exploring your logs in **Discover**, refer to [Explore logs in Discover](/solutions/observability/logs/discover-logs.md).
::::::

::::::{step} Create your first dashboards

Elastic provides a wide range of prebuilt dashboards for visualizing observability data from a variety of sources. These dashboards are loaded automatically when you install [Elastic integrations](https://docs.elastic.co/integrations). You can also create new dashboards and visualizations based on your data views.

To create a new dashboard, select **Create Dashboard** and begin adding visualizations. You can create charts, graphs, maps, tables, and other types of visualizations from your data, or you can add visualizations from the library. You can also add other types of panels, such as filters and controls.

For more information about creating dashboards, refer to [Create your first dashboard](/explore-analyze/dashboards/create-dashboard-of-panels-with-web-server-data.md).

::::::

::::::{step} Set up alerts

Elastic {{observability}} lets you define rules of different types which detect complex conditions and trigger relevant actions. Elastic {{observability}} can send alerts to email, Slack, and other third-party systems. Refer to [](/solutions/observability/incident-management/create-manage-rules.md) to get started.

::::::

:::::::

## Related resources

Use these resources to learn more about {{observability}} or get started in a different way.

### Quickstarts

Quickstarts are compact hands-on guides that help you experiment with Elastic {{observability}} features. Each quickstart provides a highly opinionated, fast path to data ingestion, with minimal configuration required.

[Browse the Elastic {{observability}} quickstarts](/solutions/observability/get-started/quickstarts.md) to get started with specific use cases.

### Observability integrations

Many {{observability}} integrations are available to collect and process your data. Refer to [Elastic integrations](https://www.elastic.co/docs/reference/integrations) for more information.

### Other resources

* [What's Elastic {{observability}}](/solutions/observability.md)
* [What’s new in Elastic Stack](/release-notes/elastic-observability/index.md)
* [{{obs-serverless}} billing dimensions](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md)
* [Log monitoring](/solutions/observability/logs.md)