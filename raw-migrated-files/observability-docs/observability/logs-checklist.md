---
navigation_title: "Logs"
---

# Log monitoring [logs-checklist]


Logs are an important tool for ensuring the performance and reliability of your applications and infrastructure. They provide important information for debugging, analyzing performance, and managing compliance.

On this page, you’ll find resources for sending log data to {{es}}, configuring your logs, and analyzing your logs.


## Get started with logs [logs-getting-started-checklist] 

For a high-level overview on ingesting, viewing, and analyzing logs with Elastic, refer to [Get started with logs and metrics](../../../solutions/observability/infra-and-hosts/get-started-with-system-metrics.md).

To get started ingesting, parsing, and filtering your own data, refer to these pages:

* **[Stream any log file](../../../solutions/observability/logs/stream-any-log-file.md)**: send log files from your system to {{es}} using a standalone {{agent}} and configure the {{agent}} and your data streams using the `elastic-agent.yml` file.
* **[Parse and organize logs](../../../solutions/observability/logs/parse-route-logs.md)**: break your log messages into meaningful fields that you can use to filter and analyze your data.
* **[Filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md)**: find specific information in your log data to gain insight and monitor your systems.

The following sections provide resources to important concepts or advanced use cases for working with your logs.


## Send log data to {{es}} [logs-send-data-checklist] 

You can send log data to {{es}} in different ways depending on your needs:

* **{{agent}}**: a single agent for logs, metrics, security data, and threat prevention. It can be deployed either standalone or managed by {{fleet}}:

    * **Standalone**: Manually configure, deploy and update an {{agent}} on each host.
    * **Fleet**: Centrally manage and update {{agent}} policies and lifecycles in {{kib}}.

* **{{filebeat}}**: a lightweight, logs-specific shipper for forwarding and centralizing log data.

Refer to the [{{agent}} and {{beats}} capabilities comparison](../../../manage-data/ingest/tools.md) for more information on which option best fits your situation.


### Install {{agent}} [agent-ref-guide] 

The following pages detail installing and managing the {{agent}} in different modes.

* **Standalone {{agent}}**

    Install an {{agent}} and manually configure it locally on the system where it’s installed. You are responsible for managing and upgrading the agents.

    Refer to [Stream any log file](../../../solutions/observability/logs/stream-any-log-file.md) to learn how to send a log file to {{es}} using a standalone {{agent}} and configure the {{agent}} and your data streams using the `elastic-agent.yml` file.

* **{{fleet}}-managed {{agent}}**

    Install an {{agent}} and use {{fleet}} in {{kib}} to define, configure, and manage your agents in a central location.

    Refer to [install {{fleet}}-managed {{agent}}](https://www.elastic.co/guide/en/fleet/current/install-fleet-managed-elastic-agent.html).

* **{{agent}} in a containerized environment**

    Run an {{agent}} inside of a container—either with {{fleet-server}} or standalone.

    Refer to [install {{agent}} in a containerized environment](https://www.elastic.co/guide/en/fleet/current/install-elastic-agents-in-containers.html).



### Install {{filebeat}} [beats-ref-guide] 

{{filebeat}} is a lightweight shipper for forwarding and centralizing log data. Installed as a service on your servers, {{filebeat}} monitors the log files or locations that you specify, collects log events, and forwards them either to [{{es}}](https://www.elastic.co/guide/en/elasticsearch/reference/current) or [Logstash](https://www.elastic.co/guide/en/logstash/current) for indexing.

* [{{filebeat}} overview](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html): general information on {{filebeat}} and how it works.
* [{{filebeat}} quick start](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html): basic installation instructions to get you started.
* [Set up and run {{filebeat}}](https://www.elastic.co/guide/en/beats/filebeat/current/setting-up-and-running.html): information on how to install, set up, and run {{filebeat}}.


## Parse and organize your logs [logs-configure-data-checklist] 

To get started parsing and organizing your logs, refer to [Parse and organize logs](../../../solutions/observability/logs/parse-route-logs.md) for information on breaking unstructured log data into meaningful fields you can use to filter and aggregate your data.

The following resources provide information on important concepts related to parsing and organizing your logs:

* [Data streams](../../../manage-data/data-store/data-streams.md): Efficiently store append-only time series data in multiple backing indices partitioned by time and size.
* [Data views](../../../explore-analyze/find-and-organize/data-views.md): Query log entries from the data streams of specific datasets or namespaces.
* [Index lifecycle management](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md): Configure the built-in logs policy based on your application’s performance, resilience, and retention requirements.
* [Ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md): Parse and transform log entries into a suitable format before indexing.
* [Mapping](../../../manage-data/data-store/mapping.md): define how data is stored and indexed.


## View and monitor logs [logs-monitor-checklist] 

With the {{logs-app}} in {{kib}} you can search, filter, and tail all your logs ingested into {{es}} in one place.

The following resources provide information on viewing and monitoring your logs:

* [Logs Explorer](../../../solutions/observability/logs/logs-explorer.md): monitor all of your log events flowing in from your servers, virtual machines, and containers in a centralized view.
* [Inspect log anomalies](../../../solutions/observability/logs/inspect-log-anomalies.md): use {{ml}} to detect log anomalies automatically.
* [Categorize log entries](../../../solutions/observability/logs/categorize-log-entries.md): use {{ml}} to categorize log messages to quickly identify patterns in your log events.
* [Configure data sources](../../../solutions/observability/logs/configure-data-sources.md): Specify the source configuration for logs in the Logs app settings in the Kibana configuration file.


## Monitor Kubernetes logs [logs-checklist-k8s] 

You can use the {{agent}} with the Kubernetes integration to collect and parse Kubernetes logs. Refer to [Monitor Kubernetes](../../../solutions/observability/infra-and-hosts/tutorial-observe-kubernetes-deployments.md).


## View and monitor application logs [logs-app-checklist] 

Application logs provide valuable insight into events that have occurred within your services and applications.

Refer to [Stream application logs](../../../solutions/observability/logs/stream-application-logs.md).


## Create a log threshold alert [logs-alerts-checklist] 

You can create a rule to send an alert when the log aggregation exceeds a threshold.

Refer to [Log threshold](../../../solutions/observability/incident-management/create-log-threshold-rule.md).


## Configure the default logs template [logs-template-checklist] 

Configure the default `logs` template using the `logs@custom` component template.

Refer to the [Logs index template reference](../../../solutions/observability/unknown-bucket/logs-index-template-reference.md).









