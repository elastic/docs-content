---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/upgrade.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elasticsearch.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrade-deployment.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-upgrade-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-upgrade-deployment.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrade-elastic-stack-for-elastic-cloud.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack-on-prem.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-upgrading-stack.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html
applies_to:
  stack:
products:
  - id: kibana
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: elasticsearch
---

# Upgrade your deployment or cluster [upgrade-deployment-cluster]

This section contains the upgrade instructions for {{es}} clusters and {{kib}} instances. Upgrade procedures depend on whether you installed Elastic components using Elastic-managed or self-managed infrastructure.

## Prerequisites

Before proceeding with the upgrade, review the [Plan your upgrade](/deploy-manage/upgrade/plan-upgrade.md) guidance to understand compatibility and timing considerations, and follow the steps in [Prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md) to get your environment ready for the upgrade.

Additionally, review the [Restrictions and known problems](../deploy/elastic-cloud/restrictions-known-problems.md) to gain a comprehensive understanding of the known issues. 

If you’re still running {{stack}} version 7.17 or earlier, refer to the [Upgrade from 7.17 guide](/deploy-manage/upgrade/deployment-or-cluster/upgrade-717.md) for detailed guidance on planning and executing the upgrade to the latest {{version.stack}} release.

## Out-of-order releases [out-of-order-releases]

Elastic maintains several minor versions of {{es}} at the same time. This means releases do not always happen in order of their version numbers. You can only upgrade to {{version.stack}} if the version you are currently running meets both of these conditions:

* Has a lower version number than {{version.stack}}
* Has an earlier release date than {{version.stack}}

If you are currently running a version with a lower version number but a later release date than {{version.stack}}, wait for a newer release before upgrading.

Additionally, upgrading from a release candidate build, such as 9.0.0-rc1, is unsupported. Use pre-releases only for testing in a temporary environment.

## Upgrade methods

If you’re using Elastic-managed infrastructure, use the following options:

* [Upgrade on {{ech}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md)

If you’re using self-managed infrastructure - either on-prem or public cloud - use the following options:

* [Upgrade the {{stack}} on a self-managed cluster](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md)
* [Upgrade your deployment on {{ece}} (ECE)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md)
* [Upgrade your deployment on {{eck}} (ECK)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)

:::{include} /deploy-manage/_snippets/serverless-upgrade.md
:::

## Next steps

Once you've successfully upgraded your deployment, you can [upgrade your ingest components](./ingest-components.md), such as {{ls}}, {{agent}}, or {{beats}}.