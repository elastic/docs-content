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

{{serverless-full}} billing is based on your usage across these dimensions:

* [Project charges](#project-charges)
* [Add-ons](#add-ons)

Specific prices can be found in the [{{ecloud}} Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or you can create an [Elastic Cloud Serverless Estimate](https://cloud.elastic.co/pricing/serverless).

## Project charges [project-charges]

Your charges for each {{serverless-short}} project depend on the following factors:

* **Project type**: Which solution you've created a project for ({{es}}, {{observability}}, or Security). The project type determines what features are available and how the project's core usage is metered.
* **Feature tier**: For {{observability}} and Security projects, the tier selected within the project determines which features the project can use, as well as the rates that apply to certain billing dimensions.
* **Usage**: The volume of activity in the project, such as data ingested, data retained, compute units consumed, or executions run.

For the specific billing dimensions, tiers, and usage units of each project type, refer to:
* [](elasticsearch-billing-dimensions.md)
* [](elastic-observability-billing-dimensions.md)
* [](security-billing-dimensions.md)


## Add-ons [add-ons] 

Add-ons are additional features that you can use in your project. They are billed separately from the base project charges.

The following add-ons in this section apply across all project types, and are billed based on usage or your {{ecloud}} subscription level. 

Other add-ons might impact your bill. These add-ons are specific to a project type and documented on the [individual project pages](#project-charges). Some are [opt-in](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons), such as endpoint protection and synthetics. Others apply automatically based on usage, such as agent executions, workflow executions, and managed LLMs.

### Data out [general-serverless-billing-data-out] 

*Data out* accounts for all of the traffic coming out of a serverless project. This includes search results, as well as monitoring data sent from the project. The same rate applies regardless of the destination of the data, whether to the internet, another region, or a cloud provider account in the same region. Data coming out of the project through AWS PrivateLink, GCP Private Service Connect, or Azure Private Link is also considered data out.


### Support [general-serverless-billing-support] 

How the Support charge appears on your bill depends on your organization's [{{ecloud}} subscription level](/deploy-manage/license.md). 

At the lowest subscription level, Support is included at no separate charge. At higher subscription levels, Support is billed as a percentage of the ECUs consumed by your {{serverless-short}} projects. For the support level included with each subscription level, refer to [{{ech}} pricing](https://www.elastic.co/pricing/cloud-hosted). To find out more about our support levels, go to [https://www.elastic.co/support](https://www.elastic.co/support)


### {{cps-cap}} [general-serverless-billing-cps]
```{applies_to}
serverless: preview
```

[{{cps-cap}}](/deploy-manage/cross-project-search-config.md) enables you to search across multiple {{serverless-short}} projects from a single origin project.

::::{include} /deploy-manage/_snippets/cps-billing.md
::::

