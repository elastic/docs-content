---
navigation_title: Get started
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-get-started.html
  - https://www.elastic.co/guide/en/observability/current/observability-get-started.html
  - https://www.elastic.co/guide/en/observability/current/index.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
description: Set up data collection with Elastic Observability for infrastructure, applications, synthetic monitors, dashboards, alerts, and service-level objectives.
---

# Get started with Elastic {{observability}} [observability-get-started]

```{note}
Use this guide with {{stack}} or the {{observability}} Complete feature tier of {{obs-serverless}}. If you haven't selected a deployment type, refer to [Detailed deployment comparison](/deploy-manage/deploy/deployment-comparison.md). To use {{obs-serverless}} Logs Essentials instead, refer to [Get started with Logs Essentials](/solutions/observability/get-started/logs-essentials.md). The [{{obs-serverless}} feature tiers](/solutions/observability/observability-serverless-feature-tiers.md) page explains the differences between tiers.
```

New to Elastic {{observability}}? This guide walks you through opening a deployment, collecting data from infrastructure and applications, and exploring your data.

## Get started with your use case [get-started-with-use-case]

Learn how to open an Elastic deployment and use Elastic {{observability}} to understand the behavior of your applications and systems.

:::::::{stepper}

::::::{step} Create or open your deployment

:::::{applies-switch}
::::{applies-item} serverless: ga
:::{include} /solutions/_snippets/obs-serverless-project.md
:::
::::

::::{applies-item} stack: ga
Open an existing {{stack}} deployment, or refer to [Deploy](/deploy-manage/deploy.md) to create one. To compare deployment types and supported features, refer to [Detailed deployment comparison](/deploy-manage/deploy/deployment-comparison.md).
::::
:::::

::::::

::::::{step} Collect infrastructure logs and metrics

Bring logs and metrics from your hosts and services into Elastic {{observability}} to monitor the health and performance of your infrastructure. You can collect this data from hosts, containers, {{k8s}}, and cloud services.

:::::{dropdown} Steps for collecting infrastructure logs and metrics

::::{tab-set}
:::{tab-item} Hosts

Elastic {{observability}} can collect telemetry data from hosts, containers, and {{k8s}} through {{agent}}.

1. Select **Add data** from the navigation menu and then select **Host**.
2. Select a collection method available for your platform:
    * **OpenTelemetry**: Collect native OpenTelemetry metrics and logs. Depending on your version, this option might be called **OpenTelemetry: Logs & Metrics** or **OpenTelemetry: Full {{observability}}**.
    * **{{product.elastic-agent}}**: Bring data from Elastic integrations. Depending on your version, this option might be called **{{product.elastic-agent}}: Logs & Metrics**.
3. Follow the instructions for your platform.

