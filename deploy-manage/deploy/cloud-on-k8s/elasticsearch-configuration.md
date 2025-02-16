---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elasticsearch-specification.html
---

% WORK IN PROGRESS HERE!
# Elasticsearch configuration [k8s-elasticsearch-specification]

Before you deploy and run ECK in production, take some time to look at the basic and advanced settings available on this page. These settings are related both to Elasticsearch and Kubernetes functionality.

**Basic {{es}} settings**

* [Node configuration](node-configuration.md): Configure the `elasticsearch.yml` of your {{es}} nodes.
* [Volume claim templates](volume-claim-templates.md): Configure storage in your {{es}} nodes.
* [Virtual memory](virtual-memory.md)
* [Custom configuration files and plugins](custom-configuration-files-plugins.md)
* [Init containers for plugin downloads](init-containers-for-plugin-downloads.md)

**Kubernetes and system related configuration**
* [Security Context](security-context.md): Kubernetes security context and kernel capabilities.
* [Update strategy](update-strategy.md)
* [Pod disruption budget](pod-disruption-budget.md)
* [Advanced Elasticsearch node scheduling](advanced-elasticsearch-node-scheduling.md)
* [Readiness probe](readiness-probe.md)


**Advanced configuration use cases**

* [HTTP access](./accessing-services.md): Customize the HTTP service of your cluster.
* [HTTP TLS certificates](./tls-certificates.md): Customize HTTP TLS certificates.
* [Transport settings](transport-settings.md): Customize the service and TLS certificate for the transport protocol.
* [Pod PreStop hook](pod-prestop-hook.md)


In other sections of the documentation you can find information for the following configuration use cases:

* [Secure settings](../../security/secure-settings.md)
* [Remote clusters](../../remote-clusters/eck-remote-clusters.md)
* [Create automated snapshots](../../tools/snapshot-and-restore/cloud-on-k8s.md)
* [Elasticsearch autoscaling](../../autoscaling/deployments-autoscaling-on-eck.md)

**Theory**

* [Nodes orchestration](nodes-orchestration.md): Learn how ECK orchestrates nodes, applies changes or upgrades the cluster.
* [Storage recommendations](storage-recommendations.md): Kubernetes storage considerations for {{es}} workloads.
* [Settings managed by ECK](settings-managed-by-eck.md): List of {{es}} settings that you cannot update.

**Troubleshooting utilities**

* [JVM heap dumps](../../../troubleshoot/deployments/cloud-on-k8s/jvm-heap-dumps.md)
* [ECK diagnostics utility](../../../troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md)

