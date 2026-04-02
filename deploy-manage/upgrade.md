---
applies_to:
  deployment:
    eck: ga
    ess: ga
    ece: ga
    self: ga
products:
  - id: kibana
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: elasticsearch
navigation_title: Upgrade
---

# Upgrade your deployment, cluster, or orchestrator

Upgrading to the latest version provides access to the newest Elastic features, security patches, performance improvements, and bug fixes. These updates reduce costs, speed up threat response, and improve investigative and analytical data tools.

As Elastic releases new versions, older versions of Elastic products reach their end of life on a set schedule. To keep your deployment supported, stay up to date. For more information, refer to [Product End of Life Dates](https://www.elastic.co/support/eol).

:::{include} /deploy-manage/_snippets/serverless-upgrade.md
:::

The upgrade procedure depends on how your deployment is managed. If you're using {{ech}} or {{ece}}, upgrades can often be performed with a single click in the {{ecloud}} UI. For self-managed deployments, upgrades must be carried out manually using a rolling upgrade process, upgrading the nodes one by one to minimize downtime and ensure cluster stability.

This section provides guidance to help you plan and safely perform upgrades of your {{stack}} components, with a primary focus on {{es}} and {{kib}} as the core of the stack. It also covers upgrades for orchestration platforms like {{ece}} and {{eck}}, as well as related components such as APM, {{beats}}, {{agent}}, and {{ls}}.

:::{important}
In {{stack}} 9.0.0 and beyond, Enterprise Search is unavailable. For more information, refer to [Migrating to 9.x from Enterprise Search 8.x versions](https://www.elastic.co/guide/en/enterprise-search/8.19/upgrading-to-9-x.html).
:::

## Upgrade overview

Upgrading your Elastic cluster or deployment involves several stages, including planning, preparation, and execution. This section guides you through the full upgrade process:

- [Plan your upgrade](./upgrade/plan-upgrade.md): Review compatibility, define your upgrade path and order, and understand important pre-upgrade considerations.

- [Prepare to upgrade](./upgrade/prepare-to-upgrade.md): Follow detailed preparation steps for major, minor, and patch upgrades. Identify breaking changes, run the Upgrade Assistant (for major upgrades), and verify readiness.

- [Upgrade your deployment or cluster](./upgrade/deployment-or-cluster.md): Step-by-step instructions for performing the upgrade, organized by deployment type:

    - [Upgrade deployments on {{ech}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md)
    - [Upgrade deployments on {{ece}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md)
    - [Upgrade deployments on {{eck}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)
    - [Upgrade self-managed clusters](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md)

- [Upgrade ingest components](./upgrade/ingest-components.md): Covers supporting components such as {{beats}}, {{agent}}, {{ls}}, and APM Server.

:::{note}
If you’re still running {{stack}} version 7.17 or earlier, refer to the [Upgrade from 7.17 guide](/deploy-manage/upgrade/deployment-or-cluster/upgrade-717.md) for detailed guidance on planning and executing the upgrade to the latest {{version.stack}} release.
:::

Additionally, if you're using a self-managed orchestration platform such as {{ece}} or {{eck}}, refer to [Upgrade your ECE or ECK orchestrator](/deploy-manage/upgrade/orchestrator.md) to keep the orchestrator up to date.

## Availability during upgrades

{{es}} supports rolling upgrades, where nodes are upgraded one at a time to minimize downtime and ensure cluster stability. If your deployment or cluster follows high availability best practices, such as using replicated indices and distributing nodes across multiple availability zones, it should remain available throughout the entire upgrade process.

{{kib}} upgrades, however, require downtime. All running instances must be shut down before starting the upgrade.

::::{important}
Ensure your deployment is properly sized and configured for high availability to reduce the risk of service interruption during upgrades.

If you want to learn more about scaling, high availability, and performance, refer to:
* [Run {{es}} in production](/deploy-manage/production-guidance/elasticsearch-in-production-environments.md)
* [Run {{kib}} in production](/deploy-manage/production-guidance/kibana-in-production-environments.md)
* [{{ech}} > Plan for production](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md)
::::

You’ll find more information about availability considerations for specific deployment types in the related upgrade guides within this section.

## Upgrade paths [upgrade-paths]

You can upgrade to a higher version if the target version was released *after* your current version. Upgrades to versions released *before* your current version are not supported, even if the version number is higher. Refer to [out-of-order releases](/deploy-manage/upgrade/deployment-or-cluster.md#out-of-order-releases) for more information.

For example:  
- ✅ Upgrade allowed: From 9.0.4 to 9.1.0 (9.1.0 released *after* 9.0.4)
- ❌ Not allowed: From 9.0.5 to 9.1.0 (9.1.0 released *before* 9.0.5) → wait for 9.1.1 to be released
<!--
Uncomment this example when 9.1.1 is released.
- ✅ Upgrade allowed: From 9.0.5 to 9.1.1 (9.1.1 released *after* 9.0.5)
-->

### Upgrade paths from 8.x [upgrade-paths-8.x]

To perform a major upgrade from 8.x, the required starting version depends on the target release:

- To upgrade to the **9.0.x series**, you must be on **8.18.x**.
- To upgrade to **9.1.0 or later**, you must be on **8.19.x**, which is the latest minor release of the 8.x series.

::::{note}
While 8.19 is the final minor release in the 8.x series, 8.18 was released at the same time as 9.0, enabling a supported upgrade path between the 8.18.x and 9.0.x series. This compatibility also applies to other features and clients.
::::

If you're upgrading to the current {{version.stack}} release from an earlier 8.x version, first upgrade to the latest available 8.19 release.

#### Ingest tools and clients considerations

For flexible upgrade scheduling, 8.19 {{agent}}, {{beats}}, and {{ls}} are compatible with all 9.x versions of {{es}}.

By default, 8.x {{es}} clients are compatible with 9.x and use [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to maintain compatibility with the 9.x cluster.

### Upgrade paths from 7.17 [upgrade-paths-7.x]

Upgrading from {{stack}} version 7.17 to the latest {{version.stack}} release involves two major upgrades:

- From 7.17 to 8.19
- From 8.19 to {{version.stack}}

For detailed guidance on planning and executing these upgrades, refer to the [Upgrade from 7.17 guide](/deploy-manage/upgrade/deployment-or-cluster/upgrade-717.md).
