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
---

# Get started with Elastic {{observability}} [observability-get-started]

New to Elastic {{observability}}? Discover more about our observability features and how to get started. The following instructions will guide you through setting up your first Elastic {{observability}} deployment, collecting data from infrastructure and applications, and exploring your data.

## Get started with your use case [get-started-with-use-case]

Learn how to create an {{obs-serverless}} project and use Elastic {{observability}} to gain deeper insight into the behavior of your applications and systems.

:::::::{stepper}

::::::{step} Create an Observability project

:::{include} /solutions/_snippets/obs-serverless-project.md
:::

For other types of deployments, refer to [Deploy](/deploy-manage/deploy.md). For a breakdown of the differences between deployment types and what they support, refer to [Detailed deployment comparison](/deploy-manage/deploy/deployment-comparison.md).
::::
::::::

::::::{step} Collect infrastructure logs and metrics

Bring logs and metrics from your hosts and services into Elastic {{observability}} to monitor the health and performance of your infrastructure. You can collect this data from hosts, containers, Kubernetes, and Cloud services.

:::::{dropdown} Steps for collecting infrastructure logs and metrics

::::{tab-set}
:::{tab-item} Hosts

Elastic {{observability}} can collect telemetry data from hosts, containers, and Kubernetes through the EDOT Collector or the Elastic Agent.

1. Select **Add data** from the main menu and then select **Host**.
2. Select one of these options:
    * **OpenTelemetry: Full Observability**: Collect native OpenTelemetry metrics and logs.
    * **Elastic Agent: Logs & Metrics**: Bring data from Elastic integrations.
3. Follow the instructions for your platform.

For an overview of the Elastic Distribution of OpenTelemetry Collector, refer to [Elastic Distribution of OpenTelemetry (EDOT)](opentelemetry://reference/index.md).

:::

:::{tab-item} Kubernetes

Elastic {{observability}} can collect telemetry data from Kubernetes through the Elastic Distribution of OpenTelemetry Collector or the Elastic Agent.

1. Select **Add data** from the main menu and then select **Kubernetes**.
2. Select one of these options:
    * **OpenTelemetry: Full Observability**: Collect native OpenTelemetry metrics and logs.
    * **Elastic Agent: Logs & Metrics**: Bring data from Elastic integrations.
3. Follow the instructions for your platform.

For an overview of EDOT, refer to [Elastic Distribution of OpenTelemetry (EDOT)](opentelemetry://reference/index.md).

:::

:::{tab-item} Integrations

Elastic {{observability}} can collect telemetry data from services through Elastic integrations.

1. Select **Add data** from the main menu.
2. In **Search through other ways of ingesting data**, type the name of an integration (for example, NGINX).
3. Select the integration you want to add.
4. Select **Add**.
:::

:::{tab-item} Cloud

Elastic {{observability}} can collect telemetry data from cloud services through Elastic integrations.

1. Select **Add data** from the main menu and then select **Cloud**.
2. Select your Cloud provider to view the collection of integrations available for that provider.
3. Select the integration you want to add.
4. Select **Add**.
:::

:::{tab-item} CI/CD

Elastic {{observability}} can collect telemetry data from CI/CD pipelines using OpenTelemetry.

Refer to [CI/CD](/solutions/observability/cicd.md) for more information.
:::

:::{tab-item} LLMs

Elastic provides a powerful LLM observability framework including key metrics, logs, and traces, along with pre-configured, out-of-the-box dashboards that deliver deep insights into model prompts and responses, performance, usage, and costs.

Refer to [LLM observability](/solutions/observability/applications/llm-observability.md) for more information.
:::

:::::
::::::

::::::{step} Collect application traces, metrics, and logs

::::{include} /solutions/_snippets/obs-apm-project.md
::::

::::::

::::::{step} Add Synthetics monitoring

[Synthetics monitoring](/solutions/observability/synthetics/index.md) lets you simulate, track, and visualize user journeys to catch performance, availability, and functionality issues in your services and applications. It periodically checks the status of your services and applications.

:::::{dropdown} Steps for adding Synthetics monitoring
1. Select **Add data** from the main menu and then select **Application**.
2. Select **Synthetic monitor**. 
3. Select a [monitor type](/solutions/observability/synthetics/index.md).
4. Fill out the details.
5. (Optional) Add a [Playwright](https://playwright.dev/) script.
6. Test and create your monitor.
:::::
::::::

::::::{step} Explore your logs, metrics, and traces

After you've onboarded your data, you can explore it in the following Elastic {{observability}} UIs, or query it using [query languages](elasticsearch://reference/query-languages/index.md).

- [Explore your logs](/solutions/observability/logs/explore-logs.md) in the Logs UI.
- [Analyze infrastructure and host metrics](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) in the Infrastructure UI.
- [View and analyze APM data](/solutions/observability/apm/view-analyze-data.md) in the Applications UI.
- Use the [Elastic Query Language ({{esql}})](/explore-analyze/discover/try-esql.md) to search and filter your data.

::::::

::::::{step} Create your first dashboards

Elastic provides a wide range of prebuilt dashboards for visualizing observability data from a variety of sources. These dashboards are loaded automatically when you install [Elastic integrations](https://docs.elastic.co/integrations). You can also create new dashboards and visualizations based on your data views.

To create a new dashboard, select **Create Dashboard** and begin adding visualizations. You can create charts, graphs, maps, tables, and other types of visualizations from your data, or you can add visualizations from the library. You can also add other types of panels, such as filters and controls.

For more information about creating dashboards, refer to [Create your first dashboard](/explore-analyze/dashboards/create-dashboard-of-panels-with-web-server-data.md).

::::::

::::::{step} Set up alerts and SLOs

Elastic {{observability}} lets you define rules of different types which detect complex conditions and trigger relevant actions. {{observability}} can send alerts to email, Slack, and other third-party systems. Refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md) to get started.

{{observability}} also lets you define Service Level Objectives (SLOs) to set clear, measurable targets for your service performance, based on factors like availability, response times, error rates, and other key metrics. Refer to [Create and manage SLOs](/solutions/observability/incident-management/service-level-objectives-slos.md) to get started.

::::::

:::::::

## Related resources

Use these resources to learn more about {{observability}} or get started in a different way.

### Quickstarts

Quickstarts are compact hands-on guides that help you experiment with {{observability}} features. Each quickstart provides a highly opinionated, fast path to data ingestion, with minimal configuration required.

[Browse the Elastic {{observability}} quickstarts](/solutions/observability/get-started/quickstarts.md) to get started with specific use cases.

### Observability integrations

Many [{{observability}} integrations](https://www.elastic.co/integrations/data-integrations?solution=observability) are available to collect and process your data. Refer to [Elastic integrations](https://www.elastic.co/docs/reference/integrations) for more information.

### Other resources

* [What's Elastic {{observability}}](/solutions/observability/get-started/what-is-elastic-observability.md)
* [What’s new in Elastic Stack](/release-notes/elastic-observability/index.md)
* [{{obs-serverless}} billing dimensions](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md)
