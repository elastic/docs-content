---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-elastic-agents-in-containers.html
products:
  - id: fleet
  - id: elastic-agent
---

# Install Elastic Agents in a containerized environment [install-elastic-agents-in-containers]

You can run {{agent}} inside of a container — either with {{fleet-server}} or standalone. Docker images for all versions of {{agent}} are available from the Elastic Docker registry, and we provide deployment manifests for running on Kubernetes.

To learn how to run {{agent}}s in a containerized environment, see:

* [Run {{agent}} in a container](/reference/fleet/elastic-agent-container.md)
* [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/fleet/running-on-kubernetes-managed-by-fleet.md)

    * [Advanced {{agent}} configuration managed by {{fleet}}](/reference/fleet/advanced-kubernetes-managed-by-fleet.md)
    * [Configuring Kubernetes metadata enrichment on {{agent}}](/reference/fleet/configuring-kubernetes-metadata.md)
    * [Run {{agent}} on GKE managed by {{fleet}}](/reference/fleet/running-on-gke-managed-by-fleet.md)
    * [Run {{agent}} on Amazon EKS managed by {{fleet}}](/reference/fleet/running-on-eks-managed-by-fleet.md)
    * [Run {{agent}} on Azure AKS managed by {{fleet}}](/reference/fleet/running-on-aks-managed-by-fleet.md)

* [Run {{agent}} Standalone on Kubernetes](/reference/fleet/running-on-kubernetes-standalone.md)
* [Scaling {{agent}} on {{k8s}}](/reference/fleet/scaling-on-kubernetes.md)
* [Using a custom ingest pipeline with the {{k8s}} Integration](/reference/fleet/ingest-pipeline-kubernetes.md)
* [Run {{agent}} on ECK](/deploy-manage/deploy/cloud-on-k8s/standalone-elastic-agent.md) — for {{eck}} users

::::{note}
Enrollment handling for {{agent}} in a containerized environment has some special nuances.
For details refer to [Enrollment handing for containerized agents](./enrollment-handling-containerized-agent.md).
::::














