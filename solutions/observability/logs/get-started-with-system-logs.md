---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-get-started-with-logs.html
applies_to:
  stack: all
  serverless: all
products:
  - id: cloud-serverless
---

# Get started with system logs [observability-get-started-with-logs]

In this guide you can learn how to onboard system log data from a machine or server, then explore the data in **Discover**.

## Prerequisites [logs-prereqs]

::::{applies-switch}

:::{applies-item} stack:

To follow the steps in this guide, you need an {{stack}} deployment that includes:

* {{es}} for storing and searching data
* {{kib}} for visualizing and managing data
* Kibana user with `All` privileges on {{fleet}} and Integrations. Because many Integrations assets are shared across spaces, users need the Kibana privileges in all spaces.

To get started quickly, create an {{ech}} deployment and host it on AWS, GCP, or Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

:::

:::{applies-item} serverless:

The **Admin** role or higher is required to onboard log data. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).

:::

::::

## Onboard system log data [onboard-system-log-data]

Follow these steps to onboard system log data.

::::::{stepper}

:::::{step} Open your project

Open an [{{obs-serverless}} project](/solutions/observability/get-started.md) or Elastic Stack deployment.

:::::

:::::{step} Select data collection method

From the Observability UI, go to **Add data**. Under **What do you want to monitor?**, select **Host**, then select one of these options:

::::{tab-set}
:::{tab-item} OpenTelemetry: Full Observability

Collect native OpenTelemetry metrics and logs using {{agent}}.

**Recommended for**: Users who want to collect native OpenTelemetry data or are already using OpenTelemetry in their environment.

:::

:::{tab-item} Elastic Agent: Logs & Metrics

Bring data from Elastic integrations using the Elastic Agent.

**Recommended for**: Users who want to leverage Elastic's pre-built integrations and centralized management through Fleet.

:::

::::
:::::

:::::{step} Follow setup instructions

Follow the in-product steps to auto-detect your logs and install and configure your chosen data collector.

:::::

:::::{step} Verify data collection

After the agent is installed and successfully streaming log data, you can view the data in the UI:

1. From the navigation menu, go to **Discover**.
2. Select **All logs** from the **Data views** menu. The view shows all log datasets. Notice you can add fields, change the view, expand a document to see details, and perform other actions to explore your data.

:::::

:::::{step} Explore and analyze your data

Now that you have logs flowing into Elasticsearch, you can start exploring and analyzing your data:

* **[Explore logs](/solutions/observability/logs/explore-logs.md)**: Search, filter, and tail all your logs from a central location
* **[Process logs](/solutions/observability/logs/process.md)**: Extract structured fields from unstructured logs and route them to specific data streams
* **[Filter and aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md)**: Filter logs by specific criteria and aggregate data to find patterns and gain insights

:::::

::::::

## Other ways to collect log data [other-data-collection-methods]

{{agent}} is the recommended collector for most users. For {{filebeat}}, {{ls}}, the {{es}} REST APIs, and when each one fits, refer to [Other ways to collect logs](/solutions/observability/logs/ingest.md#logs-ingest-other). For Windows event logs, refer to the [Winlogbeat documentation](beats://reference/winlogbeat/index.md).

## Next steps [observability-get-started-with-logs-next-steps]

Now that you've added logs and explored your data, plan the rest of your logs setup or onboard other types of data:

* [Ingest logs](/solutions/observability/logs/ingest.md): choose the collection path for each of your log sources
* [Send any log file using {{agent}}](stream-any-log-file.md)
* [Send application log data](stream-application-logs.md)
* [Get started with traces and APM](/solutions/observability/apm/get-started.md)

To onboard other types of data, select **Add Data** from the main menu.
