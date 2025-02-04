---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elasticsearch-specification.html
---

# Elasticsearch configuration [k8s-elasticsearch-specification]

Before you deploy and run ECK, take some time to look at the basic and advanced settings available on this page. These settings are related both to Elasticsearch and Kubernetes.

**Basic settings**

* [Node configuration](node-configuration.md)
* [Volume claim templates](volume-claim-templates.md)
* [Storage recommendations](storage-recommendations.md)
* [Transport settings](transport-settings.md)

**Advanced settings**

::::{note}
Snapshots are essential for recovering Elasticsearch indices in case of accidental deletion or for migrating data between clusters.
::::


* [Virtual memory](virtual-memory.md)
* [Settings managed by ECK](settings-managed-by-eck.md)
* [Secure settings](../../security/secure-settings.md)
* [Custom configuration files and plugins](custom-configuration-files-plugins.md)
* [Init containers for plugin downloads](init-containers-for-plugin-downloads.md)
* [Update strategy](update-strategy.md)
* [Pod disruption budget](pod-disruption-budget.md)
* [Advanced Elasticsearch node scheduling](advanced-elasticsearch-node-scheduling.md)
* [Nodes orchestration](nodes-orchestration.md)
* [Create automated snapshots](../../tools/snapshot-and-restore/cloud-on-k8s.md)
* [Remote clusters](../../remote-clusters/eck-remote-clusters.md)
* [Readiness probe](readiness-probe.md)
* [Pod PreStop hook](pod-prestop-hook.md)
* [Elasticsearch autoscaling](../../autoscaling/deployments-autoscaling-on-eck.md)
* [JVM heap dumps](../../../troubleshoot/deployments/cloud-on-k8s/jvm-heap-dumps.md)
* [Security Context](security-context.md)
