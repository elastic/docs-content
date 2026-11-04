---
navigation_title: "{{vectordb}} projects"
applies_to:
  vectordb: ga
products:
  - id: cloud-serverless
  - id: serverless-vector-database
description: >-
  Learn how costs for Elasticsearch Vector Database Serverless projects
  are calculated across storage, search, ingest, and infrastructure.
sub:
  abb-anchor: vector-database-billing-agent-builder-executions
  abb-preamble: |
    Elastic Agent Builder enables you to create AI agents that assist with data exploration, analysis, and automated tasks within your {{es}} {{vectordb}} project. Agent usage is billed in addition to the other billing dimensions of your project, based on the number of executions completed in your project over the course of a month.
  abb-free-executions: 1,000
  abb-pricing-label: "{{es}} {{vectordb}} pricing page"
  abb-pricing-url: https://cloud.elastic.co/pricing/serverless?s=vectordb
  wfe-anchor: vector-database-billing-workflow-executions
  wfe-preamble: Workflows enable you to automate multi-step processes within your {{es}} {{vectordb}} project.
  wfe-billing-detail: In addition to the other billing dimensions above, workflow usage is billed based on the number of executions completed successfully in your project over the course of a month. Each execution represents one end-to-end run of a workflow. Failed executions are not billed.
  wfe-free-executions: 10,000
  wfe-pricing-label: "{{es}} {{vectordb}} pricing page"
  wfe-pricing-url: https://cloud.elastic.co/pricing/serverless?s=vectordb
---

# {{es}} {{vectordb}} billing dimensions [vector-database-billing]

{{es}} {{vectordb}} projects on {{serverless-full}} are priced based on consumption across storage, search, ingest, and infrastructure.

Your monthly bill is calculated based on these components:

* **Storage** - Measured by the total amount of data stored in your project, in GB.
* **Search** - Measured by reserved search capacity for your stored data. Capacity is controlled by your project's [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) setting and scales with your project's active storage.
* **Ingest** - Measured by the volume of data you ingest into your project over the course of a month, in GB.
* **Infrastructure fee** - A recurring project fee. Usage is metered by the hour for as long as the project exists, so a full month looks like a flat monthly charge and partial months are pro-rated.

For current rates, refer to the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or the [{{serverless-full}} pricing](https://cloud.elastic.co/pricing/serverless?s=vectordb) pages.

## Storage [vector-database-billing-storage]

You are charged per GB of data stored in the project. Storage charges apply for as long as the data remains in the project. Each {{vectordb}} project can store up to 1 TB of data.

## Search [vector-database-billing-search]

Search charges are based on the search capacity reserved for your stored data. All stored data is searchable by default, which means it actively contributes to search charges.

Search charges scale with [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) and your project's active storage. Active storage is the volume of data used as the basis for search billing. For billing, active storage has a 16 GB minimum: if your project stores less than 16 GB, search charges still use 16 GB as the storage basis.

At Search Power **100**, capacity is reserved to keep the project's full dataset available for low-latency search. Increasing Search Power does not increase the amount of data covered. Instead, it reserves additional search capacity for the same dataset, which can improve performance for higher query concurrency or more demanding search workloads.

Increasing Search Power reserves more capacity and raises search charges. Running more queries does not increase search charges. For current rates, refer to the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless).

## Ingest [vector-database-billing-ingest]

Ingest charges are based on the volume of data written to your project, measured in GB for the billing period. This uses the same definition of billable ingested bytes as other Serverless offerings.

## Infrastructure [vector-database-billing-infrastructure]

You are billed an infrastructure fee for as long as the project exists. Elastic meters this fee by the hour, so on your bill it behaves like a monthly project fee that is pro-rated if you create or delete the project mid-month.

There is no separate control to pause or make a project unavailable. To stop infrastructure charges, [delete the project](/deploy-manage/uninstall/delete-a-cloud-deployment.md).

## Managing {{vectordb}} costs [vector-database-billing-managing-costs]

{{vectordb}} costs follow your storage footprint, search resource allocation, ingest volume, and the infrastructure fee for the time your project exists. To balance performance with spend, adjust the controls described in this section.

### Search Power setting [vector-database-billing-search-power-setting]

[Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) reserves search capacity for your project. Start at the default of **100**, measure latency and throughput for your workload, then increase Search Power if you need more capacity. You increase Search Power in increments of 100. Higher Search Power increases search charges in proportion to the setting and your active storage. You can increase Search Power up to **1900**.

:::{include} _snippets/agent-builder-executions-billing.md
:::

:::{include} _snippets/workflow-executions-billing.md
:::

## Elastic Managed LLMs [vector-database-billing-elastic-managed-llms]

[Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md) enable you to use AI-powered features without deploying a model in your project. Using Elastic Managed LLMs consumes tokens and incurs token-based billing in addition to the other billing dimensions of your project. For current rates, refer to the [{{es}} {{vectordb}} pricing page](https://cloud.elastic.co/pricing/serverless?s=vectordb).

## Related billing dimensions [vector-database-billing-related]

Shared {{serverless-short}} add-ons such as [data out](serverless-project-billing-dimensions.md#general-serverless-billing-data-out) and [support](serverless-project-billing-dimensions.md#general-serverless-billing-support) may also appear on your bill. Refer to [](serverless-project-billing-dimensions.md).

If you use [{{cps}}](/deploy-manage/cross-project-search-config.md), charges are billed to the origin project. For how those charges are calculated, refer to [{{cps-cap}}](serverless-project-billing-dimensions.md#general-serverless-billing-cps).
