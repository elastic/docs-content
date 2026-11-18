---
navigation_title: "Managed Prometheus Remote Write endpoint"
description: "Ingest Prometheus metrics into Elasticsearch using the Prometheus Remote Write protocol through the Elastic Cloud Managed Prometheus Remote Write endpoint."
applies_to:
  stack: ga 9.4+
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

# Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint [prometheus-remote-write]

The Managed Prometheus Remote Write endpoint ingests metrics sent in the [Prometheus Remote Write v1](https://prometheus.io/docs/specs/remote_write_spec/) (PRW) protocol. It accepts PRW traffic natively, so you don't need to convert metrics to OTLP, and it's a dedicated [managed input](index.md) separate from the [Managed OTLP Endpoint](managed-otlp-endpoint.md). Metrics land in {{es}} time series data streams (TSDS), the same result as sending PRW directly to {{es}}.

## When to use the Managed Prometheus Remote Write endpoint

For {{serverless-full}} projects and {{ech}} deployments, the Managed Prometheus Remote Write endpoint is the recommended way to ingest Prometheus metrics. Compared to sending metrics directly to the [{{es}} Prometheus Remote Write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md), it provides:

- A single ingest endpoint and API key shared with the other [managed inputs](index.md).
- Durable buffering, back-pressure, and retry on `429 Too Many Requests`.
- The same Prometheus-to-TSDS mapping as the {{es}} PRW endpoint, so the resulting data is identical.

:::{warning}
On {{serverless-full}} and {{ech}}, use the Managed Prometheus Remote Write endpoint rather than sending metrics directly to the [{{es}} Prometheus Remote Write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).

Direct ingest bypasses managed inputs and has no buffering or processing before data reaches {{es}}. It also authenticates differently: the direct {{es}} endpoint uses {{es}} credentials or an API key with index privileges, while the Managed Prometheus Remote Write endpoint uses an API key with the `event:write` privilege for the `apm` application. Use the direct {{es}} endpoint only for self-managed deployments, where managed inputs aren't available.
:::

## Prerequisites

- A compatible Elastic environment:
   - An {{serverless-full}} Observability or Security project
   - {applies_to}`stack: ga 9.4+` An {{ech}} deployment
- An API key with the `event:write` privilege for the `apm` application. Refer to [Authentication](authentication-delivery-and-failure-handling.md#authentication) for the required key format and generation steps.

## Send Prometheus metrics through managed inputs

Follow these steps to configure Prometheus to send metrics to the Managed Prometheus Remote Write endpoint.

::::::{stepper}

:::::{step} Configure Prometheus

Add a `remote_write` entry to your Prometheus configuration:

```yaml
remote_write:
  - url: <prometheus-endpoint>
    authorization:
      type: ApiKey
      credentials: <api-key>
```

To find `<prometheus-endpoint>`:

1. Log in to the {{ecloud}} Console.
2. Do one of the following:
   - **{{serverless-full}}**: Find your project and select **Manage**.
   - **{{ech}}**: Find your deployment in **Hosted deployments** and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **Prometheus**.
4. Copy the **Prometheus** endpoint value.

:::::

:::::{step} Route metrics to custom data streams (optional)

By default, all PRW metrics land in `metrics-generic.prometheus-default`. You can control the target data stream using URL path parameters or per-time-series labels.

#### Route by URL path

Set the dataset and namespace using URL path parameters:

| Endpoint | Data stream |
| --- | --- |
| `/_prometheus/api/v1/write` | `metrics-generic.prometheus-default` |
| `/_prometheus/metrics/{dataset}/api/v1/write` | `metrics-{dataset}.prometheus-default` |
| `/_prometheus/metrics/{dataset}/{namespace}/api/v1/write` | `metrics-{dataset}.prometheus-{namespace}` |

For example, to route infrastructure metrics to a dedicated data stream, set the remote write URL to:

```yaml
remote_write:
  - url: "https://<es_endpoint>/_prometheus/metrics/infrastructure/production/api/v1/write"
```

This sends data to the `metrics-infrastructure.prometheus-production` data stream.

#### Route by labels

You can also route individual time series to different data streams by attaching the `data_stream_dataset` and `data_stream_namespace` labels to each time series:

| Label | Sets | Example |
| --- | --- | --- |
| `data_stream_dataset` | Dataset component of the data stream name | `myapp` |
| `data_stream_namespace` | Namespace component of the data stream name | `production` |

A time series with `data_stream_dataset: myapp` and `data_stream_namespace: production` routes to `metrics-myapp.prometheus-production`.

In Prometheus, use `write_relabel_configs` to add these labels to every time series sent to a `remote_write` target:

```yaml
remote_write:
  - url: <prometheus-endpoint>
    authorization:
      type: ApiKey
      credentials: <api-key>
    write_relabel_configs:
      - target_label: data_stream_dataset
        replacement: myapp
      - target_label: data_stream_namespace
        replacement: production
```

:::::

::::::

## How Prometheus data appears in {{es}}

Prometheus labels are mapped as TSDS dimensions in {{es}}, and metric types are inferred from field naming conventions:

- Fields ending in `_sum`, `_count`, `_total`, or `_bucket` are mapped as counters.
- All other fields are mapped as gauges.

For details on the full mapping behavior, refer to the [{{es}} Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md) documentation.

## Indexing errors and rate limiting

A successful response means your metrics were durably accepted for processing, not that {{es}} has indexed them. For what happens when indexing fails and how to verify your data was indexed, refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store).

For back-pressure and `429` responses, refer to [Managed inputs rate limiting](rate-limiting.md) and [Buffering and delivery](authentication-delivery-and-failure-handling.md#delivery).

## Limitations

- URL-path routing (for example, `/_prometheus/metrics/{dataset}/api/v1/write`) to custom data streams is not supported through managed inputs. Use [label-based routing](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#route-by-labels) instead.
- Samples with non-finite values (NaN, Infinity) are silently dropped by {{es}}, and staleness markers are not supported.
