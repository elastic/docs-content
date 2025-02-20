---
navigation_title: "Logs"
---

# Log monitoring [observability-log-monitoring]


{{obs-serverless}} allows you to deploy and manage logs at a petabyte scale, giving you insights into your logs in minutes. You can also search across your logs in one place, troubleshoot in real time, and detect patterns and outliers with categorization and anomaly detection. For more information, refer to the following links:

* [Get started with system logs](../../../solutions/observability/logs/get-started-with-system-logs.md): Onboard system log data from a machine or server.
* [Stream any log file](../../../solutions/observability/logs/stream-any-log-file.md): Send log files to your Observability project using a standalone {{agent}}.
* [Parse and route logs](../../../solutions/observability/logs/parse-route-logs.md): Parse your log data and extract structured fields that you can use to analyze your data.
* [Filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md#logs-filter): Filter and aggregate your log data to find specific information, gain insight, and monitor your systems more efficiently.
* [Explore logs](../../../solutions/observability/logs/logs-explorer.md): Find information on visualizing and analyzing logs.
* [Run pattern analysis on log data](../../../solutions/observability/logs/run-pattern-analysis-on-log-data.md): Find patterns in unstructured log messages and make it easier to examine your data.
* [Troubleshoot logs](../../../troubleshoot/observability/troubleshoot-logs.md): Find solutions for errors you might encounter while onboarding your logs.


## Send logs data to your project [observability-log-monitoring-send-logs-data-to-your-project]

You can send logs data to your project in different ways depending on your needs:

* {agent}
* {filebeat}

When choosing between {{agent}} and {{filebeat}}, consider the different features and functionalities between the two options. See [{{beats}} and {{agent}} capabilities](../../../manage-data/ingest/tools.md) for more information on which option best fits your situation.


### {{agent}} [observability-log-monitoring-agent]

{{agent}} uses [integrations](https://www.elastic.co/integrations/data-integrations) to ingest logs from Kubernetes, MySQL, and many more data sources. You have the following options when installing and managing an {{agent}}:


#### {{fleet}}-managed {{agent}} [observability-log-monitoring-fleet-managed-agent]

Install an {{agent}} and use {{fleet}} to define, configure, and manage your agents in a central location.

See [install {{fleet}}-managed {{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md).


#### Standalone {{agent}} [observability-log-monitoring-standalone-agent]

Install an {{agent}} and manually configure it locally on the system where it’s installed. You are responsible for managing and upgrading the agents.

See [install standalone {{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-standalone-elastic-agent.md).


#### {{agent}} in a containerized environment [observability-log-monitoring-agent-in-a-containerized-environment]

Run an {{agent}} inside of a container — either with {{fleet-server}} or standalone.

See [install {{agent}} in containers](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-elastic-agents-in-containers.md).


### {{filebeat}} [observability-log-monitoring-filebeat]

{{filebeat}} is a lightweight shipper for forwarding and centralizing log data. Installed as a service on your servers, {{filebeat}} monitors the log files or locations that you specify, collects log events, and forwards them to your Observability project for indexing.

* [{{filebeat}} overview](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/filebeat-overview.md): General information on {{filebeat}} and how it works.
* [{{filebeat}} quick start](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/filebeat-installation-configuration.md): Basic installation instructions to get you started.
* [Set up and run {{filebeat}}](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/setting-up-running.md): Information on how to install, set up, and run {{filebeat}}.


## Configure logs [observability-log-monitoring-configure-logs]

The following resources provide information on configuring your logs:

* [Data streams](../../../manage-data/data-store/data-streams.md): Efficiently store append-only time series data in multiple backing indices partitioned by time and size.
* [Data views](../../../explore-analyze/find-and-organize/data-views.md): Query log entries from the data streams of specific datasets or namespaces.
* [Index lifecycle management](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md): Configure the built-in logs policy based on your application’s performance, resilience, and retention requirements.
* [Ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md): Parse and transform log entries into a suitable format before indexing.
* [Mapping](../../../manage-data/data-store/mapping.md): Define how data is stored and indexed.


## View and monitor logs [observability-log-monitoring-view-and-monitor-logs]

Use **Logs Explorer** to search, filter, and tail all your logs ingested into your project in one place.

The following resources provide information on viewing and monitoring your logs:

* [Discover and explore](../../../solutions/observability/logs/logs-explorer.md): Discover and explore all of the log events flowing in from your servers, virtual machines, and containers in a centralized view.
* [Detect log anomalies](../../../explore-analyze/machine-learning/anomaly-detection.md): Use {{ml}} to detect log anomalies automatically.


## Monitor data sets [observability-log-monitoring-monitor-data-sets]

The **Data Set Quality** page provides an overview of your data sets and their quality. Use this information to get an idea of your overall data set quality, and find data sets that contain incorrectly parsed documents.

[Monitor data sets](../../../solutions/observability/data-set-quality-monitoring.md)


## Application logs [observability-log-monitoring-application-logs]

Application logs provide valuable insight into events that have occurred within your services and applications. See [Application logs](../../../solutions/observability/logs/stream-application-logs.md).
