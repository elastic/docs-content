---
navigation_title: "Self-managed: {{es}}"
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-production.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-monitoring.html
applies_to:
  deployment:
    self: all
---

# Enable stack monitoring for {{es}} on a self-managed cluster

The {{stack}} {{monitor-features}} consist of two components: an agent that you install on each {{es}} and Logstash node, and a Monitoring UI in {{kib}}. The monitoring agent collects and indexes metrics from the nodes and you visualize the data through the Monitoring dashboards in {{kib}}. The agent can index data on the same {{es}} cluster, or send it to an external monitoring cluster.

## Requirements

To use the {{monitor-features}} with the {{security-features}} enabled, you need to [set up {{kib}} to work with the {{security-features}}](/deploy-manage/security.md) and create at least one user for the Monitoring UI. If you are using an external monitoring cluster, you also need to configure a user for the monitoring agent and configure the agent to use the appropriate credentials when communicating with the monitoring cluster.

## Collection methods

You can collect monitoring and logging data in the following ways: 

* [Collect monitoring data with Elastic Agent](/deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-elastic-agent.md)
* [Collect monitoring data with Metricbeat](/deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md)
* [Collect log data with Filebeat](/deploy-manage/monitor/stack-monitoring/collecting-log-data-with-filebeat.md)

If you're building a production environment, then you should send monitoring data to a separate monitoring cluster so that historical data is available even when the nodes you are monitoring are not. To learn how to store monitoring data in a separate cluster, refer to [](/deploy-manage/monitor/stack-monitoring/es-self-monitoring-prod.md).

### Legacy collection methods 

You can also monitor your stack using legacy {{es}} monitoring features. This method is deprecated and should not be used. To learn more, refer to [](/deploy-manage/monitor/stack-monitoring/es-legacy-collection-methods.md).

::::{include} _snippets/legacy-warning.md
::::