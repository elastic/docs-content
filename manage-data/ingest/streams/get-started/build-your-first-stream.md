---
navigation_title: Build your first stream
description: Build your first stream. Create an OTLP source, connect it to an Elasticsearch destination, send test data, then add a processor and verify the change.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Build your first stream

A stream is a path from a source to a destination. In this tutorial you build one. You create a source that your shippers send to, connect it to an {{es}} destination, send a few test records and check that they arrive, then add a processor and watch it change the data before it's stored. By the end, you can see data flowing on the Streams Map and find the processed records in **Discover**.

The tutorial uses OpenTelemetry Protocol (OTLP) over HTTP because it needs nothing more than `curl`. A source can also accept Prometheus Remote Write requests or JSON documents sent with the {{es}} bulk API. Those paths have their own pages under [Sources](../sources.md).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

Delivery is best effort, so keep your existing ingest path running and don't send anything through Streams that you can't afford to lose or replay. Read [Streams limitations](../limitations.md) before you start.

## Before you begin [streams-first-stream-prereqs]

To build your first stream, you need:

* The **Admin** role. Refer to [Privileges and API keys](../security.md#streams-security-view-edit).
* Something that sends OTLP over HTTP. `curl` is enough for this tutorial, which also shows an OpenTelemetry Collector exporter and the `telemetrygen` tool from the OpenTelemetry Collector Contrib project.

## Build the stream [streams-first-stream-build]

Each step builds on the one before it, so follow them in order:

::::::{stepper}

:::::{step} Open the Streams Map
:anchor: streams-first-stream-open

Everything in this tutorial happens on the Streams Map. To open it, find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.

The Map opens with a toolbar at the bottom that has **Source** and **Destination** buttons for adding nodes, and **Undo**, **Redo**, and zoom controls. Once you've added nodes, the Map shows every source, pipeline, router, and destination in your project as connected nodes, and a stream is any path from a source to a destination.
:::::

:::::{step} Create a source
:anchor: streams-first-stream-source

A source is the endpoint your shippers send to. Each source has its own URL and API key.

1. Select **Source** in the toolbar at the bottom of the Map. On an empty Map, **Add source** in the middle opens the same dialog.
1. For **Source type**, select **OTLP endpoint**.
1. Enter a **Source name**, for example `my-otlp`. The type and name can't be changed later. Streams derives the source's ID, which appears in its endpoint URLs, from the name. Refer to [Endpoints and API keys](../sources.md#streams-sources-endpoints-keys).
1. Under **Signals**, keep **Logs**, **Metrics**, and **Traces** selected. There's no endpoint for a signal you don't select.
1. Select **Continue**. Streams saves the source and generates its API key.
1. Copy the **Logs endpoint**, **Metrics endpoint**, and **Traces endpoint** URLs and the **API key**, and store them somewhere safe. The key is shown only once. If you lose it, open the source from the **Sources** tab and generate a new key.
1. Select **Done**.

The source appears on the Map as a node that shows its name, **OTLP endpoint**, the three signals, and **Waiting for data...** until the first record is accepted. The dialog also shows a **Send data using** section with ready-made configuration for an OpenTelemetry Collector and for the OpenTelemetry Kubernetes Operator, with the endpoint and key filled in. To send from one of those instead of the test tools in this tutorial, refer to [OTLP source](../sources/otlp.md#streams-otlp-source-send).

::::{tip}
Copy the endpoint URLs from the dialog rather than typing them. An OTLP source's endpoints have the form `https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>/v1/<signal>`, where `<signal>` is `logs`, `metrics`, or `traces`.
::::
:::::

:::::{step} Create a destination
:anchor: streams-first-stream-destination

A destination is where data lands. For your first stream, write to the {{serverless-short}} project you're working in.

1. On the Map, select **Destination**.
1. Under **Where will this destination's data live?**, select **Local Elasticsearch**.
1. For **Index mode**, keep **Auto (default)**. In Auto mode, each record chooses its own data stream, within the destination's write patterns. Select **Fixed index per signal** only if you want every record of a signal in one data stream that you name.
1. Enter a **Destination name**, for example `my-elasticsearch`. Destinations can't be edited after you create them.
1. Optionally, add a **Description**.
1. Select **Create destination**.

The destination appears on the Map with **No source** under its name, because nothing is connected to it yet. Streams creates an API key for the destination that can write only within the destination's allowed write patterns. You don't manage this key. For details, refer to [Local Elasticsearch destination](../destinations/elasticsearch.md).
:::::

:::::{step} Connect the source to the destination
:anchor: streams-first-stream-connect

Data flows only along connections you draw and save:

1. On the Map, drag from the handle on the source node to the destination node.
1. Select **Save changes**.

The line under the destination's name changes from **No source** to **Auto**, its index mode, or to the description if you entered one, and the node shows **Data not flowing in** until data arrives. Nothing runs until you save, and saved changes apply to live data right away.
:::::

:::::{step} Send data to the source
:anchor: streams-first-stream-send

Use the API key and endpoint from [Create a source](#streams-first-stream-source). Every request carries the header `Authorization: ApiKey <key>`. Send with whichever of the following you have at hand:

::::{tab-set}

:::{tab-item} curl

One request sends one log record. Paste the source's logs endpoint URL as copied, including `https://` and the path:

```bash
LOGS_URL='https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>/v1/logs'
API_KEY='<api key>'

curl -sS -X POST "$LOGS_URL" \
  -H 'Content-Type: application/json' \
  -H "Authorization: ApiKey $API_KEY" \
  -d '{"resourceLogs":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"streams-test"}}]},"scopeLogs":[{"logRecords":[{"timeUnixNano":"'"$(date +%s)"'000000000","severityText":"INFO","body":{"stringValue":"hello from Streams"}}]}]}]}'
```

:::

:::{tab-item} OpenTelemetry Collector

Add an `otlphttp` exporter that points at the source and use it in your pipelines. This is the configuration the source dialog shows under **Send data using** → **OTel Collector**. The exporter appends `/v1/logs`, `/v1/metrics`, and `/v1/traces` to the endpoint.

```yaml
exporters:
  otlphttp/elastic:
    endpoint: "https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/my-otlp"
    headers:
      Authorization: "ApiKey <api key>"
    sending_queue:
      enabled: true

service:
  pipelines:
    logs:
      receivers: [otlp]
      exporters: [otlphttp/elastic]
    metrics:
      receivers: [otlp]
      exporters: [otlphttp/elastic]
    traces:
      receivers: [otlp]
      exporters: [otlphttp/elastic]
```
:::

:::{tab-item} telemetrygen

To see throughput on the Map, send a couple of minutes of synthetic logs with the `telemetrygen` tool from the OpenTelemetry Collector Contrib project:

`telemetrygen` takes the host and the path separately, so split the logs endpoint URL in two:

```bash
INGEST_HOST='<project>.ingest.<region>.<provider>.elastic.cloud'
SOURCE_ID='<source-id>'
API_KEY='<api key>'

telemetrygen logs --otlp-http --otlp-endpoint "$INGEST_HOST" \
  --otlp-http-url-path "/inputs/otlp/$SOURCE_ID/v1/logs" \
  --otlp-header "Authorization=\"ApiKey $API_KEY\"" \
  --otlp-attributes 'service.name="streams-test"' \
  --workers 20 --duration 2m
```

By default, each worker sends one record per second. Add workers or set `--rate` to send more.
:::

::::

A `200` response with an empty body means the source accepted the records. Where they went is what you check next.
:::::

:::::{step} Check that data arrives
:anchor: streams-first-stream-verify

Within a minute of the first request, you can see the data in two places:

1. On the Map, the source node switches from **Waiting for data...** to **Live** with the rate of accepted records, and the destination node switches from **Data not flowing in** to a rate and the average time a write took. Statistics refresh every 30 seconds and cover the last 15 minutes, so a short delay after the first request is normal, and a single `curl` request shows as `<0.01/s`. The index count next to the state is the number of indices and data streams in the project that match the destination's write patterns, not what this stream wrote, so it can be high before your data arrives.
1. Go to **Discover**, select **Query in ES|QL** in the application menu if the editor isn't in {{esql}} mode yet, then paste the following query and select **Run**. In Auto mode, a record that carries `data_stream.dataset` and `data_stream.namespace` attributes lands in `logs-<dataset>.otel-<namespace>`, and a record without them, like the ones in this tutorial, lands in the default data stream for its signal. Refer to [How Auto mode picks a data stream](../destinations/elasticsearch.md#streams-es-destination-auto-data-stream).

   ```esql
   FROM logs-*
   | WHERE resource.attributes.service.name == "streams-test"
   | SORT @timestamp DESC
   | LIMIT 10
   ```

   The results include the records you sent, with `hello from Streams` as the body of the `curl` one. If you get **No results match your search criteria**, widen the time range first, then refer to [Troubleshooting](#streams-first-stream-troubleshoot). For more on the editor, refer to [Switch to ES|QL mode in Discover](/explore-analyze/discover/switch-esql-mode.md).

If data doesn't arrive, refer to [Troubleshooting](#streams-first-stream-troubleshoot).
:::::

:::::{step} Add a processor
:anchor: streams-first-stream-process

A pipeline is a sequence of processors that runs on data before it reaches a destination. Processors run in Elastic-managed OpenTelemetry Collectors, so nothing changes in your shippers or in {{es}}.

1. On the Streams Map, hover over the connection between the source and the destination, select the {icon}`plus_circle` plus icon that appears on it, then select **Add processing**. A pipeline node appears on the connection and the **Processing** panel opens.
1. Select **Add processor**, then select **Add fields** from the **Processor** list. Its effect is the easiest to spot in **Discover**.
1. Under **Signals**, select **Logs**.
1. Under **Fields**, add one row with **Location** `Attributes`, **Name** `environment`, **Value** `staging`, and **Action** `Upsert`. Leave **Condition** empty so the field is added to every record.
1. Select **Create**, then **Save and apply**.

The pipeline node, marked with the {icon}`processor` processor icon, sits on the connection between the source and the destination. Its statistics stay empty until records pass through it. From now on, every log record that passes through it carries `attributes.environment: staging`. There's no way to test a processor against sample data first, so the next step checks the result on real data.

For the processors available and how to write OTTL conditions, refer to [Process data](../process-data.md).
:::::

:::::{step} Check that the processor ran
:anchor: streams-first-stream-verify-processor

Processors change only the data that arrives after you save, so send more:

1. Run the `curl` command from [Send data to the source](#streams-first-stream-send) again, or let `telemetrygen` keep running.
1. On the Map, look at the pipeline node. Once records pass through it, it shows a rate per second and the average time a record spends in it.
1. In **Discover**, run the same query as before. The newest records have `attributes.environment` set to `staging`, and the records from before you added the processor don't.

Your first stream is complete. Data flows from a source through a pipeline to a destination.
:::::

::::::

## Troubleshooting [streams-first-stream-troubleshoot]

These are the three problems you're most likely to run into while following this tutorial:

* The source returns `404 page not found`. The URL path is wrong. It must contain `/inputs/otlp/<source-id>/v1/<signal>`, with the source ID exactly as shown in the source's endpoint URLs. Refer to [The source returns 404](../troubleshooting.md#streams-troubleshoot-404).
* The source returns `401`. The `Authorization: ApiKey <key>` header is missing, malformed, or uses a key that was deleted. Refer to [The source returns 401](../troubleshooting.md#streams-troubleshoot-401).
* Requests succeed but nothing appears in **Discover**. Check that the source is connected to the destination and that you selected **Save changes**, then widen the time range. Refer to [Requests succeed but nothing appears in Discover](../troubleshooting.md#streams-troubleshoot-no-data).

For `403`, gRPC, destinations that stop receiving data, and everything else, refer to [Troubleshoot Streams](../troubleshooting.md).

## Clean up [streams-first-stream-clean-up]

When you're done testing, remove what you built so the test source doesn't keep accepting data:

1. On the Streams Map, select the pipeline node. In the **Processing** panel, select the {icon}`trash` **Delete all processors** icon, confirm, and select **Save and apply**. The pipeline node disappears. A pipeline that's left without a source or a destination blocks saving, so it has to go first.
1. Select the source node and press {kbd}`del`, then do the same for the destination node.
1. Select **Save changes**.

Deleting the source invalidates its API key, so the `curl` command from [Send data to the source](#streams-first-stream-send) returns `401` from now on. If you'd rather keep the stream, leave it as it is and point a real shipper at the source instead.

## Next steps [streams-first-stream-next]

* Add a second destination and a router to send a copy of the data to it. Hover over the connection to your destination, select the {icon}`plus_circle` plus icon that appears on it, then select **Add routing**. Refer to [Route data](../route-data.md).
* Add an Amazon S3 destination, the **External storage** choice in the dialog, to write newline-delimited JSON to a bucket you own. Refer to [Amazon S3 destination](../destinations/s3.md).
* Send Prometheus Remote Write metrics or {{es}} bulk documents to a source of the matching type. Refer to [Sources](../sources.md).
* Read [How Streams works](how-streams-work.md) for how sources, pipelines, routers, and destinations fit together, and [Streams limitations](../limitations.md) for what Streams doesn't support.
