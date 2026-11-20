---
navigation_title: Authentication, delivery, and failure handling
description: Learn how managed inputs share authentication, buffering and delivery, failure handling, and how network security applies on Serverless and Elastic Cloud Hosted.
type: overview
applies_to:
  serverless: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
---

# Authentication, delivery, and failure handling with managed inputs [authentication-delivery-and-failure-handling]

This page covers what all managed inputs share: how you authenticate, how data is stored for a limited time, how it is delivered, what happens when indexing fails, and how network security applies to your project or deployment. For protocol-specific setup, choose your endpoint in [Next steps](#next-steps).

## Authentication [authentication]

Managed inputs authenticate with an {{es}} API key that includes the `event:write` privilege for the `apm` application. The same `event:write` / `apm` privilege applies to every managed endpoint, including the OTLP, Prometheus Remote Write, and _bulk endpoints.

:::{note}
Index-level privilege scoping is not supported for managed inputs.
:::

You can create this API key in one of the following ways:

:::{dropdown} From the Add data page in {{kib}}
:applies_to: {"serverless": {"observability": "ga"}, "ech": "ga"}

1. Select **Add data** in the navigation menu of your Serverless Observability project or {{ech}} deployment.
2. In the **Connect directly to the endpoint** section, select the managed endpoint for which you want to create an API key.
3. Select **Create key**, then copy the encoded value from the **API key** field.
:::

:::{dropdown} From the API keys management page in {{kib}}
1. Go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create API key**, enter a name for the key, and enable **Control security privileges**.
3. In the role descriptors box, enter the following privileges:

    ```json
    {
      "managed-inputs-writer": {
        "applications": [
          {
            "application": "apm",
            "resources": ["*"],
            "privileges": ["event:write"]
          }
        ]
      }
    }
    ```

4. Select **Create API key** and copy the encoded value.

For more details, refer to [Elasticsearch API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md) and [Serverless project API keys](/deploy-manage/api-keys/serverless-project-api-keys.md).
:::

:::{dropdown} Using the Create API key API
Use the [Create API key API](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-security-create-api-key). The same request works for both {{serverless-full}} and {{ech}}. For example, to create an API key named `managed-inputs-api-key`:

```console
POST /_security/api_key
{
  "name": "managed-inputs-api-key",
  "role_descriptors": {
    "managed-inputs-writer": {
      "applications": [
        {
          "application": "apm",
          "resources": ["*"],
          "privileges": ["event:write"]
        }
      ]
    }
  }
}
```
:::

Send the encoded API key in the `Authorization` header of each request to the managed endpoint as `ApiKey <encoded-api-key>`. For example:

```http
Authorization: ApiKey <api-key>
```

{{product.elastic-agent}} is the exception: its `api_key` output setting takes the key as `<id>:<api_key>` and encodes it itself, so the encoded value results in `401` errors. The **Add data** page provides only the encoded value. To get the key as `<id>:<api_key>`, create it on the {{kib}} **API keys** page and, in the **Created API key** panel, select **Beats** from the format dropdown before you copy the key. Alternatively, join the `id` and `api_key` fields from the Create API key API response with a colon.

## Buffering and delivery [delivery]

Managed inputs buffer data before delivering it to {{es}}:

- Incoming data is stored (buffered) until it's delivered to {{es}}, and then it leaves the buffer. If {{es}} is lagging or temporarily unable to index, undelivered data can stay in the buffer for up to 12 hours. Delivered data isn't kept, so you can't replay it.
- A success response means the data was buffered, not yet indexed. Managed inputs retry delivery while {{es}} is temporarily unavailable or rejecting requests, which covers typical short interruptions. Retries and buffer retention are limited, so if {{es}} can't accept data for an extended period, for example during a prolonged outage or under sustained indexing pressure, data that couldn't be delivered in time is discarded. Because it never reached {{es}}, it isn't recorded in the failure store, and the success response your client already received isn't revised.
- Delivery time depends on {{es}}. Buffered data is indexed as fast as {{es}} accepts it, so the delay grows when {{es}} is slow or unavailable. Managed inputs don't expose ingestion health or delay metrics to you, so monitor the destination data streams to detect delays, especially during {{es}} maintenance.
- When capacity controls reject data, endpoints can respond with `429 Too Many Requests`, so clients should retry with backoff. Other temporary service failures can return `503 Service Unavailable`. Refer to [Managed inputs rate limiting](rate-limiting.md).

:::{note}
For the Managed {{es}} _bulk endpoint, documents with disallowed targets are rejected individually, and a `201` status on an item in the response means the document is enqueued, not indexed. For details, refer to [Delivery behavior](elasticsearch-bulk.md#delivery-behavior).
:::

## Indexing errors and the failure store [failure-store]

To confirm your data was indexed, verify that documents landed in the destination data stream, and use [Data Set Quality](/solutions/observability/data-set-quality-monitoring.md) to monitor and triage indexing issues.

A successful accept response from a managed input means the data was accepted for processing, not that {{es}} has indexed it. Indexing errors, such as mapping conflicts, malformed fields, or ingest pipeline errors, can happen asynchronously after the data is accepted, and aren't reported back to the client.

If the destination data stream has the [failure store](/manage-data/data-store/data-streams/failure-store.md) enabled, documents that fail indexing are written there. Managed inputs don't enable or manage the failure store. You configure the failure store on the destination data stream.

:::{warning}
If a document fails indexing and the destination data stream doesn't have the failure store enabled, the document is dropped. Because indexing errors happen after the data is accepted, your shipper still reports success, so this data loss is silent.
:::

## Network security [network-security]

Support for IP filters and private connectivity on managed endpoints depends on whether you use a {{serverless-full}} project or an {{ech}} deployment.

::::{applies-switch}

:::{applies-item} serverless:
In {{serverless-full}} projects, managed inputs follow the [network security policies](/deploy-manage/security/network-security-policies.md) applied to your project:

- [IP filters](/deploy-manage/security/ip-filtering-cloud.md) apply to managed endpoints.
- Managed endpoints are available over a private connection on supported cloud providers. For the current list, refer to [Private connectivity](/deploy-manage/security/private-connectivity.md).
:::

:::{applies-item} ech:
In {{ech}} deployments, the following limitations apply to managed inputs:

- [IP filters](/deploy-manage/security/ip-filtering-cloud.md) do not apply to managed endpoints.
- Managed endpoints are not available over a [private connection](/deploy-manage/security/private-connectivity.md). When private connectivity is configured, the public managed endpoint is still available.
:::

::::

## Next steps [next-steps]

After you understand authentication and delivery, configure the endpoint for your protocol:

- [Ingest OpenTelemetry data with the Managed OTLP endpoint](managed-otlp-endpoint.md)
- [Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](prometheus-remote-write.md)
- [Ingest data with the Managed {{es}} _bulk endpoint](elasticsearch-bulk.md)
