---
navigation_title: "Elastic for Observability"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-billing.html
applies_to:
  serverless: all
---

# Elastic for Observability billing dimensions [observability-billing]

{{obs-serverless}} projects provide you with all the capabilities of Elastic Observability to monitor critical applications. Projects are provided using a Software as a Service (SaaS) model, and pricing is entirely consumption-based.

Your monthly bill is based on the capabilities you use. When you use {{obs-serverless}}, your bill is calculated based on data volume, which has these components:

* **Ingest** — Measured by the number of GB of log/event/info data that you send to your Observability project over the course of a month.
* **Retention** — Measured by the total amount of ingested data stored in your Observability project.

Data volumes for ingest and retention are based on the fully enriched normalized data size at the end of the ingest pipeline, before {{es}} compression is performed, and will be higher than the volumes traditionally reported by {{es}} index size. In addition, these volumes might be larger than those reported by cloud provider proxy logs for data going into {{es}}. This allows you to have flexibility in choosing your preferred ingest architecture for enrichment, whether it’s through Elastic Agent, Logstash, OpenTelemetry, or collectors — with no impact on the cost.


## Synthetics [synthetics-billing]

[Synthetic monitoring](../../../solutions/observability/apps/synthetic-monitoring.md) is an optional add-on to Observability Serverless projects that allows you to periodically check the status of your services and applications. In addition to the core ingest and retention dimensions, there is a charge to execute synthetic monitors on our testing infrastructure. Browser (journey) based tests are charged per-test-run, and ping (lightweight) tests have an all-you-can-use model per location used.

Refer to [Serverless billing dimensions](serverless-project-billing-dimensions.md) and the [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=observability) for more details about {{obs-serverless}} billing dimensions and rates.
