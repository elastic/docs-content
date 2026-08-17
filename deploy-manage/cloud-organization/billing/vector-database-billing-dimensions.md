---
navigation_title: Vector Database projects
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
  - id: serverless-vector-database
description: >-
  Learn how costs for Elasticsearch Vector Database Serverless projects
  are calculated across storage, search, ingest, and infrastructure.
---

# {{es}} Vector Database billing dimensions [vector-database-billing]

{{es}} Vector Database projects on {{serverless-full}} are priced based on consumption across storage, search, ingest, and infrastructure.

Your monthly bill is calculated based on these components:

* **Storage** - Measured by the total amount of data stored in your project, in GB.
* **Search** - Measured by reserved search capacity for your stored data. Capacity is controlled by your project's [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) setting and scales with how much data you store.
* **Ingest** - Measured by the volume of data you ingest into your project over the course of a month, in GB.
* **Infrastructure fee** - A recurring project fee. Usage is metered by the hour for as long as the project exists, so a full month looks like a flat monthly charge and partial months are pro-rated.

For current rates, refer to the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or the [{{serverless-full}} pricing](https://www.elastic.co/pricing/serverless) pages.

<!-- Fact-check: add a dedicated Vector Database pricing URL when marketing publishes one. -->

## Storage [vector-database-billing-storage]

You are charged per GB of data stored in the project. Storage charges apply for as long as the data remains in the project.

## Search [vector-database-billing-search]

Search charges cover the search capacity reserved for your stored data. All stored data is searchable by default, which means it actively contributes to Search charges.

[Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) determines how much capacity is reserved. At Search Power **100**, enough capacity is reserved so that 100% of your project data remains available for low-latency search. Higher Search Power values reserve more capacity in proportion to that baseline: for example, **200** reserves about twice as much as **100**.

Increasing Search Power reserves more capacity and raises search charges. Running more queries does not increase search charges. For current rates, refer to the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless).

## Ingest [vector-database-billing-ingest]

Ingest charges are based on the volume of data written to your project, measured in GB for the billing period. This uses the same definition of billable ingested bytes as other Serverless offerings.

## Infrastructure [vector-database-billing-infrastructure]

You are billed an infrastructure fee for as long as the project exists. Elastic meters this fee by the hour, so on your bill it behaves like a monthly project fee that is pro-rated if you create or delete the project mid-month.

There is no separate control to pause or make a project unavailable. To stop infrastructure charges, [delete the project](/deploy-manage/uninstall/delete-a-cloud-deployment.md).

## Managing Vector Database costs [vector-database-billing-managing-costs]

Vector Database costs follow your storage footprint, search resource allocation, ingest volume, and the infrastructure fee for the time your project exists. To balance performance with spend, adjust the controls described in this section.

### Search Power setting [vector-database-billing-search-power-setting]

[Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) reserves search capacity for your project. Start at the default of **100**, measure latency and throughput for your workload, then increase Search Power if you need more capacity. You increase Search Power in increments of 100. Higher Search Power increases search charges in proportion to the setting and your stored data volume. You can increase Search Power up to **1900**.

For high availability, you can increase Search Power to **200**. That setting reserves enough capacity for two full copies of your project data to remain available for low-latency search.

## Related billing dimensions [vector-database-billing-related]

Shared {{serverless-short}} add-ons such as [data out](serverless-project-billing-dimensions.md#general-serverless-billing-data-out) and [support](serverless-project-billing-dimensions.md#general-serverless-billing-support) may also appear on your bill. Refer to [](serverless-project-billing-dimensions.md).

If you use {{cps}}, additional charges may apply when the feature becomes generally available. For how those charges are calculated, refer to [ {{cps}} Billing](/deploy-manage/cross-project-search-config.md#cps-billing).
