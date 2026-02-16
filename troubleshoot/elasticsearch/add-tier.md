---
navigation_title: Preferred data tier
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/add-tier.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw move this page to a new index allocation subsection
% or just move it down in the ToC
% and this page really really needs rewriting

# Add a preferred data tier to a deployment [add-tier]

In an {{es}} deployment, an index and its shards can be allocated to [data tiers](../../manage-data/lifecycle/data-tiers.md) using routing and allocation settings. 

Different data tiers are optimized for specific workloads. For example, the hot tier is optimized for frequent writes and queries, while the warm tier for less frequent access. Adding a preferred tier ensures that data is stored on nodes with the appropriate hardware and performance characteristics.

When indices have specific tier preferences, shards may remain unallocated if there are no nodes available in the preferred tier. Adding a preferred data tier ensures that the shards can be allocated to the appropriate nodes.

To allow indices to be allocated, follow these steps:

1. [Determine which tiers](#determine-target-tier) an index's shards can be allocated to.
1. [Resize your deployment](#resize-your-deployment) to add resources to the required tier.


## Determine the target tier [determine-target-tier]

You can run the following step using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [Elasticsearch API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

:::{include} /troubleshoot/elasticsearch/_snippets/determine-data-tier-that-needs-capacity.md
:::

## Resize your deployment [resize-your-deployment]

:::{include} /troubleshoot/elasticsearch/_snippets/resize-your-deployment.md
:::