---
applies_to:
  stack: ga
  serverless: unavailable
---
# Upgrade from 7.17 to {{version.stack}}

{{stack}} version 7.17 has a defined end of support date of 15 January 2026, as stated in the [Elastic Product & Version End of Life Policy](https://www.elastic.co/support/eol). This document provides a guided plan to upgrade from 7.17 to the latest {{version.stack}} release. It complements the official upgrade documentation by showing how the different pieces fit together in a complete upgrade exercise.  

::::{important}
This guide applies only to deployments or clusters running {{es}} version 7.17.x. If you are using an earlier version, first upgrade to the latest 7.17 release before proceeding.
::::

The content applies to all deployment types ({{ech}} (ECH), {{ece}} (ECE), {{eck}} (ECK), and self-managed clusters). Use the tabs to follow the path for your deployment.

## Overview

Upgrading from 7.17 to {{version.stack}} requires two major upgrades. Each major upgrade must be prepared and executed independently, although the planning phase can be shared.

1. **7.17.x → 8.19.x**  
    This brings the cluster onto the latest supported 8.x release, which is the required intermediate version before upgrading to {{version.stack}}.
    Before running this upgrade, all ingest components and client libraries must be upgraded to 7.17.x.

2. **8.19.x → {{version.stack}}**  
    This completes the upgrade to the latest 9.x release.
    Before running this upgrade, all ingest components and client libraries must be upgraded to 8.19.x.

The following sections describe these phases in detail and point to the relevant documentation for each deployment type.

Refer to [upgrade paths](/deploy-manage/upgrade.md#upgrade-paths) for more information.

::::{dropdown} Alternative method: Reindex to upgrade
For basic use cases that do not rely on {{kib}} dashboards or {{stack}} features such as {{ml}}, transforms, {{kib}} alerting, or detection rules, instead of performing two sequential upgrades (7.17 → 8.19 → {{version.stack}}), you can create a new {{version.stack}} cluster or deployment and migrate your data from the 7.17 cluster by reindexing.

For detailed guidance on how to plan and execute this method, refer to [Reindex to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md#reindex-to-upgrade).

It may be suitable when:
- You prefer to build new infrastructure rather than modify an existing one.  
- You want to reduce the risk of performing two consecutive major upgrades.  
- You plan to redesign your topology or move to a new environment (for example, from self-managed to {{ech}} or {{ece}}).  

This approach is intended for {{es}} use cases focused on indexing and querying your own data. If you need a smooth transition that preserves {{kib}} configurations and {{stack}} features data, follow the standard upgrade path instead.
::::

## Upgrade planning [planning]

The [planning phase](/deploy-manage/upgrade/plan-upgrade.md) ensures that the upgrade is well understood, can be executed with minimal risk, and follows the [correct order](/deploy-manage/upgrade/plan-upgrade.md#upgrade-order).

It involves defining a clear sequence of actions and assessing the impact on [service availability](/deploy-manage/upgrade.md#availability-during-upgrades) and performance during the upgrade.

For the 7.17.x → 9.x upgrade path, the main planning outcome is a set of required actions to ensure compatibility across the ecosystem:

* **Ingest components:**

  Before the initial upgrade to 8.19.x, ensure that all ingest components ({{beats}}, {{agent}}, {{ls}}, APM) are on version 7.17.x.

  Before the final upgrade to {{version.stack}}, upgrade all ingest components to 8.19.x.

  Refer to [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for more details.
  
* **Client libraries:**

  If your use case relies on [{{es}} client libraries](/reference/elasticsearch-clients/index.md), make sure to include them in your plan. Typically, libraries are upgraded to match the {{es}} version after each of the upgrades.

* **Orchestration platforms:**

  * {applies_to}`eck:` If you are running an ECK version older than 3.x you need to upgrade ECK before the final upgrade to 9.x. This can be done at the beginning before the initial upgrade or between them.
  * {applies_to}`ece:` If you are running an ECE version older than 4.x you need to upgrade your ECE platform before the final upgrade to 9.x. This can be done at the beginning before the initial upgrade or between them.

Finally, it is strongly recommended to [test the full upgrade process in a non-production environment](/deploy-manage/upgrade/plan-upgrade.md#test-in-a-non-production-environment) before applying it to production.

## Upgrade Step 1: 7.17.x → 8.19.x

This step assumes that you want to perform the deployment upgrade as part of your [upgrade plan](#planning), and all your ingest components and client libraries are compatible with 8.19.x.

### 8.19 upgrade preparations

The most important preparation steps for a major upgrade are:
* Breaking changes and known issues analysis.
* Run the upgrade assistant in {{kib}} to detect and resolve issues.
* Take a snapshot of your deployment before the upgrade.

{{ech}} and {{ece}} platforms facilitates the upgrade preparations by automatically creating snapshots before the upgrade and by checking the upgrade assistant for critical issues before proceeding.

Also take in mind the following points:
* If you are using dedicated monitoring clusters or remote clusters, upgrade them first.

* Take a cluster snapshot before starting the ugprade

Upgrade 8.19: https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html

Prepare from 7.x: https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade


::::{applies-switch}

:::{applies-item} ess:

old doc: https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade

* **Breaking changes**

* **Known issues**

* **Snapshots**

To keep your data safe during the upgrade process, a snapshot is taken automatically before any changes are made to your cluster. After a major version upgrade is complete and a snapshot of the upgraded cluster is available, all snapshots taken with the previous major version of Elasticsearch are stored in the snapshot repository.

From version 8.3, snapshots are generally available as simple archives. Use the archive functionality to search snapshots as old as version 5.0 without the need of an old Elasticsearch cluster. This ensures that data you store in Elasticsearch doesn’t have an end of life and is still accessible when you upgrade, without requiring a reindex process.

On Elastic Cloud Enterprise, you need to [configure a snapshot repository](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) to enable snapshots.

* **Security realm settings**

  (only if needed)During the upgrade process, you are prompted to update the security realm settings if your user settings include a `xpack.security.authc.realms` value.

  If the security realms are configured in user_settings, you’ll be prompted to modify the settings:
    1. On the Update security realm settings window, edit the settings.
    2. Click Update settings. If the security realm settings are located in `user_settings_override`, contact support to help you upgrade.

* **Upgrade Assistant**

  Prior to upgrading, Elastic Cloud checks the deprecation API to retrieve information about the cluster, node, and index-level settings that need to be removed or changed. If there are any issues that would prevent a successful upgrade, the upgrade is blocked. Use the [Upgrade Assistant in 7.17](https://www.elastic.co/guide/en/kibana/7.17/upgrade-assistant.html) to identify and resolve issues and reindex any indices created before 7.0.


  If any incompatibilities are detected when you attempt to upgrade to 8.19.5, the UI provides a link to the Upgrade Assistant, which checks for deprecated settings in your cluster and indices and helps you resolve them. After resolving the issues, return to the deployments page and restart the upgrade.

* 
:::

:::{applies-item} ece:
:::


:::{applies-item} { eck: }
:::

:::{applies-item} self:
Follow all preparations per [](/deploy-manage/upgrade/prepare-to-upgrade.md)
:::

::::


### 8.19 upgrade execution

Consider the following before running the actual upgrade of your deployment or cluster:
* If you use stack monitoring, upgrade your monitoring clusters first.
* If you use remote clusters, upgrade the remote clusters first.

To upgrade your deployment or cluster, do the following depending on the deployment type:

::::{applies-switch}

:::{applies-item} ess:

To upgrade your deployment, follow the steps and guidance from [](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md#perform-cloud-upgrade).

During the upgrade process all of your deployment components will be upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}} and APM)
:::

:::{applies-item} ece:
To upgrade your deployment, follow the steps and guidance from [](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md#perform-the-upgrade).

During the upgrade process all of your deployment components will be upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}} and APM)
:::


:::{applies-item} { eck: }

Upgrade your cluster per [](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)

After the upgrade of {{es}} and {{kib}}, upgrade any [other Elastic application](/deploy-manage/deploy/cloud-on-k8s/orchestrate-other-elastic-applications.md) connected to the cluster, such as {{fleet-server}}, or Elastic APM.
:::

:::{applies-item} self:
Follow the steps in the [upgrade Elastic on-prem](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack-on-prem.html) guide, ensuring that all components are upgraded in the specified order.
:::

::::

### 8.19 upgrade validation
- Post-upgrade health checks (cluster status, ingest, search)  
- Validate monitoring dashboards and alerts  
- Resolve deprecation warnings  

### Upgrade ingest components to 8.19.x

Because the upgrade to 8.19.x is an intermediate step to reach {{version.stack}} it's mandatory to upgrade now all ingest components to 8.19.x before continuing with the next major upgrade.

Refer to [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for more details.

## Upgrade Step 2: 8.19.x → {{version.stack}}

### {{version.stack}} preparations

During the preparations of the final upgrade, the **upgrade assistant** will play an important role, as we will need to take action on the older indices created in 7.x. Pay special attention to ML or transform related items, and refer to [prepare to upgrade]() for more details.

Rest of items will be similar to the previous upgrade preparations:
* Breaking changes and known issues analysis.
* Run the upgrade assistant in {{kib}} to detect and resolve issues.
* Take a snapshot of your deployment or cluster before the upgrade.

::::{applies-switch}

:::{applies-item} ess:

{{ecloud}} detects incmpatibilities. If they are found open the Upgrade Assistant and solve them.

:::

:::{applies-item} ece:

Before upgrading to 9.x ensure ECE is upgraded to 4.x

:::


:::{applies-item} { eck: }

Before upgrading to 9.x ensure ECK is upgraded to 3.x

:::

:::{applies-item} self:
Follow all preparations per [](/deploy-manage/upgrade/prepare-to-upgrade.md)
:::

::::


### {{version.stack}} upgrade execution

As with the previous upgrade, remind the following items:
* If you use stack monitoring, upgrade your monitoring clusters first.
* If you use remote clusters, upgrade the remote clusters first.

To upgrade your deployment or cluster, do the following depending on the deployment type:

::::{applies-switch}

:::{applies-item} ess:

To upgrade your deployment, follow the steps and guidance from [](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md#perform-cloud-upgrade).

During the upgrade process all of your deployment components will be upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}} and APM)
:::

:::{applies-item} ece:
To upgrade your deployment, follow the steps and guidance from [](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md#perform-the-upgrade).

During the upgrade process all of your deployment components will be upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}} and APM)
:::


:::{applies-item} { eck: }

Upgrade your cluster per [](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)

After the upgrade of {{es}} and {{kib}}, upgrade any [other Elastic application](/deploy-manage/deploy/cloud-on-k8s/orchestrate-other-elastic-applications.md) connected to the cluster, such as {{fleet-server}}, or Elastic APM.
:::

:::{applies-item} self:
Follow the steps in the [upgrade the {{stack}} on a self-managed cluster](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md) guide, ensuring that all components are upgraded in the specified order.
:::

::::





::::{applies-switch}

:::{applies-item} ess:

Upgrade the deployment and then all ingest components as showed in:

https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade

:::

:::{applies-item} ece:

Upgrade the deployment and then all ingest components as showed in:

https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade

:::


:::{applies-item} { eck: }
:::

:::{applies-item} self:

https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack-on-prem.html

1. Upgrade {{es}} following the rolling upgrade method.
2. Upgrade {{kib}}
:::

::::

### {{version.stack}} upgrade validation

- Post-upgrade cluster validation  
- Performance and stability checks  
- Review and remove deprecated settings  

### (Optional) Upgrade ingest components to {{version.stack}}

This step is optional, because all ingest components on 8.19.x are compatible with {{stack}} 9.x.

Refer to [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for more details.


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


