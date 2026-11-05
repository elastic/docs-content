---
navigation_title: Observability projects
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-billing.html
applies_to:
  serverless:
    observability: ga
products:
  - id: cloud-serverless
sub:
  offering: Observability
  abb-preamble: |
    Elastic Agent Builder enables you to create AI agents that assist with operational tasks, including incident diagnosis, root cause analysis, and service health troubleshooting. Agent Builder Executions is a billing dimension for Elastic Observability Serverless projects on the Observability Complete tier.

    Billing is based on the number of agent executions completed in your project over the course of a month.
  abb-free-executions: 10,000
  pricing-label: Elastic Cloud pricing table
  pricing-url: https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability
  wfe-preamble: Workflows enable you to automate multi-step operational processes, including incident response, runbook automation, and service health remediation. Workflow Executions is a billing dimension for Observability Serverless projects on the Observability Complete tier.
  wfe-billing-detail: Billing is based on the number of workflow executions completed successfully in your project over the course of a month. Each execution represents one end-to-end run of a workflow. Failed executions are not billed.
  wfe-free-executions: 10,000

---

# {{obs-serverless}} billing dimensions [observability-billing]

{{obs-serverless}} projects provide you with all the capabilities of Elastic Observability to monitor critical applications. Projects are provided using a Software as a Service (SaaS) model, and pricing is entirely consumption-based. {{obs-serverless}} projects are available in the following tiers of carefully selected features to enable common observability operations:

* **Observability Logs Essentials**: Includes everything you need to store and analyze logs at scale.
* **Observability Complete**: Adds full-stack observability capabilities to monitor cloud-native and hybrid environments.

Your monthly bill is based on the capabilities you use. When you use {{obs-serverless}}, your bill is calculated based on data volume, which has these components:

* **Ingest** — Measured by the number of GB of data that you send to your Observability project over the course of a month. Metrics data ingested in [time series index mode](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) is priced at 25% of the standard per-GB ingest rate. All other data, including logs and traces, are priced at the standard rate.
* **Retention** — Measured by the total amount of ingested data stored in your Observability project. Metrics data stored in time series index mode is priced at 25% of the standard per-GB retention rate. All other data, including logs and traces, are priced at the standard rate.

:::{include} _snippets/note-data-volumes-ingest-retention.md
:::

Charges like these, which depend on your project type, are called *project charges*. Project charges also include features such as [Agent Builder](#observability-billing-agent-builder-executions) and [{{cps}}](#observability-billing-cps), whose pricing depends on your project type.

Your bill can also include [add-ons](#observability-billing-add-ons) and [organization charges](#observability-billing-organization-charges). To learn more about billing dimension categories, refer to [](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md).

Refer to the [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability) for more details about {{obs-serverless}} billing dimensions and rates, or you can create a [Serverless estimate](https://cloud.elastic.co/pricing/serverless?s=observability).

## Synthetics [synthetics-billing]

[Synthetic monitoring](/solutions/observability/synthetics/index.md) is an optional add-on to Observability Serverless projects that allows you to periodically check the status of your services and applications as a part of the "Observability Complete" feature tier. In addition to the core ingest and retention dimensions, there is a charge to execute synthetic monitors on our testing infrastructure. Browser (journey) based tests are charged per-test-run, and ping (lightweight) tests have an all-you-can-use model per location used.

## Agent Builder executions [observability-billing-agent-builder-executions]

:::{include} _snippets/agent-builder-executions-billing.md
:::

## {{cps-cap}} [observability-billing-cps]

[{{cps-cap}}](/deploy-manage/cross-project-search-config.md) enables you to search across multiple {{serverless-short}} projects from a single origin project.

:::{include} /deploy-manage/_snippets/cps-billing.md
:::

## Add-ons [observability-billing-add-ons]

Add-ons are capabilities that are available across your {{serverless-short}} projects. They're billed based on usage, in addition to the other billing dimensions of your project.

### Workflow executions [observability-billing-workflow-executions]

:::{include} _snippets/workflow-executions-billing.md
:::

### Elastic {{infer-cap}} Service [observability-billing-elastic-managed-llms]

The [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) is charged based on the tokens used with its models, including embedding models, rerankers, and Elastic Managed LLMs.

[Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md) enable you to use AI-powered features without deploying a model in your project. The models are configured by default to use with Agent Builder and other applicable AI features as a part of the "Observability Complete" feature tier.

## Organization charges [observability-billing-organization-charges]

These charges apply regardless of which product you use, and include data out and support.

:::{include} _snippets/serverless-organization-charges.md
:::