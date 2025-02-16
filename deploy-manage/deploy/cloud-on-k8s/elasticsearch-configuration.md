---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elasticsearch-specification.html
---

# Elasticsearch configuration [k8s-elasticsearch-specification]

Before you deploy and run ECK in production, take some time to look at the basic and advanced settings available on this page. These settings are related both to Elasticsearch and Kubernetes functionality.

**Read first**
* [Nodes orchestration](nodes-orchestration.md): Learn how ECK orchestrates nodes, applies changes or upgrades the cluster.
* [Storage recommendations](storage-recommendations.md): Kubernetes storage considerations for {{es}} workloads.

**Basic {{es}} settings**

* [Node configuration](node-configuration.md): Configure the `elasticsearch.yml` of your {{es}} nodes.
* [Volume claim templates](volume-claim-templates.md): Configure storage in your {{es}} nodes.
* [Virtual memory](virtual-memory.md): Methods to accomplish {{es}} virtual memory system configuration requirement.
* [Custom configuration files and plugins](custom-configuration-files-plugins.md): Learn how to 
* [Init containers for plugin downloads](init-containers-for-plugin-downloads.md)
* [Settings managed by ECK](settings-managed-by-eck.md): List of {{es}} settings that you cannot update.

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
* [Remote clusters](../../remote-clusters/eck-remote-clusters.md): Configure {{es}} remote clusters functionality for Cross Cluster Search (CCS) and Cross Cluster Replication.
* [Create automated snapshots](../../tools/snapshot-and-restore/cloud-on-k8s.md)
* [Elasticsearch autoscaling](../../autoscaling/deployments-autoscaling-on-eck.md)

**Theory**

* [Nodes orchestration](nodes-orchestration.md): Learn how ECK orchestrates nodes, applies changes or upgrades the cluster.
* [Storage recommendations](storage-recommendations.md): Kubernetes storage considerations for {{es}} workloads.
* [Settings managed by ECK](settings-managed-by-eck.md): List of {{es}} settings that you cannot update.

**Troubleshooting utilities**

* [JVM heap dumps](../../../troubleshoot/deployments/cloud-on-k8s/jvm-heap-dumps.md)
* [ECK diagnostics utility](../../../troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md)


***** REMOVED *****

**Remote Clusters**
  * [**Remote clusters**](/deploy-manage/remote-clusters/eck-remote-clusters.md): Configure {{es}} remote clusters functionality for Cross Cluster Search (CCS) and Cross Cluster Replication.

(Apps related)
* **Snapshots and Restore**
  * Manage snapshots repositories --> Pending to add to configure deployments.

* **Remote Clusters**
  * Configure interconnection between your {{es}} clusters with the help of ECK.

* **Monitoring**
  * Stack Monitoring (for deployments)

* **Licensing**
  * [Manage licenses in ECK](../../license/manage-your-license-in-eck.md)

* **Maintenance**
  * [Upgrade ECK](../../upgrade/orchestrator/upgrade-cloud-on-k8s.md)
  * [Uninstall ECK](../../uninstall/uninstall-elastic-cloud-on-kubernetes.md)

* **Autoscaling**
  * Autoscaling stateless applications
  * Elasticsearch autoscaling on ECK

* Security
  * Secure settings
  * SAML authentication
  * Users and roles
  * Built-in users
* [**Secure the Elastic Stack**](../../security.md): Manage users and roles, authentication realms, and more.


  * [Users and roles]() (SECURITY)

  * [](./requests-routing-to-elasticsearch-nodes.md): Control the nodes receiving incoming traffic when using multiple `nodeSets` with different [node roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/node-roles-overview.html).

  * [{{es}} autoscaling on ECK](../../autoscaling/deployments-autoscaling-on-eck.md): 

  * [Snapshot and Restore](../../tools/snapshot-and-restore/cloud-on-k8s.md)

  * [**Stack monitoring**](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-monitoring.html): Monitor your deployments smoothly with the help of ECK.

  * [**Remote clusters**](/deploy-manage/remote-clusters/eck-remote-clusters.md): Configure {{es}} remote clusters functionality for Cross Cluster Search (CCS) and Cross Cluster Replication.



