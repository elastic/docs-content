---
applies_to:
  stack: ga
  serverless: unavailable
---
# Upgrade from 7.17 to {{version.stack}}

% add enterprise search related comments?

{{stack}} version 7.17 has a defined end of support date of 15 January 2026, as stated in the [Elastic Product & Version End of Life Policy](https://www.elastic.co/support/eol). This document provides a guided plan to upgrade from 7.17 to the latest {{version.stack}} release. It complements the official upgrade documentation by showing how the different pieces fit together in a complete upgrade exercise.

This guide applies to all deployment types: ({{ech}} (ECH), {{ece}} (ECE), {{eck}} (ECK), and self-managed clusters) running {{es}} version **7.17.x**. If you are using an earlier version, [upgrade first to the latest 7.17 release](https://www.elastic.co/guide/en/elastic-stack/7.17/upgrading-elastic-stack.html) before proceeding.

## Overview

Upgrading from 7.17 to {{version.stack}} requires two major upgrades. Each major upgrade must be prepared and executed independently, although the planning phase can be shared.

1. **7.17.x → 8.19.x**  
    This brings the cluster onto the latest supported 8.x release, which is the required intermediate version before upgrading to {{version.stack}}.
    Before running this upgrade, all ingest components and client libraries must be upgraded to 7.17.x.

2. **8.19.x → {{version.stack}}**  
    This completes the upgrade to the latest 9.x release.
    Before running this upgrade, all ingest components and client libraries must be upgraded to 8.19.x.

:::{note}
Upgrading only to version 8.19.x is also a supported path, as it remains a maintained and fully supported release. However, we recommend completing the upgrade to the latest {{version.stack}} version to take advantage of ongoing improvements and new features.
:::

The following sections describe these phases in detail and point to the relevant documentation for each deployment type.

Refer to [upgrade paths](/deploy-manage/upgrade.md#upgrade-paths) for more information.

::::{dropdown} Alternative method: Reindex to upgrade
For basic use cases that do not rely on {{kib}} dashboards or {{stack}} features such as {{ml}}, transforms, {{kib}} alerting, or detection rules, instead of performing two sequential upgrades (7.17 → 8.19 → {{version.stack}}), you can create a new {{version.stack}} cluster or deployment and migrate your data from the 7.17 cluster by reindexing.

For detailed guidance on how to plan and execute this method, refer to [Reindex to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md#reindex-to-upgrade).

It may be suitable when:
- You prefer to build new infrastructure rather than modify an existing one.  
- You want to reduce the risk of performing two consecutive major upgrades.  
- You plan to redesign your topology or move to a new environment, for example from self-managed to {{ech}} or {{ece}}.  

This approach is intended for {{es}} use cases focused on indexing and querying your own data. If you need to preserve {{kib}} configurations and {{stack}} feature data, follow the standard upgrade path instead.
::::

## Upgrade planning [planning]

The [planning phase](/deploy-manage/upgrade/plan-upgrade.md) ensures that the upgrade is well understood, can be executed with minimal risk, and follows the [correct order](/deploy-manage/upgrade/plan-upgrade.md#upgrade-order).

It involves defining a clear sequence of actions and assessing the impact on [service availability](/deploy-manage/upgrade.md#availability-during-upgrades) and performance during the upgrade.

For the 7.17.x → 9.x upgrade path, the main planning outcome is a set of required actions to ensure compatibility across the environment:

* **Ingest components:**

  Before the initial upgrade to 8.19.x, ensure that all ingest components ({{beats}}, {{agent}}, {{ls}}, APM) are on version 7.17.x. If you are using an earlier version of any of these components, refer to the following docs to upgrade your components before proceeding:

  ::::{dropdown} 7.17 {{stack}} ingest components
  * {{beats}}: [Upgrade instructions](https://www.elastic.co/guide/en/beats/libbeat/7.17/upgrading.html)
  * {{ls}}: [Upgrade instructions](https://www.elastic.co/guide/en/logstash/7.17/upgrading-logstash.html)
  * {{fleet}} managed {{agent}}: [Upgrade instructions](https://www.elastic.co/guide/en/fleet/7.17/upgrade-elastic-agent.html)
  * Standalone {{agent}}: [Upgrade instructions](https://www.elastic.co/guide/en/fleet/7.17/upgrade-standalone.html)
  * Elastic APM: [Upgrade instructions](https://www.elastic.co/guide/en/apm/guide/7.17/upgrade.html)
  ::::

  After upgrading the cluster to 8.19.x and before proceeding to {{version.stack}}, upgrade all ingest components to 8.19.x. This step will be covered later in this guide.
  
* **Client libraries:**

  If you use custom-developed applications that rely on [{{es}} client libraries](/reference/elasticsearch-clients/index.md), make sure to include them in your plan. Typically, libraries are upgraded to match the {{es}} version after each of the major upgrades.

  Applications that use deprecated or removed APIs might require code updates, or you can use the [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) feature to maintain compatibility with the next major version.

  This topic will be revisited in more detail during the preparation steps for each major upgrade.

* **Orchestration platforms:**

  * **ECK**: If you are running an ECK version earlier than 3.x, you need to [upgrade ECK to 3.x](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) before the final upgrade to 9.x. This can be done either at the beginning, before the initial upgrade, or between the two upgrade phases.

  * **ECE**: If you are running an ECE version earlier than 4.x, you need to [upgrade your ECE platform to 4.x](/deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md) before the final upgrade to 9.x. This upgrade must be performed after upgrading your deployments to 8.19.x, because ECE 4.x is not compatible with 7.x deployments.

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

:::::{applies-switch}

::::{applies-item} ess:

The {{ecloud}} platform facilitates major upgrades by doing the following:
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

3. If you use custom-developed applications that are impacted by API-related breaking changes, make the recommended changes to ensure that your applications continue to operate as expected after the upgrade, or, as a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) to submit requests to 8.x using the 7.x syntax.

    :::{note}
    The REST API compatibility mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy. For a high-level description of the steps to ensure a smooth upgrade involving client applications that use this mode, refer to the [REST API compatibility workflow example](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html#_rest_api_compatibility_workflow).
    :::

::::

::::{applies-item} ece:

{{ece}} platform facilitates major upgrades by doing the following:
* When [snapshots are configured](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, complete the steps described in the [8.19 {{ecloud}} upgrade guide](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html) up to the "Perform the upgrade" section. 

:::{note}
Although this guide refers to {{ecloud}}, the same preparation steps apply to ECE deployments.
:::

You should make sure to:

1. Run the **Upgrade Assistant** in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
   * Reindex legacy indices (created before 7.0).  
   * Remove or update deprecated settings and mappings.  
   * Review deprecation logs for both {{es}} and {{kib}}.  

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.  

3. If you use custom-developed applications that are impacted by API-related breaking changes, make the recommended changes to ensure that your applications continue to operate as expected after the upgrade, or, as a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) to submit requests to 8.x using the 7.x syntax.

    :::{note}
    The REST API compatibility mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy. For a high-level description of the steps to ensure a smooth upgrade involving client applications that use this mode, refer to the [REST API compatibility workflow example](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html#_rest_api_compatibility_workflow).
    :::
::::

::::{applies-item} eck:

Upgrade preparations for an {{eck}}-managed cluster are similar to a self-managed deployment. Before starting the upgrade:

* Follow the steps in [Prepare to upgrade from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade).  
* Review the [{{es}} upgrade setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html) for additional details and best practices.  

As part of your preparation, make sure to complete all tasks reported by the **Upgrade Assistant**, review any installed plugins for compatibility, and check whether custom client applications are affected by API-related breaking changes so you can address them before the upgrade.

If you're running an {{eck}} version earlier than 3.x, consider [upgrading ECK](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) at this stage. Although not required for the 7.17 → 8.19 upgrade, ECK 3.x or later is needed before performing the final upgrade to 9.x.
::::

::::{applies-item} self:

Before starting the upgrade, follow the [Prepare to upgrade from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade) steps.

For additional details and best practices, review the [{{es}} upgrade setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html).

As part of your preparation, make sure to complete all tasks reported by the **Upgrade Assistant**, review any installed plugins for compatibility, and check whether custom client applications are affected by API-related breaking changes so you can address them before the upgrade.
::::

:::::

### 8.19 upgrade execution

Keep the following considerations in mind when upgrading your deployment or cluster:

* If you use [Stack monitoring](/deploy-manage/monitor/stack-monitoring.md) with a dedicated monitoring cluster, upgrade your monitoring cluster first.
* If you use [remote cluster](/deploy-manage/remote-clusters.md) functionality, upgrade the remote clusters first.
* Before starting the upgrade, run the same checks and validations you plan to perform afterward, so you have a baseline for comparison. Refer to the [upgrade validation](#819-validation) section for example checks.

The steps below describe how to upgrade the core components of your {{stack}} environment, {{es}}, {{kib}}, and, when applicable, {{fleet-server}} and Elastic APM, for each deployment type.

:::::{applies-switch}

::::{applies-item} ess:

To upgrade your deployment to 8.19, follow the steps in [Upgrade on Elastic Cloud → Perform the upgrade](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade).  

During the upgrade process, all components of your deployment are upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}} and APM)
::::

::::{applies-item} ece:

To upgrade your deployment to 8.19, follow the steps in [Upgrade on Elastic Cloud → Perform the upgrade](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade). 

:::{note}
Although this guide refers to {{ecloud}}, the same steps apply to ECE deployments.
:::

During the upgrade process, all components of your deployment are upgraded in the expected order:
- {{es}}  
- {{kib}}  
- Integrations Server ({{fleet-server}} and APM)  
::::


::::{applies-item} eck:
In ECK, upgrades are performed declaratively by updating the `spec.version` field in the resource manifest. Once the new version is applied, the operator automatically orchestrates the rolling upgrade, ensuring that each component is upgraded safely and in the correct order.

To upgrade your cluster to 8.19, follow the steps in [Upgrade on ECK](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md), and start upgrading the {{es}} and {{kib}} resources that represent the cluster.

:::{note}
For more information on how ECK manages upgrades and how to tune its behavior, refer to [Nodes orchestration](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md).
:::

After upgrading {{es}} and {{kib}}, upgrade any [other Elastic applications](/deploy-manage/deploy/cloud-on-k8s/orchestrate-other-elastic-applications.md) connected to the cluster, such as {{fleet-server}} or Elastic APM.
::::

::::{applies-item} self:
To upgrade your cluster to 8.19, follow the steps in [Upgrade self-managed {{stack}}](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack-on-prem.html).

Make sure to upgrade all components in the specified order.
::::

:::::

### 8.19 upgrade validation [819-validation]

:::{include} _snippets/upgrade-validation.md
:::

### Upgrade ingest components and {{es}} client libraries to 8.19.x

Before upgrading to {{version.stack}}, ensure that all ingest components and {{es}} clients are upgraded to version 8.19.x, as 7.x versions aren’t compatible with {{stack}} 9.x, according to the [Product compatibility support matrix](https://www.elastic.co/support/matrix#matrix_compatibility).

For more details, refer to the documentation for the following products and client libraries:

::::{dropdown} 8.19 {{stack}} ingest components
* {{beats}}: [Upgrade instructions](https://www.elastic.co/guide/en/beats/libbeat/8.19/upgrading.html)
* {{ls}}: [Upgrade instructions](https://www.elastic.co/guide/en/logstash/8.19/upgrading-logstash.html)
* {{fleet}} managed {{agent}}: [Upgrade instructions](https://www.elastic.co/guide/en/fleet/8.19/upgrade-elastic-agent.html)
* Standalone {{agent}}: [Upgrade instructions](https://www.elastic.co/guide/en/fleet/8.19/upgrade-standalone.html)
* Elastic APM: [Upgrade instructions](https://www.elastic.co/guide/en/observability/8.19/apm-upgrade.html)
::::

::::{dropdown} 8.19 {{es}} client libraries
* [Go](https://www.elastic.co/guide/en/elasticsearch/client/go-api/8.19/index.html)
* [Java](https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/8.19/index.html)
* [JavaScript (Node.js)](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/8.19/index.html)
* [.NET](https://www.elastic.co/guide/en/elasticsearch/client/net-api/8.19/index.html)
* [PHP](https://www.elastic.co/guide/en/elasticsearch/client/php-api/8.19/index.html)
* [Python](https://www.elastic.co/guide/en/elasticsearch/client/python-api/8.19/index.html)
* [Ruby](https://www.elastic.co/guide/en/elasticsearch/client/ruby-api/8.19/index.html)
* [Rust](https://www.elastic.co/guide/en/elasticsearch/client/rust-api/8.19/overview.html)
::::

After upgrading your ingest components and client libraries, verify that they’re running correctly and sending data to the cluster before proceeding with the next major upgrade.

:::{note}
At this point, you have a fully operational {{stack}} 8.19.x environment. You can choose to remain on this version, as it’s fully maintained and supported.

However, we recommend upgrading to {{version.stack}} to benefit from the latest features and performance improvements.
:::

## Upgrade Step 2: 8.19.x → {{version.stack}}

This step covers upgrading your deployment from 8.19.x to {{version.stack}}, assuming that all ingest components have been upgraded to 8.19.x, and client libraries are compatible with 9.x.

### {{version.stack}} upgrade preparations

The [upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md) are designed to prevent upgrade failures by detecting and addressing internal incompatibilities, including deprecated settings that are no longer supported in the next release.

During a major upgrade, the [**Upgrade Assistant**](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) in {{kib}} 8.19 plays a critical role. It scans your cluster for deprecated settings, incompatible indices, and other issues that could prevent nodes from starting after the upgrade. The tool guides you through reindexing old 7.x indices or marking them as read-only, fixing configuration problems, and reviewing deprecation logs to ensure your deployment is fully compatible with the next major version. Ignoring its recommendations can lead to upgrade failures or cluster downtime.

While the **Upgrade Assistant** helps you identify breaking changes that affect your deployment or cluster, it's still recommended to review the complete list of breaking changes and known issues during your preparation phase. These are available in the following documents:
* [{{es}} 9.x breaking changes](elasticsearch://release-notes/breaking-changes.md)
* [Kibana breaking changes summary](kibana://release-notes/breaking-changes.md)

Follow the guidelines below for your specific deployment type:

:::::{applies-switch}

::::{applies-item} ess:

The {{ecloud}} platform facilitates major upgrades by doing the following:
* Automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, review the [prepare to upgrade guide](/deploy-manage/upgrade/prepare-to-upgrade.md). You should make sure to:

1. [Run the **Upgrade Assistant**](/deploy-manage/upgrade/prepare-to-upgrade.md#run-the-upgrade-assistant) in {{kib}} and resolve all critical issues before continuing.

    As described in the linked guide, the assistant helps you:
    * Reindex or mark as read-only legacy indices and data streams (created before 8.0).
    * Remove or update deprecated settings and mappings.
    * Review deprecation logs for both {{es}} and {{kib}}.

    :::{note}
    If the **Upgrade Assistant** reports old {{ml}}, {{ccr}}, or transform indices that require action or reindexing, make sure to review the relevant sections in the preparations guide:
    * [Manage CCR follower data streams](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-ccr-follower-data-streams)
    * [Manage old Machine Learning indices](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-old-machine-learning-indices)
    * [Manage old Transform indices](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-old-transform-indices)
    :::

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.

3. As a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) if your custom client applications are affected by breaking changes. This mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy.

If you use custom-developed applications or clients, ensure the [{{es}} client libraries](/reference/elasticsearch-clients/index.md) are compatible with the target version. If your applications use deprecated or removed APIs, then you might need to update the client code first.

    :::{note}
    By default, 8.x {{es}} clients are compatible with 9.x and use [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to maintain compatibility with the 9.x {{es}} cluster.
    REST API compatibility is a per-request opt-in feature that can help REST clients mitigate non-compatible (breaking) changes to the REST API.
    :::


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

:::{include} _snippets/upgrade-validation.md
:::

### (Optional) Upgrade ingest components to {{version.stack}}

This step is optional, as all ingest components running on 8.19.x are fully compatible with {{stack}} 9.x. However, upgrading them to {{version.stack}} ensures version alignment across your environment and allows you to take advantage of the latest features, performance improvements, and fixes.

Refer to [Upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md) for detailed upgrade instructions.

## Next steps

You now have a fully upgraded {{stack}} {{version.stack}} environment. To explore new capabilities, see [What’s new in {{version.stack}}](/release-notes/intro/index.md#whats-new-in-the-latest-elastic-release).