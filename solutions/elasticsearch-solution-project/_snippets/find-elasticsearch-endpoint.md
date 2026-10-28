<!--
This snippet is in use in the following locations:
- solutions/elasticsearch-solution-project/search-connection-details.md
- solutions/search/set-up/api-key-and-endpoints.md
-->

:::::::{applies-switch}

::::::{applies-item} serverless: ga
Copy the {{es}} endpoint for your project from the project UI or the {{ecloud}} Console.

:::::{tab-set}

::::{tab-item} Project UI

1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), find your project and select **Open**.
2. From the **Help menu** {icon}`question` or the project selector in the header, select **Connection details**.
3. On the **Endpoints** tab, copy the **{{es}} endpoint**.

:::{image} /solutions/images/kibana-connection-details-endpoints.png
:alt: The Connection details panel showing the {{es}} endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
:screenshot:
:width: 50%
:::

::::

::::{tab-item} {{ecloud}} Console

1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), find your project and select **Manage**.
2. Under **Application endpoints**, select **{{es}}**.
3. Copy the **Direct endpoint** value.

:::{image} /solutions/images/cloud-console-serverless-endpoint.png
:alt: The Application endpoints panel in the {{ecloud}} Console, with {{es}} expanded to show the Direct endpoint and Direct Azure Private Link endpoint
:screenshot:
:width: 50%
:::

Azure and AWS also offer an endpoint you can use to connect to the deployment over a private connection. [Learn more about private connectivity](/deploy-manage/security/private-connectivity.md).

::::

:::::

::::::

::::::{applies-item} ech: ga
Copy the {{es}} endpoint for {{ech}} from the deployment UI or the {{ecloud}} Console.

:::::{tab-set}

::::{tab-item} {{kib}} UI

1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), find your deployment and select **Open**.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. On the **Endpoints** tab, copy the **{{es}} endpoint** value.

:::{image} /solutions/images/kibana-connection-details-endpoints.png
:alt: The Connection details panel showing the {{es}} endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
:screenshot:
:width: 50%
:::

:::{tip}
When the space uses the **{{es}}** solution view, the **Getting started** page shows the endpoint directly.
:::

::::

::::{tab-item} {{ecloud}} Console

1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), find your deployment and select **Manage**.
2. Under **Application endpoints, cluster and component IDs**, select **{{es}}**.
3. Copy the **Direct endpoint** value.

:::{image} /solutions/images/cloud-console-hosted-endpoint.png
:alt: The Application endpoints, cluster and component IDs panel in the {{ecloud}} Console, with {{es}} expanded to show the Endpoint, Direct endpoint, and Cluster ID
:screenshot:
:width: 50%
:::

::::

:::::

::::::

::::::{applies-item} ece: ga

:::::{tab-set}

::::{tab-item} {{kib}}

For {{ece}}, your endpoint details are in the **Connection details** panel in {{kib}}.

1. Open {{kib}} for your deployment.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Copy the **{{es}} endpoint** from the **Endpoints** tab.

:::{image} /solutions/images/kibana-connection-details-endpoints.png
:alt: The Connection details panel showing the {{es}} endpoint on the Endpoints tab, with the Show Cloud ID toggle and the API key tab
:screenshot:
:width: 50%
:::

:::{tip}
When the space uses the **{{es}}** solution view, the **Getting started** page shows the endpoint directly.
:::

::::

::::{tab-item} Cloud UI

To connect to your {{es}} cluster, copy the **{{es}} endpoint** from the deployment page in the [Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).

::::

:::::

::::::

::::{applies-item} {"deployment": {"self": "ga"}}
For a self-managed cluster, one you install and manage, your endpoint takes the form `<scheme>://<host>:<port>`. Each part comes from your cluster's HTTP settings:

* **Scheme**: `https` when TLS is enabled on the HTTP layer, and `http` when it isn't. TLS is enabled by default on first startup through [automatic security setup](/deploy-manage/security/self-auto-setup.md), unless the setup is [explicitly skipped](/deploy-manage/security/self-auto-setup.md#stack-skip-auto-configuration) or disabled, as in the local development quickstart.
* **Host**: The address clients use to reach the node, set by [`http.host` or `network.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md).
* **Port**: The HTTP port, set by [`http.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md). It defaults to the range `9200-9300`, and a node binds to the first free port in that range.

For example, a single-node cluster from the [local development quickstart](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md) runs without TLS on the default port, so its endpoint is `http://localhost:9200`.

If clients reach your cluster through a load balancer, reverse proxy, or ingress, use that address rather than the node address.
::::

::::{applies-item} {"deployment": {"eck": "ga"}}
The ECK operator automatically creates a service for your {{es}} cluster with TLS enabled. Your endpoint URL depends on where your application runs:

- **Inside the same Kubernetes namespace**: `https://<cluster-name>-es-http:9200`
- **In a different namespace**: `https://<cluster-name>-es-http.<namespace>.svc:9200`
- **Outside the Kubernetes cluster**: You need to expose the service first. Refer to [Access the endpoint](/deploy-manage/deploy/cloud-on-k8s/accessing-services.md#k8s-request-elasticsearch-endpoint) for setup steps.

To find your cluster name, run `kubectl get svc` and look for the service ending in `-es-http`.
::::

:::::::
