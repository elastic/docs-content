---
navigation_title: Vector Database projects
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
  - id: elasticsearch
description: >-
  Learn how costs for Elasticsearch Vector Database Serverless projects are
  calculated across storage, search, and indexing.
---

# {{es}} Vector Database billing dimensions [vector-database-billing]

{{es}} Vector Database projects on {{serverless-full}} are priced based on consumption across storage, search, and indexing.

Your monthly bill is calculated based on these components:

* **Storage** — Measured by the total amount of data stored in your project, in GB.
* **Search** — Measured by the resources allocated to keep your data searchable. Allocation is controlled by your project's [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) setting.
* **Indexing** — Measured by the volume of data you index into your project over the course of a month, in GB.


For current rates, refer to the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or the [{{serverless-full}} pricing](https://www.elastic.co/pricing/serverless) pages.

<!-- Fact-check: add a dedicated Vector Database pricing URL when marketing publishes one. -->

## Storage [vector-database-billing-storage]

You are charged per GB of data stored in the project. Storage charges apply for as long as the data remains in the project.

## Search [vector-database-billing-search]

Search charges cover the resources used to keep your data searchable. All stored data is boosted by default, which means it is searchable and contributes to Search charges.

[Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) controls how many baseline resources are kept ready for your data and the maximum resources the system can allocate under search load. Increasing Search Power improves query performance and increases search charges. Decreasing Search Power reduces provisioned resources and cost, with more variable query latency under load.

## Indexing [vector-database-billing-indexing]

Indexing charges are based on the volume of data written to your project, measured in GB for the billing period. This uses the same definition of billable indexing bytes as other {{serverless-short}} offerings.

## Managing Vector Database costs [vector-database-billing-managing-costs]

Vector Database costs follow your storage footprint, search resource allocation, and indexing volume. To balance performance with spend, adjust the controls described in this section.

### Search Power setting [vector-database-billing-search-power-setting]

[Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) controls search performance and the resources allocated to boosted data. Increase Search Power when you need more consistent latency and throughput. Decrease it when you want to reduce Search charges and can accept more variable latency.

### Inactivity API [vector-database-billing-inactivity-api]

Boosted versus unboosted is not a customer-facing index setting. All storage is boosted by default. To reduce Search charges for data you do not need to keep searchable, use the Inactivity API.

<!-- Fact-check: link Inactivity API reference when published. Confirm exact API name and behavior (searchability vs billing). -->

## Related billing dimensions [vector-database-billing-related]

Shared {{serverless-short}} add-ons such as [data out](serverless-project-billing-dimensions.md#general-serverless-billing-data-out) and [support](serverless-project-billing-dimensions.md#general-serverless-billing-support) may also appear on your bill. See [](serverless-project-billing-dimensions.md).
