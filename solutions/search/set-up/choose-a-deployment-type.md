---
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: serverless-vector-database
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
navigation_title: Choose a deployment type
description: Compare Elasticsearch deployment types for search, including billing, Kibana tools, custom machine learning models, and index lifecycle management.
type: overview
---

# Choose a deployment type [choose-a-deployment-type]

{{es}} runs on several deployment types, and each type fits different operational needs. This page covers the deployment types for search. The type you select sets who operates the cluster, how usage is billed, and which {{kib}} search tools you can use.

For most search workloads, we recommend an [{{es}} {{vectordb}} project](/solutions/vector-database.md). You get vector-tuned defaults, {{infer}} for embeddings, and billing based on storage and reserved search capacity.

If you need custom models on {{ml}} nodes, time series or logs index modes, or {{kib}} tools such as the Query Rules UI, use an [{{es}} project](/solutions/elasticsearch-solution-project.md) on {{serverless-full}}, or select [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) or a [self-managed deployment](/deploy-manage/deploy/self-managed.md).

## Compare deployment options [compare-search-deployments]

The following table helps you select a deployment type for a search workload.

| Capability | [{{serverless-short}}: {{es}} {{vectordb}} project](/solutions/vector-database.md) | [{{serverless-short}}: {{es}} project](/solutions/elasticsearch-solution-project.md) | [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) | [Self-managed](/deploy-manage/deploy/self-managed.md) |
| --- | --- | --- | --- | --- |
| Who manages the cluster | Elastic | Elastic | Elastic hosts it. You size it and control upgrades. | You install, scale, and upgrade it. |
| [Vector-tuned defaults](/solutions/vector-database.md) | Automatic | You configure them | You configure them | You configure them |
| [Synonyms UI](/solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms-kibana) | No | Yes | Yes | Yes |
| [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md) | No | Yes | Yes | Yes |
| [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) {applies_to}`stack: ga 9.3+` | Yes | Yes | Yes | Yes |
| Custom models on {{ml}} nodes | No | Yes | Yes | Yes |
| {{ilm-cap}} | No | No | Yes | Yes |
| Learn more | [](/solutions/vector-database/get-started.md) | [](/solutions/elasticsearch-solution-project/get-started.md) | [](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) | [](/deploy-manage/deploy/self-managed.md), [](/deploy-manage/deploy/cloud-on-k8s.md), or [](/deploy-manage/deploy/cloud-enterprise.md) |


## Next step [choose-a-deployment-type-next]

After you select a deployment type, get an endpoint and an API key in [](/solutions/search/set-up/api-key-and-endpoints.md).
