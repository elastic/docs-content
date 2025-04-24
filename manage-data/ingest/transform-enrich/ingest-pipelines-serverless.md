---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/ingest-pipelines.html
applies_to:
  stack: ga
  serverless: ga
---

# Elasticsearch ingest pipelines (Serverless) [ingest-pipelines]

This content applies to: [![Elasticsearch](/manage-data/images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](/manage-data/images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](/manage-data/images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

{{es}} ingest pipelines let you perform common transformations on your data before indexing. For example, you can use pipelines to remove fields, extract values from text, and enrich your data.

A pipeline consists of a series of configurable tasks called processors. Each processor runs sequentially, making specific changes to incoming documents. After the processors have run, {{es}} adds the transformed documents to your data stream or index.

:::{image} /manage-data/images/elasticsearch-reference-ingest-process.svg
:alt: Ingest pipeline diagram
:::

## Create and manage pipelines [ingest-pipelines-create-and-manage-pipelines]

In **{{project-settings}} → {{manage-app}} → {{ingest-pipelines-app}}**, you can:

* View a list of your pipelines and drill down into details
* Edit or clone existing pipelines
* Delete pipelines

:::{image} /manage-data/images/serverless-ingest-pipelines-management.png
:alt: {{ingest-pipelines-app}}
:screenshot:
:::

To create a pipeline, click **Create pipeline → New pipeline**. For an example tutorial, see [Example: Parse logs](example-parse-logs.md).

The **New pipeline from CSV** option lets you use a file with comma-separated values (CSV) to create an ingest pipeline that maps custom data to the Elastic Common Schema (ECS). Mapping your custom data to ECS makes the data easier to search and lets you reuse visualizations from other data sets. To get started, check [Map custom data to ECS](ecs://reference/ecs-converting.md).


## Test pipelines [ingest-pipelines-test-pipelines]

Before you use a pipeline in production, you should test it using sample documents. When creating or editing a pipeline in **{{ingest-pipelines-app}}**, click **Add documents**. In the **Documents** tab, provide sample documents and click **Run the pipeline**:

:::{image} /manage-data/images/serverless-ingest-pipelines-test.png
:alt: Test a pipeline in {{ingest-pipelines-app}}
:screenshot:
:::
