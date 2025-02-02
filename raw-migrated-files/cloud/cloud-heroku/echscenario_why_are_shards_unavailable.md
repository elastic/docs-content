# Why are my shards unavailable? [echscenario_why_are_shards_unavailable]

This section describes how to analyze unassigned shards using the Elasticsearch APIs and Kibana.

* [Analyze unassigned shards using the Elasticsearch API](../../../troubleshoot/monitoring/unavailable-shards.md)
* [Analyze unassigned shards using the Kibana UI](../../../troubleshoot/monitoring/unavailable-shards.md)
* [Remediate common issues returned by the cluster allocation explain API](../../../troubleshoot/monitoring/unavailable-shards.md)

{{es}} distributes the documents in an index across multiple shards and distributes copies of those shards across multiple nodes in the cluster. This both increases capacity and makes the cluster more resilient, ensuring your data remains available if a node goes down.

A healthy (green) cluster has a primary copy of each shard and the required number of replicas are assigned to different nodes in the cluster.

If a cluster has unassigned replica shards, it is functional but vulnerable in the event of a failure. The cluster is unhealthy and reports a status of yellow.

If a cluster has unassigned primary shards, some of your data is unavailable. The cluster is unhealthy and reports a status of red.

A formerly-healthy cluster might have unassigned shards because nodes have dropped out or moved, are running out of disk space, or are hitting allocation limits.

If a cluster has unassigned shards, you might see an error message such as this on the Elastic Cloud console:

:::{image} ../../../images/cloud-heroku-ec-unhealthy-deployment.png
:alt: Unhealthy deployment error message
:::

If your issue is not addressed here, then [contact Elastic support for help](../../../deploy-manage/deploy/elastic-cloud/ech-get-help.md).




