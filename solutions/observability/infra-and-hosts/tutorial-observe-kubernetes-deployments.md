---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-kubernetes.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Tutorial: Observe your Kubernetes deployments [monitor-kubernetes]

Applications running in a containerized environment like Kubernetes pose a unique monitoring challenge: how do you diagnose and resolve issues with hundreds of microservices on thousands (or millions) of containers, running in ephemeral and disposable pods?

A successful Kubernetes monitoring solution has a few requirements:

* Monitors all layers of your technology stack, including:

    * The host systems where Kubernetes is running.
    * Kubernetes core components, nodes, pods, and containers running within the cluster.
    * All of the applications and services are running in Kubernetes containers.

* Automatically detects and monitors services as they appear dynamically.
* Provides a way to correlate related data so that you can group and explore related metrics, logs, and other observability data.


## What you’ll learn [_what_youll_learn_4]

This guide describes how to use Elastic {{observability}} to observe all layers of your application, including the orchestration software itself:

* Collect logs and metrics from Kubernetes and your applications
* Collect trace data from applications deployed with Kubernetes
* Centralize the data in the {{stack}}
* Explore the data in real-time using tailored dashboards and {{observability}} UIs

This guide describes how to deploy Elastic monitoring agents as DaemonSets using the {{agent}} manifest files. For other deployment options, see the Kubernetes operator and custom resource definitions from [{{ecloud}} on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md).


## Monitoring architecture [kubernetes-monitoring-architecture]

The {{stack}} provides the following components for monitoring Kubernetes:

1. {{agent}} is a single, unified way to add monitoring for data like logs and metrics to your host.
2. {{agent}} Kubernetes integration, in tandem with {{agent}}, collects logs and metrics from Kubernetes clusters.
3. APM (described later) to monitor, detect, and diagnose complex application performance issues.
4. {{es}} for storing and searching your data.
5. {{observability}} apps in {{kib}} for visualizing and managing your observability data.

:::{image} /solutions/images/observability-k8s-monitoring-architecture.png
:alt: Kubernetes monitoring architecture
:::

The default installation of {{agent}} is deployed to Kubernetes as a DaemonSet to ensure an instance is running on each node of the cluster. It collects logs and metrics from pods, containers, and applications running on Kubernetes.


## Metadata [beats-metadata]

{{agent}} provides processors for adding metadata to events. The metadata is valuable for grouping and exploring related data. For example, when analyzing container logs, you want to know the host and container name, and be able to correlate logs, metrics, and traces.

The default deployments include processors, when needed, for enriching events with cloud and host metadata.

:::{image} /solutions/images/observability-metadata-processors.png
:alt: Metadata processors for cloud
:::

For more on these processors, refer to the [`add_cloud_metadata`](/reference/fleet/add-cloud-metadata-processor.md) and [`add_host_metadata`](/reference/fleet/add_host_metadata-processor.md) documentation.

By default, the Kubernetes integration enriches logs and metrics with valuable metadata.

