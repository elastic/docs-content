---
navigation_title: Monitoring
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-troubleshooting.html
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Troubleshoot monitoring [monitoring-troubleshooting]

Use the information in this section to troubleshoot common problems and find answers for frequently asked questions. See also [Troubleshooting monitoring in {{ls}}](logstash://reference/monitoring-troubleshooting.md).

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## No monitoring data is visible in {{kib}} [monitoring-troubleshooting-no-data]

**Symptoms**: There is no information about your cluster on the **Stack Monitoring** page in {{kib}}.

**Resolution**: Check whether the appropriate indices exist on the monitoring cluster. For example, use the [cat indices](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices) command to verify that there is a `.monitoring-kibana*` index for your {{kib}} monitoring data and a `.monitoring-es*` index for your {{es}} monitoring data. If you are collecting monitoring data by using {{metricbeat}} the indices have `-mb` in their names. If the indices do not exist, review your configuration. For example, see [*Monitoring in a production environment*](../../deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md).


## Monitoring data for some {{stack}} nodes or instances is missing from {{kib}} [monitoring-troubleshooting-uuid]

**Symptoms**: The **Stack Monitoring** page in {{kib}} does not show information for some nodes or instances in your cluster.

**Resolution**: Verify that the missing items have unique UUIDs. Each {{es}} node, {{ls}} node, {{kib}} instance, Beat instance, and APM Server is considered unique based on its persistent UUID, which is found in its `path.data` directory. Alternatively, you can find the UUIDs in the product logs at startup.

In some cases, you can also retrieve this information via APIs:

* For Beat instances, use the HTTP endpoint to retrieve the `uuid` property. For example, refer to [Configure an HTTP endpoint for {{filebeat}} metrics](beats://reference/filebeat/http-endpoint.md).
* For {{kib}} instances, use the [status endpoint](/troubleshoot/kibana/access.md) to retrieve the `uuid` property.
* For {{ls}} nodes, use the [monitoring APIs root resource](logstash://reference/monitoring-logstash.md) to retrieve the `id` property.

::::{tip}
When you install {{es}}, {{ls}}, {{kib}}, APM Server, or Beats, their `path.data` directory should be non-existent or empty; do not copy this directory from other installations.
::::


