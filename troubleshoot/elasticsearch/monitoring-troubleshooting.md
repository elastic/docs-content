---
navigation_title: Monitoring
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-troubleshooting.html
---

# Troubleshoot monitoring [monitoring-troubleshooting]

Use the information in this section to troubleshoot common problems and find answers for frequently asked questions. See also [Troubleshooting monitoring in {{ls}}](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/monitoring-troubleshooting.md).

For issues that you cannot fix yourself … we’re here to help. If you are an existing Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Or post in the [Elastic forum](https://discuss.elastic.co/).


## No monitoring data is visible in {{kib}} [monitoring-troubleshooting-no-data] 

**Symptoms**: There is no information about your cluster on the **Stack Monitoring** page in {{kib}}.

**Resolution**: Check whether the appropriate indices exist on the monitoring cluster. For example, use the [cat indices](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices) command to verify that there is a `.monitoring-kibana*` index for your {{kib}} monitoring data and a `.monitoring-es*` index for your {{es}} monitoring data. If you are collecting monitoring data by using {{metricbeat}} the indices have `-mb` in their names. If the indices do not exist, review your configuration. For example, see [*Monitoring in a production environment*](../../deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md).


## Monitoring data for some {{stack}} nodes or instances is missing from {{kib}} [monitoring-troubleshooting-uuid] 

**Symptoms**: The **Stack Monitoring** page in {{kib}} does not show information for some nodes or instances in your cluster.

**Resolution**: Verify that the missing items have unique UUIDs. Each {{es}} node, {{ls}} node, {{kib}} instance, Beat instance, and APM Server is considered unique based on its persistent UUID, which is found in its `path.data` directory. Alternatively, you can find the UUIDs in the product logs at startup.

In some cases, you can also retrieve this information via APIs:

* For Beat instances, use the HTTP endpoint to retrieve the `uuid` property. For example, refer to [Configure an HTTP endpoint for {{filebeat}} metrics](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/http-endpoint.md).
* For {{kib}} instances, use the [status endpoint](/troubleshoot/kibana/access.md) to retrieve the `uuid` property.
* For {{ls}} nodes, use the [monitoring APIs root resource](https://www.elastic.co/guide/en/logstash/current/monitoring-logstash.html) to retrieve the `id` property.

::::{tip} 
When you install {{es}}, {{ls}}, {{kib}}, APM Server, or Beats, their `path.data` directory should be non-existent or empty; do not copy this directory from other installations.
::::


