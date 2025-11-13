---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-overview.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/how-monitoring-works.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
---

# Stack monitoring

:::{include} _snippets/stack-monitoring-def.md
:::

:::{admonition} Simplify monitoring with AutoOps
Use [AutoOps](/deploy-manage/monitor/autoops.md) in your {{ech}}, ECE, ECK, or self-managed deployments. 

AutoOps is a monitoring tool that simplifies cluster management through performance recommendations, resource utilization visibility, and real-time issue detection with resolution paths. In the [regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md) where it has been rolled out, AutoOps is automatically available in [{{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md) and [{{serverless-full}} projects](/deploy-manage/monitor/autoops/autoops-for-serverless.md), and can be set up for [ECE, ECK, and self-managed clusters](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md).

To help you make your decision, refer to [](/deploy-manage/monitor/autoops-vs-stack-monitoring.md).
:::

## How it works

Each monitored {{stack}} component is considered unique in the cluster based on its persistent UUID, which is written to the [`path.data`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) directory when the node or instance starts.

Monitoring documents are just ordinary JSON documents built by monitoring each {{stack}} component at a specified collection interval. If you want to alter how these documents are structured or stored, refer to [Configuring data streams/indices for monitoring](/deploy-manage/monitor/monitoring-data/configuring-data-streamsindices-for-monitoring.md).

You can use {{agent}} or {{metricbeat}} to collect monitoring data and to ship it directly to the monitoring cluster.

In {{ech}}, {{ece}}, and {{eck}}, Elastic manages the installation and configuration of the monitoring agent for you.

## Production architecture

You can collect and ship data directly to your monitoring cluster rather than routing it through your production cluster.

The following diagram illustrates a typical monitoring architecture with separate production and monitoring clusters. This example shows {{metricbeat}}, but you can use {{agent}} instead.

:::{image} /deploy-manage/images/elasticsearch-reference-architecture.png
:alt: A typical monitoring environment
:::

If you have the appropriate license, you can route data from multiple production clusters to a single monitoring cluster. [Learn about the differences between various subscription levels](https://www.elastic.co/subscriptions).

::::{important}
In general, the monitoring cluster and the clusters being monitored should be running the same version of the stack. A monitoring cluster cannot monitor production clusters running newer versions of the stack. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.
::::

## Configure and use stack monitoring

Refer to the following topics to learn how to configure stack monitoring:

### Configure for ECH, ECE, and ECK deployments

* [](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md)
* [](/deploy-manage/monitor/stack-monitoring/eck-stack-monitoring.md)


### Configure for self-managed deployments

* **{{es}}**:
  * [](/deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-elastic-agent.md) (recommended): Uses a single agent to gather logs and metrics. Can be managed from a central location in {{fleet}}.
  * [](/deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md): Uses a lightweight {{beats}} shipper to gather metrics. May be preferred if you have an existing investment in {{beats}} or are not yet ready to use {{agent}}.
  * [](/deploy-manage/monitor/stack-monitoring/collecting-log-data-with-filebeat.md): Uses a lightweight {{beats}} shipper to gather logs.
  * [](/deploy-manage/monitor/stack-monitoring/es-legacy-collection-methods.md): Uses internal exporters to gather metrics. Not recommended. If you have previously configured legacy collection methods, you should migrate to using {{agent}} or {{metricbeat}}.
* **{{kib}}**:
  * [](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-elastic-agent.md) (recommended): Uses a single agent to gather logs and metrics. Can be managed from a central location in {{fleet}}.
  * [](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-metricbeat.md): Uses a lightweight {{beats}} shipper to gather metrics. May be preferred if you have an existing investment in {{beats}} or are not yet ready to use {{agent}}.
  * [](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-legacy.md): Uses internal exporters to gather metrics. Not recommended. If you have previously configured legacy collection methods, you should migrate to using {{agent}} or {{metricbeat}}.


### Monitor other {{stack}} components

:::{tip}
Most of these methods require that you configure monitoring of {{es}} before monitoring other components.
:::

* **Logstash**:
  * [Monitoring {{ls}} with {{agent}}](logstash://reference/monitoring-logstash-with-elastic-agent.md) (recommended): Uses a single agent to gather logs and metrics. Can be managed from a central location in {{fleet}}.
  * [Monitoring {{ls}} with legacy collection methods](logstash://reference/monitoring-logstash-legacy.md): Use {{metricbeat}} or legacy methods to collect monitoring data from {{ls}}.
* **{{beats}}**:

    * [Auditbeat](beats://reference/auditbeat/monitoring.md)
    * [Filebeat](beats://reference/filebeat/monitoring.md)
    * [Heartbeat](beats://reference/heartbeat/monitoring.md)
    * [Metricbeat](beats://reference/metricbeat/monitoring.md)
    * [Packetbeat](beats://reference/packetbeat/monitoring.md)
    * [Winlogbeat](beats://reference/winlogbeat/monitoring.md)

* [**APM Server**](/solutions/observability/apm/apm-server/monitor.md)

* **{{agent}}s**:
  * [{{fleet}}-managed {{agent}}s](/reference/fleet/monitor-elastic-agent.md)
  * [Standalone {{agent}}s](/reference/fleet/elastic-agent-monitoring-configuration.md)

### Access, view, and use monitoring data

* [](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md): After you collect monitoring data for one or more products in the {{stack}}, configure {{kib}} to retrieve that information and display it in on the **Stack Monitoring** page.
* [](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md): View health and performance data for {{stack}} components in real time, as well as analyze past performance.
* [](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md): Configure alerts that trigger based on stack monitoring metrics.
* [](/deploy-manage/monitor/monitoring-data/configuring-data-streamsindices-for-monitoring.md): Adjust the data streams and indices used by stack monitoring.
