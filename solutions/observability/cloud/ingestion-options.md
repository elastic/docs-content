---
navigation_title: Ingestion options
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/ingest-aws-options.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Ingestion options [ingest-aws-options]


You have a number of options for ingesting data with AWS. The following table helps you identify which option best fits your needs:

|  | Amazon Data Firehose | ESF | Elastic Agent | Beats |
| --- | --- | --- | --- | --- |
| **logs** | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| **metrics** | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| **PrivateLink support / VPC** | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| **pros** | Managed service, auto-scale | Auto-scale, built-in support for SQS | Supports all integrations, manages multiple agents using Fleet | Large configuration options |
| **cons** | Few configuration options | Partial integrations support | Not a managed service, no auto-scale | Not a managed service, no auto-scale |


## Overview of the ingest process [_overview_of_the_ingest_process]

The high-level architecture is shown below.

:::{image} /solutions/images/observability-ingest-options-overview.png
:alt: Ingest options
:screenshot:
:::

