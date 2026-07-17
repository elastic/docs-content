---
navigation_title: Vector Database projects
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
  - id: elasticsearch
description: >-
  Learn how costs for Elasticsearch Vector Database Serverless projects are
  calculated across storage, searchable capacity, indexing, and infrastructure.
---

# {{es}} Vector Database billing dimensions [vector-database-billing]

{{es}} Vector Database projects on {{serverless-full}} use a different billing model from {{es-serverless}} projects. Instead of virtual compute units (VCUs), charges are based on storage, searchable capacity, indexing volume, and project infrastructure time.

For current rates, refer to the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or the [{{serverless-full}} pricing](https://www.elastic.co/pricing/serverless) pages.

<!-- Fact-check: add a dedicated Vector Database pricing URL when marketing publishes one. -->

## Boosted and unboosted indices [vector-database-billing-boosted-unboosted]

Indices in a Vector Database project can be **boosted** or **unboosted**. These states describe searchability only:

| Index state | Meaning |
| --- | --- |
| **Boosted** | The index is searchable. |
| **Unboosted** | The index is not searchable. |

Do not treat boosted vs unboosted as billing tiers. Storage charges still apply to durable data in either state. How the invoice **Boosted** line item is calculated in the initial release is covered under [Boosted (searchable capacity)](#vector-database-billing-boosted).

::::{warning}
* **Unboosted indices are not searchable.**
* **In the initial release, billing is still computed as if all data is boosted.** Changing an index to unboosted does not reduce the Boosted line item. There is no archive or unboosted discount yet.
::::

## Billing dimensions [vector-database-billing-dimensions]

Your invoice includes these line items:

| Line item | What you pay for | How it is measured |
| --- | --- | --- |
| **Storage** | Durable data stored in the project | GB-month of stored data |
| **Boosted** | Searchable capacity for your data | GB-month of boosted data, multiplied by Search Power |
| **Indexing** | Write volume into the project | GB of billable indexing over the billing period |
| **Infrastructure** | Keeping the project available | Hours the project is running |

### Storage [vector-database-billing-storage]

**Storage** covers the durable footprint of your indices, measured in GB-month (decimal gigabytes, prorated over time).

You are charged for data as long as it remains stored in the project, whether or not it is searchable.

### Boosted (searchable capacity) [vector-database-billing-boosted]

The invoice line item named **Boosted** covers the cost of searchable capacity. Charges use GB-month of data priced as boosted, scaled by your project's [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) (SP):

```text
Boosted charge ∝ Boosted_GB × (SP_used / 100)
```

Higher Search Power increases searchable performance and increases the Boosted line item. If Search Power changes during the billing period, or if the project autoscales within a configured SP range, Elastic bills using the time-weighted Search Power actually used.

In the initial release, `Boosted_GB` matches total durable storage for pricing. See [Boosted and unboosted indices](#vector-database-billing-boosted-unboosted).

### Indexing [vector-database-billing-indexing]

**Indexing** covers billable write volume into the project, measured in GB for the billing period. This follows the same platform definition of billable indexing bytes used for other {{serverless-short}} offerings.

### Infrastructure [vector-database-billing-infrastructure]

**Infrastructure** is a project availability fee billed by the hour for the time your project is running.

Marketing may describe this as a monthly amount (for example, a full month of continuous availability). On the invoice, that amount is converted to an hourly rate and charged for the hours the project emits a heartbeat. If the project runs for only part of the month, you pay only for those hours.

## How this differs from {{es-serverless}} [vector-database-billing-vs-elasticsearch]

| | {{es}} Vector Database | {{es-serverless}} |
| --- | --- | --- |
| Primary model | Storage, boosted capacity, indexing GB, and infrastructure hours | VCUs (search, ingest, ML) plus storage |
| Search performance lever | Search Power multiplies the Boosted line | Search Power affects Search VCU baseline and scale |
| Idle project | Infrastructure accrues while the project exists; storage and boosted continue for stored data | Search VCUs keep a reduced baseline while data remains searchable |

For {{es-serverless}} billing details, see [](elasticsearch-billing-dimensions.md).

## Understand your bill [vector-database-billing-explain]

Use this mapping to relate each invoice line item to the underlying meter:

| Invoice line item | Meter | What drives the charge |
| --- | --- | --- |
| **Storage** | `Storage_GB` (GB-month) | Durable bytes stored over time for all indices (boosted and unboosted) |
| **Boosted** | `Boosted_GB` (GB-month) × (`SP_used` / 100) | Data priced as searchable capacity, scaled by the Search Power actually used over time |
| **Indexing** | `Indexing_GB` (GB) | Billable write volume during the billing period |
| **Infrastructure** | Hours running | Hours the project is available (heartbeat), at the published hourly infrastructure rate |

In the initial release, `Boosted_GB` equals `Storage_GB` for billing. Search Power changes and autoscaling within an SP range are time-weighted into `SP_used`.

Shared {{serverless-short}} add-ons such as [data out](serverless-project-billing-dimensions.md#general-serverless-billing-data-out) and [support](serverless-project-billing-dimensions.md#general-serverless-billing-support) may also appear on your bill. See [](serverless-project-billing-dimensions.md).
