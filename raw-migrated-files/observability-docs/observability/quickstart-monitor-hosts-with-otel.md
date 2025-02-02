# Quickstart: Monitor hosts with OpenTelemetry [quickstart-monitor-hosts-with-otel]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


In this quickstart guide, you’ll learn how to monitor your hosts using the Elastic Distribution of OpenTelemetry (EDOT) Collector. You’ll also learn how to use {{observability}} features to gain deeper insight into your observability data after collecting it.


## Prerequisites [_prerequisites_3]

* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. This quickstart is available for all Elastic deployment models. The quickest way to get started with this quickstart is using a trial project on [Elastic serverless](https://docs.elastic.co/serverless/quickstart-monitor-hosts-with-otel.html).
* This quickstart is only available for Linux and MacOS systems.
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md).
* Root privileges on the host—required to run the OpenTelemetry collector because of these components:

    * `hostmetrics` receiver to read all system metrics (all processes, memory, etc.).
    * `filelog` to allow the collector to read any user or application log files.



## Limitations [_limitations_2]

Refer to [Elastic OpenTelemetry Collector limitations](https://github.com/elastic/opentelemetry/blob/main/docs/collector-limitations.md) for known limitations when using the EDOT Collector.


## Collect your data [_collect_your_data_3]

Follow these steps to collect logs and metrics using the EDOT Collector:

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Host**, and then select **OpenTelemetry: Logs & Metrics**.

    :::{image} ../../../images/observability-quickstart-monitor-hosts-otel-entry-point.png
    :alt: Host monitoring entry point
    :class: screenshot
    :::

3. Select the appropriate platform.
4. Copy the command under step 1, open a terminal on your host, and run the command.

    This command downloads the {{agent}} package, extracts it in a EDOT directory. For example, `elastic-distro-8.16.0-linux-x86_64`. It also adds a sample `otel.yml` configuration file to the directory and updates the storage directory, Elastic endpoint, and API key in the file.

    The default log path is `/var/log/*.log`. To update the path, modify the `otel.yml` in the EDOT directory.

    Find additional sample `otel.yml` configuration files in the EDOT directory in the `otel_samples` folder.

5. Copy the command under Step 2 and run it in your terminal to start the EDOT Collector.

::::{note}
Logs are collected from setup onward, so you won’t see logs that occurred before starting the EDOT Collector.
::::


Under **Visualize your data**, you’ll see links to **Logs Explorer** to view your logs and **Hosts** to view your host metrics.


## Gain deeper insight into your host data [_gain_deeper_insight_into_your_host_data]

After using the Hosts page and Discover to confirm you’ve ingested all the host logs and metrics you want to monitor, use Elastic {{observability}} to gain deeper insight into your host data with the following capabilities and features:

* In the [Infrastructure UI](../../../solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md), analyze and compare data collected from your hosts. You can also:

    * [Detect anomalies](../../../solutions/observability/infra-and-hosts/detect-metric-anomalies.md) for memory usage and network traffic on hosts.
    * [Create alerts](../../../solutions/observability/incident-management/alerting.md) that notify you when an anomaly is detected or a metric exceeds a given value.

* In the [Logs Explorer](../../../solutions/observability/logs/logs-explorer.md), search and filter your log data, get information about the structure of log fields, and display your findings in a visualization. You can also:

    * [Monitor log data set quality](../../../solutions/observability/data-set-quality-monitoring.md) to find degraded documents.
    * [Run a pattern analysis](../../../explore-analyze/machine-learning/aiops-labs.md#log-pattern-analysis) to find patterns in unstructured log messages.
    * [Create alerts](../../../solutions/observability/incident-management/alerting.md) that notify you when an Observability data type reaches or exceeds a given value.

* Use [machine learning](../../../explore-analyze/machine-learning/machine-learning-in-kibana.md) to apply predictive analytics to your data:

    * [Detect anomalies](../../../explore-analyze/machine-learning/anomaly-detection.md) by comparing real-time and historical data from different sources to look for unusual, problematic patterns.
    * [Analyze log spikes and drops](../../../explore-analyze/machine-learning/aiops-labs.md#log-rate-analysis).
    * [Detect change points](../../../explore-analyze/machine-learning/aiops-labs.md#change-point-detection) in your time series data.


Refer to the [What is Elastic {{observability}}?](../../../solutions/observability/get-started/what-is-elastic-observability.md) for a description of other useful features.
