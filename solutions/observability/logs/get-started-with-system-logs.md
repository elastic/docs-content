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

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

To follow the steps in this guide, you need an {{stack}} deployment that includes:

* {{es}} for storing and searching data
* {{kib}} for visualizing and managing data
* Kibana user with `All` privileges on {{fleet}} and Integrations. Because many Integrations assets are shared across spaces, users need the Kibana privileges in all spaces.

To get started quickly, create an {{ech}} deployment and host it on AWS, GCP, or Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

:::

:::{tab-item} Serverless
:sync: serverless

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

Collect native OpenTelemetry metrics and logs using the Elastic Distribution of OpenTelemetry Collector (EDOT).

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

* **[Explore logs in Discover](/solutions/observability/logs/explore-logs.md)**: Search, filter, and tail all your logs from a central location
* **[Parse and route logs](/solutions/observability/logs/parse-route-logs.md)**: Extract structured fields from unstructured logs and route them to specific data streams
* **[Filter and aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md)**: Filter logs by specific criteria and aggregate data to find patterns and gain insights

:::::

::::::

## Other ways to collect log data [other-data-collection-methods]

While the Elastic Agent and OpenTelemetry Collector are the recommended approaches for most users, Elastic provides additional tools for specific use cases:

::::{tab-set}

:::{tab-item} Filebeat

Filebeat is a lightweight data shipper that sends log data to Elasticsearch. It's ideal for:

* Simple log collection: When you need to collect logs from specific files or directories.
* Custom parsing: When you need to parse logs using ingest pipelines before indexing.
* Legacy systems: When you can't install the Elastic Agent or OpenTelemetry Collector.

For more information, refer to [Collecting log data with Filebeat](/deploy-manage/monitor/stack-monitoring/collecting-log-data-with-filebeat.md) and [Ingest logs from applications using Filebeat](/solutions/observability/logs/plaintext-application-logs.md).

:::

:::{tab-item} Winlogbeat

Winlogbeat is specifically designed for collecting Windows event logs. It's ideal for:

* Windows environments: When you need to collect Windows security, application, and system event logs.
* Security monitoring: When you need detailed Windows security event data.
* Compliance requirements: When you need to capture specific Windows event IDs.

For more information, refer to the [Winlogbeat documentation](beats://reference/winlogbeat/index.md).

:::

:::{tab-item} Logstash

Logstash is a powerful data processing pipeline that can collect, transform, and enrich log data before sending it to Elasticsearch. It's ideal for:

* Complex data processing: When you need to parse, filter, and transform logs before indexing.
* Multiple data sources: When you need to collect logs from various sources and normalize them.
* Advanced use cases: When you need data enrichment, aggregation, or routing to multiple destinations.
* Extending Elastic integrations: When you want to add custom processing to data collected by Elastic Agent or Beats.

For more information, refer to [Logstash](logstash://reference/index.md) and [Using Logstash with Elastic integrations](logstash://reference/using-logstash-with-elastic-integrations.md).

:::

:::{tab-item} REST APIs

You can use Elasticsearch REST APIs to send log data directly to Elasticsearch. This approach is ideal for:

* Custom applications: When you want to send logs directly from your application code.
* Programmatic collection: When you need to collect logs using custom scripts or tools.
* Real-time streaming: When you need to send logs as they're generated.

For more information, refer to [Elasticsearch REST APIs](elasticsearch://reference/elasticsearch/rest-apis/index.md).

:::

::::

## Next steps [observability-get-started-with-logs-next-steps]

Now that you've added logs and explored your data, learn how to onboard other types of data:

* [Stream any log file](stream-any-log-file.md)
* [Stream application logs](stream-application-logs.md)
* [Get started with traces and APM](/solutions/observability/apm/get-started.md)

To onboard other types of data, select **Add Data** from the main menu.
