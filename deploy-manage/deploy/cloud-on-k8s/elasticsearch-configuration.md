---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elasticsearch-specification.html
---

# Elasticsearch configuration [k8s-elasticsearch-specification]

Before you deploy and run ECK in production, take some time to look at the basic and advanced settings available on this page. These settings are related both to Elasticsearch and Kubernetes functionality.

**Read first (theory)**
* [Nodes orchestration](nodes-orchestration.md): Learn how ECK orchestrates nodes, applies changes or upgrades the cluster.
* [Storage recommendations](storage-recommendations.md): Kubernetes storage considerations for {{es}} workloads.

**Basic {{es}} settings**

* [Node configuration](node-configuration.md): Configure the `elasticsearch.yml` of your {{es}} nodes.
* [Volume claim templates](volume-claim-templates.md): Configure storage in your {{es}} nodes.
* [Virtual memory](virtual-memory.md): Methods to accomplish {{es}} virtual memory system configuration requirement.
* [Settings managed by ECK](settings-managed-by-eck.md): List of {{es}} settings that you shouldn't update.
* [Custom configuration files and plugins](custom-configuration-files-plugins.md): Add extra configuration files or install plugins to your {{es}} nodes.
* [Init containers for plugin downloads](init-containers-for-plugin-downloads.md): Use Kubernetes init containers to install plugins before starting {{es}}.

**Kubernetes related configuration**

% This section shows interactions between Kubernetes standard functionality and your ECK managed clusters.

* [Advanced Elasticsearch node scheduling](advanced-elasticsearch-node-scheduling.md): Integrate standard Kubernetes scheduling options with your {{es}} nodes.
* [Update strategy](update-strategy.md): Control how the changes are applied to the cluster.
* [Pod disruption budget](pod-disruption-budget.md): Integrate Kubernetes Pod disruption budgets in your cluster.
* [Security Context](security-context.md): Kubernetes security context and kernel capabilities.
* [Readiness probe](readiness-probe.md): Customize `readinessProbe` in certain use cases.

**Traffic handling**
* [HTTP access](./accessing-services.md): Configure the HTTP service of your cluster.
* [](./requests-routing-to-elasticsearch-nodes.md): Control the nodes receiving incoming traffic when using multiple `nodeSets` with different [node roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/node-roles-overview.html).

**TLS/SSL Certificates**
* [HTTP TLS certificates](./tls-certificates.md): Customize HTTP TLS certificates.
* [Transport settings](transport-settings.md): Customize the service and TLS certificates used for transport traffic.
* Custom SSL certificate: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-custom-http-certificate.html (needs to be merged and add to security (secure HTTP communications))

**Advanced configuration use cases**

* [Pod PreStop hook](pod-prestop-hook.md)

## Other sections

In other sections of the documentation you can find information for the following configuration use cases:

**Security**
  * [Secure settings](../../security/secure-settings.md)
  * Built-in users

* [**Secure the Elastic Stack**](../../security.md): Manage users and roles, authentication realms, and more.

* **Snapshots and Restore**
  * [Create automated snapshots](../../tools/snapshot-and-restore/cloud-on-k8s.md)

**Remote Clusters**
  * [**Remote clusters**](/deploy-manage/remote-clusters/eck-remote-clusters.md): Configure {{es}} remote clusters functionality for Cross Cluster Search (CCS) and Cross Cluster Replication.

* **Autoscaling**
  * [Elasticsearch autoscaling](../../autoscaling/deployments-autoscaling-on-eck.md): Use {{es}} autoscaling functionality with ECK.

* **Monitoring**
  * [**Stack monitoring**](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-monitoring.html): Monitor your {{es}} cluster smoothly with the help of ECK.

**Troubleshoot**

  * [JVM heap dumps](../../../troubleshoot/deployments/cloud-on-k8s/jvm-heap-dumps.md)
  * [ECK diagnostics utility](../../../troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md)


***** REMOVED *****

* Security
  * Secure settings
  * SAML authentication
  * Users and roles
  * Built-in users
* [**Secure the Elastic Stack**](../../security.md): Manage users and roles, authentication realms, and more.


  * [Users and roles]() (SECURITY)


  * [{{es}} autoscaling on ECK](../../autoscaling/deployments-autoscaling-on-eck.md): 

  * [Snapshot and Restore](../../tools/snapshot-and-restore/cloud-on-k8s.md)

  
  * [**Remote clusters**](/deploy-manage/remote-clusters/eck-remote-clusters.md): Configure {{es}} remote clusters functionality for Cross Cluster Search (CCS) and Cross Cluster Replication.



