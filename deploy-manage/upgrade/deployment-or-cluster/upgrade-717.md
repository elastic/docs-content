---
applies_to:
  stack: ga
  serverless: unavailable
---
# Upgrade from 7.17 to {{version.stack}}

% add enterprise search related comments?

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

  After upgrading the cluster to 8.19.x and before proceeding to {{version.stack}}, upgrade all ingest components to 8.19.x.

  Refer to [Upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for detailed upgrade instructions.
  
* **Client libraries:**

  If your use case relies on [{{es}} client libraries](/reference/elasticsearch-clients/index.md), make sure to include them in your plan. Typically, libraries are upgraded to match the {{es}} version after each of the upgrades.

* **Orchestration platforms:**

  * {applies_to}`eck:` If you are running an ECK version earlier than 3.x, you need to upgrade [ECK before](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) the final upgrade to 9.x. This can be done either at the beginning, before the initial upgrade, or between the two upgrade phases.

  * {applies_to}`ece:` If you are running an ECE version earlier than 4.x, you need to [upgrade your ECE platform](/deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md) before the final upgrade to 9.x. This upgrade must be performed after upgrading your deployments to 8.19.x, since ECE 4.x is not compatible with 7.x deployments.

Finally, we strongly recommend [testing the full upgrade process in a non-production environment](/deploy-manage/upgrade/plan-upgrade.md#test-in-a-non-production-environment) before applying it to production.

## Upgrade Step 1: 7.17.x → 8.19.x

This step covers upgrading your deployment from 7.17.x to 8.19.x, following the [planning phase](#planning) and assuming that all ingest components and client libraries are compatible with 8.19.x.

### 8.19 upgrade preparations

The [upgrade preparation steps from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade) are designed to prevent upgrade failures by detecting and addressing internal incompatibilities, including deprecated settings that are no longer supported in the next release.

During a major upgrade, the [**Upgrade Assistant**](https://www.elastic.co/guide/en/kibana/7.17/upgrade-assistant.html) in {{kib}} 7.17 plays a critical role. It scans your cluster for deprecated settings, incompatible indices, and other issues that could prevent nodes from starting after the upgrade. The tool guides you through reindexing old indices, fixing configuration problems, and reviewing deprecation logs to ensure your deployment is fully compatible with the next major version. Ignoring its recommendations can lead to upgrade failures or cluster downtime.

While the **Upgrade Assistant** helps you identify breaking changes that affect your deployment or cluster, it's still recommended to review the complete list of breaking changes and known issues during your preparation phase. These are available in the following documents:
* [{{es}} 8.x migration guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/breaking-changes.html)
* [Kibana breaking changes summary](https://www.elastic.co/guide/en/kibana/8.19/breaking-changes-summary.html)

Follow the guidelines below for your specific deployment type:

::::{applies-switch}

:::{applies-item} ess:

The {{ecloud}} platform facilitates major upgrades by:
* Automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, complete the steps described in the [8.19 {{ecloud}} upgrade guide](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html) **up to the "Perform the upgrade" section.**  

You should make sure to:

1. Run the **Upgrade Assistant** in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
   * Reindex legacy indices (created before 7.0).  
   * Remove or update deprecated settings and mappings.  
   * Review deprecation logs for both {{es}} and {{kib}}.  

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.  

3. As a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) if your custom client applications are affected by breaking changes. This mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy.
:::

:::{applies-item} ece:

{{ece}} platform facilitates major upgrades by:
* When [snapshots are configured](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, complete the steps described in the [8.19 {{ecloud}} upgrade guide](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html) up to the "Perform the upgrade" section. *Note: Although this guide refers to {{ecloud}}, the same preparation steps apply to ECE deployments.*

You should make sure to:

1. Run the **Upgrade Assistant** in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
   * Reindex legacy indices (created before 7.0).  
   * Remove or update deprecated settings and mappings.  
   * Review deprecation logs for both {{es}} and {{kib}}.  

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.  

3. As a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) if your custom client applications are affected by breaking changes. This mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy.
:::

:::{applies-item} { eck: }

Upgrade preparations for an {{eck}}-managed cluster are similar to a self-managed deployment. Before starting the upgrade:

* Follow the steps in [Prepare to upgrade from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade).  
* Review the [{{es}} upgrade setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html) for additional details and best practices.  

If you're upgrading from an {{eck}} version earlier than 3.x, make sure to [upgrade ECK first](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) before performing the final upgrade to 9.x.
:::

:::{applies-item} self:

Before starting the upgrade, follow the [Prepare to upgrade from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade) steps.

For additional details and best practices, review the [{{es}} upgrade setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html).
:::

::::

### 8.19 upgrade execution

Keep the following considerations in mind when upgrading your deployment or cluster:

* If you use [Stack monitoring](/deploy-manage/monitor/stack-monitoring.md) with a dedicated monitoring cluster, upgrade your monitoring cluster first.
* If you use [remote clusters](/deploy-manage/remote-clusters.md) functionality, upgrade the remote clusters first.

To perform the upgrade, follow the instructions below for your specific deployment type:

::::{applies-switch}

:::{applies-item} ess:

To upgrade your deployment to 8.19, follow the steps in [Upgrade on Elastic Cloud → Perform the upgrade](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade).  

During the upgrade process, all components of your deployment are upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}} and APM)
:::

:::{applies-item} ece:

To upgrade your deployment to 8.19, follow the steps in [Upgrade on Elastic Cloud → Perform the upgrade](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade). *Note: Although this guide refers to {{ecloud}}, the same steps apply to ECE deployments.*

During the upgrade process, all components of your deployment are upgraded in the expected order:
- {{es}}  
- {{kib}}  
- Integrations Server ({{fleet-server}} and APM)  
:::

:::{applies-item} { eck: }

To upgrade your cluster to 8.19, follow the steps in [Upgrade on ECK](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md).

After upgrading {{es}} and {{kib}}, upgrade any [other Elastic applications](/deploy-manage/deploy/cloud-on-k8s/orchestrate-other-elastic-applications.md) connected to the cluster, such as {{fleet-server}} or Elastic APM.
:::

:::{applies-item} self:
To upgrade your cluster to 8.19, follow the steps in [Upgrade self-managed {{stack}}](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack-on-prem.html).

Make sure to upgrade all components in the specified order.
:::

::::

### 8.19 upgrade validation

After completing the upgrade, verify that your system is fully operational. Check that data ingestion and search are working as expected, clients and integrations can connect, and {{kib}} is accessible.

Confirm that the cluster is healthy and reports the expected version.


### Upgrade ingest components to 8.19.x

Because the upgrade to 8.19.x is an intermediate step toward {{version.stack}}, it's mandatory to upgrade all ingest components to 8.19.x before continuing with the next major upgrade.  

Refer to [Upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for more details.  

After upgrading your ingest components, verify that they’re running correctly and sending data to the cluster before proceeding with the next upgrade.

## Upgrade Step 2: 8.19.x → {{version.stack}}

This step covers upgrading your deployment from 8.19.x to {{version.stack}}, assuming that all ingest components have been upgraded to 8.19.x, and client libraries are compatible with 9.x.

### {{version.stack}} upgrade preparations

**(work in progress)**

The [upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md) are designed to prevent upgrade failures by detecting and addressing internal incompatibilities, including deprecated settings that are no longer supported in the next release.

During a major upgrade, the [**Upgrade Assistant**](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) in {{kib}} 8.19 plays a critical role. It scans your cluster for deprecated settings, incompatible indices, and other issues that could prevent nodes from starting after the upgrade. The tool guides you through reindexing old 7.x indices or marking them as read-only, fixing configuration problems, and reviewing deprecation logs to ensure your deployment is fully compatible with the next major version. Ignoring its recommendations can lead to upgrade failures or cluster downtime.

While the **Upgrade Assistant** helps you identify breaking changes that affect your deployment or cluster, it's still recommended to review the complete list of breaking changes and known issues during your preparation phase. These are available in the following documents:
* [{{es}} 9.x breaking changes](elasticsearch://release-notes/breaking-changes.md)
* [Kibana breaking changes summary](kibana://release-notes/breaking-changes.md)

Follow the guidelines below for your specific deployment type:

:::::{applies-switch}

::::{applies-item} ess:

The {{ecloud}} platform facilitates major upgrades by:
* Automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, review the [prepare to upgrade guide](/deploy-manage/upgrade/prepare-to-upgrade.md). You should make sure to:

1. Run the **Upgrade Assistant** in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
    * Reindex or mark as read-only legacy indices and data streams (created before 8.0).
    * Remove or update deprecated settings and mappings.
    * Review deprecation logs for both {{es}} and {{kib}}.

    :::{note}
    If you have old {{ml}}, {{ccr}}, or transform indices that require reindexing, refer to:
    * link1
    * link2
    * link3
    :::

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.  

3. As a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) if your custom client applications are affected by breaking changes. This mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy.

::::

::::{applies-item} ece:

Before upgrading your deployment to 9.x ensure ECE is upgraded to 4.x.

{{ece}} platform facilitates major upgrades by:
* When [snapshots are configured](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, complete the steps described in the [8.19 {{ecloud}} upgrade guide](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html) up to the "Perform the upgrade" section. *Note: Although this guide refers to {{ecloud}}, the same preparation steps apply to ECE deployments.*

You should make sure to:

1. Run the **Upgrade Assistant** in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
   * Reindex legacy indices (created in 7.0).  
   * Remove or update deprecated settings and mappings.  
   * Review deprecation logs for both {{es}} and {{kib}}.  

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.  

3. As a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) if your custom client applications are affected by breaking changes. This mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy.
::::


::::{applies-item} { eck: }

Upgrade preparations for an ECK-managed cluster are similar to a self-managed deployment. Before starting the upgrade follow the steps in [prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md).

If you're upgrading from an {{eck}} version earlier than 3.x, make sure to [upgrade ECK first](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) before performing the final upgrade to 9.x, as ECK 2.x does not support {{stack}} version 9.
::::

::::{applies-item} self:

Before starting the upgrade, follow the [prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md) steps.
::::

:::::

### {{version.stack}} upgrade execution

**(work in progress)**

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
Follow the steps in the [upgrade Elastic on-prem](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack-on-prem.html) guide, ensuring that all components are upgraded in the specified order.

1. Upgrade {{es}} following the rolling upgrade method.
2. Upgrade {{kib}}
:::

::::

### {{version.stack}} upgrade validation

(TBD)

### (Optional) Upgrade ingest components to {{version.stack}}

(TBD)
This step is optional, because all ingest components on 8.19.x are compatible with {{stack}} 9.x.

Refer to [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for more details.


## Post-Upgrade Wrap-Up

(TBD)
- Confirm cluster stability over an observation period  
- Update operational runbooks and monitoring baselines  
- Validate client library upgrades and integrations  
- Decommission old snapshots if no longer needed  
- Document lessons learned  

<!--
(internal list):
upgrade assistant
  * if you are prompted.... refer to xxx ccr / transforms / old ML indices
breaking changes
plugins
snapshot
test
monit first
remote first
close ML jobs
-->