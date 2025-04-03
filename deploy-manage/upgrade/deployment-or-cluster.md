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
  deployment:
    eck:
    ess:
    ece:
    self:
---

# Upgrade your deployment or cluster [upgrade-deployment-cluster]

When upgrading an existing cluster, you perform a minor or major upgrade. For example, a minor upgrade takes you from version 9.0.0 to 9.1.0, while a major upgrade takes you from version 8.0.0 to 9.0.0.

Upgrade procedures depend on whether you installed Elastic components using Elastic-managed or self-managed infrastructure.

If you’re using Elastic-managed infrastructure, use the following options:

* [Upgrade on {{ech}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md)
* Upgrade on [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), which is automatically performed by Elastic and requires no user management

If you’re using self-managed infrastructure - either on-prem or public cloud - use the following options:

* [Upgrade the {{stack}} on a self-managed cluster](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md)
* [Upgrade on {{ece}} (ECE)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md)
* [Upgrade on {{eck}} (ECK)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)
