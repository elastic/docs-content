---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-how-to-access.html
applies_to:
  serverless:
navigation_title: For {{serverless-full}}
---

# AutoOps for {{serverless-full}}

For [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) projects, AutoOps is set up and enabled automatically in all supported [regions](ec-autoops-regions.md#autoops-for-serverless-full-regions). More regions are coming soon. 

## How AutoOps monitors your serverless project

{{serverless-full}} is fully managed by Elastic so that you can focus on running your business. Elastic ensures that the appropriate resources are adequately provisioned and autoscaled to allow your Serverless workloads to run flawlessly at any time. As a result, Elastic Cloud Serverless is billed based on the effective usage of compute and storage resources.

Since your Serverless monthly bill is directly related to how many resources have been consumed, it is important for you to understand how past usage was influenced by your Serverless project performance so that you can adapt your workloads and better stay in control of your future Serverless bills.

AutoOps for {{serverless-full}} provides full visibility into the main serverless billing dimensions and allows you to monitor your usage metrics through the lens of your project-level and index-level performance metrics.

:::{note} 
For more information about how Elastic Cloud Serverless is priced and packaged, refer to the following pages:
* [{{serverless-full}} pricing page](https://www.elastic.co/pricing/serverless-search)
* [{{serverless-full}} pricing and packaging blog post](https://www.elastic.co/blog/elastic-cloud-serverless-pricing-packaging)
:::

## Coming soon

The following features are coming soon to AutoOps for serverless:

* An **Indexing tier** view, which will show you how indexing performance influences your Ingest VCUs.
* A **Machine learning tier** view, which will provide insight into your machine learning jobs and inference performance, as well as token usage.
* Visibility into other billing dimensions such as data transfer out of {{ecloud}} and the various Observability and Security add-ons.

## Section overview 

In this section, you'll find the following information:

* How to [access AutoOps in your serverless project](access-autoops-for-serverless.md)
* How to use the Search AI Lake view to drill down into your storage-related usage
* How to use the Search tier view to understand the impact of search performance on your Search VCUs

