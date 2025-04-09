---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-manage-storage.html
applies_to:
  stack:
---

# Manage storage [apm-manage-storage]

{{agent}} uses [data streams](data-streams.md) to store time series data across multiple indices. [Index templates](view-elasticsearch-index-template.md) are used to configure the backing indices of data streams as they are created. Each data stream ships with a customizable [index lifecycle policy](index-lifecycle-management.md) that automates data retention as your indices grow and age. Use [ingest pipelines](parse-data-using-ingest-pipelines.md) to process and enrich APM documents before indexing them.

The [storage and sizing guide](storage-sizing-guide.md) attempts to define a "typical" storage reference for Elastic APM, and there are additional settings you can tweak to [reduce storage](reduce-storage.md), or to [tune data ingestion in {{es}}](tune-data-ingestion.md#apm-tune-elasticsearch).

In addition, the Applications UI makes it easy to visualize your APM data usage with [storage explorer](storage-explorer.md). Storage explorer allows you to analyze the storage footprint of each of your services to see which are producing large amounts of data—​so you can better reduce the data you’re collecting or forecast and prepare for future storage needs.

