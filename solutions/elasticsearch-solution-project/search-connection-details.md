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

:::::{applies-switch}

::::{applies-item} { "deployment": { "ech": "ga", "ece": "ga" }, "serverless": "ga" }
Your endpoint is in the **Connection details** panel in {{kib}}.

1. Open {{kib}} for your deployment or project.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Copy the **{{es}} endpoint** from the **Endpoints** tab.

:::{image} /solutions/images/kibana-connection-details-endpoints.png
:alt: The Connection details panel showing the Elasticsearch endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
:screenshot:
:width: 50%
:::

:::{tip}

* When the space uses the **{{es}}** solution view, the **Getting started** page shows the endpoint directly.
* {applies_to}`serverless: ga` You can also open **Connection details** from the project selector in the header.

:::

::::

::::{applies-item} {"deployment": {"self": "ga"}}
Your endpoint takes the form `<scheme>://<host>:<port>`. Each part comes from your cluster's HTTP settings:

* **Scheme**: `https` when TLS is enabled on the HTTP layer, and `http` when it isn't. [Automatic security setup](/deploy-manage/security/self-auto-setup.md) enables TLS on a new archive or package installation.
* **Host**: The address clients use to reach the node, set by [`http.host` or `network.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md).
* **Port**: The HTTP port, set by [`http.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md). It defaults to the range `9200-9300`, and a node binds to the first free port in that range.

For example, a single-node cluster from the [local development quickstart](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md) runs without TLS on the default port, so its endpoint is `http://localhost:9200`.

If clients reach your cluster through a load balancer, reverse proxy, or ingress, use that address rather than the node address.
::::

::::{applies-item} {"deployment": {"eck": "ga"}}
The {{eck}} operator creates a `ClusterIP` service named `<cluster-name>-es-http` on port `9200`, with TLS enabled by default.

From inside the Kubernetes cluster, your endpoint is `https://<cluster-name>-es-http:9200` in the same namespace, or `https://<cluster-name>-es-http.<namespace>.svc:9200` from another namespace. List your services to confirm the name:

```sh
kubectl get svc
```

To reach the cluster from outside, expose the service and use its external address. Refer to [Access the endpoint](/deploy-manage/deploy/cloud-on-k8s/accessing-services.md#k8s-request-elasticsearch-endpoint) for both cases, including how to retrieve the certificate authority (CA) certificate.
::::

:::::

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
To skip {{kib}}, select **Manage** in the {{ecloud}} console and copy the **Cloud ID** from the deployment page.
:::

## Create an API key [create-an-api-key-cloud-self-managed]

:::::{applies-switch}

::::{applies-item} { "deployment": { "ech": "ga", "ece": "ga" }, "serverless": "ga" }

1. Open {{kib}} for your deployment or project.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Select the **API key** tab.
4. In the **API key name** field, enter a name, then select **Create API key**.
5. Select an **API key format**: **Encoded** for {{es}} REST API requests, or **Beats** or **Logstash** to configure those products.
6. Copy the key. It isn't available after you close the panel.

Keys created here expire in 90 days and carry your own privileges. To set an expiration or restrict privileges, select **Manage API keys** and create the key there instead.
::::

::::{applies-item} {"deployment": {"eck": "ga", "self": "ga"}}
1. Go to the **API keys** management page, using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find it.
2. Select **Create API key**.
3. Enter a name, then select **Create API key**.
4. Copy the key. It isn't available after you leave the page.

Keys created here don't expire unless you add an expiration date.
::::

:::::

For key types, privileges, and expiration options, refer to [](/deploy-manage/api-keys.md).

## Test your connection [elasticsearch-get-started-test-connection]

Verify your endpoint and API key with a request to the {{es}} root endpoint.

1. In a terminal, assign your endpoint and encoded API key to environment variables:

    ```bash
    export ES_URL="https://a1b2c3d4e5f6.us-central1.gcp.cloud.es.io:443"
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
