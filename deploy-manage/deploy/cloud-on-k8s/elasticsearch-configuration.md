---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elasticsearch-specification.html
---

# Elasticsearch configuration [k8s-elasticsearch-specification]

This section covers various Elasticsearch cluster configuration scenarios when using ECK. For configuration topics relevant to both {{es}} and {{kib}}, see the [](./configure-deployments.md).

Before deploying and running ECK in production, review the basic and advanced settings available on this page. These configurations integrate Elasticsearch, Kubernetes, and ECK operator functionality to help you fine-tune your deployment.

## Key concepts

* [Nodes orchestration](nodes-orchestration.md): Learn how ECK orchestrates nodes, applies changes or upgrades the cluster.
* [Storage recommendations](storage-recommendations.md): Kubernetes storage considerations for {{es}} workloads.

## Basic {{es}} settings

* [Node configuration](node-configuration.md): Configure the `elasticsearch.yml` of your {{es}} nodes.
* [Volume claim templates](volume-claim-templates.md): Configure storage in your {{es}} nodes.
* [Virtual memory](virtual-memory.md): Methods to accomplish {{es}} virtual memory system configuration requirement.
* [Settings managed by ECK](settings-managed-by-eck.md): List of {{es}} settings that you shouldn't update.
* [Custom configuration files and plugins](custom-configuration-files-plugins.md): Add extra configuration files or install plugins to your {{es}} nodes.
* [Init containers for plugin downloads](init-containers-for-plugin-downloads.md): Use Kubernetes init containers to install plugins before starting {{es}}.

## Scheduling and lifecycle management

* [Advanced Elasticsearch node scheduling](advanced-elasticsearch-node-scheduling.md): Integrate standard Kubernetes scheduling options with your {{es}} nodes.
* [Update strategy](update-strategy.md): Control how the changes are applied to the cluster.
* [Pod disruption budget](pod-disruption-budget.md): Integrate Kubernetes Pod disruption budgets in your cluster.
* [Security Context](security-context.md): Kubernetes security context and kernel capabilities.
* [Readiness probe](readiness-probe.md): Customize `readinessProbe` in certain use cases.
* [Pod PreStop hook](pod-prestop-hook.md): Prevent disruptions when terminating Elasticsearch Pods.

## TLS/SSL Certificates

* [Secure HTTP communications](/deploy-manage/security/secure-http-communications.md): Customize the service and TLS certificates used for transport traffic.
* [Transport settings](transport-settings.md): Customize the service and TLS certificates used for transport traffic.

## Traffic handling

* [](./requests-routing-to-elasticsearch-nodes.md): Control the nodes receiving incoming traffic when using multiple `nodeSets` with different [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md).

## Other sections

Other sections of the documentation also include relevant configuration options for your {{es}} cluster:

* [Secure settings](/deploy-manage/security/secure-settings.md)

* [Users and roles](/deploy-manage/users-roles.md)

* [Snapshots](../../tools/snapshot-and-restore/cloud-on-k8s.md)

* [Remote clusters](/deploy-manage/remote-clusters/eck-remote-clusters.md)

* [Autoscaling](../../autoscaling/deployments-autoscaling-on-eck.md)

* [Stack monitoring](/deploy-manage/monitor/stack-monitoring/eck-stack-monitoring.md): Monitor your {{es}} cluster smoothly with the help of ECK.

* [Troubleshoot](/troubleshoot/deployments/cloud-on-k8s/kubernetes.md)
