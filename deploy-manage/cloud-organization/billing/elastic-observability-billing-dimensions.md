---
navigation_title: "Elastic for Observability"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-billing.html
applies:
  serverless: all
---

# Elastic for Observability billing dimensions [observability-billing]

{{obs-serverless}} projects provide you with all the capabilities of Elastic Observability to monitor critical applications. Projects are provided using a Software as a Service (SaaS) model, and pricing is entirely consumption-based.

Your monthly bill is based on the capabilities you use. When you use {{obs-serverless}}, your bill is calculated based on data volume, which has these components:

* **Ingest** — Measured by the number of GB of log/event/info data that you send to your Observability project over the course of a month.
* **Retention** — Measured by the total amount of ingested data stored in your Observability project.

Ingest and retention metering is based on the uncompressed, normalized, fully enriched data volume you ingest into your Serverless project. This allows you flexibility and consistency when choosing your preferred ingest architecture for enrichment, whether through {{agent}}, {{ls}}, OpenTelemetry, or collectors—without the need to consider possible impacts on the cost.

::::{note}
One consequence of this metering method is that the absolute volume of data reported in your usage statement can be much larger than the "raw" data size or the compressed data size "on the wire." Your monthly bill will transparently display exactly how much data has been ingested, including valuable metadata added by your data shipper, and contextual enrichment performed by your ingest processing. Please note that we took the cost of metadata and enrichment into consideration while determining our Serverless per GB prices to help make {{obs-serverless}} a cost-effective service.
::::



## Synthetics [synthetics-billing]

[Synthetic monitoring](../../../solutions/observability/apps/synthetic-monitoring.md) is an optional add-on to Observability Serverless projects that allows you to periodically check the status of your services and applications. In addition to the core ingest and retention dimensions, there is a charge to execute synthetic monitors on our testing infrastructure. Browser (journey) based tests are charged per-test-run, and ping (lightweight) tests have an all-you-can-use model per location used.

Refer to [Serverless billing dimensions](serverless-project-billing-dimensions.md) and the [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability) for more details about {{obs-serverless}} billing dimensions and rates.
