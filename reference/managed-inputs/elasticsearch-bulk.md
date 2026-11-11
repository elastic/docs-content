---
navigation_title: "Managed Elasticsearch _bulk endpoint"
description: "Ingest log data from Elasticsearch _bulk shippers through the Elastic Cloud Managed Elasticsearch _bulk endpoint, and decide when to choose direct Elasticsearch instead."
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
---

# Ingest data with the Managed {{es}} _bulk endpoint [elasticsearch-bulk]

The Managed {{es}} _bulk endpoint ingests data sent in the [{{es}} `_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) format. It accepts `_bulk` traffic natively, so shippers that already write to {{es}} can send data through [managed inputs](index.md) by pointing their existing {{es}} output at the endpoint. It's a dedicated managed input exposed on the `/_es` path of the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md) and the [Managed Prometheus Remote Write endpoint](prometheus-remote-write.md).

The endpoint is {{es}}-compatible: it emulates a subset of the `_bulk` API, so most shippers need only a new endpoint and credentials to start sending data. The managed input buffers the data and then indexes it into {{es}} asynchronously. Only log data is supported, and bulk actions must use the `create` action.

## When to use the Managed {{es}} _bulk endpoint [when-to-use]

The Managed {{es}} _bulk endpoint isn't a drop-in replacement for sending `_bulk` requests directly to {{es}}. It supports only part of the `_bulk` API: It accepts only the `create` action, and requests that use `index`, `update`, or `delete` fail with `400 Bad Request`. Because the managed endpoint buffers data before indexing it, it also acknowledges data earlier, reports failures differently, and can add latency. Use the following sections to decide which endpoint fits your workload.

### When to send data to the managed endpoint [when-managed]

- **You already use other managed inputs.** Your `_bulk` shippers can send data to the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md) and the [Managed Prometheus Remote Write endpoint](prometheus-remote-write.md), using the same API key.
- **Your ingest volume is spiky.** The managed endpoint absorbs short spikes well above the usual rate, so you don't need to size every shipper's output for peak load.

    On {{ech}}, volume that your cluster can't keep up with still results in `429` responses. Refer to [Managed inputs rate limiting](rate-limiting.md).

- **You want to limit local buffering on your shippers.** The managed endpoint buffers data while {{es}} is slow or unavailable, so your shippers need less local buffering. They still need to retry `429` and `503` responses, and a delay in indexing must be acceptable.

If you switch an existing shipper to the managed endpoint, compare document counts between what your shipper sends and the destination data stream for a period after the switch, and monitor the destination with [Data Set Quality](/solutions/observability/data-set-quality-monitoring.md).

### When to send data directly to {{es}} [when-direct]

- **You send data other than logs, or write logs to targets that don't start with `logs-`.** The managed endpoint supports only log data in `logs-*` data streams. Refer to [Limitations](#limitations).
- **Your {{product.elastic-agent}}s are managed by {{product.fleet}}.** {{product.fleet}}-managed outputs can't use the managed endpoint.
- **You need confirmation that data was indexed.** Your shipper must know that data was indexed before it marks the data as sent. The managed endpoint returns success when data is buffered. Delivery to {{es}} completes later, and data that can't be delivered before the buffer retention period ends is discarded. Refer to [Delivery behavior](#delivery-behavior).
- **You need predictable latency**, for example for alerting. The managed endpoint can add latency, and the delay grows when {{es}} is slow or unavailable.
- **You monitor ingestion with shipper metrics.** With the managed endpoint, those metrics tell you whether the endpoint accepted the data, not whether it was indexed. Managed inputs don't expose ingestion health or throughput metrics to you.
- **You need control over how data is batched and retried into {{es}}.** Batch size, flush interval, retries, and worker count are fixed on the managed side.
- **You use IP filters or private connectivity on {{ech}}.** IP filters don't apply to the managed endpoint, and it isn't available over private connections. Refer to [Network security](authentication-delivery-and-failure-handling.md#network-security) for more information.

For the full list of constraints, refer to [Limitations](#limitations).

## Prerequisites [prerequisites]

- An {{serverless-full}} Observability or Security project, or an {{ech}} deployment on {{stack}} version 9.0 or later.
- A `_bulk`-compatible shipper that sends `create` actions to log data streams, such as standalone {{product.elastic-agent}}, {{product.logstash}}, or another shipper with an {{es}} output.
- An API key with the `event:write` privilege for the `apm` application. Refer to [Authentication](authentication-delivery-and-failure-handling.md#authentication) for the required key format and generation steps.
- Any {{es}} index templates and {{kib}} assets your shipper relies on, installed beforehand. The endpoint doesn't install them for you. Refer to [Limitations](#limitations).

## Set up the Managed {{es}} _bulk endpoint [set-up]

The Managed {{es}} _bulk endpoint uses the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md), with the `/_es` path appended. Its exact format depends on your deployment type. Copy the exact value from the {{ecloud}} Console, as described in the following steps.

::::::{stepper}

:::::{step} Find your endpoint

To find your Managed {{es}} _bulk endpoint:

::::{applies-switch}

:::{applies-item} serverless:
1. Log in to the {{ecloud}} Console.
2. Find your project and select **Manage**.
3. In the **Application endpoints** section, select **{{es}}**. A flyout opens that lists the endpoints for each application as expandable sections, with **{{es}}** expanded.
4. Copy the {{es}} **Endpoint** value. Don't use the **Direct endpoint** value, which is the endpoint for sending data directly to {{es}}.
:::

:::{applies-item} ech:
1. Log in to the {{ecloud}} Console.
2. Find your deployment in **Hosted deployments** and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **{{es}}**. A flyout opens that lists the endpoints for each application as expandable sections, with **{{es}}** expanded.
4. Copy the {{es}} **Endpoint** value. Don't use the **Direct endpoint** value, which is the endpoint for sending data directly to {{es}}.
:::

::::

This endpoint value is shown as `<managed-_bulk-endpoint>` in the examples that follow. Your shipper appends the `_bulk` path (and any target index path) itself, so requests are sent to `POST <managed-_bulk-endpoint>/_bulk`.

:::::

:::::{step} Authenticate

Create an API key suitable for managed inputs as described in [Authentication](authentication-delivery-and-failure-handling.md#authentication). Send this key in each request's `Authorization` header as `ApiKey <api-key>`:

```http
Authorization: ApiKey <api-key>
```

Shippers that call `GET /_es` or `GET /_es/_license` at startup can use the same API key. You don't need to grant additional privileges for those requests.

:::::

:::::{step} Configure your shipper and send data

To send data, configure your shipper's {{es}} output with the following:

- **Endpoint**: Use your Managed {{es}} _bulk endpoint value (`<managed-_bulk-endpoint>`) in the host format for your deployment type.
   - If your shipper has a separate path or URL-prefix setting, set it to `/_es` instead of including it in the host.
   - The {{product.logstash}} and {{product.elastic-agent}} `elasticsearch` outputs use port `9200` when the host URL omits a port, so add `:443` before the `/_es` path, for example `https://<host>:443/_es`.
- **Authentication**: The API key you created for the managed inputs. How you pass it depends on the key format you have:
   - If you have the encoded key, for example from the **Add data** page in {{kib}}, send it as the HTTP header `Authorization: ApiKey <api-key>`. This works with any shipper. Refer to [Authentication](authentication-delivery-and-failure-handling.md#authentication) for the ways to create a key.
   - If you have the key as `<id>:<api_key>`, use the `api_key` setting in {{product.logstash}} or standalone {{product.elastic-agent}}.
- **Action**: Use `create`. Shippers that write to data streams already use this action.

The following examples show the configuration for {{product.logstash}} and standalone {{product.elastic-agent}}. Setting names and the exact way to pass credentials vary by shipper and version, so validate the configuration for your shipper.

::::{dropdown} {{product.logstash}} example
Configure the `elasticsearch` output:

```ruby
output {
  elasticsearch {
    hosts => ["<managed-_bulk-endpoint>"] <1>
    api_key => "<id>:<api_key>"
    action => "create"
  }
}
```

1. Add `:443` before `/_es`, for example `https://<host>:443/_es`.

When you create the API key on the {{kib}} **API keys** page, select **Logstash** from the format dropdown in the **Created API key** panel before you copy it, or join the `id` and `api_key` fields from the Create API key API response with a colon.

If you only have the encoded key, for example if you generated it from the **Add data** page, replace the `api_key` setting with `custom_headers` and pass the key in the `Authorization` header:

```ruby
custom_headers => {
  "Authorization" => "ApiKey <api-key>"
}
```

:::{warning}
By default, {{product.logstash}} indefinitely retries documents that the endpoint rejects with a `403` status, which can stall the pipeline. The endpoint rejects documents this way when their target isn't allowed. Refer to [Delivery behavior](#delivery-behavior).

If the dead letter queue is enabled, add `403` to `dlq_custom_codes` to send these documents there. To drop them instead, add `security_exception` to `drop_error_types`.
:::
::::

::::{dropdown} Standalone {{product.elastic-agent}} example
Configure the `elasticsearch` output. {{product.elastic-agent}} encodes the `<id>:<api_key>` value itself, so the encoded value from the **Add data** page results in `401` errors. When you create the key on the {{kib}} **API keys** page, select **Beats** from the format dropdown in the **Created API key** panel before you copy it, or join the `id` and `api_key` fields from the Create API key API response with a colon:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["<managed-_bulk-endpoint>"] <1>
    api_key: "<id>:<api_key>"
```

1. Add `:443` before `/_es`, for example `https://<host>:443/_es`.
::::

If your shipper uses the `index`, `update`, or `delete` action, switch to `create`. Refer to [Limitations](#limitations) for more information.

To confirm your setup is working, check that your shipper reports successful (`2xx`) responses, with no authentication errors and no documents rejected with a `403` status. Then open **Discover** and verify that new documents are landing in your target data stream.

If documents don't appear, they might have failed during asynchronous indexing. These errors aren't reported in the bulk response, so use [Data Set Quality](/solutions/observability/data-set-quality-monitoring.md) to monitor and triage indexing issues. For more details, refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store).

:::::

::::::

## How _bulk data appears in {{es}} [data-mapping]

Each action in a `_bulk` request can specify its target through the `_index` field, so data lands in the data stream that your shipper already targets. For example, a shipper writing nginx access logs to `logs-nginx.access-default` continues to land there. If your shipper sets a fallback target in the request path (`/_es/<target>/_bulk`), that target is used for actions that omit `_index`. Only log data streams are supported targets. Refer to [Limitations](#limitations) for more information.

## Delivery behavior [delivery-behavior]

The Managed {{es}} _bulk endpoint emulates the {{es}} `_bulk` API, but because it ingests through managed inputs, it behaves differently from indexing directly into {{es}}. Keep the following in mind:

- **Documents with disallowed targets are rejected individually.** A document whose target doesn't start with `logs-`, `metrics-`, or `traces-` gets a `403` status with a `security_exception` error in its response item, and the response sets `errors: true`. The other documents in the request are still accepted. The response is `200 OK` even if every document is rejected, so check `errors` and the status of each item. For allowed targets, refer to [Limitations](#limitations).
- **Rejected documents are handled by your shipper.** {{product.elastic-agent}} drops a rejected document and logs a warning. {{product.logstash}} retries it indefinitely by default. To change this, refer to the {{product.logstash}} example in [](#configure-your-shipper-and-send-data).
- **Accepted documents are enqueued together.** The endpoint either enqueues all accepted documents in a request, or fails the entire request. If they can't be enqueued, the whole request fails with `503 Service Unavailable`, and no document is reported as successful. Malformed requests, unsupported actions, or missing targets fail with `400 Bad Request`, and nothing in the request is enqueued.
- **A success response means the data is enqueued, not indexed.** A successful response returns an {{es}}-compatible body in which each accepted item reports a `201` status. This confirms the managed input accepted the document, not that {{es}} has indexed it. Errors that occur later during indexing, such as mapping conflicts, happen asynchronously and aren't reported in the bulk response. Your shipper counts these documents as sent.
- **Undelivered data is discarded.** The endpoint retries delivery while {{es}} is briefly unavailable or rejecting requests. If {{es}} still can't accept the data when buffer retention ends, the endpoint discards it. The success response your shipper already received doesn't change.
- **Delivery delay isn't visible to your shipper.** A direct `_bulk` request slows down or fails when {{es}} is under pressure, so your shipper can retry or back off. The managed endpoint returns success as soon as the batch is enqueued, even if delivery to {{es}} is delayed.
- **`require_data_stream` and `require_alias` are ignored.** The endpoint doesn't enforce these query parameters, so they don't protect you from writing to an unintended target the way they do with {{es}}, although targets outside the allowed prefixes are rejected anyway.
- **Compressed requests are supported.** The endpoint accepts `Content-Encoding: gzip` request bodies.

For how long undelivered data can stay in the buffer, and what happens to it after that, refer to [Buffering and delivery](authentication-delivery-and-failure-handling.md#delivery).

## Indexing errors and rate limiting [indexing-errors-and-rate-limiting]

Because indexing happens asynchronously, indexing failures such as mapping conflicts aren't reported in the bulk response, and the endpoint doesn't provide client-side visibility into them. To confirm your data was indexed, verify that documents landed in the destination data stream and use [Data Set Quality](/solutions/observability/data-set-quality-monitoring.md) to monitor indexing issues. For more detail on how indexing errors are handled, refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store).

Under load, or when the service can't accept more data, the endpoint can respond with `429 Too Many Requests` or `503 Service Unavailable`. Configure your shipper to retry these responses with backoff and to queue data locally during transient rejections. For how rate limiting works and how it differs between {{serverless-full}} and {{ech}}, refer to [Managed inputs rate limiting](rate-limiting.md).

## Limitations [limitations]

The following limitations apply when using the Managed {{es}} _bulk endpoint:

- **Only log data is supported.** It must target `logs-*` data streams, for example `logs-my_dataset-default`. The endpoint accepts only targets that start with `logs-`, `metrics-`, or `traces-`, and rejects any other target, including wired streams such as `logs.otel` and system indices, with a `403` status in the response item. `metrics-*` and `traces-*` targets are accepted but not supported. To send metrics and traces, use the direct {{es}} endpoint. For OpenTelemetry data, use the [Managed OTLP Endpoint](managed-otlp-endpoint.md).
- **{{product.beats}} aren't supported with their default settings.** They write to `<beat>-*` indices such as `filebeat-*` by default, which the endpoint rejects with a `403` status for each document.
- **Only `create` actions are supported.** Requests that use `index`, `update`, or `delete` actions are rejected with `400 Bad Request`. Features that depend on other actions, such as scripted upserts, aren't supported.
- **`require_data_stream` and `require_alias` aren't enforced.** Refer to [Delivery behavior](#delivery-behavior).
- **Duplicate detection isn't applied.** The endpoint doesn't deduplicate documents by `_id`, so client retries can produce duplicate documents.
- **Indexing outcomes aren't reported to your shipper.** The bulk response confirms that data was enqueued, not indexed, so errors such as mapping conflicts never reach your shipper. Managed inputs don't expose ingestion health metrics either, so monitor indexing with [Data Set Quality](/solutions/observability/data-set-quality-monitoring.md).
- **Delivery settings on the managed side aren't configurable.** Batching, flush intervals, retries, and worker counts are fixed, unlike the equivalent settings of a shipper's {{es}} output.
- **{{product.fleet}}-managed {{product.elastic-agent}} outputs can't use the endpoint.** {{product.fleet}} issues its agents {{es}} API keys with index privileges, which the endpoint doesn't accept. Only shippers you configure yourself, such as standalone {{product.elastic-agent}} and {{product.logstash}}, can use an API key for managed inputs.
- **Index templates, index lifecycle management (ILM) policies, and {{kib}} assets can't be installed through the endpoint.** It serves only the root (`/_es`), license (`/_es/_license`), and `_bulk` paths (`/_es/_bulk` and `/_es/<target>/_bulk`). {{product.elastic-agent}} and {{product.logstash}} setup steps that create index templates or load dashboards must run against {{es}} and {{kib}} directly before you send data.
- **IP filters and private connectivity depend on your deployment type.** For how they apply to all managed inputs, refer to [Network security](authentication-delivery-and-failure-handling.md#network-security).

## Related pages [related-pages]

- [Authentication, delivery, and failure handling with managed inputs](authentication-delivery-and-failure-handling.md): Shared authentication, buffering and delivery, and indexing-error handling across all managed inputs.
- [Managed inputs rate limiting](rate-limiting.md): How `429` responses work and how capacity limits differ between {{serverless-full}} and {{ech}}.
