---
applies_to:
  stack: ga
  serverless: unavailable
---
# Upgrade from 7.17 to {{version.stack}}

{{stack}} version 7.17 has a defined end of support date of 15 January 2026, as stated in the [Elastic Product & Version End of Life Policy](https://www.elastic.co/support/eol). This document provides a guided plan to upgrade from 7.17 to the latest {{version.stack}} release. It complements the official upgrade documentation by showing how the different pieces fit together in a complete upgrade exercise.

This guide applies to all clusters running {{stack}} version **7.17.x** across all deployment types, including {{ech}} (ECH), {{ece}} (ECE), or {{eck}} (ECK) deployments and completely self-managed clusters. If you are using an earlier version, [upgrade first to the latest 7.17 release](https://www.elastic.co/guide/en/elastic-stack/7.17/upgrading-elastic-stack.html) before proceeding.

## Overview

Upgrading from 7.17 to {{version.stack}} requires two major upgrades. Each major upgrade must be prepared and executed independently, although the planning phase can be shared.

1. **7.17.x → 8.19.x**

    This brings the cluster onto the latest supported 8.x release, which is the required intermediate version before upgrading to {{version.stack}}.
    
    Before running this upgrade, all ingest components and client libraries must be upgraded to 7.17.x.

2. **8.19.x → {{version.stack}}**

    This completes the upgrade to the latest 9.x release.
    
    Before running this upgrade, all ingest components and client libraries must be upgraded to 8.19.x.

:::{note}
Upgrading only as far as {{stack}} 8.19.x is also a supported path, as 8.19.x remains a maintained and fully supported release. However, we recommend completing the upgrade to the latest version, {{version.stack}}, to take advantage of ongoing improvements and new features.
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

  If you use custom-developed applications that rely on [{{es}} client libraries](/reference/elasticsearch-clients/index.md), make sure to include them in your plan. Client libraries must be upgraded after each major {{es}} upgrade to ensure support and compatibility.

  Applications that use deprecated or removed APIs might require code updates, or you can use the [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) feature to maintain compatibility with the next major version.

  This topic will be revisited in more detail during the preparation steps for each major upgrade.

* **Orchestration platforms:**

  * **ECK**: If you are running an ECK version earlier than 3.x, you need to [upgrade ECK to 3.x](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) before the final upgrade to 9.x. This can be done either at the beginning, before the initial upgrade, or between the two upgrade phases.

  * **ECE**: If you are running an ECE version earlier than 4.x, you need to [upgrade your ECE platform to 4.x](/deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md) before the final upgrade to 9.x. This upgrade must be performed after upgrading your deployments to 8.19.x, because ECE 4.x is not compatible with 7.x deployments.

Finally, we strongly recommend [testing the full upgrade process in a non-production environment](/deploy-manage/upgrade/plan-upgrade.md#test-in-a-non-production-environment) before applying it to production.

## Upgrade step 1: 7.17.x → 8.19.x

This step covers upgrading your deployment from 7.17.x to 8.19.x, following the [planning phase](#planning) and assuming that all ingest components and client libraries are compatible with 8.19.x.

It's highly recommended to start this upgrade from the latest 7.17.x patch release to ensure that you’re using the most recent version of the Elastic Upgrade Assistant. You should also upgrade to the latest available 8.19.x patch release so that the same benefits apply when you later upgrade to 9.x.

### 8.19 upgrade preparations

The [upgrade preparation steps from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade) are designed to prevent upgrade failures by detecting and addressing internal incompatibilities, including deprecated settings that are no longer supported in the next release.

During a major upgrade, the [Upgrade Assistant](https://www.elastic.co/guide/en/kibana/7.17/upgrade-assistant.html) in {{kib}} 7.17 plays a critical role. It scans your cluster for deprecated settings, incompatible indices, and other issues that could prevent nodes from starting after the upgrade. The tool guides you through reindexing old indices, fixing configuration problems, and reviewing deprecation logs to ensure your deployment is fully compatible with the next major version. Ignoring its recommendations can lead to upgrade failures or cluster downtime.

While the Upgrade Assistant helps you identify breaking changes that affect your deployment or cluster, it's still recommended to review the complete list of breaking changes and known issues in every release from your current version through your target version as part of the preparation phase. These are available in the following documents:
* [{{es}} 8.x migration guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/breaking-changes.html)
* [Kibana breaking changes summary](https://www.elastic.co/guide/en/kibana/8.19/breaking-changes-summary.html)

Follow the guidelines below for your specific deployment type:

:::::{applies-switch}

::::{applies-item} ess:

The {{ecloud}} platform facilitates major upgrades by doing the following:
* Automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, complete the steps described in the [8.19 {{ecloud}} upgrade guide](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html) up to the "Perform the upgrade" section.

You should make sure to:

1. Run the Upgrade Assistant in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
   * Reindex legacy indices (created before 7.0).
   * Remove or update deprecated settings and mappings.
   * Review deprecation logs for both {{es}} and {{kib}}.

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they're compatible with the next major release.

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

1. Run the Upgrade Assistant in {{kib}} and resolve all critical issues before continuing. The assistant helps you:
   * Reindex legacy indices (created before 7.0).
   * Remove or update deprecated settings and mappings.
   * Review deprecation logs for both {{es}} and {{kib}}.

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they're compatible with the next major release.

3. If you use custom-developed applications that are impacted by API-related breaking changes, make the recommended changes to ensure that your applications continue to operate as expected after the upgrade, or, as a temporary solution, you can use [REST API compatibility mode](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html) to submit requests to 8.x using the 7.x syntax.

    :::{note}
    The REST API compatibility mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy. For a high-level description of the steps to ensure a smooth upgrade involving client applications that use this mode, refer to the [REST API compatibility workflow example](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/rest-api-compatibility.html#_rest_api_compatibility_workflow).
    :::
::::

::::{applies-item} eck:

Upgrade preparations for an {{eck}}-managed cluster are similar to a self-managed deployment. Before starting the upgrade:

* Follow the steps in [Prepare to upgrade from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade).
* Review the [{{es}} upgrade setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html) for additional details and best practices.

As part of your preparation, make sure to complete all tasks reported by the Upgrade Assistant, review any installed plugins for compatibility, and check whether custom client applications are affected by API-related breaking changes so you can address them before the upgrade.

If you're running an {{eck}} version earlier than 3.x, consider [upgrading ECK](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) at this stage. Although this is not required for the 7.17 → 8.19 upgrade, ECK 3.x or later is needed before performing the final upgrade to 9.x.
::::

::::{applies-item} self:

Before starting the upgrade, follow the [Prepare to upgrade from 7.x](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrading-elastic-stack.html#prepare-to-upgrade) steps.

For additional details and best practices, review the [{{es}} upgrade setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/setup-upgrade.html).

As part of your preparation, make sure to complete all tasks reported by the Upgrade Assistant, review any installed plugins for compatibility, and check whether custom client applications are affected by API-related breaking changes so you can address them before the upgrade.
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
- Integrations Server ({{fleet-server}}, Elastic APM), if present
- Enterprise Search, if present
::::

::::{applies-item} ece:

To upgrade your deployment to 8.19, follow the steps in [Upgrade on Elastic Cloud → Perform the upgrade](https://www.elastic.co/guide/en/elastic-stack/8.19/upgrade-elastic-stack-for-elastic-cloud.html#perform-cloud-upgrade). 

:::{note}
Although this guide refers to {{ecloud}}, the same steps apply to ECE deployments.
:::

During the upgrade process, all components of your deployment are upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}}, Elastic APM), if present
- Enterprise Search, if present
::::


::::{applies-item} eck:
In ECK, upgrades are performed declaratively by updating the `spec.version` field in your resource manifests, or by setting the equivalent version values when deploying through Helm charts. Once the new version is applied, the operator orchestrates a rolling upgrade, ensuring components are upgraded safely and in the correct order.

To upgrade your cluster to 8.19, follow the steps in [Upgrade on ECK](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md), and start by upgrading the {{es}} and {{kib}} resources that represent the cluster. Set the `version` field to the latest 8.19.x release number in each manifest or Helm chart values file.

:::{note}
For more information on how ECK manages upgrades and how to tune its behavior, refer to [Nodes orchestration](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md).
:::

After upgrading {{es}} and {{kib}}, upgrade any [other Elastic applications](/deploy-manage/deploy/cloud-on-k8s/orchestrate-other-elastic-applications.md) connected to the cluster, such as {{fleet-server}} or Elastic APM, using the same version value.
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

For more details, refer to the documentation of the following products and client libraries:

::::{dropdown} 8.19 {{stack}} ingest components
* {{beats}}: [Upgrade instructions](https://www.elastic.co/guide/en/beats/libbeat/8.19/upgrading.html)
* {{ls}}: [Upgrade instructions](https://www.elastic.co/guide/en/logstash/8.19/upgrading-logstash.html)
* {{fleet}} managed {{agent}}: [Upgrade instructions](https://www.elastic.co/guide/en/fleet/8.19/upgrade-elastic-agent.html)
* Standalone {{agent}}: [Upgrade instructions](https://www.elastic.co/guide/en/fleet/8.19/upgrade-standalone.html)
* Elastic APM: [Upgrade instructions](https://www.elastic.co/guide/en/observability/8.19/apm-upgrade.html).
* Enterprise Search: [Upgrade and migration guides](https://www.elastic.co/guide/en/enterprise-search/8.19/upgrading-and-migrating.html)

:::{note}
The Elastic APM Server and Enterprise Search components require manual upgrade only in ECK-managed or self-managed environments. In {{ech}} and {{ece}}, these components are upgraded automatically as part of the deployment upgrade process.
:::

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

## Upgrade step 2: 8.19.x → {{version.stack}}

This step covers upgrading your deployment from 8.19.x to {{version.stack}}, assuming that all ingest components have been upgraded to 8.19.x, and client libraries are compatible with 9.x.

It's highly recommended to start this upgrade from the latest 8.19.x patch release to ensure that you’re using the most recent version of the Upgrade Assistant.

:::::{admonition} Important note for Enterprise Search users
In {{stack}} 9.0.0 and later, Enterprise Search is no longer available.
* You must remove any Enterprise Search nodes from your deployment before proceeding with the upgrade.
* If you are currently using App Search, Workplace Search, or the Elastic Web Crawler, these features will cease to function if you remove Enterprise Search from your deployment. Therefore, it is critical to first  [migrate your Enterprise Search use cases](https://www.elastic.co/guide/en/enterprise-search/8.19/upgrading-to-9-x.html) before decommissioning your Enterprise Search instances.
:::::

### {{version.stack}} upgrade preparations

The [upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md) are designed to prevent upgrade failures by detecting and addressing internal incompatibilities, including deprecated settings that are no longer supported in the next release.

During a major upgrade, the [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) in {{kib}} 8.19 plays a critical role. It scans your cluster for deprecated settings, incompatible indices, and other issues that could prevent nodes from starting after the upgrade. The tool guides you through reindexing old 7.x indices or marking them as read-only, fixing configuration problems, and reviewing deprecation logs to ensure your deployment is fully compatible with the next major version. Ignoring its recommendations can lead to upgrade failures or cluster downtime.

While the Upgrade Assistant helps you identify breaking changes that affect your deployment or cluster, it's still recommended to review the complete list of breaking changes and known issues in every release from your current version through your target version as part of the preparation phase. These are available in the following documents:
* [{{es}} 9.x breaking changes](elasticsearch://release-notes/breaking-changes.md)
* [Kibana breaking changes summary](kibana://release-notes/breaking-changes.md)

Follow the guidelines below for your specific deployment type:

:::::{applies-switch}

::::{applies-item} ess:

The {{ecloud}} platform facilitates major upgrades by doing the following:
* Automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, review the [Prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md) guide. You should make sure to:

1. [Run the Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade.md#run-the-upgrade-assistant) in {{kib}} and resolve all critical issues before continuing.

    As described in the linked guide, the assistant helps you:
    * Reindex or mark as read-only legacy indices and data streams (created before 8.0).
    * Remove or update deprecated settings and mappings.
    * Review deprecation logs for both {{es}} and {{kib}}.
    * Remove Enterprise Search if it's part of the deployment.

    :::{note}
    If the Upgrade Assistant reports old {{ml}}, {{ccr}}, or transform indices that require action or reindexing, make sure to review the relevant sections in the preparations guide:
    * [Manage CCR follower data streams](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-ccr-follower-data-streams)
    * [Manage old Machine Learning indices](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-old-machine-learning-indices)
    * [Manage old Transform indices](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-old-transform-indices)
    :::

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they’re compatible with the next major release.

3. If you use custom-developed applications that are impacted by API-related breaking changes, make the recommended changes to ensure that your applications continue to operate as expected after the upgrade, or, as a temporary solution, you can use [REST API compatibility mode](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to submit requests to 9.x using the 8.x syntax.

    :::{note}
    The REST API compatibility mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy. For a high-level description of the steps to ensure a smooth upgrade involving client applications that use this mode, refer to the [REST API compatibility workflow example](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md#_rest_api_compatibility_workflow).
    :::
::::

::::{applies-item} ece:

:::{important}
If you're running an {{ece}} version earlier than 4.x, ensure that you [upgrade ECE first](/deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md). ECE 3.x is not compatible with {{stack}} version 9.
:::

{{ece}} platform facilitates major upgrades by:
* When [snapshots are configured](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), automatically creating a snapshot before the upgrade.
* Detecting deprecated settings and index compatibility issues.
* Blocking the upgrade until all issues are resolved through the Upgrade Assistant, ensuring a reliable outcome.

To prepare your deployment for the upgrade, review the [Prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md) guide. You should make sure to:
1. [Run the Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade.md#run-the-upgrade-assistant) in {{kib}} and resolve all critical issues before continuing.

    As described in the linked guide, the assistant helps you:
    * Reindex or mark as read-only legacy indices and data streams (created before 8.0).
    * Remove or update deprecated settings and mappings.
    * Review deprecation logs for both {{es}} and {{kib}}.
    * Remove Enterprise Search if it's part of the deployment.

    :::{note}
    If the Upgrade Assistant reports old {{ml}}, {{ccr}}, or transform indices that require action or reindexing, make sure to review the relevant sections in the preparations guide:
    * [Manage CCR follower data streams](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-ccr-follower-data-streams)
    * [Manage old Machine Learning indices](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-old-machine-learning-indices)
    * [Manage old Transform indices](/deploy-manage/upgrade/prepare-to-upgrade.md#manage-old-transform-indices)
    :::

2. If you use [custom plugins or bundles](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), make sure they're compatible with the next major release.

3. If you use custom-developed applications that are impacted by API-related breaking changes, make the recommended changes to ensure that your applications continue to operate as expected after the upgrade, or, as a temporary solution, you can use [REST API compatibility mode](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to submit requests to 9.x using the 8.x syntax.

    :::{note}
    The REST API compatibility mode should only serve as a bridge to ease the upgrade process, not as a long-term strategy. For a high-level description of the steps to ensure a smooth upgrade involving client applications that use this mode, refer to the [REST API compatibility workflow example](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md#_rest_api_compatibility_workflow).
    :::
::::


::::{applies-item} eck:

:::{important}
If you're running an {{eck}} version earlier than 3.x, ensure that you [upgrade ECK first](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md). ECK 2.x is not compatible with {{stack}} version 9.
:::

Upgrade preparations for an ECK-managed cluster are similar to a self-managed deployment.

Before starting the upgrade, follow the steps in [Prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md).

As part of your preparation, make sure to complete all tasks reported by the Upgrade Assistant, review any installed plugins for compatibility, and check whether custom client applications are affected by API-related breaking changes so you can address them before the upgrade.
::::

::::{applies-item} self:

Before starting the upgrade, follow the steps in [Prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md).

As part of your preparation, make sure to complete all tasks reported by the Upgrade Assistant, review any installed plugins for compatibility, and check whether custom client applications are affected by API-related breaking changes so you can address them before the upgrade.
::::

:::::

### {{version.stack}} upgrade execution

As with the previous major upgrade, keep the following considerations in mind when upgrading your deployment or cluster:

* If you use [Stack monitoring](/deploy-manage/monitor/stack-monitoring.md) with a dedicated monitoring cluster, upgrade your monitoring cluster first.
* If you use [remote cluster](/deploy-manage/remote-clusters.md) functionality, upgrade the remote clusters first.
* Before starting the upgrade, run the same checks and validations you plan to perform afterward, so you have a baseline for comparison. Refer to the [upgrade validation](#819-validation) section for example checks.

The steps below describe how to upgrade the core components of your {{stack}} environment, {{es}}, {{kib}}, and, when applicable, {{fleet-server}} and Elastic APM, for each deployment type.

:::::{applies-switch}

::::{applies-item} ess:

To upgrade your deployment to {{version.stack}}, follow the steps in [Upgrade your deployment on ECH](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md).

During the upgrade process all of your deployment components will be upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}}, Elastic APM), if present
::::

::::{applies-item} ece:
To upgrade your deployment to {{version.stack}}, follow the steps in [Upgrade your deployment on ECE](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md#perform-the-upgrade).

If the [{{stack}} pack](/deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md) for this version isn’t already added to the platform, make sure to add it before starting the upgrade.

During the upgrade process all of your deployment components will be upgraded in the expected order:
- {{es}}
- {{kib}}
- Integrations Server ({{fleet-server}}, Elastic APM), if present
::::


::::{applies-item} eck:
In ECK, upgrades are performed declaratively by updating the `spec.version` field in your resource manifests, or by setting the equivalent version values when deploying through Helm charts. Once the new version is applied, the operator orchestrates a rolling upgrade, ensuring components are upgraded safely and in the correct order.

To upgrade your cluster to {{version.stack}}, follow the steps in [Upgrade on ECK](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md), and start by upgrading the {{es}} and {{kib}} resources that represent the cluster. Set the version field to {{version.stack}} in each manifest or Helm chart values file.

:::{note}
For more information on how ECK manages upgrades and how to tune its behavior, refer to [Nodes orchestration](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md).
:::

After upgrading {{es}} and {{kib}}, upgrade any [other Elastic applications](/deploy-manage/deploy/cloud-on-k8s/orchestrate-other-elastic-applications.md) connected to the cluster, such as {{fleet-server}} or Elastic APM, using the same version value.
::::

::::{applies-item} self:

To upgrade your cluster to {{version.stack}}, follow the steps in [Upgrade a self-managed cluster](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md).

Make sure to upgrade all components in the specified order:
1. [Upgrade {{es}}](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md) following the rolling upgrade method.
2. [Upgrade {{kib}}](/deploy-manage/upgrade/deployment-or-cluster/kibana.md)
::::

:::::

### {{version.stack}} upgrade validation

:::{include} _snippets/upgrade-validation.md
:::

### Upgrade ingest components and {{es}} client libraries to {{version.stack}}

After upgrading your deployment or cluster to {{version.stack}}, review your ingest components and client libraries to ensure full compatibility across the environment.

All custom-developed applications that rely on [{{es}} client libraries](/reference/elasticsearch-clients/index.md) must be upgraded to the latest {{version.stack}} client version to guarantee full API compatibility and support for new features.

For ingest components, version 8.19.x remains fully compatible with the entire 9.x series. You can keep running them on 8.19.x if you prefer a gradual rollout. However, we recommend upgrading to {{version.stack}} to take advantage of ongoing improvements and new features.

For more details, refer to the documentation of the following products and client libraries:

::::{dropdown} {{version.stack}} {{stack}} ingest components
* {{beats}}: [Upgrade instructions](beats://reference/libbeat/upgrading.md)
* {{ls}}: [Upgrade instructions](logstash://reference/upgrading-logstash.md)
* {{fleet}} managed {{agent}}: [Upgrade instructions](/reference/fleet/upgrade-elastic-agent.md)
* Standalone {{agent}}: [Upgrade instructions](/reference/fleet/upgrade-standalone.md)
* Elastic APM: [Upgrade instructions](/solutions/observability/apm/upgrade.md)
::::

::::{dropdown} {{version.stack}} {{es}} client libraries
* [Go](go-elasticsearch://reference/index.md)
* [Java](elasticsearch-java://reference/index.md)
* [JavaScript (Node.js)](elasticsearch-js://reference/index.md)
* [.NET](elasticsearch-net://reference/index.md)
* [PHP](elasticsearch-php://reference/index.md)
* [Python](elasticsearch-py://reference/index.md)
* [Eland](eland://reference/index.md)
* [Ruby](elasticsearch-ruby://reference/index.md)
* [Rust](elasticsearch-rs://reference/index.md)
::::

After completing the upgrades, verify that all ingest components and client applications can connect and send data to the deployment without issues.

## Next steps

You now have a fully upgraded {{stack}} {{version.stack}} environment. To explore new capabilities, see [What’s new in {{version.stack}}](/release-notes/intro/index.md#whats-new-in-the-latest-elastic-release).