For an overview of the {{product.edot-collector}}, refer to [{{edot}}](opentelemetry://reference/index.md).

:::

:::{tab-item} {{k8s}}

Elastic {{observability}} can collect telemetry data from {{k8s}} through {{agent}}.

1. Select **Add data** from the navigation menu, then select **{{k8s}}**. If your page groups {{k8s}} under **Containers**, select **Containers**, then **{{k8s}}**.
2. If prompted to select a collection method:
    * {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Select **OpenTelemetry: Full {{observability}}**.
    * {applies_to}`stack: ga 9.0-9.4` Select **OpenTelemetry: Full {{observability}}** or **{{product.elastic-agent}}: Logs & Metrics**.
3. Follow the instructions for your platform.

For an overview of {{edot}}, refer to [{{edot}}](opentelemetry://reference/index.md).

:::

:::{tab-item} {{integrations}}

Elastic {{observability}} can collect telemetry data from services through Elastic {{integrations}}.

1. Select **Add data** from the navigation menu.
2. In the search field, enter the name of an integration. For example, enter `NGINX`.
3. Select the integration.
4. Click the package-specific add button, such as **Add NGINX**, and follow the setup instructions.
:::

:::{tab-item} Cloud

Elastic {{observability}} can collect telemetry data from cloud services through Elastic {{integrations}}.

1. Select **Add data** from the navigation menu and then select **Cloud**.
2. Select your Cloud provider to view the collection of integrations available for that provider.
3. Select the integration you want to add.
4. Follow the integration's setup instructions.
:::

:::{tab-item} CI/CD

Elastic {{observability}} can collect telemetry data from CI/CD pipelines using OpenTelemetry.

Refer to [CI/CD](/solutions/observability/cicd.md) for more information.
:::

:::{tab-item} LLMs

Collect large language model (LLM) metrics, logs, and traces, and use preconfigured dashboards to analyze available prompt and response data, performance, token usage, and provider cost data. Cost visibility depends on the provider and integration.

Refer to [LLM observability](/solutions/observability/applications/llm-observability.md) for more information.
:::
::::
:::::

After completing a setup flow, return to it to confirm that data arrives. Use the links under **Visualize your data** to open the relevant Logs or Infrastructure page.

::::::

::::::{step} Collect application traces, metrics, and logs

::::{include} /solutions/_snippets/obs-apm-project.md
::::

::::::

::::::{step} Add Synthetics monitoring

[Synthetics monitoring](/solutions/observability/synthetics/index.md) lets you simulate, track, and visualize user journeys to catch performance, availability, and functionality issues in your services and applications. It periodically checks the status of your services and applications.

:::::{dropdown} Steps for adding Synthetics monitoring
1. Select **Add data** from the navigation menu and then select **Application**.
2. Select **Synthetic monitor**.
3. Select a [monitor type](/solutions/observability/synthetics/index.md).
4. Fill out the details.
5. If the selected monitor type requires a script, add a [Playwright](https://playwright.dev/) script.
6. (Optional) Click **Run test**.
7. Click **Create monitor**.
:::::
::::::

::::::{step} Explore your logs, metrics, and traces

After you've onboarded your data, you can explore it in the following Elastic {{observability}} UIs, or query it using [query languages](elasticsearch://reference/query-languages/index.md).

- [Explore your logs](/solutions/observability/logs/explore-logs.md) in the Logs UI.
- [Analyze infrastructure and host metrics](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) in the Infrastructure UI.
- [View and analyze APM data](/solutions/observability/apm/view-analyze-data.md) in the Applications UI.
- [Analyze synthetic monitor data](/solutions/observability/synthetics/analyze-data.md) on the **Synthetics → Overview** tab.
- Use the [Elastic Query Language ({{esql}})](/explore-analyze/discover/try-esql.md) to search and filter your data.

::::::

::::::{step} Create your first dashboards

Elastic provides prebuilt dashboards for visualizing observability data from a variety of sources. Integrations that include dashboards install them automatically with their other Kibana assets. You can also create dashboards and visualizations based on your data views.

To create a dashboard, click **Create dashboard** and add visualizations. You can create charts, graphs, maps, tables, and other types of visualizations from your data, or add visualizations from the library. You can also add other types of panels, such as filters and controls.

For more information about creating dashboards, refer to [Create your first dashboard](/explore-analyze/dashboards/create-dashboard-of-panels-with-web-server-data.md).

::::::

::::::{step} Set up alerts and SLOs

Elastic {{observability}} lets you define rules that detect conditions and trigger actions. These actions can send notifications by email, Slack, and other third-party systems. Refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md) for more information.

{{observability}} also lets you define Service Level Objectives (SLOs) to set clear, measurable targets for your service performance, based on factors like availability, response times, error rates, and other key metrics. Refer to [Create and manage SLOs](/solutions/observability/incident-management/service-level-objectives-slos.md) to get started.

::::::

:::::::

## Related resources

Use these resources to learn more about {{observability}} or get started in a different way.

### Quickstarts

Quickstarts are compact hands-on guides that help you experiment with {{observability}} features. Each quickstart provides a highly opinionated, fast path to data ingestion, with minimal configuration required.

[Browse the Elastic {{observability}} quickstarts](/solutions/observability/get-started/quickstarts.md) to get started with specific use cases.

### {{observability}} integrations

Many [{{observability}} integrations](https://www.elastic.co/integrations/data-integrations?solution=observability) are available to collect and process your data. Refer to [Elastic integrations](https://www.elastic.co/docs/reference/integrations) for more information.

If your data source doesn’t have a prebuilt integration, you can use [Automatic Import](/explore-analyze/ai-features/automatic-import.md) to create a custom integration from a sample of your data.

### Other resources

* [What's Elastic {{observability}}](/solutions/observability.md)
* [What's new in {{product.elastic-stack}}](/release-notes/elastic-observability/index.md)
* [{{obs-serverless}} billing dimensions](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md)
