---
mapped_urls:
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
---


% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/kibana/kibana/upgrade.md
% - [ ] ./raw-migrated-files/kibana/kibana/upgrade-migrations-rolling-back.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-elasticsearch.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-kibana.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-upgrade-deployment.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-upgrade-deployment.md
%      Notes: redirect only
% - [ ] ./raw-migrated-files/cloud/cloud/ec-upgrade-deployment.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrade-elastic-stack-for-elastic-cloud.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack-on-prem.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-upgrading-stack.md
%      Notes: upgrade explanations

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$preventing-migration-failures$$$

$$$prepare-to-upgrade$$$

$$$k8s-nodesets$$$

$$$k8s-orchestration-limitations$$$

$$$k8s-statefulsets$$$

$$$k8s-upgrade-patterns$$$

$$$k8s-upgrading$$$

$$$prepare-to-upgrade-8x$$$

$$$rolling-upgrades$$$

$$$upgrading-reindex$$$

% * [/raw-migrated-files/kibana/kibana/upgrade.md](/raw-migrated-files/kibana/kibana/upgrade.md)
% * [/raw-migrated-files/kibana/kibana/upgrade-migrations-rolling-back.md](/raw-migrated-files/kibana/kibana/upgrade-migrations-rolling-back.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-elasticsearch.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-elasticsearch.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-kibana.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-kibana.md)
% * [/raw-migrated-files/cloud/cloud-enterprise/ece-upgrade-deployment.md](/raw-migrated-files/cloud/cloud-enterprise/ece-upgrade-deployment.md)
% * [/raw-migrated-files/cloud/cloud-heroku/ech-upgrade-deployment.md](/raw-migrated-files/cloud/cloud-heroku/ech-upgrade-deployment.md)
% * [/raw-migrated-files/cloud/cloud/ec-upgrade-deployment.md](/raw-migrated-files/cloud/cloud/ec-upgrade-deployment.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrade-elastic-stack-for-elastic-cloud.md](/raw-migrated-files/stack-docs/elastic-stack/upgrade-elastic-stack-for-elastic-cloud.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack-on-prem.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack-on-prem.md)
% * [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-upgrading-stack.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-upgrading-stack.md)
% * [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-orchestration.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-orchestration.md)

# Upgrade your deployment or cluster [upgrade-deployment-cluster]

When upgrading an existing cluster, you perform a minor or major upgrade. For example, a minor upgrade takes you from version 9.0.0 to 9.1.0, while a major upgrade takes you from version 8.0.0 to 9.0.0.

Upgrade procedures depend on whether you installed Elastic components using Elastic-managed or self-managed infrastructure.

If you’re using Elastic-managed infrastructure, use the following options:

* [Upgrade on {{ech}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md)
* Upgrade on [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), which is automatically performed by Elastic and requires no user management

If you’re using self-managed infrastructure - either on-prem or public cloud - use the following options:

* [Upgrade the {{stack}}](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md)
* [Upgrade on {{ece}} (ECE)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md)
* [Upgrade on {{eck}} (ECK)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)
