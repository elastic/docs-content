---
navigation_title: Serverless billing dimensions
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/general-serverless-billing.html
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
---

# Serverless project billing dimensions [general-serverless-billing]

{{serverless-full}} billing is based on your usage across these categories of billing dimensions:

* [Project charges](#project-charges)
* [Organization charges](#organization-charges)
* [Add-ons](#add-ons)

Specific prices can be found in the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or you can create an [Elastic Cloud Serverless Estimate](https://cloud.elastic.co/pricing/serverless).

This page describes each category and how it applies to your projects. For details, refer to the billing dimensions page for your project type:

* [](elasticsearch-billing-dimensions.md)
* [](vector-database-billing-dimensions.md)
* [](elastic-observability-billing-dimensions.md)
* [](security-billing-dimensions.md)

## Project charges [project-charges]

Project charges are based on dimensions that best reflect how each project type, or *offering*, is used. For example, an {{obs-serverless}} project is billed based on the volume of data it ingests and retains. An {{es-serverless}} project is billed for the compute it uses to ingest and search your data, measured in virtual compute units (VCUs).

Some features that are specific to a project type, such as [Synthetics](elastic-observability-billing-dimensions.md#synthetics-billing) for {{observability}}, and [Cloud Protection](security-billing-dimensions.md#security-billing-cloud-protection) for {{elastic-sec}}, have dedicated billing dimensions.

Some features that are available in more than one offering, such as [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) and [{{cps}}](/explore-analyze/cross-project-search.md), are priced differently depending on the project type.

For details, refer to the billing dimensions page for your project type.

## Organization charges [organization-charges]

These charges apply regardless of which project type you use, and include data out and support.

:::{include} _snippets/serverless-organization-charges.md
:::

## Add-ons [add-ons]

Add-ons are capabilities that are available across your {{serverless-short}} projects. They're billed based on usage, in addition to the other billing dimensions of your project. Add-ons include [Workflows](/explore-analyze/workflows.md), which are billed based on the number of successful workflow executions, and the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md), which is billed based on the tokens used with its models, including embedding models, rerankers, and [Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md). 

Add-ons are priced the same for all project types, but their availability depends on your project type and [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md). For details, refer to the billing dimensions page for your project type.
