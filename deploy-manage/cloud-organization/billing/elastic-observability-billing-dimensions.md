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
  abb-anchor: observability-billing-agent-builder-executions
  abb-preamble: |
    Elastic Agent Builder enables you to create AI agents that assist with operational tasks, including incident diagnosis, root cause analysis, and service health troubleshooting. Agent Builder Executions is a billing dimension for Elastic Observability Serverless projects on the Observability Complete tier.

    Billing is based on the number of agent executions completed in your project over the course of a month.
  abb-free-executions: 10,000
  abb-pricing-label: Elastic Cloud pricing table
  abb-pricing-url: https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability
  wfe-anchor: observability-billing-workflow-executions
  wfe-preamble: Workflows enable you to automate multi-step operational processes, including incident response, runbook automation, and service health remediation. Workflow Executions is a billing dimension for Observability Serverless projects on the Observability Complete tier.
  wfe-billing-detail: Billing is based on the number of workflow executions completed successfully in your project over the course of a month. Each execution represents one end-to-end run of a workflow. Failed executions are not billed.
  wfe-free-executions: 10,000
  wfe-pricing-label: Elastic Cloud pricing table
  wfe-pricing-url: https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability
---

# {{obs-serverless}} billing dimensions [observability-billing]

{{obs-serverless}} projects provide you with all the capabilities of Elastic Observability to monitor critical applications. Projects are provided using a Software as a Service (SaaS) model, and pricing is entirely consumption-based. {{obs-serverless}} projects are available in the following tiers of carefully selected features to enable common observability operations:

* **Observability Logs Essentials**: Includes everything you need to store and analyze logs at scale.
* **Observability Complete**: Adds full-stack observability capabilities to monitor cloud-native and hybrid environments.

Your monthly bill is based on the capabilities you use. When you use {{obs-serverless}}, your bill is calculated based on data volume, which has these components:

* **Ingest** — Measured by the number of GB of log/event/info data that you send to your Observability project over the course of a month.
* **Retention** — Measured by the total amount of ingested data stored in your Observability project.

:::{include} _snippets/note-data-volumes-ingest-retention.md
:::

Refer to [Serverless billing dimensions](serverless-project-billing-dimensions.md) and the [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability) for more details about {{obs-serverless}} billing dimensions and rates, or you can create a [Serverless estimate](https://cloud.elastic.co/pricing/serverless?s=observability).

## Synthetics [synthetics-billing]

[Synthetic monitoring](/solutions/observability/synthetics/index.md) is an optional add-on to Observability Serverless projects that allows you to periodically check the status of your services and applications as a part of the "Observability Complete" feature tier. In addition to the core ingest and retention dimensions, there is a charge to execute synthetic monitors on our testing infrastructure. Browser (journey) based tests are charged per-test-run, and ping (lightweight) tests have an all-you-can-use model per location used.

:::{include} _snippets/agent-builder-executions-billing.md
:::

:::{include} _snippets/workflow-executions-billing.md
:::

## Elastic Managed LLMs [observability-billing-elastic-managed-llms]

[Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md) enable you to leverage AI-powered search as a service without deploying a model in your serverless project. The models are configured by default to use with the Security AI Assistant, Attack Discovery, and other applicable AI features as a part of the "Observability Complete" feature tier. Using Elastic Managed LLMs will use tokens and incur related token-based add-on billing for your serverless project.

## {{cps-cap}} [observability-billing-cps]
```{applies_to}
serverless: preview
```

:::{include} _snippets/cps-billing-obs-sec.md
:::
