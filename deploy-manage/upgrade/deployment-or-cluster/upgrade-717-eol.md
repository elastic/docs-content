---
applies_to:
  stack: all
  serverless: unavailable
---
# Upgrade from 7.17 to {{version.stack}}

{{stack}} version 7.17 has a defined end of support date of 15 January 2026, as stated in the [Elastic Product & Version End of Life Policy](https://www.elastic.co/support/eol). This document provides a guided plan to upgrade from 7.17 to the latest {{version.stack}} release. It complements the official upgrade documentation by showing how the different pieces fit together in a complete upgrade exercise.  

% to decide
Wherever possible, this document links to the existing upgrade guides. In some cases, such as upgrades on {{ech}}, we provide more detailed, step-by-step instructions.

The content applies to all deployment types ({{ech}} (ECH), {{ece}} (ECE), {{eck}} (ECK), and self-managed clusters). Use the tabs to follow the path for your deployment.

## Overview

Upgrading from 7.17 to {{version.stack}} requires two major upgrades. Each major upgrade must be prepared and executed independently, although the planning phase can be shared.

1. **7.17.x → 8.19.x**  
    This brings the cluster onto the latest supported 8.x release, which is the required intermediate version before upgrading to 9.x.
    Before being able to run this upgrade, all ingest components and client libraries must be upgraded to 7.17.x.

2. **8.19.x → {{version.stack}}**  
    This completes the upgrade to the latest 9.x release.
    Before being able to run this upgrade, all ingest components and client libraries must be upgraded to 8.19.x.

The following sections describe these phases in detail and point to the relevant documentation for each deployment type.

Refer to [upgrade paths](/deploy-manage/upgrade.md#upgrade-paths) for more information.

(TBD: Consider [reindex to upgrade](https://www.elastic.co/docs/deploy-manage/upgrade/prepare-to-upgrade#reindex-to-upgrade)? as an alternative method to move directly to a new 9.x cluster? )

## Upgrade planning

The [planning phase](/deploy-manage/upgrade/plan-upgrade.md) ensures that the upgrade is well understood and can be executed with minimal risk.  
It involves defining a clear sequence of actions and assessing the impact on [service availability](/deploy-manage/upgrade.md#availability-during-upgrades) and performance during the upgrade.

For the 7.17.x → 9.x upgrade path, the main planning outcome is a set of required actions to ensure compatibility across the ecosystem:

* **Ingest components:** Before upgrading to 8.19.x, ensure that all ingest components ({{beats}}, {{agent}}, {{ls}}, APM) are on version 7.17.x.  
  Before the 8.19.x → {{version.stack}} upgrade, upgrade all ingest components to 8.19.x.  
* **Client libraries:** If you rely on [{{es}} client libraries](/reference/elasticsearch-clients/index.md), make sure to include them in your plan.
  Typically, libraries are upgraded to match the final version after the deployment upgrade.
* **ECK:** {applies_to}`eck:` Upgrade ECK from 2.x to 3.x before moving to 9.x.  
* **ECE:** {applies_to}`ece:` Upgrade ECE from 3.x to 4.x before moving to 9.x.  

Finally, it is strongly recommended to [test the full upgrade process in a non-production environment](/deploy-manage/upgrade/plan-upgrade.md#test-in-a-non-production-environment) before applying it to production.

(recommend to perform the entire list of compatibility checks in self-managed clusters?)

### Planning result examples

The following examples illustrate what a completed planning phase might look like for different deployment types. Each example describes the initial situation and outlines the overall upgrade plan.

(TBD: maybe we remove all this section here and we just include it together with the execution steps)

::::{applies-switch}

:::{applies-item} ess:
- Ensure all deployments are in 7.17.x (upgrade any older deployment to 7.17.latest)
- Ensure all ingest components are in 7.17.x (upgrade any older component to 7.17.latest)
- Run upgrade assistant to prepare the cluster for the major upgrade to 8.19.x
- Upgrade deployments to latest 8.19.x
- Upgrade all ingest components to 8.19.x
- Run upgrade assistant to prepare the cluster for the major upgrade to 9.x
- Upgrade deployments to {{version.stack}}
- (optional) upgrade all ingest components to {{version.stack}}
:::

:::{applies-item} ece:
- Ensure all deployments are in 7.17.x (upgrade any older cluster)
- Ensure all ingest components are in 7.17.x (upgrade any older component)
- If ECE runs on 3.x, upgrade ECE to latest 4.x release.

- Upgrade deployments to latest 8.19.x
- Upgrade all ingest components to 8.19.x

- Upgrade deployments to {{version.stack}}
- (optional) upgrade all ingest components to {{version.stack}}
:::


:::{applies-item} { eck: }
- Ensure all clusters are in 7.17.x (upgrade any older cluster)
- Ensure all ingest components are in 7.17.x (upgrade any older component)
- If ECK runs on 2.x, upgrade ECK to latest 3.x release.

- Run upgrade assistant to check if the cluster is ready for a major upgrade.
- Upgrade clusters to latest 8.19.x
- Upgrade all ingest components to 8.19.x
- Run upgrade assistant to check if the cluster is ready for a major upgrade.
- Upgrade clusters to latest 9.x
- (optional) Upgrade all ingest components to 9.x
:::

:::{applies-item} self:
- Ensure all deployments are in 7.17.x (upgrade any older cluster)
- Ensure all ingest components are in 7.17.x (upgrade any older component)

- Run upgrade assistant to check if the cluster is ready for a major upgrade.
- Upgrade cluster to latest 8.19.x in the following order: {{es}}, {{kib}}, Fleet Server, and Elastic APM (if used)
- Upgrade all ingest components to 8.19.x

- Run upgrade assistant to check if the cluster is ready for a major upgrade.
- Upgrade cluster to {{version.stack}} in the same order as before
- (optional) upgrade all ingest components to {{version.stack}}
:::

::::

## Upgrade Step 1: 7.17.x → 8.19.x

draft items for preparations:
- Assess deployment topology (clusters, nodes, orchestrator type)  
- Inventory dependencies (plugins, custom ingest pipelines, clients, integrations)  
- Run Upgrade Assistant and resolve issues  
- Define snapshot/backup and rollback strategy  
- Test upgrade steps in a staging environment  
- Align with maintenance windows and SLAs  


### Preparation

* Index compatibility:  upgrade assistant.
- Confirm prerequisites and compatibility  
- Validate cluster health and shard allocation  
- Review version-specific breaking changes (link to docs)  
- Take snapshots / backups  

### Execution
- Upgrade process (tabs for {{ech}}, {{ece}}, {{eck}}, self-managed)  
- Rolling vs full-cluster downtime options  
- Client compatibility considerations  
- Ingest components compatibility considerations.

CCR / CCS / Remote clusters / ML / Transform indices implications?
Monitoring clusters implications?

### Validation
- Post-upgrade health checks (cluster status, ingest, search)  
- Validate monitoring dashboards and alerts  
- Resolve deprecation warnings  

## Upgrade Step 2: 8.19.x → {{version.stack}}

### Preparation

* Index compatibility:  upgrade assistant.
- Repeat prerequisites and compatibility checks  
- Review 9.x breaking changes  
- Ensure clients are compatible (REST API compatibility mode, etc.)  
- Take snapshots / backups  

### Execution
- Upgrade process (tabs for {{ech}}, {{ece}}, {{eck}}, self-managed)  
- Node upgrade order and orchestration  
- Upgrade ecosystem components (Beats, Logstash, Elastic Agent, APM, etc.)  

CCR / CCS / Remote clusters / ML / Transform indices implications?
Monitoring clusters implications?

### Validation
- Post-upgrade cluster validation  
- Performance and stability checks  
- Review and remove deprecated settings  

## Post-Upgrade Wrap-Up
- Confirm cluster stability over an observation period  
- Update operational runbooks and monitoring baselines  
- Validate client library upgrades and integrations  
- Decommission old snapshots if no longer needed  
- Document lessons learned  

<!--

-----
older text and links in case of need

{{stack}} version 7.17 is getting EOL soon. This document provides guidance to upgrade from 7.17 to the latest {{version.stack}} version, relying on existing documents and procedures.

old reference: https://www.elastic.co/guide/en/elastic-stack/7.17/upgrading-elastic-stack.html
https://www.elastic.co/guide/en/elastic-stack/8.18/upgrading-elastic-stack.html
new: https://www.elastic.co/docs/deploy-manage/upgrade/deployment-or-cluster

Upgrade 8.19: https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html

Prepare from 7.x: https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade

Elastic Cloud specifics? 
ECE or ECK specifics?

## Overview

Upgrading from 7.17 to the latest {{version.stack}} implies two major upgrades. Each of them needs to be treated independently in terms preparations and execution. The planning phase can be common.

* Upgrade from 7.17.x to 8.19.x

* Upgrade from 8.19.x latest to {{version.stack}}

As a general guideline we recommend reading the following documents before upgrading:
- Plan your upgrade: This doc tells you all the necessary to plan your upgrade properly.

- Preparations.

Run upgrade assistant.

Consider [reindex to upgrade](https://www.elastic.co/docs/deploy-manage/upgrade/prepare-to-upgrade#reindex-to-upgrade)? 

## Different deployment types

asda

## Upgrade order and plan


## Major upgrade to 8.19.x

### Preparations and pre-requisites.
CCR / CCS / Remote clusters / ML / Transform indices
Execute the upgrade


Run the upgrade assistant as explained in [this doc](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade).

Notes:
* If you use a monitoring cluster, upgrade the monitoring cluster first.
* If you use remote clusters functionality, upgrade the remote clusters first.

Divide the recommendations per deployment type: for Elastic Cloud we can tell that the UI takes care of almost everything, the user needs to take care of the external components (beats, Elastic Agent, Logstash, etc.)

### Execute the upgrade

Start with the deployment
Don't forget beats and external components afterwards, as upgrading them to 8.19.x is a pre-requisite to upgrade to 9.x

Self-managed: Follow the [official guide](8.19) to perform the rolling upgrade of your cluster.

ECH: (we need to guide users or check the current doc).
ECE: (we need to guide users or check the current doc).
ECK: (check docs to run the upgrade)

## Major upgrade to 9.1.x

### Preparations and pre-requisites

### Execute the upgrade

(Optional): Upgrade external components to 9.x, although 8.19.x is compatible with 9.x.


