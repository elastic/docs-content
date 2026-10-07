<!--
This snippet is in use in the following locations:
- solutions/elasticsearch-solution-project/search-connection-details.md
- solutions/search/set-up/api-key-and-endpoints.md
-->

:::::{applies-switch}

::::{applies-item} serverless: ga
Your endpoint details are on your project's page in the {{ecloud}} Console.

:::{include} /deploy-manage/deploy/elastic-cloud/_snippets/find-endpoint-serverless-console.md
:::

:::{tip}
You can also find your endpoint details in {{kib}}. From the **Help menu** {icon}`question` or the project selector in the header, select **Connection details**, then copy the **{{es}} endpoint** from the **Endpoints** tab.
:::
::::

::::{applies-item} ech: ga
Your endpoint details are on your deployment's page in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

1. In the {{ecloud}} Console, select **Hosted**.
2. Select your deployment.
3. Under **Application endpoints, cluster and component IDs**, select **{{es}}**.
4. Copy the **Endpoint** value.

    :::{image} /solutions/images/cloud-console-hosted-endpoint.png
    :alt: The Elasticsearch panel on a hosted deployment page in the Elastic Cloud Console, showing the Endpoint value with a copy button
    :screenshot:
    :width: 50%
    :::

:::{tip}
You can also find your endpoint details in {{kib}}. From the **Help menu** {icon}`question`, select **Connection details**, then copy the **{{es}} endpoint** from the **Endpoints** tab.
:::
::::

::::{applies-item} ece: ga
Your endpoint details are in the **Connection details** panel in {{kib}}.

1. Open {{kib}} for your deployment.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Copy the **{{es}} endpoint** from the **Endpoints** tab.

:::{image} /solutions/images/kibana-connection-details-endpoints.png
:alt: The Connection details panel showing the Elasticsearch endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
:screenshot:
:width: 50%
:::

:::{tip}
When the space uses the **{{es}}** solution view, the **Getting started** page shows the endpoint directly.
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
