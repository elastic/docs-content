---
navigation_title: "How it works"
---

# How monitoring works [how-monitoring-works]


Each monitored {{stack}} component is considered unique in the cluster based on its persistent UUID, which is written to the [`path.data`](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) directory when the node or instance starts.

Monitoring documents are just ordinary JSON documents built by monitoring each {{stack}} component at a specified collection interval. If you want to alter how these documents are structured or stored, refer to [*Configuring data streams/indices for monitoring*](../../../deploy-manage/monitor/monitoring-data/configuring-data-streamsindices-for-monitoring.md).

You can use {{agent}} or {{metricbeat}} to collect monitoring data and to ship it directly to the monitoring cluster.

To learn how to collect monitoring data, refer to:

* One of the following topics depending on how you want to collect monitoring data from {{es}}:

    * [Collecting monitoring data with {{agent}}](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-elastic-agent.md): Uses a single agent to gather logs and metrics. Can be managed from a central location in {{fleet}}.
    * [Collecting monitoring data with {{metricbeat}}](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md): Uses a lightweight {{beats}} shipper to gather metrics. May be preferred if you have an existing investment in {{beats}} or are not yet ready to use {{agent}}.
    * [Legacy collection methods](../../../deploy-manage/monitor/stack-monitoring/es-legacy-collection-methods.md): Uses internal exporters to gather metrics. Not recommended. If you have previously configured legacy collection methods, you should migrate to using {{agent}} or {{metricbeat}}.

* [Monitoring {{kib}}](../../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md)
* [Monitoring {{ls}}](https://www.elastic.co/guide/en/logstash/current/configuring-logstash.html)
* Monitoring {{beats}}:

    * [{{auditbeat}}](https://www.elastic.co/guide/en/beats/auditbeat/current/monitoring.html)
    * [{{filebeat}}](https://www.elastic.co/guide/en/beats/filebeat/current/monitoring.html)
    * [{{heartbeat}}](https://www.elastic.co/guide/en/beats/heartbeat/current/monitoring.html)
    * [{{metricbeat}}](https://www.elastic.co/guide/en/beats/metricbeat/current/monitoring.html)
    * [{{packetbeat}}](https://www.elastic.co/guide/en/beats/packetbeat/current/monitoring.html)
    * [{{winlogbeat}}](https://www.elastic.co/guide/en/beats/winlogbeat/current/monitoring.html)

* [Monitoring APM Server](/solutions/observability/apps/monitor-apm-server.md)
* [Monitoring {{agent}}s](https://www.elastic.co/guide/en/fleet/current/monitor-elastic-agent.html) {{fleet}}-managed agents) or [Configure monitoring for standalone {{agent}}s](https://www.elastic.co/guide/en/fleet/current/elastic-agent-monitoring-configuration.html)

