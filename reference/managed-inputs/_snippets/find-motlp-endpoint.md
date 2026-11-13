To retrieve your {{motlp}} endpoint and generate an API key to authenticate your OTLP shipper, follow the steps for your environment.

:::::{applies-switch}
::::{applies-item} serverless:
**Find your endpoint**

1. Log in to the {{ecloud}} Console.
2. Find your project and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **OpenTelemetry**.
4. Copy the endpoint value.

:::{tip}
Alternatively, from within your project, go to **Add data**, select **Applications**, then **OpenTelemetry**, and copy the endpoint value. The Add data wizard also generates a pre-configured API key for authentication with the {{motlp}}.
:::
::::

::::{applies-item} ech:
**Find your endpoint**

1. Log in to the {{ecloud}} Console.
2. From the home page, find your deployment in **Hosted deployments**, and select **Manage**. Or, on the **Hosted deployments** page, select your deployment.
3. In the **Application endpoints, cluster and component IDs** section, select **Managed OTLP**.
4. Copy the public endpoint value.
::::
:::::
