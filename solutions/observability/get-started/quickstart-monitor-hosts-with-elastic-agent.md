---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/quickstart-monitor-hosts-with-elastic-agent.html
  - https://www.elastic.co/guide/en/serverless/current/observability-quickstarts-monitor-hosts-with-elastic-agent.html
---

# Quickstart: Monitor hosts with {{agent}} [quickstart-monitor-hosts-with-elastic-agent]

In this quickstart guide, you’ll learn how to scan your host to detect and collect logs and metrics, then navigate to dashboards to further analyze and explore your observability data. You’ll also learn how to get value out of your observability data.

To scan your host, you’ll run an auto-detection script that downloads and installs {{agent}}, which is used to collect observability data from the host and send it to Elastic.

The script also generates an {{agent}} configuration file that you can use with your existing Infrastructure-as-Code tooling.


## Prerequisites [_prerequisites]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack v9
:sync: stack

* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. This quickstart is available for all Elastic deployment models. To get started quickly, try out our hosted {{ess}} on [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
* A user with the `superuser` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) or the privileges required to onboard data.

    ::::{dropdown} Expand to view required privileges
    * [**Cluster**](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `['monitor', 'manage_own_api_key']`
    * [**Index**](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `{ names: ['logs-*-*', 'metrics-*-*'], privileges: ['auto_configure', 'create_doc'] }`
    * [**Kibana**](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md): `{ spaces: ['*'], feature: { fleet: ['all'], fleetv2: ['all'] } }`

    ::::

* Root privileges on the host—required to run the auto-detection script used in this quickstart.

:::

:::{tab-item} Serverless
:sync: serverless

* An {{obs-serverless}} project. To learn more, refer to [Create an Observability project](../../../solutions/observability/get-started/create-an-observability-project.md).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
* Root privileges on the host—required to run the auto-detection script used in this quickstart.

:::

::::


## Limitations [_limitations]

* The auto-detection script works on Linux and MacOS only. Support for the `lsof` command is also required if you want to detect custom log files.
* If you’ve installed Apache or Nginx in a non-standard location, you’ll need to specify log file paths manually when you run the scan.
* Because Docker Desktop runs in a VM, its logs are not auto-detected.


## Collect your data [_collect_your_data]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack v9
:sync: stack

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Host**, and then select **Elastic Agent: Logs & Metrics**.

    :::{image} ../../../images/observability-quickstart-monitor-hosts-entry-point.png
    :alt: Host monitoring entry point
    :class: screenshot
    :::

3. Copy the install command.

    You’ll run this command to download the auto-detection script, scan your system for observability data, and install {{agent}}.

4. Open a terminal on the host you want to scan, and run the command.
5. Review the list of log files:

    * Enter `Y` to ingest all the log files listed.
    * Enter `n` to either exclude log files or specify additional log paths. Enter `Y` to confirm your selections.

:::

:::{tab-item} Serverless
:sync: serverless

1. [Create a new {{obs-serverless}} project](../../../solutions/observability/get-started/create-an-observability-project.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Add Data**.
3. Under **What do you want to monitor?** select **Host**, and then select **Elastic Agent: Logs & Metrics**.

    :::{image} ../../../images/serverless-quickstart-monitor-hosts-entry-point.png
    :alt: Host monitoring entry point
    :class: screenshot
    :::

4. Copy the install command.

    You’ll run this command to download the auto-detection script, scan your system for observability data, and install {{agent}}.

5. Open a terminal on the host you want to scan, and run the command.
6. Review the list of log files:

    * Enter `Y` to ingest all the log files listed.
    * Enter `n` to either exclude log files or specify additional log paths. Enter `Y` to confirm your selections.

:::

::::


When the script is done, you’ll see a message like "{{agent}} is configured and running."

There might be a slight delay before logs and other data are ingested.

::::{admonition} Need to scan your host again?
:class: note

The auto-detection script (`auto_detect.sh`) is downloaded to the directory where you ran the installation command. You can re-run the script on the same host to detect additional logs. The script will scan the host and reconfigure {{agent}} with any additional logs that are found. If the script misses any custom logs, you can add them manually by entering `n` after the script has finished scanning the host.

::::



## Visualize your data [_visualize_your_data]

After installation is complete and all relevant data is flowing into Elastic, the **Visualize your data** section will show links to assets you can use to analyze your data. Depending on what type of observability data was collected, the page may link to the following integration assets:

| Integration asset | Description |
| --- | --- |
| **Apache** | Prebuilt dashboard for monitoring Apache HTTP server health using error and access log data. |
| **Custom .log files** | Logs Explorer for analyzing custom logs. |
| **Docker** | Prebuilt dashboard for monitoring the status and health of Docker containers. |
| **MySQL** | Prebuilt dashboard for monitoring MySQl server health using error and access log data. |
| **Nginx** | Prebuilt dashboard for monitoring Nginx server health using error and access log data. |
| **System** | Prebuilt dashboard for monitoring host status and health using system metrics. |
| **Other prebuilt dashboards** | Prebuilt dashboards are also available for systems and services not described here,including PostgreSQL, Redis, HAProxy, Kafka, RabbitMQ, Prometheus, Apache Tomcat, and MongoDB. |

For example, you can navigate the **Host overview** dashboard to explore detailed metrics about system usage and throughput. Metrics that indicate a possible problem are highlighted in red.

:::{image} ../../../images/observability-quickstart-host-overview.png
:alt: Host overview dashboard
:class: screenshot
:::


## Get value out of your data [_get_value_out_of_your_data]

After using the dashboards to examine your data and confirm you’ve ingested all the host logs and metrics you want to monitor, you can use Elastic {{observability}} to gain deeper insight into your data.

For host monitoring, the following capabilities and features are recommended:

* In the [Infrastructure UI](../../../solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md), analyze and compare data collected from your hosts. You can also:

    * [Detect anomalies](../../../solutions/observability/infra-and-hosts/detect-metric-anomalies.md) for memory usage and network traffic on hosts.
    * [Create alerts](../../../solutions/observability/incident-management/alerting.md) that notify you when an anomaly is detected or a metric exceeds a given value.

* In the [Logs Explorer](../../../solutions/observability/logs/logs-explorer.md), search and filter your log data, get information about the structure of log fields, and display your findings in a visualization. You can also:

    * [Monitor log data set quality](../../../solutions/observability/data-set-quality-monitoring.md) to find degraded documents.
    * [Run a pattern analysis](../../../explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#log-pattern-analysis) to find patterns in unstructured log messages.
    * [Create alerts](../../../solutions/observability/incident-management/alerting.md) that notify you when an Observability data type reaches or exceeds a given value.

* Use [machine learning](../../../explore-analyze/machine-learning/machine-learning-in-kibana.md) to apply predictive analytics to your data:

    * [Detect anomalies](../../../explore-analyze/machine-learning/anomaly-detection.md) by comparing real-time and historical data from different sources to look for unusual, problematic patterns.
    * [Analyze log spikes and drops](../../../explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#log-rate-analysis).
    * [Detect change points](../../../explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#change-point-detection) in your time series data.


Refer to the [OBservability overview](../../../solutions/observability/get-started/what-is-elastic-observability.md) for a description of other useful features.