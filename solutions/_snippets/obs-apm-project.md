Bring application telemetry into Elastic APM to troubleshoot and optimize your applications. Use OpenTelemetry SDKs or Elastic APM agents to collect the data and send it to Elastic.

:::::{dropdown} Steps for collecting application traces, metrics, and logs

::::{tab-set}
:::{tab-item} OpenTelemetry

The [{{edot}} SDKs](opentelemetry://reference/edot-sdks/index.md) instrument your application and send OpenTelemetry data to Elastic {{product.apm}}.

1. Select **Add data** from the navigation menu, then select **Application** or **Applications**, depending on your version.
2. Select **OpenTelemetry**.
3. Follow the instructions for your platform.
:::

:::{tab-item} APM agents

Use the [APM agents](/solutions/observability/apm/apm-agents/index.md) to collect transactions, spans, errors, and metrics through {{apm-server-or-mis}}. Collect application logs separately or through supported OpenTelemetry instrumentation.

1. Select **Add data** from the navigation menu, then select **Application** or **Applications**, depending on your version.
2. Select **Elastic APM** or **APM**, depending on your version.
3. Select the tab for your language or framework.
4. Follow the instructions in the tab.
:::
::::
:::::