---
applies_to:
  serverless:
navigation_title: For {{serverless-full}}
---

# AutoOps for {{serverless-full}}

For [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) projects, AutoOps is set up and enabled automatically in all supported [regions](ec-autoops-regions.md#autoops-for-serverless-full-regions). More regions are coming soon. 

## How AutoOps monitors your {{serverless-short}} project

In your {{serverless-full}} project, Elastic takes care of provisioning, monitoring, and autoscaling resources so you can focus on your business. This is why {{serverless-full}} is billed based on the effective usage of compute and storage resources.

:::{tip} 
For more information about how {{serverless-full}} is priced and packaged, refer to the following pages:
* [{{serverless-full}} pricing page](https://www.elastic.co/pricing/serverless-search)
* [{{serverless-full}} pricing and packaging blog](https://www.elastic.co/blog/elastic-cloud-serverless-pricing-packaging)
:::

Since your monthly {{serverless-short}} bill is directly related to how many resources have been consumed, it's important for you to understand why your consumption fluctuates and how past usage was influenced by your project's performance. This information lets you adapt your workloads accordingly and have better control over your future bills.

This is where AutoOps comes in. With AutoOps for {{serverless-short}}, you can:

* understand and monitor your usage patterns through project-level and index-level performance metrics.
* access several curated dashboards to look at your project from all the different angles.
* have full visibility into the main {{serverless-short}} billing dimensions.

:::{note}
Stack Monitoring is not available in {{serverless-full}} because there is no need for it. Elastic takes care of monitoring and managing your {{serverless-short}} projects. Learn more about the [differences between AutoOps and Stack Monitoring](/deploy-manage/monitor/autoops-vs-stack-monitoring.md).
:::

## AutoOps for {{serverless-short}} billing dimensions

AutoOps for {{serverless-short}} focuses on different [billing dimensions](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md) related to compute and storage, which are explained in the following subsections.

### Compute billing dimensions
On [{{es-serverless}} projects](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md), the main compute-related billing dimension is called a **Virtual Compute Unit (VCU)**. 1 VCU contains 1GB of RAM and the corresponding vCPU and local storage for caching. 

There are three main types of VCUs:
* **Search VCUs** powering the search tier, which handles all search operations.
* **Indexing VCUs** powering the indexing tier, which handles all data indexing operations.
* **Machine learning VCUs** powering the machine learning tier, which handles all ML-related operations such as inference, anomaly detection, data frame analytics, transforms, and more.

VCUs materialize the load that each of the above tiers has to sustain to respond to your search, indexing, and machine learning needs respectively. As the load of a given tier fluctuates above or below some pre-defined thresholds, the tier autoscales accordingly to accommodate that load.

:::{tip} 
For more information about how autoscaling works in {{serverless-short}}, refer to the following blogs:
* [Search tier autoscaling](https://www.elastic.co/search-labs/blog/elasticsearch-serverless-tier-autoscaling)
* [Ingest autoscaling](https://www.elastic.co/search-labs/blog/elasticsearch-ingest-autoscaling)
:::

:::{admonition} Example: How search VCU billing is calculated
Let's say your constant search workload requires 4GB of RAM, which means your search VCU usage for one day will be 4 search VCUs/hour * 24 hours = 96 VCUs. 

Given that 1 search VCU = [$0.09/hour](https://www.elastic.co/pricing/serverless-search), this translates to $8.64 for that day.
:::

### Storage billing dimensions

On [Observability](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md) and [Security](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md) {{serverless-short}} projects, one storage-related billing dimension is called the **Ingest rate**, which represents the volume of data (in GB) ingested per unit of time.

On all [{{es}}](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md), [Observability](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md), and [Security](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md) {{serverless-short}} projects, the main storage-related billing dimension is called **Storage retained** or **Retention**, and it represents the total volume of data (in GB prorated over a month) retained in your project.

:::{admonition} Example: How ingest rate and storage retained billing is calculated
Let’s say you ingest 1TB of data into your Observability project.

* **Ingest rate**: Given that 1GB ingested per hour = [$0.105](https://www.elastic.co/pricing/serverless-observability), your ingest rate cost will be $107.2.
* **Retention**: Given that 1GB retained per hour = [$0.018](https://www.elastic.co/pricing/serverless-observability) and assuming it took one hour to ingest 1TB of data, that 1TB will be billed 1.42GB for that slice of one hour (1TB/720 hours per month), which translates to $0.025. Each subsequent hour in that month will cost the same.
:::

## Coming soon to AutoOps for Serverless

The following features are coming soon to AutoOps for {{serverless-short}}:

* An **Indexing tier** view, which will show you how indexing performance influences your use of ingest VCUs.
* A **Machine learning tier** view, which will provide insight into your machine learning jobs and inference performance, as well as token usage.
* Visibility into other billing dimensions such as data transfer out of {{ecloud}} and the various Observability and Security add-ons.

## Section overview 

In this section, you'll find the following information:

* How to [access AutoOps in your {{serverless-short}} project](access-autoops-for-serverless.md).
* How to use the [Search tier view](search-tier-view-autoops-serverless.md) to see the impact of search performance on your use of search VCUs.
* How to use the [Search AI Lake view](search-ai-lake-view-autoops-serverless.md) to drill down into your storage-related usage.

:::{tip}
Refer to our [FAQ](/deploy-manage/monitor/autoops/ec-autoops-faq.md) for answers to frequently asked questions about AutoOps.
:::