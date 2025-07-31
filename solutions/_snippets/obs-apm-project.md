Bring traces, logs, and metrics into Elastic APM to help you troubleshoot and optimize your applications. You can collect this data using OpenTelemetry or APM Server.

:::::{dropdown} Steps for collecting application traces, metrics, and logs

::::{tab-set}
:::{tab-item} OpenTelemetry

The [Elastic Distribution of OpenTelemetry (EDOT) SDKs](opentelemetry://reference/edot-sdks/index.md) facilitate the collection of traces, metrics, and logs in OpenTelemetry format into Elastic APM.

1. Select **Add data** from the main menu and then select **Application**.
2. Select **OpenTelemetry**.
3. Follow the instructions for your platform.
:::

:::{tab-item} APM agents

Use the [APM agents](/solutions/observability/apm/elastic-apm-agents.md) to collect traces, metrics, and logs through [APM Server](/solutions/observability/apm/configure-apm-server.md).

1. Select **Add data** from the main menu and then select **Application**.
2. Select **Elastic APM**.
3. Select the tab for your language or framework.
4. Follow the instructions in the tab.
:::
:::::