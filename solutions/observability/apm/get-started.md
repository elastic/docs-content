---
navigation_title: Get started with traces and APM
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-getting-started-apm-server.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-get-started.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-get-started.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
description: Collect application telemetry with Elastic APM using EDOT SDKs or APM agents, then verify ingestion and analyze services in the Service inventory.
---

# Get started with traces and APM [apm-getting-started-apm-server]

{{apm-server-or-mis}} receives telemetry from APM agents and [{{edot}} SDKs](opentelemetry://reference/edot-sdks/index.md), then transforms accepted events into {{es}} documents.

In this guide, you'll learn how to collect and send application performance monitoring (APM) data to Elastic, then explore and visualize the data.

::::{note}
For a general Elastic {{observability}} overview, refer to [Get started with observability](/solutions/observability/get-started.md).
::::

## Send data to Elastic APM

Follow these steps to send APM data to Elastic.

::::{admonition} Required permissions
:class: note

For {{obs-serverless}} projects, you need permission to create API keys and write APM data. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
::::

::::::{stepper}

:::::{step} Create or open your deployment

If you're using {{obs-serverless}}, create a project:

:::{include} /solutions/_snippets/obs-serverless-project.md
:::

If you're using {{stack}}, open an existing deployment or refer to [Deploy](/deploy-manage/deploy.md) to create one.

:::::

:::::{step} Add data using {{edot}} or APM agents

To send APM data to Elastic, install an {{edot}} SDK or an APM agent and configure it to send data to your deployment:

1.  ::::{include} /solutions/_snippets/obs-apm-project.md
    ::::

2. If you use an APM agent, verify its connection:
    * {applies_to}`stack: ga` Click **Check agent status**.
    * {applies_to}`serverless: ga` Click **Check status**.

    The OpenTelemetry onboarding flow detects incoming data automatically.

To learn more about APM agents, including how to fine-tune how agents send traces to Elastic, refer to [Collect application data](/solutions/observability/apm/ingest/index.md).

:::::
:::::{step} View your data

After an APM agent or {{edot}} SDK starts sending data, you can view application performance monitoring data in the UI.

Find **Service inventory** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). This page shows a high-level overview of your services' performance.

Learn more about visualizing APM data in [View and analyze data](/solutions/observability/apm/view-analyze-data.md).

::::{tip}
Not seeing any data? Find helpful tips in [Troubleshooting](/troubleshoot/observability/apm.md).
::::
:::::
::::::

## Next steps [observability-apm-get-started-next-steps]

Now that data is streaming into your project, take your investigation to a deeper level. Learn how to use [Elastic’s built-in visualizations for APM data](/solutions/observability/apm/view-analyze-data.md), [alert on APM data](/solutions/observability/incident-management/alerting.md), or [fine-tune how agents send traces to Elastic](/solutions/observability/apm/ingest/index.md).

