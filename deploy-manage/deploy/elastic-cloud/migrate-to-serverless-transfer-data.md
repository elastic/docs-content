---
navigation_title: Transfer data
description: Choose what data to copy for testing and production, then prepare the destination, transfer data, and verify the copies in Serverless.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Transfer data to {{serverless-full}} [transfer-data]

**Serverless migration process**

:::{image} /deploy-manage/images/serverless-migration-navigation-grouped-transfer-data.svg
:alt: Assess, create project, prepare and test, and switch to production. The preparation cycle runs from Prepare to Transfer data to Test and validate and back to Prepare. Transfer data is the current procedure, used during preparation and production.
:::

Previous: [Prepare destination](migrate-to-serverless-prepare.md) · Next: [Test and validate](migrate-to-serverless-test-and-validate.md)

This guide explains how to transfer data from your source deployment to the destination {{serverless-short}} project. It helps you decide which data to transfer at each stage of the migration and describes how to prepare the destination, transfer the selected data, and verify the results.

## Before you begin

Before transferring data:

- Use your [asset inventory](migrate-to-serverless-assess.md#migrate-to-serverless-inventory) to identify the indices and data streams you need to migrate and how your applications read and modify their data, including indexing, updates, and deletes.
- [Create the destination project and configure access](migrate-to-serverless-create-project.md).
- Set up the [templates and other resources](migrate-to-serverless-prepare.md#migrate-to-serverless-set-up) required by the data you plan to transfer.

## Decide what to transfer and when [select-the-data-to-transfer]

Selecting which indices and data streams to transfer, and when to transfer them, helps you validate the destination and reduce the work left for the production switch. The approach depends on your application's needs, the data it uses, and whether operations at the source add, update, or delete documents.

:::{important}
This procedure covers user data. Migrate feature configuration and assets through their [supported procedures](migrate-to-serverless-prepare.md). Exclude system and internal indices from document transfers. Identify application data stream backing indices through the data stream definition, even though their names start with `.ds-`.
:::

Use the following considerations to plan transfers throughout the migration.

- **Start with data for testing.** Copy a representative subset of historical data, recent data, or both, based on the queries and ingestion workflows you need to validate. You can copy data that continues to change at the source, treating those copies as provisional. Transfer more data as you test additional application features.
- **Track your copies.** Record the source indices and their destination names, which copies you have verified, which are provisional, and what remains pending.
- **Transfer stable data before the production switch.** If you keep the tested project for production, retain verified copies whose source data has stayed unchanged. You can transfer the remaining stable data before the final migration window. Check for updates, deletes, and retention before treating a backing index as stable, even after rollover.
- **Plan the remaining data transfer.** After testing and validating the destination, identify the data still to migrate and decide how to transfer it during the production switch. A verified incremental transfer method can reduce how long clients need to stop writing to the source. Follow [Complete the migration and switch to production](migrate-to-serverless-production.md) to plan and carry out the transition.

## Transfer and verify the data

% pequeña introducción

% TBD: pending to improve this section, prepare the destination is not properly structured (needs a lot of improvement), transfer data looks more or less ok, but the "add backing indices to data stream" needs its own optional step in case the user is transferring DS backend indices individually,

:::::{stepper}

::::{step} Prepare the destination
:anchor: migrate-to-serverless-prepare-destination

We recommend creating destination indices and data streams before transferring documents. The source's current mappings and settings can differ from its templates, for example because they were customized after creation. Creating the destination explicitly lets you preserve that configuration, with the adaptations required by {{serverless-short}}.

You can skip explicit creation if you have verified that the destination templates provide the mappings and settings you want and intend to rely on automatic index or data stream creation during the transfer.

#### Create destination indices [migrate-to-serverless-regular-indices]

If your source is a data stream, [prepare the stream in the destination](#migrate-to-serverless-data-streams) before creating standalone copies.

1. Retrieve the definition of each source index or backing index with the [get index API]({{es-apis}}operation/operation-indices-get), `GET /<source-index>`.
2. Check the [effective templates](/manage-data/data-store/templates/simulate-multi-component-templates.md) for each planned destination name. [Create the destination index]({{es-serverless-apis}}operation/operation-indices-create) with the source mappings and [settings supported in {{serverless-short}}](elasticsearch://reference/elasticsearch/index-settings/serverless.md). Omit generated metadata such as the UUID and creation date. If you set `index.refresh_interval`, use `5s` or higher, or `-1` to turn off automatic refreshes. [Adapt lifecycle configuration](migrate-to-serverless-prepare.md#migrate-to-serverless-lifecycle) where needed.

   For a copy of a backing index, choose a standalone name that matches no data stream template, such as `migration-logs-myapp-default-000042`. Omit the internal `_data_stream_timestamp` mapping. {{es}} configures it when you add the copy to the stream. Review destination retention separately because the copy has its own lifecycle state and index age.

#### Prepare a data stream [migrate-to-serverless-data-streams]

For a [time series data stream (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md), follow the [TSDS reindexing procedure](/manage-data/data-store/data-streams/reindex-tsds.md) to account for time bounds. The examples on this page use a conventional data stream.

To find the source backing indices, use the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream) in the source, for example `GET /_data_stream/logs-myapp-default`. The `indices` array lists its backing indices, with the current write index last.

Use the destination integration package or a matching [data stream template](migrate-to-serverless-prepare.md#migrate-to-serverless-templates). If needed, [create the destination data stream]({{es-serverless-apis}}operation/operation-indices-create-data-stream), for example with `PUT /_data_stream/logs-myapp-default`. Keep its write index for new ingestion.

To track and verify copies across migration phases, prepare a separate destination index for each source backing index you plan to transfer. For a conventional data stream that you can copy in a single pass, you can also [reindex directly to the destination stream](#migrate-to-serverless-reindex-data-stream).

::::

::::{step} Transfer the data
:anchor: migrate-to-serverless-transfer-documents

Choose the method based on your source and where you can run the transfer. Check the [supported deployment combinations](/manage-data/migrate.md#data-migration-guides-serverless) and the method's authentication and connectivity requirements.

- **[Reindex from remote](/manage-data/migrate/migrate-data-using-reindex-api.md).** Run reindexing from the destination project when your source is an {{ech}} deployment that the project can reach.
- **[Copy with {{ls}}](/manage-data/migrate/migrate-with-logstash.md).** Run {{ls}} on a host that can reach both the source and the destination. Configure the output to preserve document IDs when copying existing documents.
- **[Re-ingest from the original source](/manage-data/migrate.md#migration-options).** If the original data is available, send it through your ingestion tools to the destination. Confirm that the available inputs and destination pipelines can reproduce the data your application needs.

Snapshot and restore is managed by the service in {{serverless-short}}.

When copying existing documents, use explicit source and destination names. For a backing index, copy into its prepared standalone index and verify it before adding it to the data stream.

:::{tip}
For conventional data streams, you can copy the whole stream by targeting the source and destination stream names, or transfer its backing indices individually. This guide recommends individual backing index copies to give you control over what to transfer and help track and verify each copy. [Time series data streams (TSDS)](/manage-data/data-store/data-streams/reindex-tsds.md) require additional preparation.
:::

:::{dropdown} Check embeddings, pipelines, and transfer load
:name: migrate-to-serverless-transfer-considerations

- **Vector embeddings.** Preserve compatible vector mappings and include stored embeddings in the source reads. Refer to [dense vector retrieval](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#accessing-dense_vector-fields-in-search-responses) or [reindexing `semantic_text` while preserving embeddings](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-search-retrieval.md#reindex-while-preserving-embeddings), which requires the same `inference_id`. To regenerate embeddings, [prepare the destination inference endpoint](migrate-to-serverless-prepare.md#migrate-to-serverless-inference-endpoints) and index the input text through [`semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) or an [{{infer}} pipeline](/solutions/search/semantic-search/semantic-search-inference.md).
- **Ingest pipelines.** Check the request-selected, default, and final pipelines before copying already processed documents to avoid applying transformations twice. Use `pipeline=_none` to bypass the default pipeline. Any [final pipeline](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) still runs.
- **Transfer load.** Monitor source ingestion and query latency. Reduce the transfer rate or concurrency if production workloads are affected or the destination repeatedly returns `429`. Use [reindex throttling](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#docs-reindex-throttle) or adjust [{{ls}} batch sizes and parallel reads](/manage-data/migrate/migrate-with-logstash.md#additional-config). Review retry behavior and record failed documents.

:::

:::{dropdown} Example of copying a backing index with remote reindexing

Run this request in the destination project after creating the standalone index. Replace the source endpoint, API key, and both index names with your values.

```console
POST /_reindex
{
  "source": {
    "remote": {
      "host": "https://source.example.com:443",
      "api_key": "<SOURCE_ENCODED_API_KEY>"
    },
    "index": ".ds-logs-myapp-default-2026.10.01-000042"
  },
  "dest": {
    "index": "migration-logs-myapp-default-000042",
    "pipeline": "_none"
  }
}
```

Check the reindex response for failures. For the next backing index, change both index names.

:::

:::{dropdown} Example of copying a backing index with Logstash
:name: migrate-to-serverless-logstash-example

This example assumes log documents with an ISO 8601 `@timestamp` and no source `@version` field. The filter removes the `@version` field that {{ls}} adds. For other document structures, review the input plugin's [reserved-field handling](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-failure-handling).

Save the configuration as `migration.conf`. Replace the endpoints and set `SOURCE_API_KEY` and `DESTINATION_API_KEY` using the {{ls}} `id:api_key` format described in [Migrate data with {{ls}}](/manage-data/migrate/migrate-with-logstash.md).

```ruby
input {
  elasticsearch {
    hosts => ["https://source.example.com:443"]
    api_key => "${SOURCE_API_KEY}"
    index => ".ds-logs-myapp-default-2026.10.01-000042"
    query => '{"query":{"match_all":{}}}'
    ecs_compatibility => "disabled"
    docinfo => true
    docinfo_fields => ["_id"]
    docinfo_target => "[@metadata][migration]"
  }
}
filter {
  mutate {
    remove_field => ["@version"]
  }
}
output {
  elasticsearch {
    hosts => ["https://destination.example.com:443"]
    api_key => "${DESTINATION_API_KEY}"
    index => "migration-logs-myapp-default-000042"
    document_id => "%{[@metadata][migration][_id]}"
    action => "index"
    data_stream => false
    manage_template => false
    ilm_enabled => false
    pipeline => "_none"
  }
}
```

Run the transfer:

```bash
bin/logstash -f migration.conf
```

The input retrieves the source ID with `docinfo`, and the output preserves it with `document_id`. The output writes to the standalone index with `data_stream => false`. For the next backing index, change both `index` values. Review the {{ls}} logs for indexing failures even if the process exits successfully.

:::

:::{dropdown} Reindex a whole data stream in one pass
:name: migrate-to-serverless-reindex-data-stream

For a conventional data stream, you can [reindex directly into an empty destination data stream](/manage-data/data-store/data-streams/use-data-stream.md#reindex-with-a-data-stream). Specify the source and destination stream names and use `dest.op_type: "create"`. The destination manages its own rollovers and backing index boundaries. IDs reused across source backing indices can conflict in the destination. If you plan to run the transfer more than once, review the [risks of repeating writes through the stream name](#migrate-to-serverless-incremental-mechanisms).

:::

::::

::::{step} Verify and record the transfer
:anchor: migrate-to-serverless-verify-data

Review transfer failures and rejected documents. Refresh the destination indices. Compare source and destination document counts for the same data using `GET /<index>/_count`. Check representative documents, mappings, and query results as well. If the source changed during the copy, verify the contents against the data you expected to transfer.

:::{dropdown} Add verified backing indices to the destination stream
:name: migrate-to-serverless-add-backing-indices

If you copied backing indices to standalone indices, use the [update data streams API]({{es-serverless-apis}}operation/operation-indices-modify-data-stream) to add them. This is an expert-level API. Add only verified copies prepared for the intended stream.

```console
POST /_data_stream/_modify
{
  "actions": [
    {
      "add_backing_index": {
        "data_stream": "logs-myapp-default",
        "index": "migration-logs-myapp-default-000042"
      }
    }
  ]
}
```

Retrieve the destination stream definition to confirm membership.

:::

For any transferred data stream, query the stream by name to confirm that the historical data is available.

Recreate any [index or data stream aliases](/manage-data/data-store/aliases.md) after their targets exist. Check filters and write targets, and query through the aliases your applications use.

Record which sources and destinations you verified and which data or errors remain.

::::

:::::

## Incremental transfer mechanisms and limitations [migrate-to-serverless-incremental-mechanisms]

For when to consider incremental synchronization, refer to [Reduce the final transfer with incremental synchronization](migrate-to-serverless-production.md#migrate-to-serverless-incremental).

- **Add missing documents.** For a fixed destination index, preserve `_id` and use `create` to add only absent IDs. With reindex, use `dest.op_type: "create"` and `conflicts: "proceed"`. With {{ls}}, retrieve the source ID with `docinfo`, set the output's `document_id`, and set its `action` to `create`. Existing IDs produce conflicts. A final full scan can still take substantial time because the transfer reads and sends every selected document.
- **Reconcile updates and deletes.** Reindex's default `index` operation overwrites documents with matching IDs in a regular destination index. To account for documents deleted from the source, rebuild the destination copy or apply deletions separately.
- **Repeat a data stream transfer.** The same ID can exist in different backing indices of a conventional data stream. Repeating a transfer through the stream name after rollover can create duplicates. Keep a fixed source-to-destination index correspondence and finish the copy before adding the destination index to the stream. Direct `create` operations against an attached backing index are rejected. [TSDS](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) use generated IDs and timestamp-based routing and require separate handling.

Refer to the [reindex API]({{es-apis}}operation/operation-reindex) and [{{ls}} input field tracking](/manage-data/migrate/migrate-with-logstash.md#field-tracking) for available mechanisms. If you select changes by timestamp, choose a field that tracks arrivals or modifications. Event time alone can miss late arrivals. Test retries, updates, and deletes relevant to your workload before relying on incremental transfer.

Return to [Prepare and test the destination](migrate-to-serverless-prepare.md#migrate-to-serverless-data) or [Complete the migration and switch to production](migrate-to-serverless-production.md#migrate-to-serverless-final-transfer).