All Kubernetes metrics are enriched with metadata by default. The enrichment happens in code, and can be configured with the `add_resource_metadata` block on each dataset. For more information on configuring the `add_resource_metadata` block, refer to [Configure kubelet API metadata enrichment](#monitor-k8s-kubelet-configure-metadata) and [Configure `kube-state-metrics` metadata enrichment](#monitor-k8s-kube-state-configure-metadata).

All Kubernetes logs are enriched with metadata by default. For more on configuring metadata enrichment, refer to [Collect Kubernetes container logs](#monitor-kubernetes-integration-container-logs).

Now that you have a basic understanding of the monitoring architecture, let’s learn how to deploy monitoring to your Kubernetes environment.


## Before you begin [_before_you_begin_4]

Before you can monitor Kubernetes, you need the following:

* {{es}} for storing and searching your observability data and {{kib}} for visualizing and managing it.
* If you want to collect Kubernetes state metrics, you need to deploy `kube-state-metrics`. For deployment instructions, refer to the Kubernetes [docs](https://github.com/kubernetes/kube-state-metrics#kubernetes-deployment).


## Part 1: Add and Configure the Kubernetes integration [monitor-kubernetes-integration]

To start collecting logs and metrics from your Kubernetes clusters, first add the [Kubernetes integration](https://docs.elastic.co/en/integrations/kubernetes) to your policy and configure the metrics and logs you want to collect.


### Step 1: Add the Kubernetes integration to your deployment [monitor-k8s-add-integration]

Follow these steps to add the Kubernetes integration to your policy:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Enter "Kubernetes" in the search bar, and select the **Kubernetes** integration.
3. Click **Add Kubernetes** at the top of the Kubernetes integration page.
4. Click **Add integration only (skip agent installation)** at the bottom of the Add integration page.

Continue to [Step 2: Configure your Kubernetes integration](#monitor-k8s-configure-integration).


### Step 2: Configure your Kubernetes integration [monitor-k8s-configure-integration]

The Kubernetes integration can fetch metrics and logs from several components. From the **Add Kubernetes integration** page, configure the options for the metrics and logs you want to collect. The following sections outline the configuration options.

**Collect Metrics**

Collecting metrics about Kubernetes clusters and the workloads running on top of them is a key aspect of Kubernetes observability. You need to collect metrics about the resources running on the underlying infrastructure (for example, the machines of your Kubernetes cluster), metrics for the whole cluster, as well as individual metrics for the containers and pods. Specifically, you need to monitor the health and performance of:

* The hosts where Kubernetes components are running. Each host produces metrics like CPU, memory, disk utilization, and disk and network I/O.
* Kubernetes containers, which produce their own set of metrics.
* The applications running as Kubernetes pods, such as application servers and databases, each producing its own set of metrics.
* Additional Kubernetes resources (like services, deployments, cronjobs) are valuable assets of the whole infrastructure and produce their own set of metrics that need monitoring.

{{agent}} along with the Kubernetes integration provides a unified solution to monitor all layers of your Kubernetes technology stack, so you don’t need multiple technologies to collect metrics.

You have the following options for collecting metrics about your Kubernetes clusters and the workloads running on top of them:

* [Collect Kubernetes metrics from kubelet API](#monitor-kubernetes-integration-kubelet)
* [Collect Kubernetes metrics from `kube-state-metrics`](#monitor-kubernetes-integration-kube-state)
* [Collect Kubernetes metrics from Kubernetes API server](#monitor-kubernetes-integration-k8s-api-metrics)
* [Collect Kubernetes metrics from Kubernetes proxy](#monitor-kubernetes-integration-k8s-proxy)
* [Collect Kubernetes metrics from Kubernetes scheduler](#monitor-kubernetes-integration-k8s-scheduler)
* [Collect Kubernetes metrics from Kubernetes controller-manager](#monitor-kubernetes-integration-k8s-controller)
* [Collect Kubernetes events from Kubernetes API Server](#monitor-kubernetes-integration-k8s-api-events)

**Collect logs**

Collecting and analyzing logs of both Kubernetes core components and various applications running on top of Kubernetes is a powerful tool for Kubernetes observability. Containers running within Kubernetes pods publish logs to stdout or stderr.

You have the following options for collecting Kubernetes logs:

* [Collect Kubernetes container logs](#monitor-kubernetes-integration-container-logs)
* [Collect Kubernetes audit logs](#monitor-kubernetes-integration-audit-logs)


### Collect Kubernetes metrics from kubelet API [monitor-kubernetes-integration-kubelet]

Collecting metrics from the kubelet API is on by default. Kubelet is an agent that runs on each Kubernetes node that is key to managing individual pods and the nodes that host them. For more information on kubelet, refer to the Kubernetes [kubelet docs](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/).

{{agent}} along with the Kubernetes integration can collect metrics from the kubelet API to gather important information about the state of your Kubernetes nodes, pods, containers, and other resources. paleExpand the following list to see all available metrics from the kubelet API.

::::{dropdown} Expand to see available metrics from the kubelet API
**Container metrics**
:   Monitor the overall resource usage, performance, and status at the container level. Learn more at [kubelet container metrics](https://docs.elastic.co/en/integrations/kubernetes/kubelet#container).

**Node metrics**
:   Monitor the overall resource usage, performance, and status at the node level. Learn more at [kubelet node metrics](https://docs.elastic.co/en/integrations/kubernetes/kubelet#node).

**Pod metrics**
:   Monitor the overall resource usage, performance, and status at the pod level. Learn more at [kubelet pod metrics](https://docs.elastic.co/en/integrations/kubernetes/kubelet#pod).

**System metrics**
:   Monitor the overall resource usage, performance, and status of your system containers. Learn more at [kubelet system metrics](https://docs.elastic.co/en/integrations/kubernetes/kubelet#system).

**Volume metrics**
:   Monitor the storage usage and capacity of your persistent volumes. Learn more at [kubelet volume metrics](https://docs.elastic.co/en/integrations/kubernetes/kubelet#system).

::::



#### Configure the kubelet API options [monitor-k8s-kubelet-configure-metrics]

Provide the following information for each of the kubelet API options:

**Add Metadata**
:   This option adds metadata to events. The metadata is valuable for grouping and exploring related data. This option is on by default.

**Bearer Token File**
:   The file path to the token used to authenticate with the kubelet API.

**Hosts**
:   The address of the kubelet API server that Elastic will connect to for collecting metrics. `${env.NODE_NAME}` is an environment variable that represents the name of the Kubernetes node. Port `10250` is the default port where the kubelet API listens for HTTPS connections.

**Period**
:   How frequently to poll the kubelet API for metrics. The default is every 10 seconds.

**SSL Verification Mode**
:   Specify how to handle SSL verification. `none` means that SSL verification is disabled.


#### Configure kubelet API metadata enrichment [monitor-k8s-kubelet-configure-metadata]

Under **Kubernetes Container metrics** and **Kubernetes Pod metrics**, you can configure metadata enrichment from **Advanced options → Add node and namespace metadata**.

From here, update the `add_resource_metadata` block to configure enrichment:

```yaml
 add_resource_metadata:
   namespace:
     include_labels: ["namespacelabel1"]
   node:
     include_labels: ["nodelabel2"]
     include_annotations: ["nodeannotation1"]
   deployment: false
```


### Collect Kubernetes metrics from `kube-state-metrics` [monitor-kubernetes-integration-kube-state]

::::{note}
You need to deploy `kube-state-metrics` before you can use it to collect metric data. To learn how, refer to the Kubernetes [deployment docs](https://github.com/kubernetes/kube-state-metrics#kubernetes-deployment).
::::


Collecting metrics from `kube-state-metrics` is on by default. The `kube-state-metrics` service provides cluster-wide metrics on the health of Kubernetes objects. Refer to the [kube-state-metrics docs](https://github.com/kubernetes/kube-state-metrics) for more information.

`kube-state-metrics` provides horizontal sharding to support large Kubernetes deployments. Refer to the [`kube-state-metrics` sharding](https://github.com/elastic/elastic-agent/blob/main/docs/elastic-agent-ksm-sharding.md) documentation for more information.

With the Kubernetes integration, you can collect a number of metrics using the `kube-state-metrics`. Expand the following list to see all available metrics from `kube-state-metrics`.

::::{dropdown} Expand to see available metrics from kube-state-metrics
**Container metrics**
:   Monitor Container performance to ensure efficiency and stability in pods. Learn more at [`kube-state-metrics` container metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_container).

**CronJob metrics**
:   Monitor CronJob performance and ensure they’re running reliably and efficiently. Learn more at [`kube-state-metrics` CronJob metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_cronjob).

**Kubernetes DaemonSet metrics**
:   Monitor DaemonSet health and distribution. Learn more at [`kube-state-metrics` DaemonSet metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_daemonset).

**Kubernetes Deployment metrics**
:   Monitor deployment status and configuration. Learn more at [`kube-state-metrics` deployment metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_deployment).

**Kubernetes Job metrics**
:   Monitor job completion statuses and execution. Learn more at [`kube-state-metrics` job metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_job).

**Kubernetes Namespace metrics**
:   Monitor namespace active and terminating statuses. Learn more at [`kube-state-metrics` namespace metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_namespace).

**Kubernetes Node metrics**
:   Monitor node health and resource usage. Learn more at [`kube-state-metrics` node metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_node).

**Kubernetes PersistentVolume metrics**
:   Monitor PersistentVolume size, status, and storage configuration. Learn more at [`kube-state-metrics` PersistentVolume metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_persistentvolume).

**Kubernetes PersistentVolumeClaim metrics**
:   Monitor PersistentVolumeClaim phases, classes, and storage requests. Learn more at [`kube-state-metrics` PersistentVolumeClaim metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_persistentvolumeclaim).

**Kubernetes Pod metrics**
:   Monitor pod health and performance. Learn more at [`kube-state-metrics` pod metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_pod).

**Kubernetes ReplicaSet metrics**
:   Monitor ReplicaSets status and the number of replicas in your ReplicaSets. Learn more at [`kube-state-metrics` ReplicaSet metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_replicaset).

**Kubernetes ResourceQuota metrics**
:   Monitor resource limits and current usage. Learn more at [`kube-state-metrics` ResourceQuota metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_resourcequota).

**Kubernetes Service metrics**
:   Monitor service configuration, accessibility, and network integration. Learn more at [`kube-state-metrics` service metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_service).

**Kubernetes StatefulSet metrics**
:   Monitor StatefulSet configuration, status, and scaling. Learn more at [`kube-state-metrics` StatefulSet metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_statefulset).

**Kubernetes StorageClass metrics**
:   Monitor how storage is provisioned and allocated. Learn more at [`kube-state-metrics` StorageClass metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-state-metrics#state_storageclass).

::::



#### Configure the `kube-state-metrics` options [monitor-k8s-kube-state-configure-objects]

Provide the following information for each of the `kube-state-metrics` options:

**Add Metadata**
:   This option adds metadata to events. The metadata is valuable for grouping and exploring related data. This option is on by default.

**Hosts**
:   The address where `kube-state-metrics` is running. Port 8080 is the default.

**Leader Election**
:   When on (default behavior), only the {{agent}} that holds the leadership lock will retrieve metrics from the `kube_state_metrics`. This prevents duplicate data in multi-node Kubernetes clusters.

**Period**
:   How frequently to poll the `kube-state-metrics` for metrics. The default is every 10 seconds.


#### Configure `kube-state-metrics` metadata enrichment [monitor-k8s-kube-state-configure-metadata]

Under **Kubernetes Container metrics** and **Kubernetes Pod metrics**, you can configure metadata enrichment from **Advanced options → Add node and namespace metadata**.

From here, update the `add_resource_metadata` block to configure enrichment:

```yaml
add_resource_metadata:
  namespace:
   enabled: true
    #use_regex_include: false
    include_labels: ["namespacelabel1"]
    #use_regex_exclude: false
    #exclude_labels: ["namespacelabel2"]
  node:
   enabled: true
    #use_regex_include: false
    include_labels: ["nodelabel2"]
    include_annotations: ["nodeannotation1"]
    #use_regex_exclude: false
    #exclude_labels: ["nodelabel3"]
  #deployment: false
  #cronjob: false
```


### Collect Kubernetes metrics from Kubernetes API server [monitor-kubernetes-integration-k8s-api-metrics]

Collecting metrics from the `kube-apiserver` is on by default. The `kube-apiserver` sets up and validates pods, services, and other API objects. These metrics provide insight into the API server’s performance, workload, and health.

Refer to [`kube-apiserver` metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-apiserver) for more on the metrics collected.


#### Configure Kubernetes API server options [monitor-k8s-apiserver-configure]

Provide the following information to collect `kube-apiserver` metrics:

**Bearer Token File**
:   The file path to the token used to authenticate with the `kube-apiserver`.

**Hosts**
:   The address of the Kubernetes API server that the integration connects to. It uses the `KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT` environment variables.

**Leader Election**
:   When on (default behavior), only the {{agent}} that holds the leadership lock will retrieve metrics from the `kube-apiserver`. This prevents duplicate data in multi-node Kubernetes clusters.

**Period**
:   How frequently to poll the `kube-state-metrics` for metrics. The default is every 30 seconds.

**SSL Certificate Authorities**
:   The path to the certificate authority (CA) bundle used to verify the Kubernetes API server’s TLS certificate.


### Collect Kubernetes metrics from Kubernetes proxy [monitor-kubernetes-integration-k8s-proxy]

The `kube-proxy` runs on each node and maintains network rules. Collecting metrics from the `kube-proxy` is on by default. These metrics provide insight into the proxy’s networking activity, performance, and resource usage.

Refer to [`kube-proxy` metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-proxy) for more on the metrics collected.


#### Configure Kubernetes proxy options [monitor-k8s-proxy-configure]

Provide the following information to collect Kubernetes Proxy metrics:

**Hosts**
:   The address where `kube-proxy` is running. Port 10249 is the default.

**Period**
:   How frequently to poll the `kube-state-metrics` for metrics. The default is every 10 seconds.


### Collect Kubernetes metrics from Kubernetes scheduler [monitor-kubernetes-integration-k8s-scheduler]

The kube-scheduler assigns new pods with no node assignment to the most appropriate node. Turn this option on to get metrics from the kube-scheduler. These metrics provide insight on the performance, resource usage, and health of the `kube-scheduler`.

Refer to [`kube-scheduler` metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-scheduler) for more on the metrics collected.


#### Configure Kubernetes scheduler options [monitor-k8s-scheduler-configure]

Provide the following information to collect Kubernetes scheduler metrics:

**Bearer Token File**
:   The file path to the token used to authenticate with the `kube-scheduler`.

**Hosts**
:   The address and port of the `kube-scheduler` from which the Elastic integration should collect metrics. Port `10259` is the default.

**Period**
:   How frequently to poll the `kube-scheduler` for metrics. The default is every 10 seconds.

**SSL Verification Mode**
:   Specify how to handle SSL verification. Defaults to `none` meaning that SSL verification is disabled.


### Collect Kubernetes metrics from Kubernetes controller-manager [monitor-kubernetes-integration-k8s-controller]

The `kube-controller-manager` regulates the state of the clusters. Turn this option on to get metrics from the `kube-controller-manager`. These metrics provide insight on the performance, resource usage, and health of the kube-controller-manager.

Refer to [`kube-controller-manager` metrics](https://docs.elastic.co/en/integrations/kubernetes/kube-controller-manager) for more on the metrics collected.


#### Configure Kubernetes controller-manager options [monitor-k8s-controller-configure]

Provide the following information to collect `kube-controller-manager` metrics:

**Bearer Token File**
:   The file path to the token used to authenticate with the `kube-controller-manager`.

**Hosts**
:   The address and port of the `kube-controller-manager` from which the integration should collect metrics. Port 10259 is the default.

**Period**
:   How frequently to poll the `kube-controller-manager` for metrics. The default is every 10 seconds.

**SSL Verification Mode**
:   Specify how to handle SSL verification. Defaults to `none` meaning that SSL verification is disabled.


### Collect Kubernetes events from Kubernetes API Server [monitor-kubernetes-integration-k8s-api-events]

Event metrics give you an overall view of what’s happening in a cluster. These metrics help you understand what’s happening in your cluster and improve reliability and stability. Collecting Kubernetes events from the Kubernetes API server is on by default.

Refer to [events metrics](https://docs.elastic.co/en/integrations/kubernetes/events) for more on the metrics collected.


#### Configure events from the Kubernetes API server [monitor-k8s-api-events-configure]

Provide the following information to collect Kubernetes events metrics:

**Period**
:   How frequently to poll the `kube-api-server` for events. The default is every 10 seconds.

**Add Metadata**
:   Turn on to add metadata to events. The metadata is valuable for grouping and exploring related data.

**Skip older events**
:   Ignores events that occurred before a certain time

**Leader Election**
:   When on (default behavior), only the {{agent}} that holds the leadership lock will retrieve metrics from the `kube-apiserver`. This prevents duplicate data in multi-node Kubernetes clusters.


### Collect Kubernetes container logs [monitor-kubernetes-integration-container-logs]

Collecting and parsing Kubernetes container logs is on by default. Containers running within Kubernetes pods publish logs to stdout or stderr. These logs are written to a location known to kubelet. The container parser is enabled by default. You can enable additional parsers in **advanced settings**.

Metadata enrichment is also enabled by default, and is based on the Kubernetes provider. Use the `add_resource_metadata` block of the Kubernetes provider to configure it. Refer to the [Kubernetes provider](/reference/fleet/kubernetes-provider.md) docs for more on configuring the provider.

Refer to [Kubernetes container logs](https://docs.elastic.co/en/integrations/kubernetes/container-logs) for more on collecting container logs.


#### Configure Kubernetes container logs [monitor-k8s-container-log-configure]

Provide the following information to collect container logs:

**Use Symlinks**
:   A symlink is lightweight and doesn’t contain the data of the log files, but points to their actual location. Symlinks are used by default.

**Condition**
:   You can specify a condition to control whether a configuration is applied to the running Elastic Agent.


### Collect Kubernetes audit logs [monitor-kubernetes-integration-audit-logs]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Turn this option on to collect audit logs. Kubernetes audit logs record requests that come to the Kubernetes API from internal and external components. These logs help you understand cluster behavior and debug issues.

Refer to [Kubernetes audit logs](https://docs.elastic.co/en/integrations/kubernetes/audit-logs) for more on collecting audit logs.


## Part 2: Configure and install the standalone {{agent}} [monitor-k8s-update-agent-config]

After configuring your integration, you need to download and update your manifest. First, download the manifest by completing the following steps:

1. At the bottom of the **Add Kubernetes integration** page, click **Save and continue**.
2. Click **Add {{agent}} to your hosts**.
3. Under **Enroll in Fleet?**, select **Run standalone**.

    :::{image} /solutions/images/observability-run-standalone-option.png
    :alt: Select run standalone under Enroll in Fleet
    :screenshot:
    :::

4. Under **Configure the agent**, select **Download Manifest**.

After downloading the manifest, open it and update the `ES_USERNAME` and `ES_PASSWORD` environment variables in the DaemonSet to match your {{es}} credentials.

You can also further modify the manifest to fit your needs. For example, you might want to enable autodiscovery to automatically discover container logs. Refer to the [autodiscovery docs](/reference/fleet/elastic-agent-kubernetes-autodiscovery.md) in the {{fleet}} guide for more on enabling autodiscovery in your manifest.

Once you are ready to deploy your {{agent}}:

1. From the directory where you’ve downloaded the manifest, run the following apply command:

    ```sh
    kubectl apply -f elastic-agent-standalone-kubernetes.yml
    ```

2. Check the {{agent}} status with the following command:

    ```sh
    kubectl -n kube-system get pods -l app=elastic-agent
    ```


Refer to [Debug standalone Elastic Agents](/reference/fleet/debug-standalone-agents.md) if you run into any issues with configuring or installing your {{agent}}.


## Part 3: Explore logs and metrics [monitor-kubernetes-explore]

Use {{kib}} to view the metric and log data collected by {{agent}}. Refer to the following sections for more on viewing your data.

* [View performance and health metrics](#monitor-k8s-explore-metrics).
* [View Kubernetes logs](#monitor-k8s-explore-logs).


### View performance and health metrics [monitor-k8s-explore-metrics]

To view the performance and health metrics collected by {{agent}}, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

On the **Infrastructure inventory** page, you can switch between different views to see an overview of the containers and pods running on Kubernetes:

:::{image} /solutions/images/observability-metrics-inventory.png
:alt: Inventory page that shows Kubernetes pods
:screenshot:
:::

For more on using the Inventory page, refer to [View infrastructure metrics by resource type](view-infrastructure-metrics-by-resource-type.md).

On the **Metrics Explorer** page, you can group and analyze metrics for the resources that you are monitoring.

:::{image} /solutions/images/observability-monitor-k8s-metrics-explorer.png
:alt: Metrics dashboard that shows CPU usage for Kubernetes pods
:screenshot:
:::

For more on using the **Metrics Explorer** page, refer to [Explore infrastructure metrics over time](explore-infrastructure-metrics-over-time.md).


### View Kubernetes logs [monitor-k8s-explore-logs]

Find `Discover` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

From the **Data view** menu, select `All logs`. From here, you can quickly search and filter your log data, get information about the structure of log fields, and display your findings in a visualization. Then, you can filter your log data and dive deeper into individual logs to find and troubleshoot issues. For more information, refer to:

* [Explore logs in Discover](../logs/discover-logs.md) for an overview of viewing your logs in Discover.
* [Filter logs in Discover](../logs/filter-aggregate-logs.md#logs-filter-discover) for more on filtering logs in Discover.


## Part 4: Monitor application performance [monitor-kubernetes-application-performance]

Quickly triage and troubleshoot application performance problems with the help of Elastic application performance monitoring (APM).

Think of a latency spike — APM can help you narrow the scope of your investigation to a single service. Because you’ve also ingested and correlated logs and metrics, you can then link the problem to CPU and memory utilization or error log entries of a particular Kubernetes pod.


### Step 1: Set up APM [_step_1_set_up_apm]

Application monitoring data is streamed from your applications running in Kubernetes to APM, where it is validated, processed, and transformed into {{es}} documents.

There are many ways to deploy APM when working with Kubernetes, but this guide assumes that you’re using an {{ech}} deployment. If you haven’t done so already, enable APM in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

If you want to manage APM yourself, there are a few alternative options:

::::{dropdown} Expand alternatives
* [{{ecloud}} on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md) — The Elastic recommended approach for managing APM Server deployed with Kubernetes. Built on the Kubernetes Operator pattern, ECK extends basic Kubernetes orchestration capabilities to support the setup and management of APM Server on Kubernetes.
* Deploy APM Server as a DaemonSet — Ensure a running instance of APM Server on each node in your cluster. Useful when all pods in a node should share a single APM Server instance.
* Deploy APM Server as a sidecar — For environments that should not share an APM Server, like when directing traces from multiple applications to separate {{es}} clusters.
* [Download and install APM Server](/solutions/observability/apm/get-started.md) — The classic, non-Kubernetes option.

::::



### Step 2: Save your secret token [_step_2_save_your_secret_token]

A [secret token](/solutions/observability/apm/secret-token.md) is used to secure communication between APM agents and APM Server. To create or update your secret token in {{kib}}:

1. Find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions → Edit integration**.
4. Navigate to **Agent authorization → Secret token** and set the value of your token.
5. Click Save integration. The APM Server will restart before the change takes effect.

To avoid exposing the secret token, you can store it in a Kubernetes secret. For example:

```cmd
kubectl create secret generic apm-secret --from-literal=ELASTIC_APM_SECRET_TOKEN=asecretpassword --namespace=kube-system <1>
```

1. Create the secret in the same namespace that you’ll be deploying your applications in.


If you’re managing APM Server yourself, see [secret token](/solutions/observability/apm/secret-token.md) for instructions on how to set up your secret token.

If you are using ECK to set up APM Server, the operator automatically generates an `{{APM-server-name}}-apm-token` secret for you.


### Step 3: Install and configure APM Agents [_step_3_install_and_configure_apm_agents]

In most cases, setting up APM agents and thereby instrumenting your applications is as easy as installing a library and adding a few lines of code.

Select your application’s language for details:

:::::::{tab-set}

::::::{tab-item} Go
**Install the agent**

Install the {{apm-agent}} packages for Go.

```go
go get go.elastic.co/apm
```

**Instrument your application**

Instrument your Go application by using one of the provided instrumentation modules or by using the tracer API directly.

```go
import (
	"net/http"

	"go.elastic.co/apm/module/apmhttp"
)

func main() {
	mux := http.NewServeMux()
	...
	http.ListenAndServe(":8080", apmhttp.Wrap(mux))
}
```

**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URL
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Allowed characters: a-z, A-Z, 0-9, -, _, and space


**Learn more in the agent reference**

* [Supported technologies](apm-agent-go://reference/supported-technologies.md)
* [Advanced configuration](apm-agent-go://reference/configuration.md)
* [Detailed guide to instrumenting Go source code](apm-agent-go://reference/set-up-apm-go-agent.md)
::::::

::::::{tab-item} Java
**Attach the agent**

The Java agent can instrument supported technologies without any changes to an application image or code. To do this, you’ll need an [init container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) based on an official Elastic APM docker image.

Before your application starts, copy the agent from the init container into a shared volume. For example, with the Java agent:

```yaml
    # ...
    spec:
      volumes:
      - name: elastic-apm-agent <1>
        emptyDir: {}
      initContainers:
      - name: elastic-java-agent
        image: docker.elastic.co/observability/apm-agent-java:1.12.0 <2>
        volumeMounts:
        - mountPath: /elastic/apm/agent
          name: elastic-apm-agent
        command: ['cp', '-v', '/usr/agent/elastic-apm-agent.jar', '/elastic/apm/agent'] <3>
```

1. The shared volume
2. Build the `initContainer` from the official Elastic Java agent image
3. Copy the agent to the shared volume


The Java command line needs a way to pick up this `javaagent` configuration. You can use the standard JVM TI [JAVA_TOOL_OPTIONS](https://docs.oracle.com/javase/8/docs/platform/jvmti/jvmti.md#tooloptions) environment variable to do this. It doesn’t have to be explicitly specified and is picked up automatically by the JVM when it starts.

::::{tip}
For JVMs that don’t support this option, you can use any other environment variable — either one already defined in your startup script, like `JAVA_OPTS` in some servlet container scripts, or add a dedicated empty one that will have no effect if it’s not set.
::::


```yaml
      # ...
      containers:
      - name: your-app-container
        env:
        # ...
        - name: JAVA_TOOL_OPTIONS <1>
          value: -javaagent:/elastic/apm/agent/elastic-apm-agent.jar
```

1. Used for the command line to pick up the `javaagent` configuration


**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URLS
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
        - name: ELASTIC_APM_APPLICATION_PACKAGES
          value: "org.springframework.samples.petclinic" <4>
        - name: JAVA_TOOL_OPTIONS <5>
          value: -javaagent:/elastic/apm/agent/elastic-apm-agent.jar
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Allowed characters: a-z, A-Z, 0-9, -, _, and space
4. Used to determine whether a stack trace frame is an *in-app* frame or a *library* frame.
5. Explained previously


**Learn more in the agent reference**

* [Supported technologies](apm-agent-java://reference/supported-technologies.md)
* [Advanced configuration](apm-agent-java://reference/configuration.md)
::::::

::::::{tab-item} .NET
::::{note}
These instructions are for .NET Core v2.2+. All other use-cases require downloading the agent from NuGet and adding it to your application. See [set up the Agent](apm-agent-dotnet://reference/set-up-apm-net-agent.md) for full details. Once agent set-up is complete, jump to the **Configure the agent** section on this page.
::::


**Use an init container to download and extract the agent**

The .Net agent automatically instruments .NET Core version 2.2 and newer without any application code changes. To do this, you’ll need an [init container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) that pulls and unzips the latest agent release:

```yaml
    # ...
    spec:
      volumes:
      - name: elastic-apm-agent <1>
        emptyDir: {}
      initContainers:
      - name: elastic-dotnet-agent
        image: busybox
        command: ["/bin/sh","-c"] <2>
        args: <3>
          - wget -qO './elastic-apm-agent/ElasticApmAgent.zip' https://github.com/elastic/apm-agent-dotnet/releases/download/1.7.0/ElasticApmAgent_1.7.0.zip;
            cd elastic-apm-agent;
            cat ElasticApmAgent.zip | busybox unzip -;
        volumeMounts:
        - mountPath: /elastic-apm-agent
          name: elastic-apm-agent
```

1. The shared volume.
2. Runs a shell and executes the provided `args`.
3. Gets the latest `apm-agent-dotnet` release and saves it to `elastic-apm-agent/ElasticApmAgent.zip`. Then `cd` into the directory and unzip the file’s contents. Don’t forget to update the GitHub URL in this command with the version of the agent you’d like to use.


To connect the agent to your application, point the `DOTNET_STARTUP_HOOKS` environment variable towards `ElasticApmAgentStartupHook.dll` file that now exists in the `/elastic-apm-agent` directory of the `elastic-apm-agent` volume.

```yaml
      # ...
      containers:
      - name: your-app-container
        volumeMounts:
        - mountPath: /elastic-apm-agent
          name: elastic-apm-agent
        env:
        # ...
        - name: DOTNET_STARTUP_HOOKS
          value: "/elastic-apm-agent/ElasticApmAgentStartupHook.dll"
```

**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URLS
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
        - name: DOTNET_STARTUP_HOOKS <4>
          value: "/elastic-apm-agent/ElasticApmAgentStartupHook.dll"
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Allowed characters: a-z, A-Z, 0-9, -, _, and space
4. Explained previously and only required when using the no-code instrumentation method.


**Learn more in the agent reference**

* [Supported technologies](apm-agent-dotnet://reference/supported-technologies.md)
* [Advanced configuration](apm-agent-dotnet://reference/configuration.md)
::::::

::::::{tab-item} Node.js
**Install the {{apm-agent}}**

Install the {{apm-agent}} for Node.js as a dependency to your application.

```js
npm install elastic-apm-node --save
```

**Start the agent**

It’s important that the agent is started before you require any other modules in your Node.js application — before `express`, `http`, etc.

```js
var apm = require('elastic-apm-node').start()
```

**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URL
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Defaults to "name" field in package.json, if not specified. Allowed characters: a-z, A-Z, 0-9, -, _, and space


**Learn more in the agent reference**

* [Supported technologies](apm-agent-nodejs://reference/supported-technologies.md)
* [Configuring the agent](apm-agent-nodejs://reference/advanced-setup.md)
::::::

::::::{tab-item} PHP
**Install the agent**

Install the PHP agent using one of the [published packages](https://github.com/elastic/apm-agent-php/releases).

To use the RPM Package (RHEL/CentOS and Fedora):

```php
rpm -ivh <package-file>.rpm
```

To use the DEB package (Debian and Ubuntu):

```php
dpkg -i <package-file>.deb
```

To use the APK package (Alpine):

```php
apk add --allow-untrusted <package-file>.apk
```

If you can’t find your distribution, you can install the agent by [building it from the source](apm-agent-php://reference/set-up-apm-php-agent.md).

**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URL
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Allowed characters: a-z, A-Z, 0-9, -, _, and space


**Learn more in the agent reference**

* [Supported technologies](apm-agent-php://reference/supported-technologies.md)
* [Configuration](apm-agent-php://reference/configuration.md)
::::::

::::::{tab-item} Python
**Install the {{apm-agent}}**

Install the {{apm-agent}} for Python as a dependency:

```python
# Django
pip install elastic-apm

# Flask
pip install elastic-apm[flask]
```

**Add the agent to your application**

For Django, Add `elasticapm.contrib.django` to `INSTALLED_APPS` in your settings:

```python
INSTALLED_APPS = (
   # ...
   'elasticapm.contrib.django',
)
```

For Flask, initialize the agent for your application using environment variables:

```python
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)

apm = ElasticAPM(app)
```

**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URL
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Allowed characters: a-z, A-Z, 0-9, -, _, and space


**Learn more in the agent reference**

* [Supported technologies](apm-agent-python://reference/supported-technologies.md)
* [Advanced configuration](apm-agent-python://reference/configuration.md)
::::::

::::::{tab-item} Ruby
**Install the {{apm-agent}}**

Add the agent to your Gemfile.

```ruby
gem 'elastic-apm'
```

**Start the agent**

Rails: APM will automatically start when your app boots.

Rack: Include the middleware and start and stop Elastic APM:

```ruby
# config.ru

app = lambda do |env|
  [200, {'Content-Type' => 'text/plain'}, ['ok']]
end

# Wraps all requests in transactions and reports exceptions
use ElasticAPM::Middleware

# Start an instance of the Agent
ElasticAPM.start()

run app

# Gracefully stop the agent when process exits.
# Makes sure any pending transactions have already sent.
at_exit { ElasticAPM.stop }
```

**Configure the agent**

Configure the agent using environment variables:

```yaml
        # ...
        - name: ELASTIC_APM_SERVER_URL
          value: "apm-server-url-goes-here" <1>
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN <2>
        - name: ELASTIC_APM_SERVICE_NAME
          value: "service-name-goes-here" <3>
```

1. Defaults to `http://localhost:8200`
2. Pass in `ELASTIC_APM_SECRET_TOKEN` from the `apm-secret` keystore created previously
3. Allowed characters: a-z, A-Z, 0-9, -, _, and space


**Learn more in the agent reference**

* [Supported technologies](apm-agent-ruby://reference/supported-technologies.md)
* [Advanced configuration](apm-agent-ruby://reference/configuration.md)
::::::

:::::::

### Step 4: Configure Kubernetes data [_step_4_configure_kubernetes_data]

In most instances, APM agents automatically read Kubernetes data from inside the container and send it to APM Server. If this is not the case, or if you wish to override this data, you can set environment variables for the agents to read. These environment variable are set via the [Downward API](https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/#the-downward-api) in your Kubernetes pod spec:

```yaml
      # ...
      containers:
      - name: your-app-container
        env:
        # ...
        - name: KUBERNETES_NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: KUBERNETES_POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: KUBERNETES_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: KUBERNETES_POD_UID
          valueFrom:
            fieldRef:
              fieldPath: metadata.uid
```

The table below maps these environment variables to the APM metadata event field:

| Environment variable | Metadata field name |
| --- | --- |
| `KUBERNETES_NODE_NAME` | system.kubernetes.node.name |
| `KUBERNETES_POD_NAME` | system.kubernetes.pod.name |
| `KUBERNETES_NAMESPACE` | system.kubernetes.namespace |
| `KUBERNETES_POD_UID` | system.kubernetes.pod.uid |


### Step 5: Deploy your application [_step_5_deploy_your_application]

APM agents are deployed with your application.

::::{dropdown} Resource configuration file example
A complete resource configuration file based on the previous steps.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <<your-app>>
  namespace: kube-system
  labels:
    app: <<your-app>>
    service: <<your-app>>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <<your-app>>
  template:
    metadata:
      labels:
        app: <<your-app>>
        service: <<your-app>>
    spec:
      dnsPolicy: ClusterFirstWithHostNet
      volumes:
      - name: elastic-apm-agent
        emptyDir: {}
      initContainers:
      - name: elastic-java-agent
        image: docker.elastic.co/observability/apm-agent-java:1.12.0
        volumeMounts:
        - mountPath: /elastic/apm/agent
          name: elastic-apm-agent
        command: ['cp', '-v', '/usr/agent/elastic-apm-agent.jar', '/elastic/apm/agent']
      containers:
      - name: <<your-app>>
        image: <<your-app>>
        volumeMounts:
        - mountPath: /elastic/apm/agent
          name: elastic-apm-agent
        env:
        - name: ELASTIC_APM_SERVER_URL
          value: "apm-server-url-goes-here"
        - name: ELASTIC_APM_SECRET_TOKEN
          valueFrom:
            secretKeyRef:
              name: apm-secret
              key: ELASTIC_APM_SECRET_TOKEN
        - name: ELASTIC_APM_SERVICE_NAME
          value: "petclinic"
        - name: ELASTIC_APM_APPLICATION_PACKAGES
          value: "org.springframework.samples.petclinic"
        - name: ELASTIC_APM_ENVIRONMENT
          value: test
        - name: JAVA_TOOL_OPTIONS
          value: -javaagent:/elastic/apm/agent/elastic-apm-agent.jar
        - name: KUBERNETES_NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: KUBERNETES_POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: KUBERNETES_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: KUBERNETES_POD_UID
          valueFrom:
            fieldRef:
              fieldPath: metadata.uid
```

::::


```cmd
kubectl apply -f demo.yml
```


### View your application’s traces in {{kib}} [_view_your_applications_traces_in_kib]

Application trace data is available in the **Service Inventory**. To open **Service Inventory**, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The **Applications** app allows you to monitor your software services and applications in real-time: visualize detailed performance information on your services, identify and analyze errors, and monitor host-level and agent-specific metrics like JVM and Go runtime metrics.

:::{image} /solutions/images/observability-apm-app-landing.png
:alt: Applications UI Kubernetes
:screenshot:
:::

Having access to application-level insights with just a few clicks can drastically decrease the time you spend debugging errors, slow response times, and crashes.

Best of all, because Kubernetes environment variables have been mapped to APM metadata events, you can filter your trace data by Kubernetes `namespace`, `node.name`, `pod.name`, and `pod.uid`.

:::{image} /solutions/images/observability-apm-app-kubernetes-filter.png
:alt: Applications UI Kubernetes
:screenshot:
:::


## What’s next [_whats_next_3]

* Want to protect your endpoints from security threats? Try [{{elastic-sec}}](https://www.elastic.co/security). Adding endpoint protection is just another integration that you add to the agent policy!
* Are your eyes bleary from staring at a wall of screens? [Create alerts](../incident-management/alerting.md) and find out about problems while sipping your favorite beverage poolside.
* Want Elastic to do the heavy lifting? Use {{ml}} to [detect anomalies](../logs/inspect-log-anomalies.md).
