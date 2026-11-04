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

* [Offerings](#offerings)
* [Add-ons](#add-ons)

Specific prices can be found in the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless) or you can create an [Elastic Cloud Serverless Estimate](https://cloud.elastic.co/pricing/serverless).

## Offerings [offerings] 

To learn about billing dimensions for specific offerings, refer to:

* [](elasticsearch-billing-dimensions.md)
* [](vector-database-billing-dimensions.md)
* [](elastic-observability-billing-dimensions.md)
* [](security-billing-dimensions.md)


## Add-ons [add-ons] 


### Data out [general-serverless-billing-data-out] 

*Data out* accounts for all of the traffic coming out of a serverless project. This includes search results, as well as monitoring data sent from the project. The same rate applies regardless of the destination of the data, whether to the internet, another region, or a cloud provider account in the same region. Data coming out of the project through AWS PrivateLink, GCP Private Service Connect, or Azure Private Link is also considered data out.


### Support [general-serverless-billing-support] 

If your subscription level is Standard, there is no separate charge for Support reflected on your bill. If your subscription level is Gold, Platinum, or Enterprise, a charge is made for Support as a percentage (%) of the ECUs. To find out more about our support levels, go to [https://www.elastic.co/support](https://www.elastic.co/support).


### {{cps-cap}} [general-serverless-billing-cps]

[{{cps-cap}}](/deploy-manage/cross-project-search-config.md) enables you to search across multiple {{serverless-short}} projects from a single origin project.

::::{include} /deploy-manage/_snippets/cps-billing.md
::::


### Agent Builder Executions [general-serverless-billing-agent-builder]

Agent Builder usage is billed in addition to the other billing dimensions of your project. Free allocations and requirements depend on your project type. For details, refer to Agent Builder Executions for your project type:

* [{{es-serverless}}](elasticsearch-billing-dimensions.md#elasticsearch-billing-agent-builder-executions)
* [{{es}} {{vectordb}}](vector-database-billing-dimensions.md#vector-database-billing-agent-builder-executions)
* [{{obs-serverless}}](elastic-observability-billing-dimensions.md#observability-billing-agent-builder-executions)
* [{{elastic-sec}}](security-billing-dimensions.md#security-billing-agent-builder-executions)


### Workflow Executions [general-serverless-billing-workflow-executions]

Workflow usage is billed in addition to the other billing dimensions of your project. Free allocations and requirements depend on your project type. For details, refer to Workflow Executions for your project type:

* [{{es-serverless}}](elasticsearch-billing-dimensions.md#elasticsearch-billing-workflow-executions)
* [{{es}} {{vectordb}}](vector-database-billing-dimensions.md#vector-database-billing-workflow-executions)
* [{{obs-serverless}}](elastic-observability-billing-dimensions.md#observability-billing-workflow-executions)
* [{{elastic-sec}}](security-billing-dimensions.md#security-billing-workflow-executions)


### Elastic Managed LLMs [general-serverless-billing-elastic-managed-llms]

Using Elastic Managed LLMs consumes tokens and incurs token-based billing in addition to the other billing dimensions of your project. For details, refer to Elastic Managed LLMs for your project type:

* [{{es-serverless}}](elasticsearch-billing-dimensions.md#elasticsearch-billing-information-about-the-vcu-types-search-ingest-and-ml)
* [{{es}} {{vectordb}}](vector-database-billing-dimensions.md#vector-database-billing-elastic-managed-llms)
* [{{obs-serverless}}](elastic-observability-billing-dimensions.md#observability-billing-elastic-managed-llms)
* [{{elastic-sec}}](security-billing-dimensions.md#security-billing-elastic-managed-llms)

