# Diagnose unavailable nodes [echscenario_why_is_my_node_unavailable]

This section provides a list of common symptoms and possible actions that you can take to resolve issues when one or more nodes become unhealthy or unavailable. This guide is particularly useful if you are not [shipping your logs and metrics](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) to a dedicated monitoring cluster.

**What are the symptoms?**

* [Full disk on single-node deployment](../../../troubleshoot/monitoring/unavailable-nodes.md)
* [Full disk on multiple-nodes deployment](../../../troubleshoot/monitoring/unavailable-nodes.md)
* [JVM heap usage exceeds the allowed threshold on master nodes](../../../troubleshoot/monitoring/unavailable-nodes.md)
* [CPU usage exceeds the allowed threshold on master nodes](../../../troubleshoot/monitoring/unavailable-nodes.md)
* [Some nodes are unavailable and are displayed as missing](../../../troubleshoot/monitoring/unavailable-nodes.md)

**What is the impact?**

* Only some search results are successful
* Ingesting, updating, and deleting data do not work
* Most {{es}} API requests fail

::::{note}
Some actions described here, such as stopping indexing or Machine Learning jobs, are temporary remediations intended to get your cluster into a state where you can make configuration changes to resolve the issue.
::::


For production deployments, we recommend setting up a dedicated monitoring cluster to collect metrics and logs, troubleshooting views, and cluster alerts.

If your issue is not addressed here, then [contact Elastic support for help](../../../deploy-manage/deploy/elastic-cloud/ech-get-help.md).
