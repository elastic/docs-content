---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitor-elasticsearch-cluster.html
  - https://www.elastic.co/guide/en/cloud/current/ec-monitoring.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
  - id: cloud-hosted
---

# Monitoring

Keeping on top of the health of your cluster or deployment, as well as your orchestrator, is an important part of maintenance. It also helps you to identify and troubleshoot issues. When you move to [production](/deploy-manage/production-guidance.md), detecting and resolving issues when they arise is a key component of keeping your deployment highly available.

Depending on your deployment type, you can use a variety of solutions for monitoring your Elastic components.

## Monitoring your cluster or deployment

You have several options for monitoring your cluster or deployment.

Use [AutoOps](/deploy-manage/monitor/autoops.md) in your {{ech}}, ECE, ECK, or self-managed deployments. AutoOps is a monitoring tool that simplifies cluster management through performance recommendations, resource utilization visibility, and real-time issue detection with resolution paths. 

Alternatively, you can use [Stack Monitoring](/deploy-manage/monitor/stack-monitoring.md) to monitor logs and metrics across the {{stack}}.

To help you decide between these two options, refer to [](/deploy-manage/monitor/autoops-vs-stack-monitoring.md).

For ECE and {{ech}} deployments, there are also a number of out of the box monitoring tools available.

The following sections provide more details.

### AutoOps (recommended)

```{applies_to}
deployment:
  ess:
  self:
  ece:
  eck:
```

AutoOps diagnoses issues in {{es}} by analyzing hundreds of metrics, providing root-cause analysis and accurate resolution paths. With AutoOps, customers can prevent and resolve issues, cut down administration time, and optimize resource utilization.

In the [regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md) where it has been rolled out, AutoOps is automatically available in [{{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md), and can be set up for [ECE, ECK, and self-managed clusters](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md).

### Stack monitoring

```{applies_to}
deployment:
  ess:
  ece:
  eck:
  self:
```

:::{include} /deploy-manage/monitor/_snippets/stack-monitoring-def.md
:::

In {{ece}} and {{ech}}, Elastic manages the installation and configuration of the monitoring agent for you, simplifying the stack monitoring setup process.

:::{include} /deploy-manage/monitor/_snippets/stack-monitoring-prod.md
:::

### Cluster health and performance metrics

```{applies_to}
deployment:
  ece:
  ess:
```

{{ece}} and {{ech}} provide out of the box tools for monitoring the health of your deployment and resolving health issues when they arise:

* [Cluster health information](/deploy-manage/monitor/cloud-health-perf.md#ec-es-cluster-health), including [health warnings](/deploy-manage/monitor/cloud-health-perf.md#ec-es-health-warnings)
* A [JVM memory pressure indicator](/deploy-manage/monitor/ec-memory-pressure.md)

{{ech}} only:
* [Cluster performance information](/deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md)
* [Preconfigured logs and metrics](/deploy-manage/monitor/cloud-health-perf.md#ec-es-health-preconfigured)

{{ece}} only:
* [Platform monitoring](/deploy-manage/monitor/orchestrators/ece-platform-monitoring.md), including logs, metrics, and proxy logs

:::{tip}
Out of the box logs and metrics tools, including ECH preconfigured logs and metrics and ECE platform monitoring logs and metrics, are useful for providing information in a non-production environment. In a production environment, it’s important set up either AutoOps or stack monitoring to retain the logs and metrics that can be used to troubleshoot any health issues in your deployments. In the event of that you need to [contact our support team](/troubleshoot/index.md#contact-us), they can use the retained data to help diagnose any problems that you may encounter.
:::

To learn more about the health and performance tools in {{ecloud}}, refer to [](/deploy-manage/monitor/cloud-health-perf.md).

## {{kib}} task manager monitoring

```{applies_to}
stack: preview
```
The {{kib}} [task manager](/deploy-manage/distributed-architecture/kibana-tasks-management.md) has an internal monitoring mechanism to keep track of a variety of metrics, which can be consumed with either the health monitoring API or the {{kib}} server log. [Learn how to configure thresholds and consume related to {{kib}} task manager](/deploy-manage/monitor/kibana-task-manager-health-monitoring.md).

## Monitoring your orchestrator
```{applies_to}
deployment:
  ece:
  eck:
```

In addition to monitoring your cluster or deployment health and performance, you need to monitor your orchestrator. Monitoring is especially important for orchestrators hosted on infrastructure that you control.

Learn how to enable monitoring of your orchestrator:

* [ECK operator metrics](/deploy-manage/monitor/orchestrators/eck-metrics-configuration.md): Open and secure a metrics endpoint that can be used to monitor the operator’s performance and health. This endpoint can be scraped by third-party Kubernetes monitoring tools.
* [ECE platform monitoring](/deploy-manage/monitor/orchestrators/ece-platform-monitoring.md): Learn about how ECE collects monitoring data for your installation in the `logging-and-metrics` deployment, and how to access monitoring data.

:::{admonition} Monitoring {{ecloud}}
Elastic monitors [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md) service metrics and performance as part of [our shared responsibility](https://www.elastic.co/cloud/shared-responsibility). We provide service availability information on our [service status page](/deploy-manage/cloud-organization/service-status.md).
:::

## Logging

You can configure several types of logs in {{stack}} that can help you to gain insight into {{stack}} operations, diagnose issues, and track certain types of events. [Learn about the types of logs available, where to find them, and how to configure them](/deploy-manage/monitor/logging-configuration.md).
