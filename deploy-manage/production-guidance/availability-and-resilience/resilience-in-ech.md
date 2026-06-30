---
navigation_title: Resilience in ECH and ECE
applies_to:
  deployment:
    ess: all
    ece: all
products:
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: elastic-stack
  - id: elasticsearch
---

# Resiliency in ECH and ECE deployments

With {{ech}} (ECH) and {{ece}} (ECE), your deployment can be spread across up to three separate availability zones, each hosted in an isolated infrastructure domain, such as separate data centers in the case of {{ech}}.

::::{note}
While this document focuses on how ECH and ECE handle resilience, all the concepts and recommendations described in this section are also applicable to other deployment types. For example, in {{eck}}, you can configure [availability zone distribution and node scheduling](/deploy-manage/deploy/cloud-on-k8s/advanced-elasticsearch-node-scheduling.md) through your Kubernetes platform.
::::

Why this matters:

* Data centers can have issues with availability. Internet outages, earthquakes, floods, or other events could affect the availability of a single data center. With a single availability zone, you have a single point of failure that can bring down your deployment.
* Multiple availability zones help your deployment remain available. This includes your {{es}} cluster, provided that your cluster is sized so that it can sustain your workload on the remaining data centers and that your indices are configured to have at least one replica.
* Multiple availability zones enable you to perform changes to resize your deployment with zero downtime.

::::{important}
ECH and ECE orchestators automatically handle several aspects of cluster resilience that are discussed in the self-managed resiliency guidance for [small](./resilience-in-small-clusters.md) and [large](./resilience-in-larger-clusters.md) clusters:

* Configuring master-eligible nodes:
  * Setting up a [voting-only tiebreaker](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node) when the cluster spans to two availability zones.
  * Promoting [dedicated master nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#dedicated-master-node) as the cluster grows to improve stability and fault tolerance.
* Enabling [shard allocation awareness](../../distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md) to maintain resilience during whole-zone failures.
* Automatically assigning [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) based on the configured [data tiers](/manage-data/lifecycle/data-tiers.md).
* Creating [automatic snapshots](/deploy-manage/tools/snapshot-and-restore.md) at regular configurable intervals, to provide an extra level of redundancy.
::::

## Recommendations [cloud-ha]

* For ECH, review [plan for production](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md) page for how to plan your deployment for production.
* For ECE, review [high availability in ECE](/deploy-manage/deploy/cloud-enterprise/ece-ha.md) page for how to configure your ECE installation to be highly available. 
