---
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
---

# Upgrade

Upgrading to the latest version provides access to the newest Elastic features, security patches, performance improvements, and bug fixes. These updates reduce costs, speed up threat response, and improve investigative and analytical data tools.

When Elastic releases new versions, older versions reach their end of life on a set schedule. To keep your deployment supported, stay up to date. For more information, refer to [Product End of Life Dates](https://www.elastic.co/support/eol).

::::{note}
With [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), upgrades are fully managed by Elastic. Users automatically receive the latest features and improvements, with no need to plan or perform upgrade steps.
::::

The upgrade procedure depends on how your deployment is managed. If you're using {{ech}} or {{ece}}, upgrades can often be performed with a single click in the {{ecloud}} UI. For self-managed deployments, upgrades must be carried out manually using a rolling upgrade process, upgrading the nodes one by one to minimize downtime and ensure cluster stability.

This section provides guidance to help you plan and safely perform upgrades of your Elastic Stack components, with a primary focus on {{es}} and {{kib}} as the core of the stack. It also covers upgrades for orchestration platforms like {{ece}} and {{eck}}, as well as related components such as APM, Beats, Elastic Agent, and Logstash.

:::{important}
In {{stack}} 9.0.0 and beyond, Enterprise Search is unavailable. For more information, refer to [Migrating to 9.x from Enterprise Search 8.x versions](https://www.elastic.co/guide/en/enterprise-search/8.18/upgrading-to-9-x.html).
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

- [Upgrade ingest components](./upgrade/ingest-components.md): Covers supporting components such as Beats, Elastic Agent, Logstash, and APM Server.

Additionally, if you're using a self-managed orchestration platform such as {{ece}} or {{eck}}, refer to [Upgrade your ECE or ECK orchestrator](/deploy-manage/upgrade/orchestrator.md) to keep the orchestrator up to date.

## Upgrade paths [upgrade-paths]
% alternative title : Upgrade paths / Can I upgrade to any version?

You can upgrade to a higher version if the target version was released *after* your current version. Upgrades to versions released *before* your current version are not supported, even if the version number is higher. Refer to [out-of-order releases](/deploy-manage/upgrade/deployment-or-cluster.md#out-of-order-releases) for more information.

For example:  
- ✅ Upgrade allowed: From 9.0.2 to 9.1.0 (9.1.0 released *after* 9.0.2)
- ❌ Not allowed: From 9.0.4 to 9.1.0 (9.1.0 released *before* 9.0.4)

Refer to the [download past releases](https://www.elastic.co/downloads/past-releases#elasticsearch) page to check the release dates of different versions.

::::{note}
Major upgrades must be performed from the latest minor version of the previous major. For example, to upgrade to {{stack-version}}, you need to be on 8.19 first.
::::