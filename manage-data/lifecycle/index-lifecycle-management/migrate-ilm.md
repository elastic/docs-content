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

You may already be using index curation, which is now deprecated, or another mechanism to manage the lifecycle of your indices. To help you adapt your existing indices from using earlier lifecycle mechanisms to use {{ilm}}, a few guides are available:

[](/manage-data/lifecycle/index-lifecycle-management/migrate-index-management.md)
:   Describes how to migrate {{es}} indices in an {{ech}} or {{ece}} deployment from using deprecated index curation to use {{ilm}}.

[](/manage-data/lifecycle/index-lifecycle-management/manage-existing-indices.md)
:   Describes how to migrate {{es}} indices in any {{stack}} environment from using deprecated index curation, or any other lifecycle mechanism, to use {{ilm}}.

[](/manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md)
:   Describes how to migrate from using custom node attributes and attribute-based allocation filters to move indices through data tiers in a hot-warm-cold architecture, to use {{ilm}}.

If you are configuring {{ilm-init}} for new indices, refer to [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md). If you plan to manually apply an {{ilm}} policy to existing indices that are not already using another type of lifecycle management, refer to [Manually apply a lifecycle policy to an index](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md).