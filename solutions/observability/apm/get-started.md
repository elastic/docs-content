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
---

# Get started with traces and APM [apm-getting-started-apm-server]

Elastic APM receives performance data from your APM agents or [Elastic Distributions of OpenTelemetry (EDOT) SDKs](opentelemetry://reference/edot-sdks/index.md), validates and processes it, and then transforms the data into {{es}} documents.

In this guide you'll learn how to collect and send Application Performance Monitoring (APM) data to Elastic, then explore and visualize the data in real time.

::::{note}
For a general Elastic {{observability}} overview, refer to [Get started with observability](/solutions/observability/get-started.md).
::::

## Send data to Elastic APM

Follow these steps to send APM data to Elastic.

::::{admonition} Required role
:class: note

**For Observability Serverless projects**, the **Admin** role or higher is required to send APM data to Elastic. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
::::

::::::{stepper}

:::::{step} Create an Observability project

:::{include} /solutions/_snippets/obs-serverless-project.md
:::

:::::

:::::{step} Add data using EDOT or APM Agents

To send APM data to Elastic, you must install an Elastic Distribution of OpenTelemetry or an APM agent and configure it to send data to your project:

1.  ::::{include} /solutions/_snippets/obs-apm-project.md
    ::::

2. If you’re using the step-by-step instructions in the UI, after you’ve installed and configured an agent, you can click **Check Agent Status** to verify that the agent is sending data.

To learn more about APM agents, including how to fine-tune how agents send traces to Elastic, refer to [Collect application data](/solutions/observability/apm/ingest/index.md).

:::::
:::::{step} View your data

After one or more APM agents are installed and successfully sending data, you can view application performance monitoring data in the UI.

In the **Applications** section of the main menu, select **Service Inventory**. This will show a high-level overview of the health and general performance of all your services.

Learn more about visualizing APM data in [View and analyze data](/solutions/observability/apm/view-analyze-data.md).

::::{tip}
Not seeing any data? Find helpful tips in [Troubleshooting](/troubleshoot/observability/apm.md).
::::
:::::
::::::

## Next steps [observability-apm-get-started-next-steps]

Now that data is streaming into your project, take your investigation to a deeper level. Learn how to use [Elastic’s built-in visualizations for APM data](/solutions/observability/apm/view-analyze-data.md), [alert on APM data](/solutions/observability/incident-management/alerting.md), or [fine-tune how agents send traces to Elastic](/solutions/observability/apm/ingest/index.md).

