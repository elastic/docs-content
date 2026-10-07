---
navigation_title: Find connection details
description: Find your Elasticsearch endpoint and create an API key so that client applications and tools can connect to your cluster or project.
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html
applies_to:
  stack:
  serverless:
products:
  - id: kibana
  - id: elasticsearch
type: how-to
---

# Find connection details [search-space-connection-details]

To connect a client application or a third-party tool to {{es}}, you need two things: the {{es}} endpoint URL, and credentials that authenticate the request. For secure connections, use an API key.

## Before you begin [before-you-begin]

To create an API key, you need the `manage_api_key` or the `manage_own_api_key` cluster privilege.

## Find your {{es}} endpoint [find-endpoint-cloud-self-managed]

::::{include} _snippets/find-elasticsearch-endpoint.md
::::

### Find your Cloud ID [find-cloud-id-cloud-self-managed]

```{applies_to}
deployment:
  ech: ga
  ece: ga
serverless: ga
```

[{{beats}}](beats://reference/index.md) and [{{ls}}](logstash://reference/index.md) can use a Cloud ID instead of the endpoint URL. All other clients and tools use the endpoint.

1. Open {{kib}} for your deployment or project.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Turn on **Show Cloud ID**, then copy the value.

    :::{image} /solutions/images/kibana-serverless-connection-details.png
    :alt: serverless connection details
    :screenshot:
    :width: 50%
    :::

:::{tip}
:applies_to: {ech: ga}
To skip {{kib}}, select **Hosted** in the {{ecloud}} Console, open your deployment, and copy the **Cloud ID** from the deployment page.
:::

## Create an API key [create-an-api-key-cloud-self-managed]

::::{include} _snippets/create-an-api-key.md
::::

For key types, privileges, and expiration options, refer to [](/deploy-manage/api-keys.md).

## Test your connection [elasticsearch-get-started-test-connection]

Verify your endpoint and API key with a request to the {{es}} root endpoint.

1. In a terminal, assign your endpoint and encoded API key to environment variables:

    ```bash
    export ES_URL="https://my-deployment-a1b2c3.es.us-central1.gcp.elastic-cloud.com"
    export API_KEY="ZFZRbF9Jb0JDMEoxaVhoR2pSa3Q6dExwdmJSaldRTHFXWEp4TFFlR19Hdw=="
    ```

2. Send the request:

    ```bash
    curl "${ES_URL}" -H "Authorization: ApiKey ${API_KEY}"
    ```

A successful response returns your cluster details:

```json
{
  "name" : "instance-0000000000",
  "cluster_name" : "my-deployment",
  "cluster_uuid" : "ws0IbTBUQfigmYAVMztkZQ",
  "version" : { ... },
  "tagline" : "You Know, for Search"
}
```

:::{note}
:applies_to: {eck: ga, self: ga}
If your cluster uses a self-signed certificate, pass your CA certificate with `curl --cacert`. Refer to [Automatic security setup](/deploy-manage/security/self-auto-setup.md) for the certificate location.
:::

## Next steps

* [Connect a client library](/reference/elasticsearch-clients/index.md) in your language of choice.
* [Ingest data](/solutions/search/ingest-for-search.md) into your cluster or project.
* [Build search queries](/solutions/search/querying-for-search.md) against your data.

## Related pages

* [Configure Beats and {{ls}} with a Cloud ID](/deploy-manage/deploy/elastic-cloud/find-cloud-id.md)
* [Connect to {{es}} on {{ece}}](/deploy-manage/deploy/cloud-enterprise/connect-elasticsearch.md)
* [Securing HTTP client applications](/deploy-manage/security/httprest-clients-security.md)
