---
navigation_title: Migrate to {{ilm-init}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrate-index-management.html
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-index-management.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
  - id: cloud-enterprise
  - id: cloud-hosted
---

# Migrate to {{ilm-init}} [migrate-ilm]

You may already be another mechanism to manage the lifecycle of your indices. To help you adapt your existing indices to use {{ilm}}, a few guides are available:

[](/manage-data/lifecycle/index-lifecycle-management/migrate-index-management.md) {applies_to}`ess:` {applies_to}`ece:`
:   Describes how to migrate {{es}} indices in an {{ech}} or {{ece}} deployment from using deprecated index curation or another periodic indices management mechanism to use {{ilm}}.

[](/manage-data/lifecycle/index-lifecycle-management/manage-existing-indices.md)  {applies_to}`self:` {applies_to}`eck:`
:   Describes how to migrate {{es}} indices in a self-managed environment from using deprecated index curation, or any other lifecycle mechanism, to use {{ilm}}.

[](/manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md) {applies_to}`stack:`
:   Describes how to migrate from using custom node attributes and attribute-based allocation filters to using built-in node roles, enabling {{ilm-init}} to automatically move indices between data tiers.

If you are configuring {{ilm-init}} for new indices, refer to [](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md). If you plan to manually apply an {{ilm}} policy to existing indices that are not already using another type of lifecycle management, refer to [](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md).